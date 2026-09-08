#!/usr/bin/env python3
"""E3's separate durable allowance and restricted native Codex boundary.

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
from e3_state import classify_failure, E3, opportunities, assign_opportunity
import time

from e1r_process import bounded_run
from e1r_io import write_json
from e1r_status import read_status, require_subscription_capacity

ROOT = Path(__file__).resolve().parent
MODEL = "gpt-5.6-terra"
ORDER = ("S101", "S202", "S303")
TOTAL_LIMIT = 60
RUN_LIMIT = 20
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
    return {k: v for k, v in os.environ.items() if k in keep or k.startswith("E3_")}


def reserve(ledger, run_id, slot):
    if ledger.get("stopped") or ledger.get("closed"):
        raise RuntimeError("E3 ledger is stopped or closed; counters cannot be reset")
    if run_id not in ORDER or not 1 <= slot <= RUN_LIMIT:
        raise RuntimeError("Unknown E3 run or out-of-range proposal slot")
    records = ledger["invocations"]
    same_run = [r for r in records if r["run_id"] == run_id]
    if len(records) >= TOTAL_LIMIT or len(same_run) >= RUN_LIMIT:
        raise RuntimeError("E3 invocation allowance exhausted")
    if any(r["slot"] == slot for r in same_run):
        raise RuntimeError("E3 proposal slot already consumed; retries forbidden")
    if 'opportunities' in ledger:
        matches = [r for r in ledger['opportunities'] if (r['run_id'], r['slot']) == (run_id, slot)]
        if len(matches) != 1 or matches[0]['status'] != 'assigned':
            raise RuntimeError('No unique unused assigned opportunity')
        if len(records) >= ledger['further_external_limit']:
            raise RuntimeError('Continuation external allowance exhausted')
    else:
        expected_run = ORDER[len(records) // RUN_LIMIT]
        if run_id != expected_run or slot != len(same_run) + 1:
            raise RuntimeError("E3 frozen run/slot order violated")
    record = {"invocation": len(records) + 1, "run_id": run_id, "slot": slot,
              "reserved_utc": utc(), "status": "reserved", "model": MODEL}
    records.append(record)
    if 'opportunities' in ledger:
        matches[0]['external_invocation'] = record['invocation']
    return record


def verify_freeze():
    from e3_state import verify_freeze as check
    check(E3)


def run_codex(args):
    env = clean_environment()
    if args in (["--version"], ["-V"]):
        return subprocess.call([env["E3_REAL_CODEX"], *args], env=env, timeout=15)
    if "exec" not in args or "resume" in args or "fork" in args:
        raise RuntimeError("Only fresh Codex exec invocations are permitted")
    if "--model" not in args or args[args.index("--model") + 1] != MODEL:
        raise RuntimeError("E3 model mismatch")
    from run_e3 import verify_committed
    verify_committed()
    run_id, slot = env["E3_RUN_ID"], int(env["E3_SLOT"])
    ledger_path = E3 / "ledger.json"
    with (E3 / "ledger.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        ledger = json.loads(ledger_path.read_text())
        if not ledger.get('execution_started'):
            raise RuntimeError('Live parent launcher has not opened this experiment')
        if ledger.get("stopped") or ledger.get("closed"):
            raise RuntimeError("E3 ledger is stopped or closed")
        try:
            diagnostics = []
            status = read_status(env["E3_REAL_CODEX"], diagnostics=diagnostics)
            require_subscription_capacity(status)
            if not any(m.get("model") == MODEL and any(e['reasoningEffort'] == 'low'
                       for e in m.get('supportedReasoningEfforts', [])) for m in status["models"]):
                raise RuntimeError("Frozen model unavailable; no substitution")
        except BaseException as exc:
            ledger.update(stopped=True, stop_reason=f"Subscription check: {type(exc).__name__}: {exc}", failure_class="metadata_or_capacity", metadata_failure_diagnostics=diagnostics)
            write_json(ledger_path, ledger)
            raise
        record = reserve(ledger, run_id, slot)
        write_json(ledger_path, ledger)  # Persist BEFORE attempting external launch.
        folder = E3 / "runs" / run_id / "invocations" / f"{slot:02d}"
        folder.mkdir(parents=True, exist_ok=False)
        write_json(folder / "subscription_before.json", status)
        prompt = sys.stdin.read()
        (folder / "prompt.md").write_text(prompt)
        record["prompt_sha256"] = hashlib.sha256(prompt.encode()).hexdigest()
        if slot == 1:
            expected = (E3 / "protocol" / "initial_prompt.md").read_text()
            if prompt != expected:
                ledger.update(stopped=True, stop_reason="Initial/B prompt differs from frozen initial information")
                record["status"] = "blocked_prompt_mismatch"
                write_json(ledger_path, ledger)
                raise RuntimeError(ledger["stop_reason"])
        cmd = command(env["E3_REAL_CODEX"], E3 / "protocol" / "codex_model_catalog.json")
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
            items = [e.get('item', {}) for e in events if e.get('type', '').startswith('item.')]
            unexpected = [i.get('type') for i in items if i.get('type') not in ('agent_message', 'reasoning', 'error')]
            if unexpected:
                ledger.update(stopped=True, stop_reason='Unexpected native tool activity', failure_class='information_boundary')
                record.update(status='failed', unexpected_item_types=unexpected)
                rc = 2
            if rc or any(e.get("type") in ("turn.failed", "error") for e in events):
                ledger.update(stopped=True, stop_reason=ledger.get('stop_reason') or "Codex backend failure", failure_class=ledger.get('failure_class') or classify_failure(stdout, stderr))
                record["failure_class"] = ledger["failure_class"]
                record['status'] = 'failed'
                rc = rc or 2
            sys.stdout.write(stdout)
            sys.stderr.write(stderr)
            return rc
        except BaseException as exc:
            record["status"] = "interrupted_or_launch_error"
            ledger.update(stopped=True, stop_reason=f"{type(exc).__name__}: external launch interrupted", failure_class="ambiguous")
            raise
        finally:
            record.update(runtime_seconds=time.monotonic() - started, finished_utc=utc())
            write_json(ledger_path, ledger)


def run_headless(args):
    env = clean_environment()
    if args == ["--check"]:
        return subprocess.call([env["E3_REAL_HEADLESS"], "codex", "--check"], env=env, timeout=30)
    if not args or args[0] != "codex" or "--prompt-file" not in args:
        raise RuntimeError("Only native Headless/Codex proposals are permitted")
    rc, stdout, stderr = bounded_run([env["E3_REAL_HEADLESS"], *args, "--timeout", "200"],
                                     timeout=210, env=env)
    folder = E3 / "runs" / env["E3_RUN_ID"] / "invocations" / f"{int(env['E3_SLOT']):02d}"
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "headless.stdout.txt").write_text(stdout)
    (folder / "headless.stderr.txt").write_text(stderr)
    if rc:
        with (E3 / "ledger.lock").open("a") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            ledger = json.loads((E3 / "ledger.json").read_text())
            ledger.update(stopped=True, stop_reason=ledger.get("stop_reason") or "Headless backend failure")
            write_json(E3 / "ledger.json", ledger)
    sys.stdout.write(stdout)
    sys.stderr.write(stderr)
    return rc


if __name__ == "__main__":
    try:
        raise SystemExit(run_codex(sys.argv[1:]) if Path(sys.argv[0]).name == "codex"
                         else run_headless(sys.argv[1:]))
    except (RuntimeError, OSError, subprocess.TimeoutExpired) as exc:
        print(f"E3 boundary: {exc}", file=sys.stderr)
        raise SystemExit(2)
