import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import environment as env
from e2_common import (ROOT, aggregate, ast_sha, encounters, inventory, policy_for,
                       remaining, score_match, sha, verify_freeze)
from policy import parse_policy


class E2Checks(unittest.TestCase):
    def test_manifest_and_seed_separation(self):
        rows = encounters()
        self.assertEqual(len(rows), 1200)
        self.assertEqual(len({r['id'] for r in rows}), 1200)
        for split, seeds, names in [('train', set(range(100001, 100101)), env.TRAIN_OPPONENTS),
                                    ('holdout', set(range(200001, 200101)), env.HOLDOUT_OPPONENTS)]:
            panel = [r for r in rows if r['split'] == split]
            self.assertEqual(len(panel), 600)
            self.assertFalse(seeds & set(env.TRAIN_SEEDS + env.HOLDOUT_SEEDS))
            for name in names:
                self.assertEqual({r['seed'] for r in panel if r['opponent'] == name}, seeds)
            for r in panel:
                self.assertEqual(r['turns'], env.horizon(r['seed']))
        self.assertEqual(rows, encounters())

    def test_adapter_identical_historical_encounters(self):
        import hashlib
        fn = env.reference_policy('tit_for_tat')
        for split in ('train', 'holdout'):
            old = env.evaluate_policy(fn, split)
            for row in old['rows']:
                enc = dict(opponent=row['opponent'], turns=row['turns'], match_seed=int.from_bytes(
                    hashlib.sha256(f"{split}/{row['opponent']}/{row['seed']}".encode()).digest()[:8], 'big'))
                new = score_match(fn, enc)
                self.assertEqual(new.pop('status'), 'ok')
                self.assertEqual(new, {k: v for k, v in row.items() if k not in ('opponent', 'seed')})

    def test_weighted_scoring_and_failure_not_omitted(self):
        rows = [dict(status='ok', turns=1, total_payoff=5, cooperations=0, opponent_total_payoff=0),
                dict(status='ok', turns=9, total_payoff=9, cooperations=0, opponent_total_payoff=9)]
        self.assertEqual(aggregate(rows, 2)['mean_payoff'], 1.4)
        self.assertIsNone(aggregate(rows + [dict(status='policy_invalid')], 3)['mean_payoff'])
        self.assertIsNone(aggregate(rows, 3)['mean_payoff'])

    def test_inventory_provenance_live_validity(self):
        inv = inventory()
        self.assertEqual(inv['counts'], {'e1': 40, 'e1_r': 18})
        generated = [p for p in inv['policies'] if p['kind'] == 'generated']
        self.assertEqual(len(generated), 35)
        self.assertEqual(len(inv['policies']), 72)
        self.assertEqual(len(inv['exclusions']), 62)
        origins = [o for p in generated for o in p['origins']]
        self.assertEqual(len({(o['experiment'], o['run'], o['slot']) for o in origins}), 58)
        self.assertTrue(any(o['run_status'] == 'incomplete' for o in origins))
        self.assertEqual(sum(e['original_status'] == 'evaluation_missing' for e in inv['exclusions']), 2)
        self.assertEqual(sum(e['original_status'] == 'rejected' for e in inv['exclusions']), 3)
        self.assertEqual(ast_sha('def policy(own_history, opponent_history):\n return 1\n'),
                         ast_sha('# comment\ndef policy(own_history, opponent_history):\n    return 1\n'))
        self.assertNotEqual(ast_sha('def policy(own_history, opponent_history):\n return 1\n'),
                            ast_sha('def policy(own_history, opponent_history):\n return 0\n'))

    def test_source_integrity(self):
        with self.assertRaises(AssertionError):
            policy_for(dict(kind='seed', source='initial.py', source_sha256='wrong'))

    def test_counterexample_and_infrastructure(self):
        fn = parse_policy('def policy(own_history, opponent_history):\n return opponent_history[-1]\n')
        enc = dict(opponent='always_defect', turns=5, match_seed=42)
        result = score_match(fn, enc)
        self.assertEqual(result['status'], 'policy_invalid')
        self.assertEqual(result['counterexample']['round'], 1)
        self.assertEqual(result['counterexample']['opponent_history'], [])
        with patch('environment.play', side_effect=OSError('disk fault')):
            with self.assertRaises(OSError):
                score_match(fn, enc)

    def test_cumulative_runtime_not_reset(self):
        runtime = dict(boot_id='boot', boot_seconds=100, allowance_seconds=2700)
        self.assertEqual(remaining(runtime, dict(boot_id='boot', boot_seconds=500)), 2300)
        self.assertEqual(remaining(runtime, dict(boot_id='boot', boot_seconds=2900)), 0)
        with self.assertRaises(RuntimeError):
            remaining(runtime, dict(boot_id='another', boot_seconds=100))

    def test_existing_frozen_source_integrity(self):
        if (ROOT / 'results/e2/protocol/freeze.json').exists():
            verify_freeze()


if __name__ == '__main__':
    unittest.main()
