#!/usr/bin/env python3
"""Zero-external-call reproductions of E1 infrastructure failure mechanisms."""
import json
import os
from pathlib import Path
import selectors
import subprocess
import tempfile
import time
from types import SimpleNamespace
from unittest.mock import Mock, patch

from e1_backend import E1
from subscription_guard import write_json
import subscription_status


def check_buffered_metadata():
    """Two replies arrive in one write: TextIO buffering hides one from select."""
    real_selector = selectors.DefaultSelector

    class FastFixtureSelector:
        def __init__(self):
            self.inner = real_selector()
        def register(self, *args, **kwargs):
            return self.inner.register(*args, **kwargs)
        def select(self, timeout=None):
            return self.inner.select(min(timeout, .2))
        def close(self):
            self.inner.close()

    with tempfile.TemporaryDirectory(prefix="e1_metadata_fixture_") as tmp:
        fake = Path(tmp) / "fake_codex"
        fake.write_text("#!/usr/bin/env python3\nimport os,sys\nsys.stdin.readline()\nos.write(1, b'{\"method\":\"fixture_notification\"}\\n{\"id\":1,\"result\":{}}\\n')\nsys.stdin.readline()\n")
        fake.chmod(0o755)
        start = time.monotonic()
        with patch.object(subscription_status.selectors, "DefaultSelector", FastFixtureSelector):
            try:
                subscription_status.read_status(str(fake))
            except TimeoutError as exc:
                legacy = {"outcome": type(exc).__name__, "message": str(exc), "seconds": time.monotonic() - start}
            else:
                raise AssertionError("Fixture did not expose buffered-reply failure")
        # Control: receive complete bytes into an explicit buffer, consume queued
        # lines before polling again. This demonstrates the required repair;
        # the frozen live transport is deliberately not modified or rerun.
        child = subprocess.Popen([str(fake)], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        child.stdin.write(b'{"id":1}\n')
        child.stdin.flush()
        with real_selector() as poller:
            poller.register(child.stdout, selectors.EVENT_READ)
            assert poller.select(2)
            buffered = os.read(child.stdout.fileno(), 65536)
            messages = [json.loads(line) for line in buffered.splitlines()]
            assert [m.get("id") for m in messages] == [None, 1]
        child.terminate()
        child.wait(timeout=2)
        child.stdin.close()
        child.stdout.close()
    return {"legacy": legacy, "explicit_byte_buffer_control": "Received notification and requested reply without another fd poll",
            "live_attribution": "Reproduces a concrete vulnerability, but the live check did not log the RPC stage/buffer, so the exact live cause remains unproven"}


def check_evaluation_clock():
    from shinka.launch import LocalJobConfig
    from shinka.launch.scheduler import JobScheduler
    from shinka.launch.local import ProcessWithLogging
    inner = Mock()
    inner.poll.return_value = None
    inner.pid = 999999
    process = ProcessWithLogging(inner, (), ())
    scheduler = JobScheduler(job_type="local", config=LocalJobConfig(time="00:01:00"), verbose=False)
    now = time.time()
    job = SimpleNamespace(job_id=process, start_time=now - 82, evaluation_started_at=now, generation=4)
    assert scheduler.check_job_status(job) is False
    process.kill.assert_called_once()
    process.reset_mock()
    job.start_time = job.evaluation_started_at
    assert scheduler.check_job_status(job) is True
    process.kill.assert_not_called()
    job.start_time = now - 61
    assert scheduler.check_job_status(job) is False
    process.kill.assert_called_once()
    return {"proposal_clock_82s_evaluation_clock_0s": "Killed immediately by pinned scheduler",
            "evaluation_clock_0s_control": "Kept running", "evaluation_clock_61s_control": "Killed at real evaluation limit",
            "uses_mock_process_only": True}


def checks():
    return {"external_proposal_invocations": 0,
            "metadata_reader": check_buffered_metadata(), "evaluation_timer": check_evaluation_clock(),
            "stop_finalization": {"source_observation": "Pinned runner waits for finalization_complete; setting should_stop alone exits monitor/coordinator without necessarily setting finalization_complete",
                                  "live_observation": "No further launch after stop latch; supervisor sent SIGINT to stopped A303 child; finally block saved summary and parent closed ledger",
                                  "required_repair": "Explicit finalization after draining/cancelling in-flight work; test terminal metadata failures without a manual interrupt"}}


if __name__ == "__main__":
    output = E1 / "setup" / "failure_reproductions.json"
    if output.exists():
        raise SystemExit("Refusing to overwrite failure evidence")
    result = checks()
    write_json(output, result)
    print(json.dumps(result, indent=2))
