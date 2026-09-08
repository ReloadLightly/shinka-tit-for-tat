import copy
import json
import unittest
from unittest.mock import patch
import e3_state as state
import e3_backend as backend
import reconcile_e3


class ContinuationTests(unittest.TestCase):
    def initial(self):
        return {'invocations': [], 'opportunities': [{'run_id': 'S101', 'slot': 1,
            'status': 'local_prelaunch_failure'}], 'further_external_limit': 59}

    def test_fifty_nine_external_calls_and_sixty_opportunities(self):
        value = self.initial()
        with self.assertRaises(RuntimeError):
            state.assign_opportunity(value, 'S101', 1)
        with self.assertRaises(RuntimeError):
            backend.reserve(value, 'S101', 1)
        for run in backend.ORDER:
            for slot in range(2 if run == 'S101' else 1, 21):
                opportunity = state.assign_opportunity(value, run, slot)
                record = backend.reserve(value, run, slot)
                record['status'] = opportunity['status'] = 'completed'
                with self.assertRaises(RuntimeError):
                    backend.reserve(value, run, slot)
        self.assertEqual(len(value['invocations']), 59)
        self.assertEqual(len(state.opportunities(value)), 60)

    def test_local_failure_consumes_without_external_reservation(self):
        value = self.initial()
        op = state.assign_opportunity(value, 'S101', 2)
        op['status'] = 'local_prelaunch_failure'
        with self.assertRaises(RuntimeError):
            backend.reserve(value, 'S101', 2)
        state.assign_opportunity(value, 'S101', 3)
        backend.reserve(value, 'S101', 3)
        self.assertEqual(len(value['invocations']), 1)
        self.assertEqual(len(state.opportunities(value)), 3)

    def test_derived_checkpoint_preserves_native_fields_and_idempotence(self):
        if not (state.CONTINUATION / 'reconciliation.json').exists():
            self.skipTest('Continuation not prepared in this checkout')
        before = state.read(state.ORIGINAL / 'runs/S101/checkpoints/001_terminal_00/state.json')
        after = state.read(state.CONTINUATION / 'runs/S101/checkpoints/002_reconciled_01/state.json')
        for key in ('runner', 'rng', 'database_runtime', 'database_digest', 'database_sha256', 'configuration_sha256'):
            self.assertEqual(before[key], after[key])
        self.assertEqual((after['consumed'], after['external_invocations']), (1, 0))
        first = reconcile_e3.prepare()
        self.assertEqual(first, reconcile_e3.prepare())
        with patch.object(reconcile_e3, 'sha', return_value='contradictory'):
            with self.assertRaisesRegex(RuntimeError, 'contradictory original'):
                reconcile_e3.prepare()


if __name__ == '__main__':
    unittest.main()
