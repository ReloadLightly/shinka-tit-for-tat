import asyncio
import json
import io
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch

import e1r_backend
from e1r_status import JsonLinesRPC, read_status
from e1r_runtime import StopAwareFinalization, evaluation_clock_check
import run_e1r


class MetadataTests(unittest.TestCase):
    def fixture(self, body, timeout=.25, number=1):
        process = subprocess.Popen(["python3", "-c", body], stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE, bufsize=0)
        rpc = JsonLinesRPC(process, timeout)
        try:
            return rpc.request(number, "fixture", {})
        finally:
            rpc.selector.close()
            process.terminate()
            process.wait(timeout=2)
            process.stdin.close()
            process.stdout.close()

    def test_notification_and_response_single_write(self):
        body = 'import os,time; os.write(1,b\'{"method":"notice"}\\n{"id":1,"result":42}\\n\'); time.sleep(2)'
        self.assertEqual(self.fixture(body), 42)

    def test_partial_reads_and_utf8(self):
        body = 'import os,time; os.write(1,b\'{"id":1,"result":"\'); time.sleep(.02); os.write(1,b"\\xc3"); time.sleep(.02); os.write(1,b\'\\xa9"}\\n\')'
        self.assertEqual(self.fixture(body), "é")

    def test_eof_and_partial_eof(self):
        for body in ('pass', 'import os; os.write(1,b\'{"id":1\')'):
            with self.assertRaisesRegex(EOFError, "fixture"):
                self.fixture(body)

    def test_deadline_and_unmatched_notification_flood(self):
        for body in ('import time; time.sleep(2)',
                     'import os\nwhile True: os.write(1,b\'{"method":"notice"}\\n\')'):
            start = time.monotonic()
            with self.assertRaisesRegex(TimeoutError, "fixture"):
                self.fixture(body, timeout=.1)
            self.assertLess(time.monotonic() - start, 1)

    def test_rpc_error_does_not_echo_payload(self):
        with self.assertRaisesRegex(RuntimeError, "Codex metadata RPC error: fixture") as caught:
            self.fixture('import os; os.write(1,b\'{"id":1,"error":"PRIVATE"}\\n\')')
        self.assertNotIn("PRIVATE", str(caught.exception))

    def test_complete_status_with_coalesced_notifications(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "codex"
            path.write_text('''#!/usr/bin/env python3
import json,sys,os
for line in sys.stdin:
 m=json.loads(line)
 if 'id' not in m: continue
 result={2:{'account':{'type':'chatgpt','planType':'pro','email':'PRIVATE'}},3:{'rateLimits':{'primary':{'usedPercent':4}}},4:{'data':[{'model':'gpt-5.6-terra'}]}}.get(m['id'],{})
 os.write(1,(json.dumps({'method':'notice'})+'\\n'+json.dumps({'id':m['id'],'result':result})+'\\n').encode())
''')
            path.chmod(0o755)
            status = read_status(str(path), timeout=1)
            self.assertEqual(status["account"], {"type": "chatgpt", "planType": "pro"})
            self.assertEqual(len(status["rpc_diagnostics"]), 4)
            self.assertNotIn("PRIVATE", json.dumps(status))


@unittest.skipUnless(run_e1r.dependency_status()["installed"], "Pinned dependency required")
class TimerTests(unittest.TestCase):
    def test_old_clock_failure_and_fixed_evaluation_timeout(self):
        from shinka.launch import LocalJobConfig
        from shinka.launch.scheduler import JobScheduler
        from shinka.launch.local import ProcessWithLogging
        process = ProcessWithLogging(Mock(), (), ())
        process.poll.return_value = None
        scheduler = JobScheduler(job_type="local", config=LocalJobConfig(time="00:01:00"), verbose=False)
        now = time.time()
        job = SimpleNamespace(job_id=process, start_time=now-82, evaluation_started_at=now, generation=1)
        self.assertFalse(scheduler.check_job_status(job))
        process.kill.assert_called_once()
        process.reset_mock()
        self.assertTrue(evaluation_clock_check(scheduler.check_job_status, job))
        process.kill.assert_not_called()
        self.assertEqual(job.start_time, now-82)
        job.evaluation_started_at = now-61
        self.assertFalse(evaluation_clock_check(scheduler.check_job_status, job))
        process.kill.assert_called_once()


class TerminalTests(unittest.IsolatedAsyncioTestCase):
    async def test_stopped_evaluation_drains_through_native_finalizer(self):
        from unittest.mock import AsyncMock
        job = SimpleNamespace(job_id="fixture")
        runner = SimpleNamespace(should_stop=asyncio.Event(), active_proposal_tasks={}, running_jobs=[job],
            scheduler=SimpleNamespace(check_job_status=Mock(return_value=False)),
            _process_single_job_safely=AsyncMock())
        event = StopAwareFinalization(runner, Mock())
        runner.should_stop.set()
        await asyncio.wait_for(event.wait(), .5)
        runner._process_single_job_safely.assert_awaited_once_with(job)
        self.assertEqual(runner.running_jobs, [])

    async def test_stop_drains_outstanding_task_without_manual_signal(self):
        records = []
        task = asyncio.create_task(asyncio.sleep(.02))
        runner = SimpleNamespace(should_stop=asyncio.Event(), active_proposal_tasks={"p": task}, running_jobs=[])
        event = StopAwareFinalization(runner, records.append, drain_timeout=.1)
        runner.should_stop.set()
        await asyncio.wait_for(event.wait(), .5)
        self.assertTrue(task.done())
        self.assertTrue(records[-1]["drained"])

    async def test_stop_cancels_stalled_task_with_bound(self):
        task = asyncio.create_task(asyncio.sleep(999))
        runner = SimpleNamespace(should_stop=asyncio.Event(), active_proposal_tasks={"p": task}, running_jobs=[])
        records = []
        event = StopAwareFinalization(runner, records.append, drain_timeout=.02)
        runner.should_stop.set()
        await asyncio.wait_for(event.wait(), .5)
        self.assertTrue(task.cancelled())
        self.assertEqual(records[-1]["cancelled_proposals"], 1)

    async def test_normal_native_finalization(self):
        runner = SimpleNamespace(should_stop=asyncio.Event())
        event = StopAwareFinalization(runner, Mock())
        event.set()
        await asyncio.wait_for(event.wait(), .1)


class AccountingTests(unittest.TestCase):
    def test_failed_external_launch_reserved_once_then_latched(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "protocol").mkdir()
            (root / "protocol/initial_prompt.md").write_text("fixture only")
            (root / "ledger.json").write_text('{"invocations": [], "stopped": false, "closed": false}')
            status = {"account": {"type": "chatgpt", "planType": "pro"},
                      "limits": {"rateLimits": {"primary": {"usedPercent": 4}}},
                      "models": [{"model": "gpt-5.6-terra"}]}
            with patch.object(e1r_backend, "E1", root), patch.object(e1r_backend, "verify_freeze"), \
                 patch.object(e1r_backend, "read_status", return_value=status), \
                 patch.object(e1r_backend, "bounded_run", return_value=(1, "", "LOCAL failed launch")) as launch, \
                 patch.dict(os.environ, {"E1R_REAL_CODEX": "fixture", "E1R_RUN_ID": "A101", "E1R_SLOT": "1"}), \
                 patch.object(e1r_backend.sys, "stdin", io.StringIO("fixture only")):
                self.assertEqual(e1r_backend.run_codex(["exec", "--model", e1r_backend.MODEL]), 1)
                state = json.loads((root / "ledger.json").read_text())
                self.assertEqual(len(state["invocations"]), 1)
                self.assertTrue(state["stopped"])
                with self.assertRaises(RuntimeError):
                    e1r_backend.run_codex(["exec", "--model", e1r_backend.MODEL])
                launch.assert_called_once()

    def test_all_sixty_slots_and_each_duplicate_refused(self):
        state = {"invocations": []}
        for run in e1r_backend.ORDER:
            for slot in range(1, 11):
                e1r_backend.reserve(state, run, slot)
                with self.assertRaises(RuntimeError):
                    e1r_backend.reserve(state, run, slot)
        self.assertEqual(len(state["invocations"]), 60)
        with self.assertRaises(RuntimeError):
            e1r_backend.reserve(state, "B303", 11)
        for state in ({"invocations": [], "closed": True}, {"invocations": [], "stopped": True}):
            with self.assertRaises(RuntimeError):
                e1r_backend.reserve(state, "A101", 1)

    def test_frozen_no_retry_no_auxiliary_configuration(self):
        self.assertEqual(run_e1r.ENV_CONTROLS["SHINKA_LLM_MAX_RETRIES"], "1")
        self.assertEqual(run_e1r.ENV_CONTROLS["SHINKA_LLM_BACKOFF_MAX_TRIES"], "1")
        command = e1r_backend.command("codex", Path("catalog"))
        for setting in ("request_max_retries=0", "stream_max_retries=0"):
            self.assertTrue(any(setting in arg for arg in command))
        self.assertNotIn("--search", command)


class ProcessTests(unittest.TestCase):
    def test_timeout_returns_failure_and_preserves_output(self):
        from e1r_process import bounded_run
        rc, stdout, stderr = bounded_run([sys.executable, "-c", 'import time; print("fixture",flush=True); time.sleep(30)'],
                                         timeout=.1, env=dict(os.environ))
        self.assertEqual(rc, 124)
        self.assertEqual(stdout, "fixture\n")
        self.assertIn("timeout", stderr)

    def test_nested_child_dies_when_guard_dies(self):
        with tempfile.TemporaryDirectory() as tmp:
            pid_path = Path(tmp) / "child.pid"
            child_code = f'import os,time; open({str(pid_path)!r},"w").write(str(os.getpid())); time.sleep(30)'
            parent_code = f'from e1r_process import bounded_run; import os,sys; bounded_run([sys.executable,"-c",{child_code!r}],timeout=25,env=dict(os.environ))'
            parent = subprocess.Popen([sys.executable, "-c", parent_code])
            try:
                deadline = time.monotonic() + 3
                while not pid_path.exists() and time.monotonic() < deadline:
                    time.sleep(.01)
                self.assertTrue(pid_path.exists())
                child = int(pid_path.read_text())
                parent.kill()
                parent.wait(timeout=2)
                status = Path(f"/proc/{child}/status")
                deadline = time.monotonic() + 2
                while status.exists() and "State:\tZ" not in status.read_text() and time.monotonic() < deadline:
                    time.sleep(.01)
                self.assertTrue(not status.exists() or "State:\tZ" in status.read_text())
            finally:
                if parent.poll() is None:
                    parent.kill()
                parent.wait(timeout=2)


if __name__ == "__main__":
    unittest.main()
