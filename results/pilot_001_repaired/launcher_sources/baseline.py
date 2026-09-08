"""No-LLM reference measurements and exhaustive finite comparator, not Shinka evolution."""
import argparse
import hashlib
import itertools
import json
import platform
from pathlib import Path
from environment import evaluate_policy, reference_policy, horizon, TRAIN_SEEDS, HOLDOUT_SEEDS
from policy import load_policy
from recognize import analyze_policy

ROOT = Path(__file__).resolve().parent


def memory_one(bits):
    # bits: initial action, after CC, CD, DC, DD (own action first).
    def candidate(own, other):
        return bits[1 + 2 * own[-1] + other[-1]] if own else bits[0]
    return candidate


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--output', default='results/baseline.json')
    args = p.parse_args()
    out = Path(args.output)
    if out.exists():
        raise SystemExit('Refusing to overwrite evidence; choose a new --output')
    baseline = {}
    names = ['always_cooperate', 'always_defect', 'tit_for_tat', 'grim', 'win_stay_lose_shift']
    for name in ['initial'] + names:
        fn = load_policy(ROOT / 'initial.py') if name == 'initial' else reference_policy(name)
        baseline[name] = {'train': evaluate_policy(fn), 'holdout': evaluate_policy(fn, 'holdout'),
                          'recognition': analyze_policy(fn)}
    oracle = []
    for bits in itertools.product((0, 1), repeat=5):
        fn = memory_one(bits)
        train = evaluate_policy(fn)
        oracle.append({'bits': ''.join(map(str, bits)), 'train_mean_payoff': train['mean_payoff']})
    oracle.sort(key=lambda row: (-row['train_mean_payoff'], row['bits']))
    tft_score = next(row['train_mean_payoff'] for row in oracle if row['bits'] == '00101')
    report = {'kind': 'reference baseline and exhaustive 32-policy comparator; no LLM evolution',
              'python': platform.python_version(), 'llm_calls': 0,
              'source_sha256': {f.name: hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(ROOT.glob('*.py'))},
              'train_horizons': [horizon(s) for s in TRAIN_SEEDS],
              'holdout_horizons': [horizon(s) for s in HOLDOUT_SEEDS],
              'baselines': baseline, 'memory_one_order': ['initial', 'CC', 'CD', 'DC', 'DD'],
              'memory_one_ranking': oracle,
              'tft_rank_competition': 1 + sum(r['train_mean_payoff'] > tft_score for r in oracle)}
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'output': str(out), 'llm_calls': 0,
                      'train': {name: data['train']['mean_payoff'] for name, data in baseline.items()},
                      'best_memory_one': oracle[0], 'tft_rank': report['tft_rank_competition']}, indent=2))


if __name__ == '__main__':
    main()
