#!/usr/bin/env python3
"""Full native six-run and stopped-path rehearsals; NO external proposal calls."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from unittest.mock import patch

import e1r_backend as backend
import run_e1r as run
from e1r_io import write_json


def child(root, run_id, mode):
    run.E1 = backend.E1 = root
    run.configure_imports()
    from shinka.llm import AsyncLLMClient
    from shinka.llm.providers import QueryResult
    from shinka.llm.providers.headless import _render_prompt

    async def fake_query(self, msg, system_msg, msg_history, **kwargs):
        slot = int(os.environ["E1R_SLOT"])
        state = run.ledger()
        if mode in ("metadata_failure", "quota_stop") and slot == 3:
            state.update(stopped=True, stop_reason=f"LOCAL fixture {mode} before launch")
            write_json(root / "ledger.json", state)
            raise RuntimeError(state["stop_reason"])
        record = backend.reserve(state, run_id, slot)
        record["local_mock_only"] = True
        record["external_proposal_invocations"] = 0
        write_json(root / "ledger.json", state)
        prompt = _render_prompt(msg=msg, system_msg=system_msg, msg_history=msg_history)
        target = root / "runs" / run_id / "invocations" / f"{slot:02d}"
        target.mkdir(parents=True)
        (target / "prompt.md").write_text(prompt)
        if run_id.startswith("B") or slot == 1:
            assert prompt == run.initial_prompt()
        if mode == "backend_failure" and slot == 3:
            state.update(stopped=True, stop_reason="LOCAL fixture failed external launch")
            record["status"] = "failed_mock_launch"
            write_json(root / "ledger.json", state)
            raise RuntimeError(state["stop_reason"])
        # Never introduce a target-strategy fixture into the experiment.
        value = "(0, 1)[0]" if slot == 2 else "0"
        content = f"<NAME>local_fixture</NAME>\n<DESCRIPTION>Local fixture</DESCRIPTION>\n```python\n# EVOLVE-BLOCK-START\ndef policy(own_history, opponent_history):\n    return {value}\n# EVOLVE-BLOCK-END\n```"
        record["status"] = "completed_mock"
        write_json(root / "ledger.json", state)
        return QueryResult(content, msg, system_msg, [], backend.MODEL, {}, 0, 1, cost=0)

    with patch.object(run, "verify_freeze"), patch.object(AsyncLLMClient, "query", fake_query):
        return run.run_one(run_id)


def rehearsal(root, mode):
    root.mkdir(parents=True, exist_ok=False)
    (root / "protocol").mkdir()
    (root / "setup").mkdir()
    (root / "setup/printed_setup.txt").write_text("LOCAL MOCK ONLY; no external calls\n")
    (root / "protocol/freeze.json").write_text('{"source_sha256": {}}')
    write_json(root / "ledger.json", {"invocations": [], "limit": 60, "per_run_limit": 10,
        "order": backend.ORDER, "stopped": False, "closed": False, "execution_started": False,
        "local_mock_only": True})
    real_popen = subprocess.Popen

    def mocked_popen(args, **kwargs):
        if "--run" in args:
            return real_popen([sys.executable, str(run.ROOT / "rehearse_e1r.py"), "--child", args[-1],
                               "--mode", mode, "--root", str(root)], **kwargs)
        raise AssertionError(f"Unexpected subprocess launch: {args}")

    # Exercise the exact parent serial/stop/closure path, only replacing commit
    # validation and child entrypoint; real Shinka search/parser/evaluator inside.
    started = time.monotonic()
    with patch.object(run, "E1", root), patch.object(run, "verify_freeze"), \
         patch.object(run.subprocess, "Popen", mocked_popen), \
         patch.object(run, "verify_committed", return_value="LOCAL_MOCK_COMMIT"):
        rc = run.execute()
        state = run.ledger()
        selections = json.loads((root / "training_selections_frozen.json").read_text())
        expected = 60 if mode == "full" else 3 if mode == "backend_failure" else 2
        assert len(state["invocations"]) == expected, state
        assert state["closed"] and state["stopped"] == (mode != "full")
        assert rc == (0 if mode == "full" else 2)
        assert len(selections["selections"]) == 6
        if mode == "full":
            for run_id in backend.ORDER:
                rows = run.training_records(run_id)
                assert len(rows) == 11 and not rows[2]["correct"]
                assert sum(r["correct"] for r in rows[1:]) == 9
                assert selections["selections"][run_id]["slot"] == 0
        else:
            assert selections["statuses"]["A101"] == "incomplete"
            assert selections["statuses"]["B101"] == "not_started"
            assert json.loads((root / "runs/A101/terminal_finalization.json").read_text())["drained"]
        try:
            run.execute()
        except RuntimeError:
            pass
        else:
            raise AssertionError("Duplicate execution permitted")
    return {"mode": mode, "passed": True, "mock_proposal_slots": expected,
            "external_proposal_invocations": 0, "returncode": rc,
            "runtime_seconds": time.monotonic() - started, "manual_interruption": False}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=run.E1 / "setup/rehearsal")
    parser.add_argument("--child", choices=backend.ORDER)
    parser.add_argument("--mode", default="full")
    args = parser.parse_args()
    args.root = args.root.resolve()
    if args.child:
        raise SystemExit(child(args.root, args.child, args.mode))
    records = [rehearsal(args.root / mode, mode) for mode in
               ("full", "metadata_failure", "backend_failure", "quota_stop")]
    write_json(args.root / "summary.json", {"passed": True, "external_proposal_invocations": 0, "records": records})
    print(json.dumps(records, indent=2))
