#!/usr/bin/env python3
"""Read-only E3 prelaunch diagnosis. Starts no model or proposal process."""
import json
import os
from pathlib import Path
import re
import sqlite3
import subprocess
import sys

from e3_state import E3, ROOT, read, sha, database_digest


def diagnose():
    state = read(E3 / 'ledger.json')
    pointer = read(E3 / 'runs/S101/checkpoint.json')
    checkpoint = read(E3 / pointer['path'] / 'state.json')
    log = (E3 / 'runs/S101/console.log').read_text()
    errors = re.findall(r'([123])/3 Error in query', log)
    with sqlite3.connect(f'file:{E3 / "runs/S101/programs.sqlite"}?mode=ro', uri=True) as conn:
        programs = conn.execute('SELECT id,generation,correct,combined_score FROM programs').fetchall()
        archive = conn.execute('SELECT * FROM archive').fetchall()
        attempts = conn.execute('SELECT generation,stage,status,details FROM attempt_log ORDER BY id').fetchall()
    # Reproduce the original import-order defect in a fresh process, then the
    # corrected order, without querying a model or constructing a live runner.
    env = {k: v for k, v in os.environ.items() if not k.startswith('SHINKA_')}
    commands = []
    for label, code in [
        ('original_order', 'from e1r_runtime import verify_upstream; verify_upstream(); from run_e1r import configure_imports; configure_imports()'),
        ('repaired_order', 'from run_e1r import configure_imports; configure_imports(); from e1r_runtime import verify_upstream; verify_upstream()')]:
        code += '; from shinka.llm.constants import MAX_RETRIES, OPENAI_MAX_RETRIES; print(MAX_RETRIES, OPENAI_MAX_RETRIES)'
        command = [sys.executable, '-c', code]
        result = subprocess.run(command, cwd=ROOT, env=env, capture_output=True, text=True, timeout=45)
        commands.append({'case': label, 'command': command, 'returncode': result.returncode,
                         'stdout': result.stdout, 'stderr': result.stderr})
    assert errors == ['1', '2', '3'], errors
    assert not state['invocations']
    assert len(programs) == len(archive) == 1
    assert checkpoint['consumed'] == 0 and checkpoint['runner']['next_generation_to_submit'] == 2
    return {'external_model_invocations': 0, 'reserved_ledger_invocations': 0,
        'failed_local_wrapper_attempts': 3, 'assigned_generation': 1,
        'new_generated_sources': 0, 'completed_runs': 0,
        'program_rows': programs, 'archive_rows': archive, 'attempt_records': attempts,
        'checkpoint': pointer, 'checkpoint_consumed': checkpoint['consumed'],
        'checkpoint_next_generation': checkpoint['runner']['next_generation_to_submit'],
        'checkpoint_database_digest': checkpoint['database_digest'],
        'actual_database_digest': database_digest(E3 / 'runs/S101/programs.sqlite'),
        'console_sha256': sha(E3 / 'runs/S101/console.log'),
        'original_freeze_sha256': sha(E3 / 'protocol/freeze.json'),
        'import_order_reproductions': commands,
        'accounting': 'Failed local wrapper attempts reached no external Codex launch. Slot assignment and zero reservations disagree. No retrospective reservation, slot reuse, ledger reset or resume was performed.',
        'analysis': 'No final selections, recognition or transfer. Seed-only interim training summary is not a final selection.'}


if __name__ == '__main__':
    print(json.dumps(diagnose(), indent=2))
