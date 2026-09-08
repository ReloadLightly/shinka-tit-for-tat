"""Shinka evaluator: payoff feedback only. Recognition is a separate offline command."""
import argparse
import json
from pathlib import Path
from environment import evaluate_policy
from policy import load_policy


def evaluate_file(program_path, results_dir):
    out = Path(results_dir)
    out.mkdir(parents=True, exist_ok=True)
    try:
        report = evaluate_policy(load_policy(program_path), 'train')
        metrics = {'combined_score': report['mean_payoff'], 'public': {'mean_payoff': report['mean_payoff']}, 'private': {}}
        correct = {'correct': True, 'error': None}
    except Exception as exc:
        metrics = {'combined_score': -1.0, 'public': {}, 'private': {}}
        correct = {'correct': False, 'error': f'{type(exc).__name__}: {exc}'}
    (out / 'metrics.json').write_text(json.dumps(metrics, indent=2) + '\n')
    (out / 'correct.json').write_text(json.dumps(correct, indent=2) + '\n')
    return metrics, correct


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--program_path', required=True)
    parser.add_argument('--results_dir', required=True)
    args = parser.parse_args()
    metrics, correct = evaluate_file(args.program_path, args.results_dir)
    print(json.dumps({'metrics': metrics, **correct}, indent=2))
    # Failed candidate is a recorded evaluation, not a crashed evaluation job.


if __name__ == '__main__':
    main()
