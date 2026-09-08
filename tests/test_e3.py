import io
import json
import os
from pathlib import Path
import random
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import e3_backend as backend
import e3_state as state
import run_e3 as run
from e1r_io import write_json


class Accounting(unittest.TestCase):
    def test_commit_guard_works_outside_repository(self):
        previous = Path.cwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                with patch.object(run, 'verify_freeze'), patch.object(run, 'read', return_value={
                        'source_sha256': {'task_prompt.txt': 'checked separately'}, 'artifact_sha256': {}}):
                    self.assertEqual(len(run.verify_committed()), 40)
            finally:
                os.chdir(previous)

    def test_commit_guard_sets_retry_limits_before_first_shinka_import(self):
        code = '''
from unittest.mock import patch
import run_e3
with patch.object(run_e3, 'verify_freeze'), patch.object(run_e3, 'read', return_value={'source_sha256': {}, 'artifact_sha256': {}}):
    run_e3.verify_committed()
from shinka.llm import constants
assert constants.MAX_RETRIES == 1, constants.MAX_RETRIES
assert constants.OPENAI_MAX_RETRIES == 0, constants.OPENAI_MAX_RETRIES
print('Fresh-process frozen retry settings: one attempt, zero OpenAI retries')
'''
        proc = subprocess.run([sys.executable, '-c', code], cwd=run.ROOT, capture_output=True, text=True, timeout=45)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)

    def test_sixty_unique_ordered_slots_and_pause(self):
        value = {'invocations': []}
        for name in backend.ORDER:
            for slot in range(1, 21):
                backend.reserve(value, name, slot)
                with self.assertRaises(RuntimeError):
                    backend.reserve(value, name, slot)
        self.assertEqual(len(value['invocations']), 60)
        with self.assertRaises(RuntimeError):
            backend.reserve(value, 'S303', 21)
        for flag in ('stopped', 'closed'):
            with self.assertRaises(RuntimeError):
                backend.reserve({'invocations': [], flag: True}, 'S101', 1)

    def test_failure_classifier_is_narrow_and_auth_wins(self):
        self.assertEqual(state.classify_failure('Connection failed: error sending request', ''), 'transient_send')
        self.assertEqual(state.classify_failure('Connection failed: error sending request; quota', ''), 'quota_or_auth')
        self.assertEqual(state.classify_failure('', 'timeout'), 'ambiguous')

    def test_launch_failure_is_reserved_once_no_fitness(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'protocol').mkdir()
            (root / 'protocol/initial_prompt.md').write_text('LOCAL')
            write_json(root / 'ledger.json', {'invocations': [], 'execution_started': True})
            status = {'account': {'type': 'chatgpt', 'planType': 'pro'},
                      'limits': {'rateLimits': {'primary': {'usedPercent': 11}}},
                      'models': [{'model': backend.MODEL}]}
            with patch.object(backend, 'E3', root), patch.object(backend, 'verify_freeze'), \
                 patch.object(run, 'verify_committed'), \
                 patch.object(backend, 'read_status', return_value=status), \
                 patch.object(backend, 'bounded_run', return_value=(1, '', 'Connection failed: error sending request')) as launch, \
                 patch.dict(os.environ, E3_REAL_CODEX='LOCAL', E3_RUN_ID='S101', E3_SLOT='1'), \
                 patch.object(backend.sys, 'stdin', io.StringIO('LOCAL')):
                self.assertEqual(backend.run_codex(['exec', '--model', backend.MODEL]), 1)
                value = state.read(root / 'ledger.json')
                self.assertEqual(value['failure_class'], 'transient_send')
                self.assertEqual(len(value['invocations']), 1)
                self.assertNotIn('fitness', value['invocations'][0])
                with self.assertRaises(RuntimeError):
                    backend.run_codex(['exec', '--model', backend.MODEL])
                launch.assert_called_once()

    def test_at_most_two_read_only_recoveries(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'runs/S101').mkdir(parents=True)
            write_json(root / 'runs/S101/checkpoint.json', {})
            write_json(root / 'ledger.json', {'invocations': [], 'stopped': True, 'failure_class': 'transient_send'})
            status = {'account': {'type': 'chatgpt', 'planType': 'pro'},
                      'limits': {'rateLimits': {'primary': {'usedPercent': 11}}},
                      'models': [{'model': backend.MODEL, 'supportedReasoningEfforts': [{'reasoningEffort': 'low'}]}]}
            with patch.object(run, 'E3', root), patch.object(run, 'verify_checkpoint', return_value={'consumed': 3}), \
                 patch.object(run, 'surviving_workers', return_value=[]), patch.object(run, 'read_status', return_value=status) as check:
                for _ in range(2):
                    self.assertTrue(run.recovery_check('S101'))
                    value = state.read(root / 'ledger.json')
                    value.update(stopped=True, failure_class='transient_send')
                    write_json(root / 'ledger.json', value)
                self.assertFalse(run.recovery_check('S101'))
                self.assertEqual(check.call_count, 2)

    def test_no_post_search_before_three_completions(self):
        with patch.object(run, 'ledger', return_value={'closed': False}):
            with self.assertRaises(RuntimeError):
                run.freeze_selections()


@unittest.skipUnless(run.dependency_status()['installed'], 'Pinned Shinka required')
class FaithfulState(unittest.TestCase):
    def test_python_and_numpy_rng_roundtrip(self):
        import numpy as np
        random.seed(101)
        np.random.seed(101)
        before = json.loads(json.dumps(state.rng_state()))
        expected = [random.random(), np.random.random()]
        state.restore_rng(before)
        self.assertEqual(expected, [random.random(), np.random.random()])

    def test_native_checkpoint_recovers_context_and_entire_archive(self):
        from shinka.database import ProgramDatabase, DatabaseConfig, Program
        import numpy as np
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'programs.sqlite'
            config = DatabaseConfig(db_path=str(path), num_islands=1, archive_size=16,
                archive_criteria={'combined_score': 1.0}, num_archive_inspirations=0, num_top_k_inspirations=1)
            db = ProgramDatabase(config)
            for slot in range(5):
                db.add(Program(id=f'local_{slot}', code=f'LOCAL source {slot}', generation=slot,
                               correct=True, combined_score=slot + 1, island_idx=0))
            random.seed(202)
            np.random.seed(202)
            before = json.loads(json.dumps(state.rng_state()))
            expected = db.sample_with_fix_mode(target_generation=5)
            after = json.loads(json.dumps(state.rng_state()))
            digest = state.database_digest(path)
            db.close()
            restored = ProgramDatabase(config)
            self.assertEqual(state.database_digest(path), digest)
            state.restore_rng(before)
            actual = restored.sample_with_fix_mode(target_generation=5)
            def identify(value):
                return [value[0].to_dict(), [p.to_dict() for p in value[1]], [p.to_dict() for p in value[2]], value[3]]
            self.assertEqual(identify(expected), identify(actual))
            self.assertEqual(json.loads(json.dumps(state.rng_state())), after)
            self.assertEqual(len(restored.get_all_programs()), 5)
            restored.close()


if __name__ == '__main__':
    unittest.main()
