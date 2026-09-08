#!/usr/bin/env python3
"""Native E3 boundary rehearsal. Only final external executable is synthetic.

Each case uses a disposable committed checkout, actual temporary mutation cwd,
real frozen-source/Git/import checks, installed Shinka/Headless and real parsing.
The failing case restores the original cwd defect in a fixture-only shim; the
production guard itself still runs Git. No AsyncLLMClient.query replacement.
"""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from unittest.mock import patch
from e1r_io import write_json
from e3_state import ROOT, E3, read, sha, verify_checkpoint


def child(stop_after):
    import run_e3 as run
    original = run.checkpoint
    def stop(runner, root, run_id, phase):
        saved = original(runner, root, run_id, phase)
        if phase == 'boundary' and saved['consumed'] >= stop_after:
            runner.should_stop.set()
        return saved
    with patch.object(run, 'checkpoint', stop):
        return run.run_one('S101')


def fixture(out):
    out.mkdir(parents=True, exist_ok=False)
    results = []
    with tempfile.TemporaryDirectory(prefix='e3_boundary_repo_') as tmp:
        repo = Path(tmp) / 'repo'
        repo.mkdir()
        names = subprocess.check_output(['git', 'ls-files'], cwd=ROOT, text=True).splitlines()
        names += ['reconcile_e3.py', 'check_e3_boundary.py', 'tests/test_e3_continuation.py']
        for name in names:
            source = ROOT / name
            if not source.is_file() or name.startswith('results/e3/continuation_v1/'):
                continue
            dest = repo / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, dest)
            shutil.copymode(source, dest)
        base = repo / 'results/e3/continuation_v1'
        shutil.copytree(E3, base, ignore=shutil.ignore_patterns('setup', 'bin', 'execution.lock', 'ledger.lock'))
        # This is a local technical freeze of the exact production sources.
        original = read(repo / 'results/e3/protocol/freeze.json')
        sources = list(original['source_sha256']) + ['reconcile_e3.py', 'check_e3_boundary.py', 'tests/test_e3_continuation.py']
        original['source_sha256'] = {n: sha(repo / n) for n in sources}
        original['artifact_sha256'] = {n: sha(base / n) for n in original['artifact_sha256'] if n.startswith('protocol/')}
        write_json(base / 'protocol/freeze.json', original)
        subprocess.run(['git', 'init', '-q'], cwd=repo, check=True)
        subprocess.run(['git', 'add', '.'], cwd=repo, check=True)
        subprocess.run(['git', '-c', 'user.name=Local fixture', '-c', 'user.email=fixture@localhost', 'commit', '-qm', 'Local zero-call production boundary fixture'], cwd=repo, check=True)
        fakebin = Path(tmp) / 'external'
        fakebin.mkdir()
        capture = Path(tmp) / 'launches.jsonl'
        fake = fakebin / 'codex'
        seed = (base / 'protocol/seed.py').read_text()
        content = '<NAME>local_fixture</NAME>\n<DESCRIPTION>Local boundary fixture only.</DESCRIPTION>\n```python\n' + seed + '\n```'
        fake.write_text('''#!/usr/bin/env python3
import json,sys,os
from pathlib import Path
if sys.argv[1:] in (['--version'], ['-V']):
 print('codex-cli 0.153.4'); sys.exit(0)
if 'app-server' in sys.argv:
 for line in sys.stdin:
  m=json.loads(line)
  if 'id' not in m: continue
  result={2:{'account':{'type':'chatgpt','planType':'pro'}},3:{'rateLimits':{'primary':{'usedPercent':0}}},4:{'data':[{'model':'gpt-5.6-terra','supportedReasoningEfforts':[{'reasoningEffort':'low'}]}]}}.get(m['id'],{})
  print(json.dumps({'id':m['id'],'result':result}),flush=True)
 sys.exit(0)
prompt=sys.stdin.read()
''' + f'with open({str(capture)!r},"a") as f: f.write(json.dumps({{"args":sys.argv[1:],"cwd":os.getcwd(),"prompt":prompt}})+"\\n")\n' + f'''
for event in [{{'type':'thread.started','thread_id':'local-fixture'}},
 {{'type':'item.completed','item':{{'id':'local','type':'agent_message','text':{content!r}}}}},
 {{'type':'turn.completed','usage':{{'input_tokens':0,'cached_input_tokens':0,'output_tokens':0}}}}]:
 print(json.dumps(event),flush=True)
''')
        fake.chmod(0o755)
        env = dict(os.environ, PATH=str(fakebin) + os.pathsep + os.environ['PATH'])
        shim = base / 'bin/codex'
        shim.parent.mkdir()
        # Capture the actual guard's cwd omission from the historical defect.
        def install_shim(fail):
            shim.write_text('#!' + sys.executable + '\nimport sys,subprocess\nsys.path.insert(0,' + repr(str(repo)) + ')\nimport e3_backend\n' + ('''real = subprocess.check_output
def old_cwd(*args, **kwargs):
 if args and args[0][0] == 'git': kwargs.pop('cwd', None)
 return real(*args, **kwargs)
subprocess.check_output = old_cwd
''' if fail else '') + 'raise SystemExit(e3_backend.run_codex(sys.argv[1:]))\n')
            shim.chmod(0o755)
        for label, fail, stop_after in [('original_prelaunch_failure', True, 2), ('resume_next_opportunity_success', False, 3)]:
            install_shim(fail)
            value = read(base / 'ledger.json')
            value.update(stopped=False, stop_reason=None, failure_class=None, local_fixture_only=True)
            write_json(base / 'ledger.json', value)
            command = [sys.executable, str(repo / 'check_e3_boundary.py'), '--child', '--stop-after', str(stop_after)]
            with (out / f'{label}.log').open('w') as log:
                proc = subprocess.run(command, cwd=repo, env=env, stdout=log, stderr=subprocess.STDOUT, timeout=180)
            saved = verify_checkpoint(base, 'S101')
            value = read(base / 'ledger.json')
            logs = (out / f'{label}.log').read_text()
            if fail:
                assert proc.returncode == 2, logs[-5000:]
                assert saved['consumed'] == 2 and not value['invocations'], saved
                assert 'fatal: not a git repository' in logs
                assert '1/1' in logs and '2/3' not in logs
                assert not capture.exists()
                assert not (base / 'runs/S101/gen_2/main.py').exists()
            else:
                assert proc.returncode == 0, logs[-5000:]
                assert saved['consumed'] == 3 and len(value['invocations']) == 1
                assert value['invocations'][0]['slot'] == 3
                assert read(base / 'runs/S101/gen_3/results/correct.json')['correct']
                calls = [json.loads(s) for s in capture.read_text().splitlines()]
                assert len(calls) == 1
                assert calls[0]['cwd'].startswith('/tmp/e3_mutation_')
                from e3_backend import command as production_command
                assert calls[0]['args'] == production_command(str(fake), base / 'protocol/codex_model_catalog.json')[1:]
                assert saved['runner']['completed_generations'] == 4
                write_json(out / 'captured_local_launches.json', calls)
            shutil.copytree(base / 'runs/S101', out / label, ignore=shutil.ignore_patterns('headless_prompts'))
            results.append({'mode': label, 'passed': True, 'consumed_opportunities': saved['consumed'],
                'synthetic_final_launches': len(value['invocations']), 'external_proposal_invocations': 0,
                'returncode': proc.returncode, 'runner': saved['runner']})
    write_json(out / 'summary.json', {'passed': True, 'records': results, 'external_proposal_invocations': 0})


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output', type=Path)
    p.add_argument('--child', action='store_true')
    p.add_argument('--stop-after', type=int)
    a = p.parse_args()
    if a.child:
        raise SystemExit(child(a.stop_after))
    fixture(a.output.resolve())
