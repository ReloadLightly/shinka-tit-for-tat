"""Post-search identification; never imported by the selection evaluator."""
import argparse
import itertools
import json
from pathlib import Path
from environment import evaluate_policy
from policy import load_policy


def analyze_policy(candidate):
    checked = 0
    failures = []

    def probe(own, other):
        nonlocal checked
        checked += 1
        expected = other[-1] if other else 0
        try:
            actual = candidate(own, other)
            matches = type(actual) is int and actual == expected
        except Exception as exc:
            actual, matches = type(exc).__name__, False
        if not matches and len(failures) < 8:
            failures.append({'length': len(own), 'own_tail': list(own[-8:]),
                             'other_tail': list(other[-8:]), 'expected': expected, 'actual': actual})
        return matches

    matches = True
    for n in range(6):
        histories = list(itertools.product((0, 1), repeat=n))
        for own in histories:
            for other in histories:
                matches = probe(own, other) and matches
    # Include long histories with distant defections, recovery, alternation and endgame clocks.
    for n in (10, 63, 77, 151, 156, 198, 199, 200, 201, 308, 1000):
        examples = [(0,) * n, (1,) * n, (1,) + (0,) * (n - 1),
                    (0,) * (n - 1) + (1,), tuple(i % 2 for i in range(n))]
        for own in examples:
            for other in examples:
                matches = probe(own, other) and matches
    return {'matches_tft_probes': matches, 'probe_count': checked,
            'first_mismatches': failures,
            'claim': 'Agreement on finite probes is not proof of equivalence on every possible history.'}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--program_path', required=True)
    p.add_argument('--output', required=True)
    args = p.parse_args()
    candidate = load_policy(args.program_path)
    report = {'program_path': args.program_path, 'recognition': analyze_policy(candidate),
              'holdout': evaluate_policy(candidate, 'holdout')}
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.exists():
        raise SystemExit('Refusing to overwrite existing diagnostic output')
    out.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'recognition': report['recognition'], 'holdout_mean_payoff': report['holdout']['mean_payoff']}, indent=2))


if __name__ == '__main__':
    main()
