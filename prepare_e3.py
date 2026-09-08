#!/usr/bin/env python3
"""Freeze E3 only after successful zero-call preparation; never proposes."""
from dataclasses import asdict
import importlib
import json
from pathlib import Path
import subprocess

from e1r_io import write_json
from e1r_status import require_subscription_capacity
from e3_state import E3, ROOT, read, sha
from e3_backend import MODEL, ORDER
from run_e3 import preflight, initial_prompt, RUN_SECONDS
from analyze_e3 import encounters


def freeze():
    if (E3 / 'ledger.json').exists() or (E3 / 'protocol/freeze.json').exists():
        raise RuntimeError('E3 already frozen; cannot reset')
    checked = preflight()
    for name in ('restriction_checks_verified.json', 'rehearsal_release/summary.json'):
        result = read(E3 / 'setup' / name)
        assert result['passed'] and result['external_proposal_invocations'] == 0
    status = read(E3 / 'setup/subscription_before.json')
    require_subscription_capacity(status)
    model = next(m for m in status['models'] if m['model'] == MODEL)
    assert any(e['reasoningEffort'] == 'low' for e in model['supportedReasoningEfforts'])
    assert 'OK' in (E3 / 'setup/tests_e3_release.txt').read_text()
    assert (E3 / 'setup/tests_full_release.txt').read_text().rstrip().endswith('OK')
    assert list(read(E3 / 'setup/catalog_comparison.json')['differences']) == ['apply_patch_tool_type']
    versions = {n: subprocess.check_output([n, '--version'], text=True, timeout=15).strip() for n in ('codex', 'headless')}
    assert versions == {'codex': 'codex-cli 0.153.4', 'headless': '0.6.1'}
    from shinka.database import DatabaseConfig
    db = DatabaseConfig(num_islands=1, archive_size=16, archive_selection_strategy='fitness',
        archive_criteria={'combined_score': 1.0}, num_archive_inspirations=0, num_top_k_inspirations=1,
        migration_rate=0.0, enable_dynamic_islands=False)
    upstream = {}
    for name in ('shinka.core.async_runner', 'shinka.core.sampler', 'shinka.database.dbase',
                 'shinka.database.async_dbase', 'shinka.database.parents', 'shinka.database.inspirations',
                 'shinka.database.island_sampler', 'shinka.launch.scheduler', 'shinka.llm.providers.headless'):
        upstream[name] = sha(importlib.import_module(name).__file__)
    write_json(E3 / 'protocol/encounters.json', encounters())
    (E3 / 'protocol/initial_prompt.md').write_text(initial_prompt())
    write_json(E3 / 'protocol/protocol.json', {**checked, 'versions': versions,
        'run_ids': ORDER, 'local_seeds': [101, 202, 303], 'remote_deterministic': False,
        'limit': 60, 'per_run_limit': 20, 'generations_including_seed': 21,
        'database': asdict(db), 'upstream_sha256': upstream, 'automatic_recoveries': 2,
        'timeouts_seconds': {'codex': 180, 'headless_wrapper': 210, 'native_provider': 240,
                             'evaluation': 60, 'drain': 350, 'cumulative_per_run': RUN_SECONDS,
                             'transfer_worker_per_policy_panel': 300},
        'fitness': 'unchanged original-training total own payoff / total rounds',
        'selection': 'highest admissible original-training payoff including seed; earliest exact tie',
        'primary_outcome': 'selected development payoff minus seed development payoff',
        'analysis_gate': 'all three runs completed and selections frozen',
        'retries': 'one Shinka attempt, zero Codex request/stream retries, no resampling',
        'continuation': 'quiescent native archive/database/generation/Python+NumPy RNG checkpoint; no best-only restart'})
    sources = ['initial.py', 'environment.py', 'policy.py', 'evaluate.py', 'task_prompt.txt',
        'run_e3.py', 'e3_backend.py', 'e3_state.py', 'prepare_e3.py', 'analyze_e3.py', 'rehearse_e3.py',
        'tests/test_e3.py', 'run_e1r.py', 'run_evo.py', 'e1r_status.py', 'subscription_status.py',
        'e1r_runtime.py', 'e1r_process.py', 'e1r_io.py', 'check_e1r_restrictions.py', 'e2_common.py',
        'baseline.py', 'requirements-shinka.txt']
    artifacts = ['protocol/PROTOCOL.md', 'protocol/protocol.json', 'protocol/encounters.json',
                 'protocol/seed.py', 'protocol/initial_prompt.md', 'protocol/codex_model_catalog.json',
                 'setup/restriction_checks_verified.json', 'setup/rehearsal_release/summary.json',
                 'setup/tests_e3_release.txt', 'setup/catalog_comparison.json']
    historical = ['results/subscription_pilot_001_usage/invocations.json', 'results/e1/ledger.json',
                  'results/e1_r/ledger.json', 'results/e1_r/runs/A101/gen_4/main.py']
    write_json(E3 / 'protocol/freeze.json', {'reviewed_main': '9564d2125d5b818e24df1aa2b958938dc2f843f6',
        'source_sha256': {n: sha(ROOT / n) for n in sources},
        'artifact_sha256': {n: sha(E3 / n) for n in artifacts},
        'historical_sha256': {n: sha(ROOT / n) for n in historical}})
    write_json(E3 / 'ledger.json', {'limit': 60, 'per_run_limit': 20, 'order': ORDER,
        'invocations': [], 'stopped': False, 'closed': False, 'execution_started': False,
        'recoveries': [], 'runs': {r: {'status': 'unstarted'} for r in ORDER}})
    print('E3 frozen with zero external proposal invocations. Commit before --execute.')


if __name__ == '__main__':
    freeze()
