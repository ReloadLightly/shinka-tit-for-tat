#!/usr/bin/env python3
"""E1: zero-call preflight by default; --freeze then one --execute, no resume."""
import argparse
import ast
from dataclasses import asdict
import hashlib
import json
import os
from pathlib import Path
import random
import shlex
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import time

from e1r_backend import E1, MODEL, ORDER, ROOT, utc, verify_freeze
from evaluate import evaluate_file
from run_evo import dependency_status
from e1r_io import write_json
from e1r_runtime import install, verify_upstream
from e1r_status import read_status, require_subscription_capacity

ENV_CONTROLS = {"SHINKA_LLM_MAX_RETRIES": "1", "SHINKA_OPENAI_MAX_RETRIES": "0",
                "SHINKA_LLM_BACKOFF_MAX_TRIES": "1", "SHINKA_LLM_TIMEOUT": "240",
                "SHINKA_HEADLESS_TIMEOUT": "240", "SHINKA_PRICING_MODE": "offline"}
FROZEN_SOURCES = ("initial.py", "policy.py", "environment.py", "evaluate.py", "task_prompt.txt",
                  "run_e1r.py", "e1r_backend.py", "e1r_status.py", "subscription_guard.py",
                  "check_e1r_restrictions.py", "e1r_runtime.py", "e1r_io.py", "rehearse_e1r.py",
                  "tests/test_e1r.py", "e1r_process.py")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def configure_imports():
    os.environ.update(ENV_CONTROLS)
    for key in list(os.environ):
        if key.endswith("API_KEY") or key in ("OPENAI_BASE_URL", "OPENAI_API_BASE"):
            os.environ.pop(key)
    if (ROOT / ".env").exists():
        raise RuntimeError("Local dotenv ambiguity")
    # Freeze ONE upstream full-rewrite format equally in both conditions.
    # No task content or candidate code is supplied by this adaptation.
    import shinka.core.sampler as sampler
    sampler.FULL_SYS_FORMATS = sampler.FULL_SYS_FORMATS[:1]


def task():
    return (ROOT / "task_prompt.txt").read_text() + (
        "\nUse only this task, the supplied programs, and training feedback. "
        "Do not read local files or search for additional experiment information. "
        "Return the requested proposal as text.\n")


def initial_prompt():
    from shinka.core.sampler import PromptSampler
    from shinka.database import Program
    from shinka.llm.providers.headless import _render_prompt
    with tempfile.TemporaryDirectory() as tmp:
        metrics, correct = evaluate_file(ROOT / "initial.py", tmp)
    seed = Program(id="initial", code=(ROOT / "initial.py").read_text(), generation=0,
                   correct=correct["correct"], combined_score=metrics["combined_score"],
                   public_metrics=metrics["public"], private_metrics=metrics["private"], text_feedback="")
    sampler = PromptSampler(task_sys_msg=task(), patch_types=["full"], patch_type_probs=[1.0], use_text_feedback=True)
    system, user, _ = sampler.sample(seed, [], [])
    return _render_prompt(msg=user, system_msg=system, msg_history=[])


def preflight():
    if not dependency_status()["pinned_commit_matches"]:
        raise RuntimeError("Pinned Shinka installation required")
    configure_imports()
    upstream = verify_upstream()
    prompt = initial_prompt()
    assert prompt == (ROOT / "results/e1/protocol/initial_prompt.md").read_text()
    return {"external_proposal_invocations": 0, "initial_prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
            "model": MODEL, "order": ORDER, "limit": 60, "limit_per_run": 10,
            "dependency": dependency_status(), "upstream_source_sha256": upstream}


def freeze():
    checked = preflight()
    if (E1 / "protocol" / "freeze.json").exists() or (E1 / "ledger.json").exists():
        raise RuntimeError("Existing E1 freeze/ledger cannot be replaced")
    restrictions = json.loads((E1 / "setup" / "restriction_checks_verified.json").read_text())
    if not restrictions.get("passed") or restrictions["external_proposal_invocations"] != 0:
        raise RuntimeError("Effective local restriction checks required")
    rehearsal = json.loads((E1 / "setup/rehearsal_release/summary.json").read_text())
    if not rehearsal.get("passed") or rehearsal["external_proposal_invocations"] != 0:
        raise RuntimeError("Full local rehearsal including stop paths required")
    status = read_status()
    require_subscription_capacity(status)
    if not any(m.get("model") == MODEL for m in status["models"]):
        raise RuntimeError("Requested subscription model unavailable; substitution forbidden")
    model = next(m for m in status["models"] if m.get("model") == MODEL)
    if not any(r.get("reasoningEffort") == "low" for r in model["supportedReasoningEfforts"]):
        raise RuntimeError("Frozen low reasoning effort unavailable")
    versions = {name: subprocess.check_output([name, "--version"], text=True, timeout=15).strip()
                for name in ("codex", "headless")}
    if versions != {"codex": "codex-cli 0.153.4", "headless": "0.6.1"}:
        raise RuntimeError(f"Restriction-tested versions changed: {versions}")
    write_json(E1 / "setup" / "subscription_before.json", status)
    protocol = {**checked, "frozen_utc": utc(), "versions": versions, "reasoning_effort": "low",
                "conditions": {"A": "Native Shinka parent selection, accumulated programs, training feedback",
                               "B": "Native common proposal/evaluation harness; parent/context sampler always returns original seed and empty inspirations"},
                "proposal_format": "Native FULL_SYS_FORMATS[0], fixed for both arms",
                "selection": "Highest admissible training payoff including seed; exact ties earliest slot",
                "duplicate_definition": "AST-identical to earlier admissible or invalid parsed source in same run, including seed; formatting/comments ignored. No replacement.",
                "analysis_gate": "Freeze all six training selections before ANY holdout evaluation or recognition",
                "primary_outcome": "Development-holdout payoff of training-selected candidate",
                "secondary_outcomes": ["training payoff", "valid proposal rate", "best training trajectory", "admissible TFT-compatible appearance and slot"],
                "timeouts_seconds": {"codex": 180, "headless": 210, "native_provider": 240, "run": 2600},
                "retry_resample_attempts": 1, "embeddings": False, "auxiliary_models": False,
                "fallback": False, "max_api_costs": None, "concurrency": 1,
                "local_seeds": [101, 202, 303], "remote_deterministic": False,
                "order_balance": "A first in two pairs, B first in one; approximate balance",
                "hypothesis": "At equal proposal opportunities the combined Shinka search procedure improves training-selected development-holdout payoff over independent generation.",
                "interpretation": "Consistent positive paired differences support; negative weaken; small/inconsistent/invalidity-dominated or incomplete differences leave uncertain. Three pairs exploratory, not sixty independent replicates.",
                "boundary": "Supported native tool-registration controls; inactive code-mode host. No file/search/MCP/agent integrations; no OS confidentiality container or knowledge-free invention claim.",
                "harness_adapter_version": 1, "evaluation_timeout_seconds": 60,
                "stopped_drain_timeout_seconds": 350, "ledger_durability": "atomic replace plus file and directory fsync",
                "restrictions_sha256": sha(E1 / "setup" / "restriction_checks_verified.json"),
                "environment_controls": ENV_CONTROLS}
    write_json(E1 / "protocol" / "protocol.json", protocol)
    (E1 / "protocol" / "initial_prompt.md").write_text(initial_prompt())
    frozen = {"frozen_utc": utc(), "source_sha256": {name: sha(ROOT / name) for name in FROZEN_SOURCES},
              "protocol_sha256": sha(E1 / "protocol" / "protocol.json"),
              "catalog_sha256": sha(E1 / "protocol" / "codex_model_catalog.json"),
              "pilot_ledger_sha256": sha(ROOT / "results/subscription_pilot_001_usage/invocations.json")}
    frozen["e1_ledger_sha256"] = sha(ROOT / "results/e1/ledger.json")
    write_json(E1 / "protocol" / "freeze.json", frozen)
    write_json(E1 / "ledger.json", {"limit": 60, "per_run_limit": 10, "order": ORDER,
        "invocations": [], "stopped": False, "closed": False, "execution_started": False})
    setup = (E1 / "protocol" / "PROTOCOL.md").read_text()
    (E1 / "setup" / "printed_setup.txt").write_text(setup)
    print(setup, flush=True)
    print(json.dumps({"freeze": str(E1 / "protocol" / "freeze.json"), "external_invocations": 0}), flush=True)


def ledger():
    return json.loads((E1 / "ledger.json").read_text())


def progress(run_id, slot, stage, valid=None, score=None, best=None):
    count = len(ledger()["invocations"])
    print(f"[E1-R] condition={run_id[0]} replicate={run_id[1:]} slot={slot}/10 stage={stage} "
          f"valid={valid} training={score} current_best={best} invocations={count}/60", flush=True)


def training_records(run_id):
    records = []
    for slot in range(11):
        folder = E1 / "runs" / run_id / f"gen_{slot}"
        if not (folder / "main.py").exists():
            continue
        correctness = folder / "results" / "correct.json"
        metrics = folder / "results" / "metrics.json"
        correct = json.loads(correctness.read_text()) if correctness.exists() else {"correct": False, "error": "No evaluator result"}
        score = json.loads(metrics.read_text())["combined_score"] if metrics.exists() else None
        records.append({"slot": slot, "source": str((folder / "main.py").relative_to(ROOT)),
                        "sha256": sha(folder / "main.py"), "correct": correct["correct"],
                        "error": correct.get("error"), "training": score})
    return records


def select(records):
    return max((r for r in records if r["correct"] and r["training"] is not None),
               key=lambda r: (r["training"], -r["slot"]))


def run_one(run_id):
    verify_freeze()
    configure_imports()
    from shinka.core import EvolutionConfig, ShinkaEvolveRunner
    from shinka.database import DatabaseConfig, Program
    from shinka.launch import LocalJobConfig
    import numpy as np
    random.seed(int(run_id[1:]))
    np.random.seed(int(run_id[1:]))
    folder = E1 / "runs" / run_id
    if (folder / "gen_0").exists():
        raise RuntimeError("E1 runs cannot be resumed or overwritten")
    folder.mkdir(parents=True, exist_ok=True)
    shim_dir = E1 / "bin"
    shim_dir.mkdir(exist_ok=True)
    shim = shim_dir / "codex"
    if not shim.exists():
        shim.symlink_to(ROOT / "e1r_backend.py")
    os.environ.update(E1R_REAL_CODEX=shutil.which("codex"), E1R_REAL_HEADLESS=shutil.which("headless"),
                      E1R_RUN_ID=run_id, PATH=str(shim_dir) + os.pathsep + os.environ["PATH"],
                      SHINKA_HEADLESS_COMMAND=shlex.join([sys.executable, str(ROOT / "e1r_backend.py")]))
    work = Path(tempfile.mkdtemp(prefix="e1_mutation_"))
    evo = EvolutionConfig(task_sys_msg=task(), init_program_path=str(ROOT / "initial.py"),
        results_dir=str(folder), num_generations=11, job_type="local", language="python",
        patch_types=["full"], patch_type_probs=[1.0], max_patch_resamples=1, max_patch_attempts=1,
        llm_models=[f"headless/codex@{MODEL}?effort=low"], llm_dynamic_selection=None,
        llm_kwargs={"headless_work_dir": str(work)}, embedding_model=None,
        meta_rec_interval=None, meta_llm_models=None, novelty_llm_models=None,
        max_novelty_attempts=1, evolve_prompts=False, prompt_evolution_interval=None,
        use_text_feedback=True, enable_wandb_logging=False, enable_controlled_oversubscription=False,
        max_api_costs=None)
    db = DatabaseConfig(num_islands=1, archive_size=16, archive_selection_strategy="fitness",
        archive_criteria={"combined_score": 1.0}, num_archive_inspirations=0,
        num_top_k_inspirations=1, migration_rate=0.0, enable_dynamic_islands=False)
    job = LocalJobConfig(eval_program_path=str(ROOT / "evaluate.py"), python_executable=sys.executable, time="00:01:00")
    write_json(folder / "configuration.json", {"run_id": run_id, "evolution": asdict(evo),
                                                "database": asdict(db), "job": asdict(job), "started_utc": utc()})

    class E1Runner(ShinkaEvolveRunner):
        async def _setup_async(self):
            await super()._setup_async()
            if run_id.startswith("B"):
                programs = await self.async_db.get_programs_by_generation_async(0)
                seed_dict = programs[0].to_dict()

                async def independent_context(**kwargs):
                    return Program.from_dict(seed_dict), [], [], False

                self.async_db.sample_with_fix_mode_async = independent_context

        async def _run_patch_async(self, parent_program, archive_programs, top_k_programs, generation, meta_recs=None, **kwargs):
            if ledger().get("stopped"):
                raise RuntimeError("Stopped experiment: no further proposals")
            os.environ["E1R_SLOT"] = str(generation)
            target = folder / f"gen_{generation}"
            target.mkdir(exist_ok=True)
            write_json(target / "supplied_context.json", {"parent": parent_program.to_dict(),
                "archive_inspirations": [p.to_dict() for p in archive_programs],
                "top_k_inspirations": [p.to_dict() for p in top_k_programs]})
            progress(run_id, generation, "proposal", best=select(training_records(run_id))["training"])
            try:
                return await super()._run_patch_async(parent_program, archive_programs, top_k_programs, generation, meta_recs, **kwargs)
            except BaseException as exc:
                state = ledger()
                state.update(stopped=True, stop_reason=state.get("stop_reason") or f"Proposal infrastructure: {type(exc).__name__}")
                write_json(E1 / "ledger.json", state)
                raise
            finally:
                if ledger().get("stopped"):
                    self.should_stop.set()

        async def _process_single_job_safely(self, job):
            result = await super()._process_single_job_safely(job)
            if job.db_retry_count:
                state = ledger()
                state.update(stopped=True, stop_reason="Database finalization failed; no retry")
                write_json(E1 / "ledger.json", state)
                self.should_stop.set()
            rows = training_records(run_id)
            newest = rows[-1]
            progress(run_id, newest["slot"], "evaluated", newest["correct"], newest["training"], select(rows)["training"])
            return result

    runner = E1Runner(evo_config=evo, db_config=db, job_config=job,
                     max_evaluation_jobs=1, max_proposal_jobs=1, max_db_workers=1, verbose=True)
    runner.MAX_DB_RETRY_ATTEMPTS = 1
    install(runner, lambda record: write_json(folder / "terminal_finalization.json", record))
    start = time.monotonic()
    try:
        runner.run()
    finally:
        if (work / "headless_prompts").exists():
            shutil.copytree(work / "headless_prompts", folder / "headless_prompts")
        records = training_records(run_id)
        summary = {"run_id": run_id, "records": records, "training_selected": select(records) if records else None,
                   "runtime_seconds": time.monotonic() - start, "finished_utc": utc(),
                   "shinka_completed_generations": runner.completed_generations,
                   "headless_list_price_estimate_not_charge": runner.total_api_cost}
        write_json(folder / "training_summary.json", summary)
    return 2 if ledger().get("stopped") else 0


def freeze_selections():
    path = E1 / "training_selections_frozen.json"
    if path.exists():
        raise RuntimeError("Selections already frozen")
    state = ledger()
    if not state.get("closed"):
        raise RuntimeError("Terminal closed ledger required")
    selections, statuses = {}, {}
    # Training-only seed measurement also handles failure before initial setup.
    with tempfile.TemporaryDirectory() as tmp:
        metrics, correct = evaluate_file(ROOT / "initial.py", tmp)
    baseline = {"slot": 0, "source": "initial.py", "sha256": sha(ROOT / "initial.py"),
                "correct": correct["correct"], "error": correct.get("error"), "training": metrics["combined_score"]}
    for run_id in ORDER:
        rows = training_records(run_id)
        count = sum(r["run_id"] == run_id for r in state["invocations"])
        selections[run_id] = select(rows) if rows else dict(baseline)
        finished = state.get("run_results", {}).get(run_id, {}).get("returncode") == 0
        statuses[run_id] = "complete" if count == 10 and finished else "incomplete" if count or rows else "not_started"
    write_json(path, {"frozen_utc": utc(), "complete_design": all(v == "complete" for v in statuses.values()),
        "selection_rule": "Highest admissible recorded training payoff including seed; earliest exact tie",
        "terminal_handling": "Incomplete/unstarted runs have provisional/seed placeholder selections and no primary outcome; no reselection",
        "statuses": statuses, "selections": selections, "ledger_sha256": sha(E1 / "ledger.json")})


def verify_committed():
    # Require the exact frozen files to exist in a commit before any proposal.
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    frozen = json.loads((E1 / "protocol" / "freeze.json").read_text())
    for name in [*frozen["source_sha256"], "results/e1_r/protocol/freeze.json",
                 "results/e1_r/protocol/protocol.json", "results/e1_r/protocol/initial_prompt.md"]:
        committed = subprocess.check_output(["git", "show", f"{commit}:{name}"])
        if committed != (ROOT / name).read_bytes():
            raise RuntimeError(f"Uncommitted protocol/source: {name}")
    return commit


def execute():
    import fcntl
    with (E1 / "execution.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        try:
            return _execute_locked()
        except BaseException as exc:
            state = ledger()
            if state.get("execution_started") and not state.get("closed"):
                state.update(stopped=True, closed=True,
                             stop_reason=state.get("stop_reason") or f"Launcher: {type(exc).__name__}")
                write_json(E1 / "ledger.json", state)
                freeze_selections()
            raise


def _execute_locked():
    verify_freeze()
    path = E1 / "ledger.json"
    state = ledger()
    if state.get("execution_started") or state.get("closed") or state.get("stopped") or state["invocations"]:
        raise RuntimeError("E1-R already attempted: no reset, continuation or duplicate experiment")
    commit = verify_committed()
    state.update(execution_started=True, protocol_commit=commit, execution_started_utc=utc())
    write_json(path, state)
    print((E1 / "setup" / "printed_setup.txt").read_text(), flush=True)
    for run_id in ORDER:
        folder = E1 / "runs" / run_id
        folder.mkdir(parents=True, exist_ok=True)
        with (folder / "console.log").open("w") as log:
            child = subprocess.Popen([sys.executable, str(ROOT / "run_e1r.py"), "--run", run_id],
                                     stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, start_new_session=True)
            # Per-proposal bounds plus a run watchdog; stdout streaming exposes meaningful progress.
            import threading
            import signal
            timer = threading.Timer(2600, lambda: os.killpg(child.pid, signal.SIGKILL) if child.poll() is None else None)
            timer.start()
            try:
                for line in child.stdout:
                    log.write(line)
                    log.flush()
                    if "[E1-R]" in line:
                        print(line.strip(), flush=True)
                rc = child.wait()
            finally:
                timer.cancel()
        state = ledger()
        state.setdefault("run_results", {})[run_id] = {"returncode": rc, "finished_utc": utc()}
        write_json(path, state)
        if rc or state.get("stopped"):
            state.update(stopped=True, stop_reason=state.get("stop_reason") or f"Run {run_id} failed ({rc})", closed=True)
            write_json(path, state)
            freeze_selections()
            return 2
    state = ledger()
    if len(state["invocations"]) != 60:
        state.update(stopped=True, stop_reason="Incomplete proposal accounting", closed=True)
        write_json(path, state)
        freeze_selections()
        return 2
    state.update(closed=True, completed_utc=utc())
    write_json(path, state)
    freeze_selections()
    print("All six training selections frozen. Offline holdout/recognition may now begin.", flush=True)
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--preflight", action="store_true")
    modes.add_argument("--freeze", action="store_true")
    modes.add_argument("--execute", action="store_true")
    modes.add_argument("--run", choices=ORDER)
    args = parser.parse_args()
    if args.freeze:
        freeze()
    elif args.execute:
        raise SystemExit(execute())
    elif args.run:
        raise SystemExit(run_one(args.run))
    else:
        print(json.dumps(preflight(), indent=2))
