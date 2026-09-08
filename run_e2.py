#!/usr/bin/env python3
"""Frozen zero-call E2 evaluation with durable, non-retrying match records."""
import argparse
import fcntl
import json
import os
import signal
from pathlib import Path
import subprocess
import sys
import time
import traceback

from e2_common import (E2, ROOT, TOTAL_SECONDS, WORKER_SECONDS, aggregate, append,
                       clock_state, create, encounters, inventory, policy_for, read,
                       remaining, score_match, sha, verify_freeze)


def prepare():
    if (E2 / 'protocol/freeze.json').exists():
        raise RuntimeError('Existing freeze; refusing replacement')
    inv = inventory()
    create(E2 / 'protocol/inventory.json', inv)
    create(E2 / 'protocol/encounters.json', encounters())
    create(E2 / 'protocol/config.json', dict(experimental_model_calls=0, allowance_seconds=TOTAL_SECONDS,
        worker_seconds=WORKER_SECONDS, workers=1, matches_per_policy=1200, original_commit=
        'fd19af5dd0f168f14b82dd5e2f5b1e68b210fe33', python=sys.version, platform=sys.platform))
    historical = ['initial.py', 'environment.py', 'policy.py', 'baseline.py', 'evaluate.py']
    historical += [str(p.relative_to(ROOT)) for exp in ('e1', 'e1_r')
                   for p in (ROOT / 'results' / exp).rglob('*') if p.is_file() and (
                       p.name in ('audit.json', 'ledger.json', 'training_selections_frozen.json')
                       or (p.name in ('main.py', 'metrics.json', 'correct.json') and '/runs/' in str(p)))]
    files = historical + ['e2_common.py', 'run_e2.py', 'tests/test_e2.py']
    files += [str(p.relative_to(ROOT)) for p in sorted((E2 / 'protocol').glob('*'))]
    create(E2 / 'protocol/freeze.json', dict(created=clock_state(), sha256={f: sha(ROOT / f) for f in sorted(set(files))}))
    print(json.dumps(dict(counts=inv['counts'], asts=inv['generated_ast_count'], policies=len(inv['policies']))))


def events_for(path):
    if not path.exists():
        return []
    # An interrupted partial JSON line is preserved and blocks automatic continuation.
    return [json.loads(line) for line in path.read_text().splitlines()]


def worker(policy_id):
    verify_freeze()
    runtime = read(E2 / 'runtime.json')
    marker = read(E2 / 'workers' / (policy_id + '.json'))
    available = min(remaining(runtime), WORKER_SECONDS - (clock_state()['boot_seconds'] - marker['boot_seconds']))
    if available <= 0:
        return
    signal.setitimer(signal.ITIMER_REAL, available)
    fn = policy_for(next(p for p in read(E2 / 'protocol/inventory.json')['policies'] if p['id'] == policy_id))
    path = E2 / 'matches' / (policy_id + '.jsonl')
    events = events_for(path)
    started = {e['encounter_id'] for e in events if e['event'] == 'started'}
    done = {e['encounter_id'] for e in events if e['event'] == 'result'}
    for enc in read(E2 / 'protocol/encounters.json'):
        if enc['id'] in done:
            continue
        if enc['id'] in started:
            append(path, dict(event='result', policy_id=policy_id, encounter_id=enc['id'],
                              status='infrastructure_failure', error='Interrupted after durable start; outcome unknown; not retried'))
            continue
        if remaining(runtime) <= 1:
            return
        append(path, dict(event='started', policy_id=policy_id, encounter_id=enc['id'], clock=clock_state()))
        try:
            result = score_match(fn, enc)
        except Exception as exc:
            result = dict(status='infrastructure_failure', error=str(exc), traceback=traceback.format_exc())
        append(path, dict(event='result', policy_id=policy_id, encounter_id=enc['id'], **result))
        if result['status'] == 'infrastructure_failure':
            return


def execute():
    verify_freeze()
    # Refuse fresh evaluation unless the freeze and all its contents exist in committed HEAD.
    frozen = read(E2 / 'protocol/freeze.json')
    for name in list(frozen['sha256']) + ['results/e2/protocol/freeze.json']:
        committed = subprocess.check_output(['git', 'show', 'HEAD:' + name], cwd=ROOT)
        if committed != (ROOT / name).read_bytes():
            raise RuntimeError('Freeze is not committed: ' + name)
    lock_path = E2 / 'execution.lock'
    with lock_path.open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        if (E2 / 'completion.json').exists():
            raise RuntimeError('Evaluation closed; no rerun')
        if not (E2 / 'historical_replay.json').exists() or not read(E2 / 'historical_replay.json')['passed']:
            raise RuntimeError('Historical replay required')
        if not (E2 / 'runtime.json').exists():
            create(E2 / 'runtime.json', dict(**clock_state(), allowance_seconds=TOTAL_SECONDS,
                deadline_rule='CLOCK_BOOTTIME, cumulative including downtime, same boot required',
                freeze_commit=subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()))
        runtime = read(E2 / 'runtime.json')
        (E2 / 'matches').mkdir(exist_ok=True)
        (E2 / 'workers').mkdir(exist_ok=True)
        for spec in read(E2 / 'protocol/inventory.json')['policies']:
            if remaining(runtime) <= 1:
                break
            path = E2 / 'matches' / (spec['id'] + '.jsonl')
            if len([e for e in events_for(path) if e['event'] == 'result']) == 1200:
                continue
            # Each policy gets at most one bounded worker attempt; recovery never renews it.
            marker = E2 / 'workers' / (spec['id'] + '.json')
            if marker.exists():
                continue
            create(marker, dict(policy_id=spec['id'], **clock_state(), timeout_seconds=min(WORKER_SECONDS, remaining(runtime))))
            print(f"Starting {spec['id']}; cumulative remaining {remaining(runtime):.1f}s", flush=True)
            with (E2 / 'workers' / (spec['id'] + '.log')).open('x') as log:
                proc = subprocess.Popen([sys.executable, str(ROOT / 'run_e2.py'), '--worker', spec['id']],
                                        stdout=log, stderr=subprocess.STDOUT, pass_fds=(lock.fileno(),))
                try:
                    code = proc.wait(timeout=min(WORKER_SECONDS, remaining(runtime)))
                    status = 'exited'
                except subprocess.TimeoutExpired:
                    proc.kill()
                    code = proc.wait()
                    status = 'timeout'
                except BaseException:
                    proc.kill()
                    proc.wait()
                    raise
            append(E2 / 'execution.jsonl', dict(policy_id=spec['id'], status=status, returncode=code,
                                               remaining_seconds=remaining(runtime), clock=clock_state()))
            print(f"Finished {spec['id']}: {status}, code={code}", flush=True)
        # Started-without-result matches remain explicit unknown infrastructure outcomes in analysis.
        create(E2 / 'completion.json', dict(clock=clock_state(), elapsed_seconds=TOTAL_SECONDS - remaining(runtime),
               budget_exhausted=remaining(runtime) <= 1, experimental_model_calls=0))


def replay():
    from environment import evaluate_policy
    verify_freeze()
    inv = read(E2 / 'protocol/inventory.json')
    baselines = read(ROOT / 'results/baseline.json')['baselines']
    records = []
    for spec in inv['policies'][:7]:
        if spec['kind'] == 'generated':
            origin = spec['origins'][0]
            slot = read(ROOT / 'results' / origin['experiment'] / 'audit.json')['runs'][origin['run']]['slots'][origin['slot']]
            expected = {split: slot[split] for split in ('train', 'holdout') if split in slot}
        else:
            expected = {split: baselines[spec['id']][split] for split in ('train', 'holdout')}
        for split, old in expected.items():
            result = evaluate_policy(policy_for(spec), split)
            assert result == old, (spec['id'], split)
            records.append(dict(policy_id=spec['id'], split=split, matches=result['matches'],
                                total_payoff=result['total_payoff'], turns=result['turns'], passed=True))
    create(E2 / 'historical_replay.json', dict(passed=True, records=records, clock=clock_state()))
    print('Historical replay passed:', len(records), 'policy/panel records')


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--prepare', action='store_true')
    group.add_argument('--replay-history', action='store_true')
    group.add_argument('--execute', action='store_true')
    group.add_argument('--worker')
    args = parser.parse_args()
    if args.prepare: prepare()
    elif args.replay_history: replay()
    elif args.worker: worker(args.worker)
    else: execute()


if __name__ == '__main__':
    main()
