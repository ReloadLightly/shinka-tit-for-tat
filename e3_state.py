"""E3 durable checkpoints and explicit failure classification; no generation."""
import hashlib
import json
import os
from pathlib import Path
import random
import sqlite3

from e1r_io import write_json

ROOT = Path(__file__).resolve().parent
E3 = ROOT / 'results/e3'
RUNNER_FIELDS = ('completed_generations', 'next_generation_to_submit', 'best_program_id',
    'total_proposals_generated', 'total_api_cost', 'completed_proposal_costs', 'avg_proposal_cost',
    '_sampling_seconds_ewma', '_evaluation_seconds_ewma', '_proposal_timing_samples',
    'prompt_evolution_counter', 'prompt_percentile_recompute_counter', 'prompt_api_cost',
    'stuck_detection_count', 'cost_limit_reached')
DB_FIELDS = ('last_iteration', 'best_program_id', 'beam_search_parent_id', '_schedule_migration',
             'best_score_generation', 'best_score_ever')


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read(path):
    return json.loads(Path(path).read_text())


def classify_failure(stdout, stderr):
    # Only a positively identified send/connection error permits auto recovery.
    value = (stdout + '\n' + stderr).lower()
    if any(x in value for x in ('quota', 'rate limit', 'usage limit', 'unauthorized',
                                'authentication', '401', '403', 'credits exhausted')):
        return 'quota_or_auth'
    if 'connection failed: error sending request' in value:
        return 'transient_send'
    return 'ambiguous'


def verify_freeze(root=E3):
    frozen = read(root / 'protocol/freeze.json')
    for name, digest in frozen['source_sha256'].items():
        if sha(ROOT / name) != digest:
            raise RuntimeError('Frozen source mismatch: ' + name)
    for name, digest in frozen['artifact_sha256'].items():
        if sha(root / name) != digest:
            raise RuntimeError('Frozen artifact mismatch: ' + name)
    for name, digest in frozen['historical_sha256'].items():
        if sha(ROOT / name) != digest:
            raise RuntimeError('Historical evidence mismatch: ' + name)
    import importlib.util
    for name, digest in read(root / 'protocol/protocol.json')['upstream_sha256'].items():
        if sha(importlib.util.find_spec(name).origin) != digest:
            raise RuntimeError('Pinned upstream mismatch: ' + name)


def rng_state():
    import numpy as np
    n = np.random.get_state()
    return {'python': random.getstate(), 'numpy': [n[0], n[1].tolist(), *n[2:]]}


def restore_rng(state):
    import numpy as np
    def tuples(value):
        return tuple(map(tuples, value)) if isinstance(value, list) else value
    random.setstate(tuples(state['python']))
    n = state['numpy']
    np.random.set_state((n[0], np.array(n[1], dtype='uint32'), *n[2:]))


def database_digest(path):
    with sqlite3.connect(f'file:{path}?mode=ro', uri=True) as conn:
        if conn.execute('PRAGMA integrity_check').fetchone()[0] != 'ok':
            raise RuntimeError('SQLite integrity failure')
        tables = [r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
        data = {name: conn.execute('SELECT * FROM "' + name + '" ORDER BY ' +
                                  ('key' if name == 'metadata_store' else 'rowid')).fetchall() for name in tables}
    return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()


def assert_drained(runner):
    if (any(not t.done() for t in runner.active_proposal_tasks.values()) or runner.running_jobs
        or runner.failed_jobs_for_retry or runner._get_completed_job_work_count()
        or runner._has_background_side_effect_work() or runner.assigned_generations):
        raise RuntimeError('Checkpoint has surviving native work')


def checkpoint(runner, root, run_id, phase):
    assert_drained(runner)
    folder = root / 'runs' / run_id
    state = read(root / 'ledger.json')
    records = [r for r in state['invocations'] if r['run_id'] == run_id]
    if any(r['status'] == 'reserved' for r in records):
        raise RuntimeError('Ambiguous reserved invocation')
    parent = folder / 'checkpoints'
    parent.mkdir(exist_ok=True)
    target = parent / f'{len(list(parent.iterdir())):03d}_{phase}_{len(records):02d}'
    target.mkdir()
    db_path = folder / 'programs.sqlite'
    with sqlite3.connect(db_path) as source, sqlite3.connect(target / 'programs.sqlite') as dest:
        source.backup(dest)
    with (target / 'programs.sqlite').open('rb') as f:
        os.fsync(f.fileno())
    write_json(target / 'ledger.json', state)
    saved = {'version': 1, 'phase': phase, 'run_id': run_id, 'consumed': len(records),
        'runner': {k: getattr(runner, k) for k in RUNNER_FIELDS},
        'database_runtime': {k: getattr(runner.db, k) for k in DB_FIELDS},
        'rng': rng_state(), 'database_digest': database_digest(db_path),
        'database_sha256': sha(target / 'programs.sqlite'), 'ledger_sha256': sha(target / 'ledger.json'),
        'invocations': state['invocations'], 'drained': True,
        'configuration_sha256': sha(folder / 'configuration.json')}
    write_json(target / 'state.json', saved)
    write_json(folder / 'checkpoint.json', {'path': str(target.relative_to(root)),
                                          'sha256': sha(target / 'state.json')})
    return saved


def verify_checkpoint(root, run_id):
    folder = root / 'runs' / run_id
    pointer = read(folder / 'checkpoint.json')
    target = root / pointer['path']
    if sha(target / 'state.json') != pointer['sha256']:
        raise RuntimeError('Checkpoint state hash mismatch')
    saved = read(target / 'state.json')
    if not saved['drained'] or saved['run_id'] != run_id:
        raise RuntimeError('Invalid checkpoint identity')
    for path, key in [('programs.sqlite', 'database_sha256'), ('ledger.json', 'ledger_sha256')]:
        if sha(target / path) != saved[key]:
            raise RuntimeError('Checkpoint artifact hash mismatch')
    if (database_digest(folder / 'programs.sqlite') != saved['database_digest']
        or database_digest(target / 'programs.sqlite') != saved['database_digest']
        or sha(folder / 'configuration.json') != saved['configuration_sha256']
        or read(root / 'ledger.json')['invocations'] != saved['invocations']):
        raise RuntimeError('Checkpoint/database/configuration/ledger disagreement')
    if saved['runner']['next_generation_to_submit'] != saved['consumed'] + 1:
        raise RuntimeError('Ambiguous checkpoint generation boundary')
    return saved


def restore(runner, saved):
    for key, value in saved['runner'].items():
        setattr(runner, key, value)
    for key, value in saved['database_runtime'].items():
        setattr(runner.db, key, value)
    restore_rng(saved['rng'])


def surviving_workers(root, exclude=()):
    import psutil
    found = []
    for proc in psutil.process_iter(['pid', 'cmdline', 'status']):
        try:
            args = proc.info['cmdline'] or []
            if proc.pid in exclude or proc.info['status'] == psutil.STATUS_ZOMBIE:
                continue
            if any('e3_backend.py' in a or (a.endswith('run_e3.py') and '--run' in args)
                   or (str(root) in a and any(x in ' '.join(args) for x in ('evaluate.py', 'codex', 'headless'))) for a in args):
                found.append({'pid': proc.pid, 'command': args})
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return found
