#!/usr/bin/env python3
"""Preflight or run a bounded, subscription-only ShinkaEvolve experiment.

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
import shlex
import shutil
import subprocess
import sys
import tempfile


TASK_DIR = Path(__file__).resolve().parent
SHINKA_COMMIT = "9912af12d423504b8d580f4179fd15f5f88b8c50"
MODEL = "headless/codex@gpt-5.6-terra?effort=low"


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
    def local_check(command):
        try:
            result = subprocess.run(command, capture_output=True, text=True, timeout=15)
            return (result.stdout + result.stderr).strip() if result.returncode == 0 else None
        except (OSError, subprocess.TimeoutExpired):
            return None
    auth = local_check(["codex", "login", "status"])
    codex_version = local_check(["codex", "--version"])
    headless_version = local_check(["headless", "--version"])
    chatgpt = auth is not None and "Logged in using ChatGPT" in auth
    return {
        "mode": "preflight", "external_proposal_invocations": 0, "model_turns": 0,
        "seed_valid": True, "seed_combined_score": metrics["combined_score"],
        "model": MODEL, "mutation_budget": args.mutations,
        "shinka_num_generations_including_seed": args.mutations + 1,
        "budget_semantics": "At most five external Codex proposal invocations, not model turns",
        "dependency": dependency, "chatgpt_authenticated": chatgpt,
        "codex_version": codex_version, "headless_version": headless_version,
        "live_ready": dependency["pinned_commit_matches"] and chatgpt and headless_version == "0.6.1",
        "subscription_quota_and_live_model_checked": False,
        "provider_connectivity_tested": False,
    }


def write_manifest(path: Path, manifest: dict) -> None:
    path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def execute(args: argparse.Namespace, checked: dict) -> int:
    if not checked["dependency"]["pinned_commit_matches"]:
        raise RuntimeError("Install the verified dependency: python -m pip install -r requirements-shinka.txt")
    if not checked["live_ready"]:
        raise RuntimeError("Native Headless 0.6.1 and Codex ChatGPT authentication are required")
    from subscription_status import read_status, require_subscription_capacity
    subscription = read_status()
    require_subscription_capacity(subscription)
    if not any(m.get("model") == "gpt-5.6-terra" for m in subscription["models"]):
        raise RuntimeError("Configured subscription model is not available")
    usage_dir = TASK_DIR / "results" / "subscription_pilot_001_usage"
    previous_usage = None
    if usage_dir.exists():
        previous_usage = json.loads((usage_dir / "invocations.json").read_text())
        records = previous_usage["invocations"]
        # One explicit repair path for the observed pre-model config failure.
        # Preserve that invocation and spend only the remaining original slots.
        config_failure = (usage_dir / "invocation_1" / "stderr.txt").read_text()
        if not (args.continue_after_config_failure and len(records) == 1
                and previous_usage.get("stopped") and not previous_usage.get("manual_configuration_repair")
                and records[0]["status"] == "failed" and not records[0]["thread_ids"]
                and "reserved built-in provider IDs" in config_failure
                and args.mutations <= previous_usage["limit"] - len(records)):
            raise RuntimeError("First-pilot usage record already exists; no automatic restart or fresh budget")
    # Refuse dotenv files which upstream loads with override=True.
    package_root = Path(metadata.distribution("shinka-evolve").locate_file("shinka"))
    if any((p / ".env").exists() for p in (Path.cwd(), package_root)):
        raise RuntimeError("Remove launcher dotenv ambiguity before this subscription-only workflow")

    # These are supported upstream controls, set before Shinka imports constants.
    # One proposal attempt; no automatic retries at either wrapper/provider layer.
    bounded_environment = {
        "SHINKA_LLM_MAX_RETRIES": "1",
        "SHINKA_OPENAI_MAX_RETRIES": "0",
        "SHINKA_LLM_BACKOFF_MAX_TRIES": "1",
        "SHINKA_LLM_TIMEOUT": "240",
        "SHINKA_HEADLESS_TIMEOUT": "240",
        "SHINKA_PRICING_MODE": "offline",
    }
    os.environ.update(bounded_environment)
    # These removals affect this launcher process only, never global credentials.
    for key in list(os.environ):
        if key.endswith("API_KEY") or key in ("OPENAI_BASE_URL", "OPENAI_API_BASE", "CODEX_API_KEY"):
            os.environ.pop(key)
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
    if previous_usage is None:
        usage_dir.mkdir(parents=True, exist_ok=False)
        write_manifest(usage_dir / "invocations.json", {"limit": args.mutations, "invocations": [], "stopped": False})
        write_manifest(usage_dir / "subscription_before.json", subscription)
    else:
        previous_usage["stopped"] = False
        previous_usage["manual_configuration_repair"] = {
            "utc": datetime.now(timezone.utc).isoformat(),
            "reason": "Codex reserves built-in provider IDs; use a named local provider with existing ChatGPT auth and fixed subscription endpoint",
            "previous_invocations_retained": 1, "remaining_invocations": 4,
        }
        write_manifest(usage_dir / "invocations.json", previous_usage)
        write_manifest(usage_dir / "subscription_before_repair.json", subscription)
    mutation_dir = Path(tempfile.mkdtemp(prefix="shinka_mutation_"))
    bin_dir = usage_dir / "bin"
    bin_dir.mkdir(exist_ok=True)
    shim = bin_dir / "codex"
    if not shim.exists():
        shim.symlink_to(TASK_DIR / "subscription_guard.py")
    os.environ.update({
        "PILOT_REAL_CODEX": shutil.which("codex"),
        "PILOT_REAL_HEADLESS": shutil.which("headless"),
        "PILOT_RECORD_DIR": str(usage_dir),
        "PATH": str(bin_dir) + os.pathsep + os.environ["PATH"],
        "SHINKA_HEADLESS_COMMAND": shlex.join([sys.executable, str(TASK_DIR / "subscription_guard.py")]),
    })
    task_prompt = (TASK_DIR / "task_prompt.txt").read_text(encoding="utf-8")
    task_prompt += "\nUse only this task, the supplied programs, and training feedback. Do not read local files or search for additional experiment information. Return the requested proposal as text.\n"
    evo_config = EvolutionConfig(
        task_sys_msg=task_prompt,
        init_program_path=str(TASK_DIR / "initial.py"),
        results_dir=str(results_dir),
        num_generations=args.mutations + 1,
        job_type="local", language="python",
        patch_types=["full"], patch_type_probs=[1.0],
        max_patch_resamples=1, max_patch_attempts=1,
        llm_models=[MODEL], llm_dynamic_selection=None,
        llm_kwargs={"headless_work_dir": str(mutation_dir)},
        embedding_model=None, meta_rec_interval=None, meta_llm_models=None,
        novelty_llm_models=None, max_novelty_attempts=1,
        evolve_prompts=False, prompt_evolution_interval=None,
        use_text_feedback=True, enable_wandb_logging=False,
        enable_controlled_oversubscription=False,
        max_api_costs=None,
    )
    job_config = LocalJobConfig(
        eval_program_path=str(TASK_DIR / "evaluate.py"),
        python_executable=sys.executable, time="00:01:00",
    )
    db_config = DatabaseConfig(
        num_islands=1, archive_size=16,
        archive_selection_strategy="fitness", archive_criteria={"combined_score": 1.0},
        num_archive_inspirations=0, num_top_k_inspirations=1,
        migration_rate=0.0, enable_dynamic_islands=False,
    )
    results_dir.mkdir(parents=True, exist_ok=False)
    sources = [*sorted(TASK_DIR.glob("*.py")), TASK_DIR / "task_prompt.txt"]
    source_dir = results_dir / "launcher_sources"
    source_dir.mkdir()
    for source in sources:
        shutil.copyfile(source, source_dir / source.name)
    manifest = {
        **checked, "mode": "live", "status": "starting",
        "external_proposal_invocations": None, "model_turns": None,
        "shinka_reported_cost": None,
        "cost_semantics": "Headless estimates or missing values are not a subscription charge",
        "subscription_quota_and_live_model_checked": True,
        "usage_records": str(usage_dir),
        "authentication": "existing ChatGPT Pro; forced chatgpt; no API keys or fallback",
        "shinka_commit": SHINKA_COMMIT, "search_seed": args.seed,
        "search_reproducibility": "Local sampling seeded; remote model outputs are not guaranteed deterministic",
        "started_utc": stamp, "python_version": sys.version,
        "runtime_environment_controls": bounded_environment,
        "max_output_tokens_per_request": None,
        "token_limit_note": "Native Headless provider ignores max_tokens; wall-clock and invocation limits apply",
        "codex_timeout_seconds": 180, "headless_timeout_seconds": 210,
        "api_fallback_enabled": False,
        "proposal_concurrency": 1, "evaluation_concurrency": 1,
        "embeddings_enabled": False, "novelty_calls_enabled": False,
        "meta_calls_enabled": False, "prompt_evolution_enabled": False,
        "model_has_filesystem_tools": True,
        "blinding": "unblinded integration pilot",
        "access_limit": "Read-only permits broad filesystem reads; separate cwd and instructions are not confidentiality isolation",
        "web_search_enabled": False,
        "mutation_work_dir": str(mutation_dir),
        "source_sha256": {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},
    }
    manifest_path = results_dir / "launch_manifest.json"
    write_manifest(manifest_path, manifest)
    freeze = sorted(f"{d.metadata['Name']}=={d.version}" for d in metadata.distributions())
    (results_dir / "environment.txt").write_text("\n".join(freeze) + "\n", encoding="utf-8")
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
        manifest["shinka_reported_cost"] = runner.total_api_cost
        # A finished runner can have rejected/failed proposals; inspect its DB and
        # candidate logs before calling this successful behavioral rediscovery.
    except BaseException as exc:
        manifest["status"] = "interrupted" if isinstance(exc, KeyboardInterrupt) else "failed"
        manifest["error_type"] = type(exc).__name__
        raise
    finally:
        if runner is not None:
            manifest["shinka_reported_cost"] = runner.total_api_cost
        usage = json.loads((usage_dir / "invocations.json").read_text())
        manifest["external_proposal_invocations"] = len(usage["invocations"])
        manifest["model_turns"] = None
        manifest["completed_codex_turn_events"] = sum(r.get("completed_codex_turn_events", 0) for r in usage["invocations"])
        manifest["usage_count_note"] = "Codex turn.completed events are not counts of internal model requests"
        if usage.get("stopped"):
            manifest["status"] = "stopped_after_backend_failure"
        if (mutation_dir / "headless_prompts").exists():
            shutil.copytree(mutation_dir / "headless_prompts", results_dir / "headless_prompts", dirs_exist_ok=True)
        manifest["finished_utc"] = datetime.now(timezone.utc).isoformat()
        write_manifest(manifest_path, manifest)
    print(json.dumps({"status": manifest["status"], "results_dir": str(results_dir),
                      "external_proposal_invocations": manifest["external_proposal_invocations"]}, indent=2))
    return 0 if manifest["status"] == "runner_finished" else 2


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--execute", action="store_true", help="Run the bounded ChatGPT subscription pilot")
    mode.add_argument("--preflight", action="store_true", help="Zero-call check (the default)")
    parser.add_argument("--mutations", type=int, choices=range(1, 6), default=5)
    parser.add_argument("--seed", type=int, default=20260908)
    parser.add_argument("--results-dir", type=Path)
    parser.add_argument("--continue-after-config-failure", action="store_true",
                        help="Explicit one-time repair of recorded pre-model provider config failure; retains the original five-slot ledger")
    args = parser.parse_args()
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
