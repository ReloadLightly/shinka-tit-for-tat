#!/usr/bin/env python3
"""Preflight or run a bounded, API-only ShinkaEvolve experiment.

The default makes no network or model calls and needs only Python's standard
library. --execute imports the pinned Shinka dependency and calls its real
ShinkaEvolveRunner. Five mutations mean six Shinka generations including seed 0.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
from importlib import metadata
import json
import os
from pathlib import Path
import random
import subprocess
import sys
import tempfile


TASK_DIR = Path(__file__).resolve().parent
SHINKA_COMMIT = "9912af12d423504b8d580f4179fd15f5f88b8c50"
MODEL = "gpt-5-mini"


def dependency_status() -> dict:
    """Read installed metadata without importing Shinka or contacting a provider."""
    try:
        dist = metadata.distribution("shinka-evolve")
    except metadata.PackageNotFoundError:
        return {"installed": False, "pinned_commit_matches": False}
    direct_url = json.loads(dist.read_text("direct_url.json") or "{}")
    installed_commit = direct_url.get("vcs_info", {}).get("commit_id")
    return {
        "installed": True,
        "version": dist.version,
        "installed_commit": installed_commit,
        "pinned_commit_matches": installed_commit == SHINKA_COMMIT,
    }


def preflight(args: argparse.Namespace) -> dict:
    required = [TASK_DIR / name for name in ("initial.py", "evaluate.py", "task_prompt.txt")]
    missing = [path.name for path in required if not path.is_file()]
    if missing:
        raise RuntimeError("Missing task files: " + ", ".join(missing))
    if not (TASK_DIR / "task_prompt.txt").read_text(encoding="utf-8").strip():
        raise RuntimeError("task_prompt.txt is empty")
    with tempfile.TemporaryDirectory(prefix="shinka_ipd_preflight_") as tmp:
        result = subprocess.run(
            [sys.executable, str(TASK_DIR / "evaluate.py"),
             "--program_path", str(TASK_DIR / "initial.py"), "--results_dir", tmp],
            cwd=TASK_DIR, capture_output=True, text=True, timeout=60, check=False,
        )
        if result.returncode:
            raise RuntimeError("Seed evaluator failed; run evaluate.py directly for diagnostics")
        metrics = json.loads((Path(tmp) / "metrics.json").read_text(encoding="utf-8"))
        correct = json.loads((Path(tmp) / "correct.json").read_text(encoding="utf-8"))
        if correct.get("correct") is not True:
            raise RuntimeError("Seed evaluator rejected initial.py")
    dependency = dependency_status()
    key_present = bool(os.environ.get("OPENAI_API_KEY", "").strip())
    return {
        "mode": "preflight", "model_calls": 0, "api_cost_usd": 0.0,
        "seed_valid": True, "seed_combined_score": metrics["combined_score"],
        "model": MODEL, "mutation_budget": args.mutations,
        "shinka_num_generations_including_seed": args.mutations + 1,
        "api_stop_threshold_usd": args.max_api_cost,
        "budget_semantics": "soft scheduling threshold; an in-flight request can exceed it",
        "dependency": dependency, "openai_api_key_present": key_present,
        "live_ready": dependency["pinned_commit_matches"] and key_present,
        "provider_connectivity_tested": False,
    }


def write_manifest(path: Path, manifest: dict) -> None:
    path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def execute(args: argparse.Namespace, checked: dict) -> int:
    if not checked["dependency"]["pinned_commit_matches"]:
        raise RuntimeError("Install the verified dependency: python -m pip install -r requirements-shinka.txt")
    if not checked["openai_api_key_present"]:
        raise RuntimeError("Set OPENAI_API_KEY in your local environment before --execute")

    # These are supported upstream controls, set before Shinka imports constants.
    # One proposal attempt; no automatic retries at either wrapper/provider layer.
    bounded_environment = {
        "SHINKA_LLM_MAX_RETRIES": "1",
        "SHINKA_OPENAI_MAX_RETRIES": "0",
        "SHINKA_LLM_BACKOFF_MAX_TRIES": "1",
        "SHINKA_LLM_TIMEOUT": "180",
        "SHINKA_PRICING_MODE": "offline",
    }
    os.environ.update(bounded_environment)
    from shinka.core import EvolutionConfig, ShinkaEvolveRunner
    from shinka.database import DatabaseConfig
    from shinka.launch import LocalJobConfig
    import numpy as np

    random.seed(args.seed)
    np.random.seed(args.seed)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    results_dir = (args.results_dir or TASK_DIR / "results" / ("pilot_" + stamp)).resolve()
    if results_dir.exists():
        raise RuntimeError("Use a new --results-dir; this runner does not silently resume or overwrite")
    task_prompt = (TASK_DIR / "task_prompt.txt").read_text(encoding="utf-8")
    evo_config = EvolutionConfig(
        task_sys_msg=task_prompt,
        init_program_path=str(TASK_DIR / "initial.py"),
        results_dir=str(results_dir),
        num_generations=args.mutations + 1,
        job_type="local", language="python",
        patch_types=["full"], patch_type_probs=[1.0],
        max_patch_resamples=1, max_patch_attempts=1,
        llm_models=[MODEL], llm_dynamic_selection=None,
        llm_kwargs={"temperatures": [1.0], "max_tokens": 4096,
                    "reasoning_efforts": ["low"]},
        embedding_model=None, meta_rec_interval=None, meta_llm_models=None,
        novelty_llm_models=None, max_novelty_attempts=1,
        evolve_prompts=False, prompt_evolution_interval=None,
        use_text_feedback=True, enable_wandb_logging=False,
        enable_controlled_oversubscription=False,
        max_api_costs=args.max_api_cost,
    )
    job_config = LocalJobConfig(
        eval_program_path=str(TASK_DIR / "evaluate.py"),
        python_executable=sys.executable, time="00:01:00",
    )
    db_config = DatabaseConfig(
        num_islands=1, archive_size=16,
        num_archive_inspirations=0, num_top_k_inspirations=1,
        migration_rate=0.0, enable_dynamic_islands=False,
    )
    results_dir.mkdir(parents=True, exist_ok=False)
    sources = [*sorted(TASK_DIR.glob("*.py")), TASK_DIR / "task_prompt.txt"]
    manifest = {
        **checked, "mode": "live", "status": "starting",
        "model_calls": None, "api_cost_usd": None,
        "shinka_commit": SHINKA_COMMIT, "search_seed": args.seed,
        "search_reproducibility": "Local sampling seeded; remote model outputs are not guaranteed deterministic",
        "started_utc": stamp, "python_version": sys.version,
        "runtime_environment_controls": bounded_environment,
        "max_output_tokens_per_request": 4096,
        "proposal_concurrency": 1, "evaluation_concurrency": 1,
        "embeddings_enabled": False, "novelty_calls_enabled": False,
        "meta_calls_enabled": False, "prompt_evolution_enabled": False,
        "model_has_filesystem_tools": False,
        "source_sha256": {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},
    }
    manifest_path = results_dir / "launch_manifest.json"
    write_manifest(manifest_path, manifest)
    freeze = subprocess.run([sys.executable, "-m", "pip", "freeze"],
                            capture_output=True, text=True, timeout=30, check=False)
    (results_dir / "environment.txt").write_text(freeze.stdout, encoding="utf-8")
    runner = None
    try:
        runner = ShinkaEvolveRunner(
            evo_config=evo_config, job_config=job_config, db_config=db_config,
            max_evaluation_jobs=1, max_proposal_jobs=1, max_db_workers=1,
            verbose=True,
        )
        runner.run()
        manifest["status"] = "runner_finished"
        manifest["completed_generations_including_seed"] = runner.completed_generations
        manifest["api_cost_usd"] = runner.total_api_cost
        # A finished runner can have rejected/failed proposals; inspect its DB and
        # candidate logs before calling this successful behavioral rediscovery.
    except BaseException as exc:
        manifest["status"] = "interrupted" if isinstance(exc, KeyboardInterrupt) else "failed"
        manifest["error_type"] = type(exc).__name__
        raise
    finally:
        if runner is not None:
            manifest["api_cost_usd"] = runner.total_api_cost
        manifest["finished_utc"] = datetime.now(timezone.utc).isoformat()
        write_manifest(manifest_path, manifest)
    print(json.dumps({"status": manifest["status"], "results_dir": str(results_dir),
                      "api_cost_usd": manifest["api_cost_usd"]}, indent=2))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--execute", action="store_true", help="Run paid model mutation calls")
    mode.add_argument("--preflight", action="store_true", help="Zero-call check (the default)")
    parser.add_argument("--mutations", type=int, choices=range(1, 11), default=5)
    parser.add_argument("--max-api-cost", type=float, default=0.50,
                        help="Soft USD stop threshold, 0 < value <= 1.00 (default: 0.50)")
    parser.add_argument("--seed", type=int, default=20260908)
    parser.add_argument("--results-dir", type=Path)
    args = parser.parse_args()
    if not 0 < args.max_api_cost <= 1.0:
        parser.error("--max-api-cost must be greater than 0 and at most 1.00")
    if not 0 <= args.seed < 2**32:
        parser.error("--seed must be in [0, 2**32)")
    if sys.version_info < (3, 10):
        parser.error("Python >=3.10 is required")
    try:
        checked = preflight(args)
        if not args.execute:
            print(json.dumps(checked, indent=2, sort_keys=True))
            return 0
        return execute(args, checked)
    except (RuntimeError, ImportError, subprocess.TimeoutExpired) as exc:
        print(str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
