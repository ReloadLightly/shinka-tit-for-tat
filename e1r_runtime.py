"""Version 1 adapters for pinned Shinka; no changes to search or evaluator.

The original modules remain installed and unchanged. Hash checks fail closed on
an upstream change. Only this runner's scheduler and finalization event adapt.
"""
import asyncio
import copy
import hashlib
from pathlib import Path
import time

UPSTREAM_HASHES = {
    "shinka.core.async_runner": "153a6e1b9a7bdb673767bd3109de085c2f4e60cae07a0107858c5318f7557fed",
    "shinka.launch.scheduler": "c32d0682ac0c572d01dc10b49887cb54eb7d6b6ba760ba74c132465a1366266b",
}


def verify_upstream():
    import importlib
    for name, expected in UPSTREAM_HASHES.items():
        module = importlib.import_module(name)
        actual = hashlib.sha256(Path(module.__file__).read_bytes()).hexdigest()
        if actual != expected:
            raise RuntimeError(f"E1-R runtime adapter needs reviewed upstream: {name}")
    return dict(UPSTREAM_HASHES)


def evaluation_clock_check(original, job):
    # Copy only the job record; preserve the original proposal timestamps and
    # the real process handle. The scheduler's existing timeout/kill logic stays.
    timed = copy.copy(job)
    if getattr(job, "evaluation_started_at", None) is not None:
        timed.start_time = job.evaluation_started_at
    return original(timed)


class StopAwareFinalization(asyncio.Event):
    """Wake the native loop on its normal signal OR after bounded stopped drain."""
    def __init__(self, runner, save, drain_timeout=250):
        super().__init__()
        self.runner, self.save, self.drain_timeout = runner, save, drain_timeout

    async def wait(self):
        normal = asyncio.create_task(super().wait())
        stopped = asyncio.create_task(self.runner.should_stop.wait())
        try:
            await asyncio.wait([normal, stopped], return_when=asyncio.FIRST_COMPLETED)
            if self.runner.should_stop.is_set():
                await asyncio.wait_for(self.drain(), 350)
            return True
        finally:
            for task in (normal, stopped):
                task.cancel()
            await asyncio.gather(normal, stopped, return_exceptions=True)

    async def drain(self):
        runner = self.runner
        start = time.monotonic()
        record = {"stop_observed": True, "manual_interruption": False,
                  "proposal_tasks_at_stop": len(runner.active_proposal_tasks),
                  "evaluation_jobs_at_stop": len(runner.running_jobs)}
        self.save(record)
        # No new proposal can launch after should_stop or the durable ledger
        # latch. Let existing bounded provider calls finish and save their logs.
        tasks = list(runner.active_proposal_tasks.values())
        if tasks:
            _, pending = await asyncio.wait(tasks, timeout=self.drain_timeout)
            for task in pending:
                task.cancel()
            if pending:
                await asyncio.wait(pending, timeout=5)
            record["cancelled_proposals"] = len(pending)
        # The native monitor exits on should_stop; explicitly drain remaining
        # submitted evaluations through its original finalization method.
        for job in list(runner.running_jobs):
            deadline = time.monotonic() + 65
            while runner.scheduler.check_job_status(job) and time.monotonic() < deadline:
                await asyncio.sleep(.1)
            if runner.scheduler.check_job_status(job):
                await asyncio.wait_for(runner.scheduler.cancel_job_async(job.job_id), 5)
            await asyncio.wait_for(runner._process_single_job_safely(job), 30)
            runner.running_jobs.remove(job)
        record.update(runtime_seconds=time.monotonic() - start, drained=True)
        self.save(record)
        self.set()


def install(runner, save):
    verify_upstream()
    original = runner.scheduler.check_job_status
    runner.scheduler.check_job_status = lambda job: evaluation_clock_check(original, job)
    runner.finalization_complete = StopAwareFinalization(runner, save)
