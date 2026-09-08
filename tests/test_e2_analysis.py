import tempfile
from pathlib import Path
import unittest
from unittest.mock import patch

import analyze_e2
from e2_common import create, append


class E2AnalysisChecks(unittest.TestCase):
    def test_partial_coverage_and_duplicate_rejection(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            create(root / 'protocol/inventory.json', dict(policies=[dict(id='test')]))
            encs = [dict(id=str(i), split='train', opponent='always_defect', turns=1, seed=i, match_seed=i) for i in range(3)]
            create(root / 'protocol/encounters.json', encs)
            (root / 'matches').mkdir()
            path = root / 'matches/test.jsonl'
            append(path, dict(event='started', policy_id='test', encounter_id='0'))
            good = dict(event='result', policy_id='test', encounter_id='0', status='ok', turns=1,
                        total_payoff=1, opponent_total_payoff=1, mean_payoff=1.0,
                        opponent_mean_payoff=1.0, cooperations=0)
            append(path, good)
            append(path, dict(event='started', policy_id='test', encounter_id='1'))
            with patch.object(analyze_e2, 'E2', root), patch.object(analyze_e2, 'verify_freeze'):
                _, rows = analyze_e2.collect()
                self.assertEqual([r['status'] for r in rows], ['ok', 'infrastructure_unknown', 'not_evaluated'])
                append(path, good)
                with self.assertRaises(AssertionError):
                    analyze_e2.collect()

    def test_unstarted_panel_does_not_acquire_fresh_rank(self):
        from e2_common import inventory
        summary = analyze_e2.summarize(inventory(), [])
        self.assertEqual(summary['policies']['initial']['panels']['train']['original_rank'], 4)
        self.assertEqual(len(summary['policies']['initial']['panels']['train']['rank_population']), 5)
        for policy in summary['policies'].values():
            for panel in policy['panels'].values():
                self.assertIsNone(panel['fresh_rank'])
                self.assertIsNone(panel['fresh_rank_original_available_subset'])
                self.assertIsNone(panel['mean_payoff'])

    def test_competition_ranks_keep_missing_and_ties(self):
        self.assertEqual(analyze_e2.rank(2.5, [3, 2.5, 2.5, None]), 2)
        self.assertIsNone(analyze_e2.rank(None, [3, 2]))


if __name__ == '__main__':
    unittest.main()
