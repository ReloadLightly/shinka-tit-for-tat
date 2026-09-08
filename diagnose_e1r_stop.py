#!/usr/bin/env python3
"""Bounded reproduction of the old native stop hang; zero external calls."""
import json
import os
from pathlib import Path
import sys
from unittest.mock import patch

from e1r_process import bounded_run
from e1r_io import write_json


def child(root):
    import run_e1
    run_e1.configure_imports()
    from shinka.llm import AsyncLLMClient

    async def local_failure(*args, **kwargs):
        write_json(root / "ledger.json", {"invocations": [], "stopped": True,
                                          "stop_reason": "LOCAL metadata failure fixture"})
        print("LOCAL_OLD_STOP_TRIGGERED", flush=True)
        raise RuntimeError("LOCAL fixture only")

    with patch.object(run_e1, "E1", root), patch.object(run_e1, "verify_freeze"), \
         patch.object(AsyncLLMClient, "query", local_failure):
        run_e1.run_one("A101")


if __name__ == "__main__":
    root = Path(__file__).resolve().parent / "results/e1_r/setup/legacy_stop"
    if "--child" in sys.argv:
        child(root)
    else:
        root.mkdir(parents=True, exist_ok=False)
        write_json(root / "ledger.json", {"invocations": [], "stopped": False})
        rc, stdout, stderr = bounded_run([sys.executable, __file__, "--child"], timeout=25, env=dict(os.environ))
        (root / "console.log").write_text(stdout)
        (root / "stderr.txt").write_text(stderr)
        assert "LOCAL_OLD_STOP_TRIGGERED" in stdout
        assert rc == 124 and not (root / "runs/A101/training_summary.json").exists()
        write_json(root / "reproduction.json", {"external_proposal_invocations": 0,
            "legacy_failure_reproduced": True, "returncode": rc,
            "observation": "Original E1 native runner remained stuck after durable stop until automatic 25-second fixture timeout; no manual signal", "live_e1r": False})
        print("Old native stop hang reproduced with zero calls; fixture bounded at 25 seconds.")
