#!/usr/bin/env python3
"""Zero-external-call E3 rehearsal in the genuine pinned Shinka loop."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from unittest.mock import patch

import e3_backend as backend
import run_e3 as run
from e3_state import read, verify_checkpoint, database_digest, rng_state, restore_rng
from e1r_io import write_json


def initialize(root):
    root.mkdir(parents=True, exist_ok=False)
    (root / 'protocol').mkdir()
    shutil.copyfile(run.E3 / 'protocol/seed.py', root / 'protocol/seed.py')
    write_json(root / 'ledger.json', {'invocations': [], 'limit': 60, 'per_run_limit': 20,
        'order': list(backend.ORDER), 'stopped': False, 'closed': False, 'execution_started': False,
        'local_mock_only': True, 'recoveries': [], 'runs': {r: {'status': 'unstarted'} for r in backend.ORDER}})


def child(root, failures, stop_after=None):
    run.E3 = backend.E3 = root
    run.configure_imports()
    from shinka.llm import AsyncLLMClient
    from shinka.llm.providers import QueryResult
    from shinka.llm.providers.headless import _render_prompt

    async def fake_query(self, msg, system_msg, msg_history, **kwargs):
        slot = int(os.environ['E3_SLOT'])
        state = run.ledger()
        record = backend.reserve(state, 'S101', slot)
        record.update(local_mock_only=True, external_proposal_invocations=0)
        folder = root / 'runs/S101/invocations' / f'{slot:02d}'
        folder.mkdir(parents=True)
        prompt = _render_prompt(msg=msg, system_msg=system_msg, msg_history=msg_history)
        (folder / 'prompt.md').write_text(prompt)
        if slot == 1:
            assert prompt == run.initial_prompt()
        if slot in failures:
            record.update(status='failed', failure_class='transient_send')
            state.update(stopped=True, failure_class='transient_send', stop_reason='LOCAL connection failed: error sending request')
            write_json(root / 'ledger.json', state)
            raise RuntimeError(state['stop_reason'])
        value = '(0, 1)[0]' if slot == 2 else str(slot % 2)
        content = f'<NAME>local_fixture</NAME>\n<DESCRIPTION>Local fixture</DESCRIPTION>\n```python\n# EVOLVE-BLOCK-START\ndef policy(own_history, opponent_history):\n    return {value}\n# EVOLVE-BLOCK-END\n```'
        record['status'] = 'completed'
        write_json(root / 'ledger.json', state)
        return QueryResult(content, msg, system_msg, [], backend.MODEL, {}, 0, 1, cost=0)

    original_checkpoint = run.checkpoint
    def save(runner, base, run_id, phase):
        result = original_checkpoint(runner, base, run_id, phase)
        if phase == 'boundary' and result['consumed'] == stop_after:
            # Simulate a clean process interruption at a quiescent boundary.
            runner.should_stop.set()
        return result

    with patch.object(run, 'verify_freeze'), patch.object(run, 'checkpoint', save), patch.object(AsyncLLMClient, 'query', fake_query):
        return run.run_one('S101')


def launch(root, failures, stop_after=None):
    command = [sys.executable, str(run.ROOT / 'rehearse_e3.py'), '--child', '--root', str(root),
               '--failures', failures]
    if stop_after is not None:
        command += ['--stop-after', str(stop_after)]
    index = len(list(root.glob('child*.log')))
    with (root / f'child{index}.log').open('w') as log:
        result = subprocess.run(command, stdout=log, stderr=subprocess.STDOUT, timeout=240)
    saved = verify_checkpoint(root, 'S101')
    return result.returncode, saved


def rehearse(root):
    records = []
    for label, failures in [('normal', ''), ('middle', '3'), ('final', '20'), ('first', '1')]:
        folder = root / label
        initialize(folder)
        rc, saved = launch(folder, failures)
        expected = int(failures) if failures else 20
        assert saved['consumed'] == expected, saved
        assert rc == (2 if failures else 0), rc
        if failures:
            assert not (folder / f'runs/S101/gen_{expected}/main.py').exists()
        if failures and expected < 20:
            state = read(folder / 'ledger.json')
            state.update(stopped=False, failure_class=None)
            write_json(folder / 'ledger.json', state)
            rc, saved = launch(folder, failures)
            assert rc == 0 and saved['consumed'] == 20
        state = read(folder / 'ledger.json')
        assert [r['slot'] for r in state['invocations']] == list(range(1, 21))
        assert saved['runner']['completed_generations'] == 21
        records.append({'mode': label, 'passed': True, 'mock_slots': 20, 'external_proposal_invocations': 0})
    write_json(root / 'summary.json', {'passed': True, 'records': records, 'external_proposal_invocations': 0})


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root', type=Path, required=True)
    p.add_argument('--child', action='store_true')
    p.add_argument('--failures', default='')
    p.add_argument('--stop-after', type=int)
    args = p.parse_args()
    root = args.root.resolve()
    if args.child:
        raise SystemExit(child(root, [int(v) for v in args.failures.split(',') if v], args.stop_after))
    root.mkdir(parents=True, exist_ok=False)
    rehearse(root)
