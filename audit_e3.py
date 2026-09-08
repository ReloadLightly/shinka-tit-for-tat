#!/usr/bin/env python3
"""Evidence-only E3 audit; source interpreted exclusively through policy.py.

Training/context/usage audits permit terminal partial evidence. Recognition is
strictly gated on all three completed runs and the frozen training selections.
"""
import argparse
import ast
from collections import Counter
import hashlib
import json
from pathlib import Path
import shutil
import sqlite3
from unittest.mock import patch
import audit_e1r
from e3_state import E3, ROOT, ORIGINAL, read, sha, opportunities, validate_accounting, surviving_workers
from e3_backend import ORDER, utc
from run_e3 import training_records
from e1r_io import write_json


def audit():
    ledger = read(E3 / 'ledger.json')
    validate_accounting(ledger)
    assert not any(v.get('open_segment') for v in ledger['runs'].values()), 'Search must be terminal before audit'
    # Exact existing native extraction, using E3's independently verified fixture.
    shutil.copyfile(E3 / 'setup/restrictions.json', E3 / 'setup/restriction_checks_verified.json')
    with patch.object(audit_e1r, 'E1', E3), patch.object(audit_e1r, 'ORDER', ORDER):
        usage = audit_e1r.collect_usage()
    gate = ledger.get('closed') and all(ledger['runs'][r]['status'] == 'completed' for r in ORDER)
    frozen = read(E3 / 'training_selections_frozen.json') if gate else None
    if gate:
        assert frozen['ledger_sha256'] == sha(E3 / 'ledger.json')
    runs = {}
    catalogue = ['# Every E3 continuation opportunity and original generated source', '',
        'Local fixture outputs under setup are excluded. No generated source is repaired.', '']
    for run_id in ORDER:
        records = training_records(run_id)
        previous_asts = {}
        by_slot = {}
        best = None
        for record in records:
            source = ROOT / record['source']
            try:
                dump = ast.dump(ast.parse(source.read_text()), include_attributes=False)
                digest = hashlib.sha256(dump.encode()).hexdigest()
            except SyntaxError:
                digest = None
            record['ast_sha256'] = digest
            record['duplicate_of_slot'] = previous_asts.get(digest) if digest else None
            if digest: previous_asts.setdefault(digest, record['slot'])
            if record['correct']:
                best = max(best, record['training']) if best is not None else record['training']
            record['best_training_so_far'] = best
            by_slot[record['slot']] = record
        ops = []
        for opportunity in [o for o in opportunities(ledger) if o['run_id'] == run_id]:
            slot = opportunity['slot']
            row = {**opportunity, 'program': by_slot.get(slot)}
            context = E3 / 'runs' / run_id / f'gen_{slot}/supplied_context.json'
            if context.exists():
                supplied = read(context)
                def identity(p):
                    assert not p.get('private_metrics') and not p.get('text_feedback')
                    return {k: p.get(k) for k in ('id','generation','combined_score','children_count')}
                row['parent'] = identity(supplied['parent'])
                row['inspirations'] = [identity(p) for key in ('archive_inspirations','top_k_inspirations') for p in supplied[key]]
            ops.append(row)
            catalogue += [f'## {run_id} opportunity {slot}', '', f'Outcome: `{opportunity["status"]}`. External invocation: {opportunity.get("external_invocation", "none")}.', '']
            if 'parent' in row:
                catalogue += [f'Native parent: slot {row["parent"]["generation"]}, training {row["parent"]["combined_score"]}; inspiration slots: {[i["generation"] for i in row["inspirations"]]}.', '']
            program = row['program']
            if program:
                catalogue += [f'Valid: {program["correct"]}; original training: {program["training"]}; duplicate of slot: {program["duplicate_of_slot"]}.',
                    f'Original source: `{program["source"]}`; SHA-256 `{program["sha256"]}`.', '',
                    '```python', (ROOT / program['source']).read_text().rstrip(), '```', '',
                    'Branch explanation: ' + __import__('write_e3_report').logic((ROOT / program['source']).read_text()), '']
            else:
                catalogue += ['No generated program or measured proposal fitness.', '']
        db_path = E3 / 'runs' / run_id / 'programs.sqlite'
        counts = None
        if db_path.exists():
            with sqlite3.connect(f'file:{db_path}?mode=ro', uri=True) as db:
                counts = {table: db.execute('SELECT COUNT(*) FROM '+table).fetchone()[0] for table in ('programs','archive')}
        generated = [r for r in records if r['slot'] > 0]
        runs[run_id] = {'status': ledger['runs'][run_id], 'opportunities': ops, 'records': records,
            'generated':len(generated),'evaluated':sum(r['training'] is not None for r in generated),
            'valid':sum(r['correct'] for r in generated), 'ast_duplicates':sum(r['duplicate_of_slot'] is not None for r in generated),
            'native_database_counts':counts, 'selection':frozen['selections'][run_id] if gate else None,
            'best_measured_training':best}
        if gate:
            from recognize import analyze_policy
            from policy import load_policy
            for record in records:
                if record['correct']:
                    record['recognition'] = analyze_policy(load_policy(ROOT / record['source']))
    result = {'generated_utc':utc(), 'analysis_gate_open':bool(gate), 'runs':runs,
        'opportunities_consumed':len(opportunities(ledger)), 'external_invocations':len(ledger['invocations']),
        'completed_runs':sum(ledger['runs'][r]['status']=='completed' for r in ORDER),
        'usage':usage,'original_e3_evidence_unchanged':True,
        'continuation_freeze':read(E3/'setup/remote_prelaunch_verified.json')}
    for name,digest in read(E3/'reconciliation.json')['preserved_sha256'].items():
        assert sha(ROOT/name)==digest,name
    write_json(E3/'audit.json',result)
    (E3/'PROPOSALS.md').write_text('\n'.join(catalogue))
    print(json.dumps({k:result[k] for k in ('analysis_gate_open','opportunities_consumed','external_invocations','completed_runs')},indent=2))
    return result


if __name__ == '__main__':
    audit()
