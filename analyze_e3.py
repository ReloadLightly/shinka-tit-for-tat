#!/usr/bin/env python3
"""Frozen E3 transfer evaluator and scored-trace reproduction. No model calls."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import random
import subprocess
import sys
import time

import environment as env
from policy import load_policy
from e1r_io import write_json
from e2_common import aggregate, score_match
from e3_state import E3, ROOT, read, sha, verify_freeze


def encounters():
    old = set(env.TRAIN_SEEDS + env.HOLDOUT_SEEDS) | set(range(100001, 100101)) | set(range(200001, 200101))
    rows = []
    for split, names, seeds in [('train', env.TRAIN_OPPONENTS, range(300001, 300101)),
                                 ('holdout', env.HOLDOUT_OPPONENTS, range(400001, 400101))]:
        assert not old.intersection(seeds)
        for name in names:
            for seed in seeds:
                key = f'{split}/{name}/{seed}'
                rows.append({'id': key, 'split': split, 'opponent': name, 'seed': seed,
                    'turns': env.horizon(seed), 'match_seed': int.from_bytes(hashlib.sha256(key.encode()).digest()[:8], 'big')})
    return rows


def policies():
    selected = read(E3 / 'training_selections_frozen.json')
    result = {k: {'source': v['source'], 'sha256': v['sha256']} for k, v in selected['selections'].items()}
    result['seed'] = {'source': str((E3 / 'protocol/seed.py').relative_to(ROOT)), 'sha256': sha(E3 / 'protocol/seed.py')}
    result['TFT'] = {'reference': 'tit_for_tat'}
    return result


def policy_for(name):
    spec = policies()[name]
    if 'reference' in spec:
        return env.reference_policy(spec['reference'])
    assert sha(ROOT / spec['source']) == spec['sha256']
    return load_policy(ROOT / spec['source'])


def worker(name, split):
    verify_freeze()
    fn = policy_for(name)
    path = E3 / 'transfer' / f'{name}_{split}.jsonl'
    with path.open('x') as f:
        for encounter in read(E3 / 'protocol/encounters.json'):
            if encounter['split'] == split:
                row = {'policy': name, **encounter, **score_match(fn, encounter)}
                f.write(json.dumps(row) + '\n')
                f.flush()


def transfer():
    verify_freeze()
    specs = policies()  # All three selections must already be frozen.
    folder = E3 / 'transfer'
    folder.mkdir(exist_ok=False)
    started = time.monotonic()
    records = []
    for name in specs:
        for split in ('train', 'holdout'):
            cmd = [sys.executable, str(ROOT / 'analyze_e3.py'), '--worker', name, '--split', split]
            tick = time.monotonic()
            with (folder / f'{name}_{split}.log').open('w') as log:
                try:
                    rc = subprocess.run(cmd, stdout=log, stderr=subprocess.STDOUT, timeout=300).returncode
                except subprocess.TimeoutExpired:
                    rc = 124
            records.append({'policy': name, 'split': split, 'command': cmd, 'returncode': rc,
                            'runtime_seconds': time.monotonic()-tick})
            write_json(folder / 'execution.json', {'workers': records, 'runtime_seconds': time.monotonic()-started,
                                                  'external_proposal_invocations': 0})
            if rc:
                raise RuntimeError('Transfer worker failed; preserve partial records')
            print(f'[E3 transfer] {name} {split}: 600 encounters scored', flush=True)
    summarize()


def summarize():
    output = {}
    for name in policies():
        output[name] = {}
        for split in ('train', 'holdout'):
            rows = [json.loads(s) for s in (E3 / 'transfer' / f'{name}_{split}.jsonl').read_text().splitlines()]
            assert len(rows) == 600 and len({r['id'] for r in rows}) == 600
            output[name][split] = aggregate(rows)
            output[name][split]['opponents'] = {op: aggregate([r for r in rows if r['opponent'] == op], expected=100)
                                                for op in sorted({r['opponent'] for r in rows})}
    write_json(E3 / 'transfer/summary.json', output)
    return output


def trace(name, split, opponent, seed, rounds=16):
    encounter = next(r for r in read(E3 / 'protocol/encounters.json')
                     if (r['split'], r['opponent'], r['seed']) == (split, opponent, seed))
    fn = policy_for(name)
    measured = env.play(fn, opponent, encounter['turns'], encounter['match_seed'])
    rows = [json.loads(s) for s in (E3 / 'transfer' / f'{name}_{split}.jsonl').read_text().splitlines()]
    scored = next(r for r in rows if r['id'] == encounter['id'])
    assert scored['status'] == 'ok' and all(scored[k] == v for k, v in measured.items())
    rng = random.Random(encounter['match_seed'])
    own, other, steps = (), (), []
    for i in range(min(rounds, encounter['turns'])):
        action = fn(own, other)
        opposite = env.reference(opponent, other, own, rng)
        steps.append({'round': i+1, 'own_history': list(own), 'opponent_history': list(other),
                      'action': action, 'opponent_action': opposite, 'payoff': env.PAYOFFS[action, opposite]})
        own += (action,)
        other += (opposite,)
    return {'policy': name, 'encounter': encounter, 'scored_totals_verified': measured, 'steps': steps}


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--transfer', action='store_true')
    p.add_argument('--worker', choices=['S101', 'S202', 'S303', 'seed', 'TFT'])
    p.add_argument('--trace', choices=['S101', 'S202', 'S303', 'seed', 'TFT'])
    p.add_argument('--split', choices=['train', 'holdout'])
    p.add_argument('--opponent')
    p.add_argument('--seed', type=int)
    p.add_argument('--rounds', type=int, default=16)
    args = p.parse_args()
    if args.transfer:
        transfer()
    elif args.worker:
        worker(args.worker, args.split)
    elif args.trace:
        print(json.dumps(trace(args.trace, args.split, args.opponent, args.seed, args.rounds), indent=2))
    else:
        p.print_help()
