"""Separate, zero-call E2 adapter. Never executes generated Python."""
import ast
from collections import Counter
import hashlib
import itertools
import json
import os
from pathlib import Path
import time

import environment as env
from baseline import memory_one
from policy import PolicyError, load_policy

ROOT = Path(__file__).resolve().parent
E2 = ROOT / 'results/e2'
TOTAL_SECONDS = 2700
WORKER_SECONDS = 300


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def ast_sha(source):
    return hashlib.sha256(ast.dump(ast.parse(source), include_attributes=False).encode()).hexdigest()


def read(path):
    return json.loads(Path(path).read_text())


def create(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x') as f:
        json.dump(value, f, indent=2, sort_keys=True)
        f.write('\n')
        f.flush()
        os.fsync(f.fileno())


def append(path, value):
    with Path(path).open('a') as f:
        f.write(json.dumps(value, sort_keys=True) + '\n')
        f.flush()
        os.fsync(f.fileno())


def encounters():
    rows = []
    for split, names, seeds in [('train', env.TRAIN_OPPONENTS, range(100001, 100101)),
                                 ('holdout', env.HOLDOUT_OPPONENTS, range(200001, 200101))]:
        assert not set(seeds) & set(env.TRAIN_SEEDS + env.HOLDOUT_SEEDS)
        for name in names:
            for seed in seeds:
                rows.append(dict(id=f'{split}/{name}/{seed}', split=split, opponent=name,
                                 seed=seed, turns=env.horizon(seed), match_seed=int.from_bytes(
                                     hashlib.sha256(f'{split}/{name}/{seed}'.encode()).digest()[:8], 'big')))
    return rows


def inventory():
    groups, excluded, counts = {}, [], Counter()
    for experiment in ('e1', 'e1_r'):
        base = ROOT / 'results' / experiment
        audit, frozen = read(base / 'audit.json'), read(base / 'training_selections_frozen.json')
        for run, data in audit['runs'].items():
            for slot in data['slots']:
                if slot['slot'] == 0:
                    continue
                source = slot.get('source')
                origin = dict(experiment=experiment, condition=run[0], run=run, slot=slot['slot'],
                              run_status=frozen['statuses'][run], original_status=slot['opportunity_status'],
                              source=source, source_sha256=slot.get('sha256'),
                              historical_selected=slot['slot'] == frozen['selections'][run]['slot'])
                if source:
                    assert sha(ROOT / source) == slot['sha256']
                    assert (ROOT / source).read_text() == slot['complete_source']
                if not slot['correct']:
                    excluded.append(dict(origin, reason=slot.get('error')))
                    continue
                assert source and slot['opportunity_status'] == 'valid'
                live = ROOT / source
                assert read(live.parent / 'results/correct.json')['correct'] is True
                assert read(live.parent / 'results/metrics.json')['combined_score'] == slot['training']
                assert any(r['correct'] and r['archived'] and r['source_sha256'] == slot['sha256']
                           for r in slot['database_rows'])
                load_policy(live)
                origin['original_train'] = slot['training']
                origin['original_holdout'] = slot.get('holdout', {}).get('mean_payoff')
                key = ast_sha(live.read_text())
                group = groups.setdefault(key, dict(id='ast_' + key[:16], kind='generated', ast_sha256=key,
                                                    source=source, source_sha256=sha(live), origins=[]))
                group['origins'].append(origin)
                counts[experiment] += 1
    assert counts == {'e1': 40, 'e1_r': 18}
    # Put predeclared focal policies first, then references, then other ASTs and memory one.
    focal = []
    for exp, run, slot in [('e1_r', 'A101', 4), ('e1', 'A202', 5)]:
        focal.append(next(g for g in groups.values() if any(
            (o['experiment'], o['run'], o['slot']) == (exp, run, slot) for o in g['origins'])))
    refs = [dict(id='initial', kind='seed', source='initial.py', source_sha256=sha(ROOT / 'initial.py'))]
    refs += [dict(id=n, kind='reference') for n in ('always_cooperate', 'tit_for_tat', 'grim', 'win_stay_lose_shift')]
    policies = focal + refs + sorted((g for g in groups.values() if g not in focal), key=lambda g: g['id'])
    policies += [dict(id='m1_' + ''.join(map(str, b)), kind='memory_one', bits=list(b))
                 for b in itertools.product((0, 1), repeat=5)]
    return dict(counts=dict(counts), generated_ast_count=len(groups), policies=policies,
                exclusions=excluded, deduplication='ast.dump(include_attributes=False); docstrings retained; no behavioral merging')


def policy_for(spec):
    if spec['kind'] in ('generated', 'seed'):
        assert sha(ROOT / spec['source']) == spec['source_sha256'], 'Source integrity failure'
        return load_policy(ROOT / spec['source'])
    if spec['kind'] == 'reference':
        return env.reference_policy(spec['id'])
    if spec['kind'] == 'memory_one':
        return memory_one(tuple(spec['bits']))
    raise ValueError('Unknown policy kind')


def score_match(fn, encounter):
    """Retain the exact pre-decision history on a policy failure; infrastructure errors propagate."""
    last = {}
    def wrapped(own, other):
        try:
            action = fn(own, other)
            if type(action) is not int or action not in (0, 1):
                raise PolicyError('Invalid action')
            return action
        except PolicyError as exc:
            last.update(round=len(own) + 1, own_history=list(own), opponent_history=list(other),
                        exception_type=type(exc).__name__, error=str(exc))
            raise
    try:
        result = env.play(wrapped, encounter['opponent'], encounter['turns'], encounter['match_seed'])
        return dict(status='ok', **result)
    except PolicyError:
        return dict(status='policy_invalid', counterexample=last)


def aggregate(rows, expected=600):
    ok = [r for r in rows if r['status'] == 'ok']
    totals = {k: sum(r[k] for r in ok) for k in ('total_payoff', 'opponent_total_payoff', 'turns', 'cooperations')}
    complete = len(rows) == expected and len(ok) == expected
    return dict(**totals, completed_matches=len(ok), recorded_matches=len(rows), expected_matches=expected,
                statuses=dict(Counter(r['status'] for r in rows)), complete=complete,
                mean_payoff=totals['total_payoff'] / totals['turns'] if complete else None,
                cooperation_rate=totals['cooperations'] / totals['turns'] if complete else None)


def verify_freeze():
    frozen = read(E2 / 'protocol/freeze.json')
    for name, expected in frozen['sha256'].items():
        assert sha(ROOT / name) == expected, 'Frozen file changed: ' + name
    return frozen


def clock_state():
    return dict(boot_id=Path('/proc/sys/kernel/random/boot_id').read_text().strip(),
                boot_seconds=time.clock_gettime(time.CLOCK_BOOTTIME), unix_seconds=time.time())


def remaining(runtime, now=None):
    now = now or clock_state()
    if runtime['boot_id'] != now['boot_id']:
        raise RuntimeError('Boot changed: elapsed runtime uncertain; refuse continuation')
    elapsed = now['boot_seconds'] - runtime['boot_seconds']
    if elapsed < 0:
        raise RuntimeError('Clock moved backwards; elapsed runtime uncertain')
    # Charge all downtime, conservatively; never reset the original deadline.
    return max(0, runtime['allowance_seconds'] - elapsed)
