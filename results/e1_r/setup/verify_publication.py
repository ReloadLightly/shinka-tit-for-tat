import hashlib
import json
from pathlib import Path
import re
import sqlite3
import subprocess
import sys
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from audit_e1r import audit, collect_usage
from diagnose_e1r import diagnose

E1 = ROOT / 'results/e1_r'
read = lambda path: json.loads(path.read_text())
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
ledger_hash = sha(E1 / 'ledger.json')
ledger = read(E1 / 'ledger.json')
assert ledger['execution_started'] and ledger['closed'] and ledger['stopped']
assert len(ledger['invocations']) == 20 and ledger['invocations'][-1]['status'] == 'failed'
assert ledger['run_results']['A101']['returncode'] == 0
assert ledger['run_results']['B101']['returncode'] == 2
freeze = read(E1 / 'protocol/freeze.json')
for name, digest in freeze['source_sha256'].items():
    assert sha(ROOT / name) == digest, name
assert sha(E1 / 'protocol/protocol.json') == freeze['protocol_sha256']
assert sha(E1 / 'protocol/codex_model_catalog.json') == freeze['catalog_sha256']
assert sha(ROOT / 'results/e1/ledger.json') == freeze['e1_ledger_sha256']
assert sha(ROOT / 'results/subscription_pilot_001_usage/invocations.json') == freeze['pilot_ledger_sha256']
print('Frozen execution/scientific sources and closed ledgers match.', flush=True)

old = read(E1 / 'audit.json')
new = audit()
new['analysis_started_utc'] = old['analysis_started_utc']
assert new == old, 'Recomputed audit differs'
assert old['paired_descriptive_summary'] == {'n': 0}
assert all(row['A_minus_B'] is None for row in old['paired_holdout'])
assert old['analysis_started_utc'] > read(E1 / 'training_selections_frozen.json')['frozen_utc']
print('Independent interpreter replay reproduces the complete archived audit.', flush=True)

captured = {}
with patch('audit_e1r.write_json', side_effect=lambda path, data: captured.update({str(path): data})):
    usage = collect_usage()
usage['generated_utc'] = read(E1 / 'usage_summary.json')['generated_utc']
assert usage == read(E1 / 'usage_summary.json')
fixture = read(E1 / 'setup/restriction_checks_verified.json')['records'][0]['requests'][0]
for record in ledger['invocations']:
    folder = E1 / 'runs' / record['run_id'] / 'invocations' / f"{record['slot']:02d}"
    data = captured[str(folder / 'native_context_usage.json')]
    assert data == read(folder / 'native_context_usage.json')
    assert not data['tool_calls']
    assert data['native_base_instructions']['text'] == fixture['input'][1]['content'][0]['text']
    developers = [m for m in data['messages'] if m['role'] == 'developer']
    users = [m for m in data['messages'] if m['role'] == 'user']
    assert len(developers) == len(users) == 1
    assert developers[0]['content'] == fixture['input'][2]['content']
    assert ''.join(c.get('text', '') for c in users[0]['content']) == (folder / 'prompt.md').read_text()
    assert sha(folder / 'prompt.md') == record['prompt_sha256']
for previous, current in zip(ledger['invocations'], ledger['invocations'][1:]):
    assert previous['finished_utc'] < current['started_utc']
print('All 20 native contexts, fresh sessions, serial accounting and usage reproduced.', flush=True)

with patch.object(Path, 'write_text', autospec=True,
                  side_effect=lambda path, data: captured.update({str(path): json.loads(data)})):
    diagnoses = diagnose()
assert len(diagnoses) == 19
assert sum('source_established_tft_equivalence' in d for d in diagnoses.values()) == 7
for name in ('source_diagnoses.json', 'interpretation_traces.json'):
    assert captured[str(E1 / name)] == read(E1 / name)
integrity = {}
for run in ('A101', 'B101'):
    with sqlite3.connect(f'file:{E1}/runs/{run}/programs.sqlite?mode=ro', uri=True) as db:
        integrity[run] = db.execute('PRAGMA integrity_check').fetchone()[0]
        assert integrity[run] == 'ok'
assert sha(E1 / 'ledger.json') == ledger_hash
print('Source proofs, supplemental scored traces and SQLite integrity verified.', flush=True)

# Scan publication scope without printing possible credential values.
paths = subprocess.check_output(['git', 'ls-files', '-z', '--cached', '--others', '--exclude-standard'], cwd=ROOT).decode().split('\0')
patterns = [rb'sk-(?:proj-|svcacct-)?[A-Za-z0-9_-]{20,}',
            rb'gh[pousr]_[A-Za-z0-9]{30,}', rb'github_pat_[A-Za-z0-9_]{30,}',
            rb'eyJ[A-Za-z0-9_-]{15,}\.eyJ[A-Za-z0-9_-]{15,}\.[A-Za-z0-9_-]{15,}',
            rb'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----']
scanned = 0
for name in sorted(set(paths)):
    path = ROOT / name
    if not name or not path.is_file():
        continue
    data = path.read_bytes()
    assert not any(re.search(pattern, data) for pattern in patterns), f'Credential-pattern match in {name}'
    scanned += 1
broken = []
for path in [ROOT / 'README.md', ROOT / 'PROJECT_STATUS.md', *E1.glob('*.md')]:
    prose = re.sub(r'```.*?```', '', path.read_text(), flags=re.S)
    for target in re.findall(r'\]\(([^\s)]+)\)', prose):
        if '://' in target or target.startswith('#'):
            continue
        if not (path.parent / target.split('#')[0]).exists():
            broken.append([str(path.relative_to(ROOT)), target])
assert not broken, broken
result = {'ledger_sha256_unchanged': ledger_hash, 'external_invocations': 20,
          'frozen_sources_match': True, 'archived_audit_reproduced': True,
          'usage_reproduced': True, 'native_contexts_verified': 20,
          'source_proofs_and_traces_reproduced': True, 'sqlite_integrity': integrity,
          'credential_pattern_files_scanned': scanned, 'credential_pattern_matches': 0,
          'report_local_links_resolve': True, 'verification_external_proposal_invocations': 0}
output = E1 / 'setup/publication_verification.json'
assert not output.exists()
output.write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
