#!/usr/bin/env python3
"""Read-only E2 analysis and verified trace extraction; never proposes a policy."""
import argparse
import ast
from collections import Counter, defaultdict
import json
from pathlib import Path
import sys

import environment as env
from e2_common import E2, ROOT, aggregate, create, policy_for, read, sha, verify_freeze
from run_e2 import events_for


def collect():
    verify_freeze()
    inventory = read(E2 / 'protocol/inventory.json')
    encounters = read(E2 / 'protocol/encounters.json')
    ids = {r['id'] for r in encounters}
    rows = []
    for spec in inventory['policies']:
        events = events_for(E2 / 'matches' / (spec['id'] + '.jsonl'))
        started, results = set(), {}
        for event in events:
            eid = event['encounter_id']
            assert event['policy_id'] == spec['id'] and eid in ids
            if event['event'] == 'started':
                assert eid not in started
                started.add(eid)
            else:
                assert event['event'] == 'result' and eid in started and eid not in results
                results[eid] = {k: v for k, v in event.items() if k not in ('event', 'encounter_id', 'policy_id')}
        for enc in encounters:
            result = results.get(enc['id'], dict(status='infrastructure_unknown' if enc['id'] in started else 'not_evaluated'))
            if result['status'] == 'ok':
                assert result['turns'] == enc['turns']
                assert result['mean_payoff'] == result['total_payoff'] / enc['turns']
                assert 0 <= result['cooperations'] <= enc['turns']
                assert 0 <= result['total_payoff'] <= 5 * enc['turns']
                assert result['opponent_mean_payoff'] == result['opponent_total_payoff'] / enc['turns']
            rows.append({'policy_id': spec['id'], **enc, **result})
    return inventory, rows


def rank(value, values):
    return None if value is None else 1 + sum(x is not None and x > value for x in values)


def summarize(inv, rows):
    grouped = defaultdict(list)
    for row in rows:
        grouped[row['policy_id'], row['split']].append(row)
    summaries = {}
    baseline = read(ROOT / 'results/baseline.json')
    m1 = {r['bits']: r['train_mean_payoff'] for r in baseline['memory_one_ranking']}
    for spec in inv['policies']:
        result = dict(kind=spec['kind'], panels={})
        for split in ('train', 'holdout'):
            panel = grouped[spec['id'], split]
            stats = aggregate(panel)
            # recorded_matches must exclude explicit expansion of never-started rows.
            stats['recorded_matches'] = sum(r['status'] != 'not_evaluated' for r in panel)
            stats['per_opponent'] = {name: aggregate([r for r in panel if r['opponent'] == name], 100)
                                     for name in sorted({r['opponent'] for r in panel})}
            if spec['kind'] == 'generated':
                originals = {o['original_' + split] for o in spec['origins'] if o['original_' + split] is not None}
                assert len(originals) <= 1, 'AST duplicates disagree on original score'
                original = next(iter(originals), None)
            elif spec['kind'] in ('seed', 'reference'):
                original = baseline['baselines'][spec['id']][split]['mean_payoff']
            else:
                original = m1[spec['id'][3:]] if split == 'train' else None
            stats['original_mean_payoff'] = original
            result['panels'][split] = stats
        summaries[spec['id']] = result
    generated = [p['id'] for p in inv['policies'] if p['kind'] == 'generated']
    for pid, result in summaries.items():
        for split, stats in result['panels'].items():
            for ref in ('tit_for_tat', 'grim'):
                comparator = summaries[ref]['panels'][split]
                stats['difference_from_' + ref] = (stats['mean_payoff'] - comparator['mean_payoff']
                    if stats['complete'] and comparator['complete'] else None)
                for name, opp in stats['per_opponent'].items():
                    refopp = comparator['per_opponent'][name]
                    opp['difference_from_' + ref] = (opp['mean_payoff'] - refopp['mean_payoff']
                        if opp['complete'] and refopp['complete'] else None)
            if pid in generated:
                family = generated
            elif result['kind'] in ('seed', 'reference'):
                family = [p['id'] for p in inv['policies'] if p['kind'] in ('seed', 'reference')]
            else:
                family = [p['id'] for p in inv['policies'] if p['kind'] == result['kind']]
            historic_ids = [i for i in family if summaries[i]['panels'][split]['original_mean_payoff'] is not None]
            stats['rank_population'] = family
            fresh_values = [summaries[i]['panels'][split]['mean_payoff'] for i in family]
            stats['fresh_rank'] = rank(stats['mean_payoff'], fresh_values) if all(v is not None for v in fresh_values) else None
            stats['original_rank'] = rank(stats['original_mean_payoff'], [summaries[i]['panels'][split]['original_mean_payoff'] for i in historic_ids])
            stats['original_rank_population_count'] = len(historic_ids)
            stats['fresh_rank_original_available_subset'] = (rank(stats['mean_payoff'], [summaries[i]['panels'][split]['mean_payoff'] for i in historic_ids])
                if pid in historic_ids and all(summaries[i]['panels'][split]['complete'] for i in historic_ids) else None)
    return dict(policies=summaries, coverage=dict(Counter(r['status'] for r in rows)),
                planned_matches=len(rows), panel_pooling=False, experimental_model_calls=0)


def trace(policy_id, split, opponent, seed, count=16):
    """Replay one already scored E2 encounter, checking the complete result, not adding a record."""
    verify_freeze()
    inv = read(E2 / 'protocol/inventory.json')
    spec = next(p for p in inv['policies'] if p['id'] == policy_id)
    enc = next(e for e in read(E2 / 'protocol/encounters.json') if
               (e['split'], e['opponent'], e['seed']) == (split, opponent, seed))
    recorded = next(e for e in events_for(E2 / 'matches' / (policy_id + '.jsonl'))
                    if e['event'] == 'result' and e['encounter_id'] == enc['id'])
    assert recorded['status'] == 'ok', 'Only successful scored encounters can be traced'
    fn = policy_for(spec)
    rows = []
    def wrapped(own, other):
        tests = []
        def tracer(frame, event, value):
            if event == 'return' and frame.f_code.co_name == 'expression' and frame.f_code.co_filename == str(ROOT / 'policy.py'):
                node = frame.f_locals.get('n')
                parent = frame.f_back.f_locals.get('n') if frame.f_back else None
                if isinstance(parent, (ast.If, ast.IfExp)) and node is parent.test:
                    tests.append(dict(test=ast.unparse(node), result=bool(value)))
            return tracer
        previous = sys.gettrace()
        if len(own) < count:
            sys.settrace(tracer)
        try:
            action = fn(own, other)
        finally:
            sys.settrace(previous)
        if len(own) < count:
            rows.append(dict(round=len(own) + 1, own_history=list(own), opponent_history=list(other),
                             action=action, branch_tests=tests))
        # Last full histories recover actual opponent actions without a second play.
        wrapped.final_history = (own, other)
        return action
    full = env.play(wrapped, enc['opponent'], enc['turns'], enc['match_seed'])
    assert all(recorded[k] == v for k, v in full.items()), 'Trace replay differs from scored result'
    # For a featured round, opponent action is in the next callback history.
    # If the whole match is shorter than count, use deterministic reference replay for final action only.
    import random
    rng = random.Random(enc['match_seed'])
    total = 0
    for row in rows:
        enemy = env.reference(opponent, tuple(row['opponent_history']), tuple(row['own_history']), rng)
        row['opponent_action'] = enemy
        row['payoff'] = env.PAYOFFS[row['action'], enemy]
        total += row['payoff']
        row['cumulative_payoff'] = total
    return dict(policy_id=policy_id, encounter=enc, full_match=full, rows=rows,
                verified_against_main_record=True, purpose='Separate trace verification; not another main evaluation')


def export():
    assert (E2 / 'completion.json').exists(), 'Wait for main execution closure'
    inv, rows = collect()
    summary = summarize(inv, rows)
    create(E2 / 'summary.json', summary)
    with (E2 / 'per_match.jsonl').open('x') as out:
        for row in rows:
            out.write(json.dumps(row, sort_keys=True) + '\n')
    create(E2 / 'failures.json', [r for r in rows if r['status'] not in ('ok', 'not_evaluated')])
    traces = []
    for spec in inv['policies'][:2]:
        for split, opponent, seed in [('train', 'random', 100001), ('holdout', 'alternator', 200001),
                                       ('holdout', 'suspicious_tit_for_tat', 200001)]:
            if summary['policies'][spec['id']]['panels'][split]['complete']:
                traces.append(trace(spec['id'], split, opponent, seed))
    create(E2 / 'traces.json', traces)
    print(json.dumps(summary['coverage']))



def clock_audit():
    runtime = read(E2 / 'runtime.json')
    completion = read(E2 / 'completion.json')['clock']
    points = [dict(label='runtime start', **runtime)]
    for spec in read(E2 / 'protocol/inventory.json')['policies']:
        points.extend(dict(label=spec['id'] + '/' + e['encounter_id'], **e['clock'])
                      for e in events_for(E2 / 'matches' / (spec['id'] + '.jsonl')) if e['event'] == 'started')
    points.append(dict(label='completion', **completion))
    monotonic = all(b['boot_seconds'] >= a['boot_seconds'] for a, b in zip(points, points[1:]))
    points.sort(key=lambda p: p['boot_seconds'])
    changes = []
    for a, b in zip(points, points[1:]):
        delta = (b['unix_seconds'] - a['unix_seconds']) - (b['boot_seconds'] - a['boot_seconds'])
        if abs(delta) > .1:
            changes.append(dict(from_label=a['label'], to_label=b['label'],
                boot_elapsed=b['boot_seconds'] - a['boot_seconds'],
                unix_elapsed=b['unix_seconds'] - a['unix_seconds'], discrepancy_seconds=delta))
    elapsed = completion['boot_seconds'] - runtime['boot_seconds']
    utc_span = completion['unix_seconds'] - runtime['unix_seconds']
    return dict(primary_clock='CLOCK_BOOTTIME (frozen)', boot_elapsed_seconds=elapsed,
                utc_timestamp_interval_seconds=utc_span, difference_seconds=utc_span - elapsed,
                same_boot=len({p['boot_id'] for p in points}) == 1, monotonic_starts=monotonic,
                clock_observations=len(points), detected_discontinuities=changes,
                cause='UTC/boottime divergence observed; host clock adjustment cause unestablished; original accounting untouched')


def main():
    p = argparse.ArgumentParser()
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument('--export', action='store_true')
    g.add_argument('--trace')
    g.add_argument('--verify', action='store_true')
    p.add_argument('--split', choices=('train', 'holdout'))
    p.add_argument('--opponent')
    p.add_argument('--seed', type=int)
    p.add_argument('--rounds', type=int, default=16)
    args = p.parse_args()
    if args.export:
        export()
    elif args.verify:
        inv, rows = collect()
        assert summarize(inv, rows) == read(E2 / 'summary.json')
        with (E2 / 'per_match.jsonl').open() as f:
            assert [json.loads(line) for line in f] == rows
        assert read(E2 / 'failures.json') == [r for r in rows if r['status'] not in ('ok', 'not_evaluated')]
        for t in read(E2 / 'traces.json'):
            e = t['encounter']
            assert trace(t['policy_id'], e['split'], e['opponent'], e['seed'], len(t['rows'])) == t
        assert clock_audit() == read(E2 / 'runtime_clock_audit.json')
        print('Verified freeze, source identities, unique encounter coverage, aggregates, exports, failures, all six scored traces and discrepant clock accounting')
    else:
        print(json.dumps(trace(args.trace, args.split, args.opponent, args.seed, args.rounds), indent=2))


if __name__ == '__main__':
    main()
