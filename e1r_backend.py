#!/usr/bin/env python3
"""E1's separate durable allowance and restricted native Codex boundary.

No policy generation, repair, evaluation, or selection occurs here. Shinka's
native Headless provider still builds prompts and parses native Headless output.
"""
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

from e1r_process import bounded_run
from e1r_io import write_json
from e1r_status import read_status, require_subscription_capacity

ROOT = Path(__file__).resolve().parent
E1 = ROOT / "results" / "e1_r"
MODEL = "gpt-5.6-terra"
ORDER = ("A101", "B101", "B202", "A202", "A303", "B303")
TOTAL_LIMIT = 60
RUN_LIMIT = 10
DISABLED_FEATURES = (
    "shell_tool", "unified_exec", "apps", "plugins", "remote_plugin",
    "skill_search", "skill_mcp_dependency_install", "multi_agent", "multi_agent_v2",
    "memories", "browser_use", "browser_use_external", "computer_use", "view_image",
    "image_generation", "code_mode", "code_mode_host", "code_mode_only", "hooks",
    "tool_suggest", "recommended_plugins", "workspace_dependencies", "goals",
    "unbounded_connection_retries", "enable_request_compression",
)


def utc():
    return datetime.now(timezone.utc).isoformat()


def restricted_settings(catalog):
    return [
        'web_search="disabled"', "project_doc_max_bytes=0",
        "skills.include_instructions=false", "skills.bundled.enabled=false",
        "mcp_servers={}", "agents.enabled=false", "tools.update_plan.enabled=false",
        "tools.experimental_request_user_input.enabled=false",
        "include_environment_context=false",
        "model_reasoning_effort=\"low\"", "service_tier=\"default\"",
        "model_catalog_json=" + json.dumps(str(catalog)),
        *(f"features.{name}=false" for name in DISABLED_FEATURES),
    ]


def command(codex, catalog):
    settings = restricted_settings(catalog) + [
        'forced_login_method="chatgpt"', 'model_provider="e1_subscription"',
        'model_providers.e1_subscription.name="OpenAI"',
        'model_providers.e1_subscription.base_url="https://chatgpt.com/backend-api/codex"',
        "model_providers.e1_subscription.requires_openai_auth=true",
        "model_providers.e1_subscription.request_max_retries=0",
        "model_providers.e1_subscription.stream_max_retries=0",
        "model_providers.e1_subscription.stream_idle_timeout_ms=60000",
        "model_providers.e1_subscription.supports_websockets=false",
    ]
    args = [codex, "--sandbox", "read-only", "--ask-for-approval", "never",
            "exec", "--ignore-user-config", "--skip-git-repo-check", "--model", MODEL,
            "--json"]
    for setting in settings:
        args.extend(["-c", setting])
    return args + ["-"]


def clean_environment():
    keep = {"HOME", "PATH", "CODEX_HOME", "LANG", "TMPDIR", "SSL_CERT_FILE"}
    return {k: v for k, v in os.environ.items() if k in keep or k.startswith("E1R_")}


def reserve(ledger, run_id, slot):
    if ledger.get("stopped") or ledger.get("closed"):
        raise RuntimeError("E1 ledger is stopped or closed; counters cannot be reset")
    if run_id not in ORDER or not 1 <= slot <= RUN_LIMIT:
        raise RuntimeError("Unknown E1 run or out-of-range proposal slot")
    records = ledger["invocations"]
    same_run = [r for r in records if r["run_id"] == run_id]
    if len(records) >= TOTAL_LIMIT or len(same_run) >= RUN_LIMIT:
        raise RuntimeError("E1 invocation allowance exhausted")
    if any(r["slot"] == slot for r in same_run):
        raise RuntimeError("E1 proposal slot already consumed; retries forbidden")
    expected_run = ORDER[len(records) // RUN_LIMIT]
    if run_id != expected_run or slot != len(same_run) + 1:
        raise RuntimeError("E1 frozen run/slot order violated")
    record = {"invocation": len(records) + 1, "run_id": run_id, "slot": slot,
              "reserved_utc": utc(), "status": "reserved", "model": MODEL}
    records.append(record)
    return record


def verify_freeze():
    frozen = json.loads((E1 / "protocol" / "freeze.json").read_text())
    for name, expected in frozen["source_sha256"].items():
        if hashlib.sha256((ROOT / name).read_bytes()).hexdigest() != expected:
            raise RuntimeError(f"E1 frozen source changed: {name}")
    if hashlib.sha256((E1 / "protocol" / "protocol.json").read_bytes()).hexdigest() != frozen["protocol_sha256"]:
        raise RuntimeError("E1 protocol changed after freeze")
    if hashlib.sha256((E1 / "protocol" / "codex_model_catalog.json").read_bytes()).hexdigest() != frozen["catalog_sha256"]:
        raise RuntimeError("Restricted Codex model catalog changed after freeze")
    for name, field in (("results/e1/ledger.json", "e1_ledger_sha256"),
                        ("results/subscription_pilot_001_usage/invocations.json", "pilot_ledger_sha256")):
        if hashlib.sha256((ROOT / name).read_bytes()).hexdigest() != frozen[field]:
            raise RuntimeError(f"Historical closed ledger changed: {name}")


def run_codex(args):
    env = clean_environment()
    if args in (["--version"], ["-V"]):
        return subprocess.call([env["E1R_REAL_CODEX"], *args], env=env, timeout=15)
    if "exec" not in args or "resume" in args or "fork" in args:
        raise RuntimeError("Only fresh Codex exec invocations are permitted")
    if "--model" not in args or args[args.index("--model") + 1] != MODEL:
        raise RuntimeError("E1 model mismatch")
    verify_freeze()
    run_id, slot = env["E1R_RUN_ID"], int(env["E1R_SLOT"])
    ledger_path = E1 / "ledger.json"
    with (E1 / "ledger.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        ledger = json.loads(ledger_path.read_text())
        if ledger.get("stopped") or ledger.get("closed"):
            raise RuntimeError("E1 ledger is stopped or closed")
        try:
            diagnostics = []
            status = read_status(env["E1R_REAL_CODEX"], diagnostics=diagnostics)
            require_subscription_capacity(status)
            if not any(m.get("model") == MODEL for m in status["models"]):
                raise RuntimeError("Frozen model unavailable; no substitution")
        except BaseException as exc:
            ledger.update(stopped=True, stop_reason=f"Subscription check: {type(exc).__name__}: {exc}", metadata_failure_diagnostics=diagnostics)
            write_json(ledger_path, ledger)
            raise
        record = reserve(ledger, run_id, slot)
        write_json(ledger_path, ledger)  # Persist BEFORE attempting external launch.
        folder = E1 / "runs" / run_id / "invocations" / f"{slot:02d}"
        folder.mkdir(parents=True, exist_ok=False)
        write_json(folder / "subscription_before.json", status)
        prompt = sys.stdin.read()
        (folder / "prompt.md").write_text(prompt)
        record["prompt_sha256"] = hashlib.sha256(prompt.encode()).hexdigest()
        if run_id.startswith("B") or slot == 1:
            expected = (E1 / "protocol" / "initial_prompt.md").read_text()
            if prompt != expected:
                ledger.update(stopped=True, stop_reason="Initial/B prompt differs from frozen initial information")
                record["status"] = "blocked_prompt_mismatch"
                write_json(ledger_path, ledger)
                raise RuntimeError(ledger["stop_reason"])
        cmd = command(env["E1R_REAL_CODEX"], E1 / "protocol" / "codex_model_catalog.json")
        record.update(command=cmd, headless_supplied_args=args, cwd=os.getcwd(), started_utc=utc())
        write_json(ledger_path, ledger)
        started = time.monotonic()
        try:
            rc, stdout, stderr = bounded_run(cmd, timeout=180, env=env, stdin=prompt)
            (folder / "codex.jsonl").write_text(stdout)
            (folder / "stderr.txt").write_text(stderr)
            events = []
            for line in stdout.splitlines():
                try:
                    events.append(json.loads(line))
                except ValueError:
                    pass
            record.update(returncode=rc, status="completed" if rc == 0 else "failed",
                          completed_codex_turn_events=sum(e.get("type") == "turn.completed" for e in events),
                          turn_usage=[e.get("usage") for e in events if e.get("type") == "turn.completed"],
                          thread_ids=[e.get("thread_id") for e in events if e.get("type") == "thread.started"])
            if rc or any(e.get("type") in ("turn.failed", "error") for e in events):
                ledger.update(stopped=True, stop_reason="Codex backend failure; no retry or replacement")
            sys.stdout.write(stdout)
            sys.stderr.write(stderr)
            return rc
        except BaseException as exc:
            record["status"] = "interrupted_or_launch_error"
            ledger.update(stopped=True, stop_reason=f"{type(exc).__name__}: external launch interrupted")
            raise
        finally:
            record.update(runtime_seconds=time.monotonic() - started, finished_utc=utc())
            write_json(ledger_path, ledger)


def run_headless(args):
    env = clean_environment()
    if args == ["--check"]:
        return subprocess.call([env["E1R_REAL_HEADLESS"], "codex", "--check"], env=env, timeout=30)
    if not args or args[0] != "codex" or "--prompt-file" not in args:
        raise RuntimeError("Only native Headless/Codex proposals are permitted")
    rc, stdout, stderr = bounded_run([env["E1R_REAL_HEADLESS"], *args, "--timeout", "200"],
                                     timeout=210, env=env)
    folder = E1 / "runs" / env["E1R_RUN_ID"] / "invocations" / f"{int(env['E1R_SLOT']):02d}"
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "headless.stdout.txt").write_text(stdout)
    (folder / "headless.stderr.txt").write_text(stderr)
    if rc:
        with (E1 / "ledger.lock").open("a") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            ledger = json.loads((E1 / "ledger.json").read_text())
            ledger.update(stopped=True, stop_reason=ledger.get("stop_reason") or "Headless backend failure")
            write_json(E1 / "ledger.json", ledger)
    sys.stdout.write(stdout)
    sys.stderr.write(stderr)
    return rc


if __name__ == "__main__":
    try:
        raise SystemExit(run_codex(sys.argv[1:]) if Path(sys.argv[0]).name == "codex"
                         else run_headless(sys.argv[1:]))
    except (RuntimeError, OSError, subprocess.TimeoutExpired) as exc:
        print(f"E1 boundary: {exc}", file=sys.stderr)
        raise SystemExit(2)
