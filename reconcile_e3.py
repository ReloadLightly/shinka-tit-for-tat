#!/usr/bin/env python3
"""One idempotent, evidence-bound E3 continuation; never makes model calls."""
import argparse
import copy
import json
from pathlib import Path
import shutil
import sqlite3
import subprocess
from datetime import datetime, timezone
from e1r_io import write_json
from e3_state import ROOT, ORIGINAL, CONTINUATION, read, sha, database_digest, verify_checkpoint

REVIEWED = '7b5e8b40a2ac040b09c5c3247244a5844ab3e72b'


def preserved():
    names = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', REVIEWED, 'results/e3'], cwd=ROOT, text=True).splitlines()
    # Reports are updated for publication; their original bytes are copied below.
    return {n: sha(ROOT / n) for n in names if n not in ('results/e3/E3_REPORT.md', 'results/e3/COMMANDS.md')}


def prepare():
    root = CONTINUATION
    if (root / 'reconciliation.json').exists():
        record = read(root / 'reconciliation.json')
        for name, digest in record['preserved_sha256'].items():
            if sha(ROOT / name) != digest:
                raise RuntimeError('New contradictory original evidence: ' + name)
        for name, digest in record['derived_initial_sha256'].items():
            if sha(root / name) != digest:
                raise RuntimeError('Derived immutable reconciliation changed: ' + name)
        verify_checkpoint(root, 'S101')
        return record
    if root.exists():
        raise RuntimeError('Ambiguous partial continuation directory')
    hashes = preserved()
    for name, digest in hashes.items():
        import hashlib
        expected = hashlib.sha256(subprocess.check_output(['git', 'show', f'{REVIEWED}:{name}'], cwd=ROOT)).hexdigest()
        if digest != expected:
            raise RuntimeError('Evidence progressed or changed: ' + name)
    ledger = read(ORIGINAL / 'ledger.json')
    pointer = read(ORIGINAL / 'runs/S101/checkpoint.json')
    target = ORIGINAL / pointer['path']
    saved = read(target / 'state.json')
    assert sha(target / 'state.json') == pointer['sha256']
    assert ledger['invocations'] == saved['invocations'] == []
    assert ledger['runs']['S101']['runtime_seconds'] == 67.56626177899307
    assert all(ledger['runs'][r]['status'] == 'unstarted' for r in ('S202', 'S303'))
    assert saved['runner']['next_generation_to_submit'] == 2 and saved['consumed'] == 0
    assert saved['runner']['completed_generations'] == 1 and saved['drained']
    assert sha(target / 'programs.sqlite') == saved['database_sha256']
    assert sha(target / 'ledger.json') == saved['ledger_sha256']
    assert database_digest(target / 'programs.sqlite') == database_digest(ORIGINAL / 'runs/S101/programs.sqlite') == saved['database_digest']
    assert sha(ORIGINAL / 'runs/S101/configuration.json') == saved['configuration_sha256']
    audit = read(ORIGINAL / 'prelaunch_failure_audit.json')
    assert audit['failed_local_wrapper_attempts'] == 3 and audit['new_generated_sources'] == 0
    root.mkdir()
    shutil.copytree(ORIGINAL / 'protocol', root / 'protocol')
    (root / 'protocol/freeze.json').unlink()  # Original is unchanged and linked by hash.
    shutil.copytree(ORIGINAL / 'runs', root / 'runs')
    (root / 'historical').mkdir()
    for name in ('E3_REPORT.md', 'COMMANDS.md', 'ledger.json'):
        shutil.copyfile(ORIGINAL / name, root / 'historical' / name)
    now = datetime.now(timezone.utc).isoformat()
    opportunity = {'run_id': 'S101', 'slot': 1, 'status': 'local_prelaunch_failure',
        'local_attempts': 3, 'external_launches': 0, 'generated_policy': None, 'fitness': None,
        'reconciled_utc': now, 'provenance': 'Original terminal checkpoint and prelaunch_failure_audit.json; recorded now, no historical reservation claimed'}
    ledger.update(opportunities=[opportunity], further_external_limit=59, continuation_version=1,
        stopped=False, stop_reason=None, failure_class=None, continuation_created_utc=now)
    write_json(root / 'ledger.json', ledger)
    write_json(root / 'runs/S101/gen_1/opportunity.json', {**opportunity, 'no_program': True})
    derived = root / 'runs/S101/checkpoints/002_reconciled_01'
    derived.mkdir()
    # Full terminal backup is copied, never reconstructed from a program source.
    shutil.copyfile(target / 'programs.sqlite', derived / 'programs.sqlite')
    write_json(derived / 'ledger.json', ledger)
    new = copy.deepcopy(saved)
    new.update(version=2, phase='reconciled', consumed=1, external_invocations=0,
        opportunities=[opportunity], ledger_sha256=sha(derived / 'ledger.json'),
        original_checkpoint={'path': str(target.relative_to(ROOT)), 'sha256': pointer['sha256']})
    write_json(derived / 'state.json', new)
    write_json(root / 'runs/S101/checkpoint.json', {'path': str(derived.relative_to(root)), 'sha256': sha(derived / 'state.json')})
    assert new['runner'] == saved['runner'] and new['rng'] == saved['rng'] and new['database_runtime'] == saved['database_runtime']
    verify_checkpoint(root, 'S101')
    immutable = [str(p.relative_to(root)) for p in derived.iterdir() if not p.name.endswith(('-shm', '-wal'))]
    record = {'version': 1, 'reconciled_utc': now, 'reviewed_commit': REVIEWED,
        'original_freeze_commit': ledger['protocol_commit'], 'preserved_sha256': hashes,
        'derived_initial_sha256': {n: sha(root / n) for n in immutable},
        'opportunity': opportunity, 'external_invocations_before': 0, 'further_external_limit': 59,
        'remaining_opportunities': {'S101': list(range(2,21)), 'S202': list(range(1,21)), 'S303': list(range(1,21))},
        'native_fields_and_rng_unchanged': True, 'cumulative_runtime_seconds_before': 67.56626177899307}
    write_json(root / 'reconciliation.json', record)
    return record


def freeze():
    root = CONTINUATION
    record = prepare()
    original = read(ORIGINAL / 'protocol/freeze.json')
    sources = list(original['source_sha256']) + ['reconcile_e3.py', 'tests/test_e1r.py', 'tests/test_e3_continuation.py', 'check_e3_boundary.py']
    artifacts = [n for n in original['artifact_sha256'] if n.startswith('protocol/')]
    artifacts += ['AMENDMENT.md', 'reconciliation.json', 'setup/tests_focused.txt', 'setup/tests_full.txt',
                  'setup/boundary/summary.json', 'setup/restrictions.json', 'setup/readiness.json']
    result = {**original, 'continuation_version': 1,
        'source_sha256': {n: sha(ROOT / n) for n in sources},
        'artifact_sha256': {n: sha(root / n) for n in artifacts}, 'preserved_sha256': record['preserved_sha256']}
    write_json(root / 'protocol/freeze.json', result)
    return result


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--freeze', action='store_true')
    args = p.parse_args()
    value = freeze() if args.freeze else prepare()
    print(json.dumps({'version': 1, 'external_calls': 0, 'continuation': str(CONTINUATION)}, indent=2))
