#!/usr/bin/env python3
"""Audited subprocess boundary for Shinka's native Headless/Codex provider.

This is a usage guard, NOT a filesystem confidentiality sandbox. It does not
generate, edit, select, or evaluate policies. Native Shinka and Headless do that.
"""
from datetime import datetime, timezone
import fcntl
import json
import os
from pathlib import Path
import signal
import subprocess
import sys

MODEL = "gpt-5.6-terra"
MAX_INVOCATIONS = 5
CODEX_TIMEOUT = 180


def now():
    return datetime.now(timezone.utc).isoformat()


def child_environment():
    # Never forward API keys, API base URLs, agent fallback settings, or parent
    # session identifiers. Keep the existing credential location unchanged.
    allowed = {"HOME", "PATH", "CODEX_HOME", "LANG", "TMPDIR", "SSL_CERT_FILE"}
    return {k: v for k, v in os.environ.items()
            if k in allowed or k.startswith("PILOT_")}


def write_json(path, data):
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(data, indent=2) + "\n")
    temporary.replace(path)


def reserve(state):
    if state.get("stopped"):
        raise RuntimeError("Subscription pilot stopped after backend failure")
    if len(state["invocations"]) >= min(MAX_INVOCATIONS, state["limit"]):
        raise RuntimeError("Subscription invocation budget exhausted")
    record = {"invocation": len(state["invocations"]) + 1,
              "reserved_utc": now(), "status": "reserved", "model": MODEL}
    state["invocations"].append(record)
    return record


def codex_command(original):
    if "exec" not in original or "resume" in original or "fork" in original:
        raise RuntimeError("Only fresh Codex exec proposals are allowed")
    if "--model" not in original or original[original.index("--model") + 1] != MODEL:
        raise RuntimeError("Unexpected subscription model")
    args = [arg for arg in original if arg != "--search"]
    pos = args.index("exec") + 1
    args[pos:pos] = ["--ignore-user-config",
                    "-c", 'forced_login_method="chatgpt"',
                    "-c", 'model_provider="openai"',
                    "-c", 'web_search="disabled"',
                    "-c", "model_providers.openai.request_max_retries=0",
                    "-c", "model_providers.openai.stream_max_retries=0",
                    "-c", "model_providers.openai.stream_idle_timeout_ms=60000",
                    "-c", "project_doc_max_bytes=0"]
    if "--dangerously-bypass-approvals-and-sandbox" in args:
        raise RuntimeError("Read-only proposals required")
    return [os.environ["PILOT_REAL_CODEX"], *args]


def bounded_run(command, *, timeout, env, stdin=None):
    proc = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, text=True, env=env,
                            start_new_session=True)
    try:
        stdout, stderr = proc.communicate(stdin, timeout=timeout)
        return proc.returncode, stdout, stderr
    except subprocess.TimeoutExpired:
        os.killpg(proc.pid, signal.SIGKILL)
        stdout, stderr = proc.communicate()
        return 124, stdout, stderr + "\nPilot subprocess timeout; process group killed.\n"


def run_codex(args):
    env = child_environment()
    # Headless --check invokes version checks, never a proposal.
    if args in (["--version"], ["-V"]):
        return subprocess.call([env["PILOT_REAL_CODEX"], *args], env=env, timeout=15)
    command = codex_command(args)
    root = Path(env["PILOT_RECORD_DIR"])
    ledger = root / "invocations.json"
    with (root / "invocations.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        state = json.loads(ledger.read_text())
        # Read-only metadata, no model turn. Check before EVERY proposal, with
        # ample margin; never choose paid-credit continuation on exhaustion.
        from subscription_status import read_status, require_subscription_capacity
        try:
            subscription = read_status(env["PILOT_REAL_CODEX"])
            require_subscription_capacity(subscription)
        except BaseException:
            state["stopped"] = True
            write_json(ledger, state)
            raise
        record = reserve(state)
        write_json(ledger, state)  # Reserve BEFORE attempting an external launch.
        folder = root / f"invocation_{record['invocation']}"
        folder.mkdir()
        write_json(folder / "subscription_before.json", subscription)
        prompt = sys.stdin.read()
        (folder / "prompt.md").write_text(prompt)
        record["command"] = command
        record["cwd"] = os.getcwd()
        record["started_utc"] = now()
        write_json(ledger, state)
        try:
            rc, stdout, stderr = bounded_run(command, timeout=CODEX_TIMEOUT,
                                             env=env, stdin=prompt)
            (folder / "codex.jsonl").write_text(stdout)
            (folder / "stderr.txt").write_text(stderr)
            record.update(returncode=rc, status="completed" if rc == 0 else "failed")
            events = []
            for line in stdout.splitlines():
                try:
                    events.append(json.loads(line))
                except ValueError:
                    pass
            record["completed_codex_turn_events"] = sum(e.get("type") == "turn.completed" for e in events)
            record["internal_model_requests"] = None
            record["turn_usage"] = [e.get("usage") for e in events if e.get("type") == "turn.completed"]
            record["thread_ids"] = [e.get("thread_id") for e in events if e.get("type") == "thread.started"]
            if rc or any(e.get("type") in ("turn.failed", "error") for e in events):
                state["stopped"] = True
                record["status"] = "failed"
            sys.stdout.write(stdout)
            sys.stderr.write(stderr)
            return rc
        except BaseException:
            record["status"] = "interrupted_or_launch_error"
            state["stopped"] = True
            raise
        finally:
            record["finished_utc"] = now()
            write_json(ledger, state)


def run_headless(args):
    env = child_environment()
    if args == ["--check"]:
        return subprocess.call([env["PILOT_REAL_HEADLESS"], "codex", "--check"],
                               env=env, timeout=30)
    if not args or args[0] != "codex" or "--prompt-file" not in args:
        raise RuntimeError("Only native Headless Codex proposals are allowed")
    # Native wrapper still renders/parses the prompt, response, and usage.
    command = [env["PILOT_REAL_HEADLESS"], *args, "--timeout", "200"]
    rc, stdout, stderr = bounded_run(command, timeout=210, env=env)
    prompt = Path(args[args.index("--prompt-file") + 1])
    root = Path(env["PILOT_RECORD_DIR"])
    (root / (prompt.stem + "_headless.stdout.txt")).write_text(stdout)
    (root / (prompt.stem + "_headless.stderr.txt")).write_text(stderr)
    sys.stdout.write(stdout)
    sys.stderr.write(stderr)
    return rc


if __name__ == "__main__":
    try:
        raise SystemExit(run_codex(sys.argv[1:]) if Path(sys.argv[0]).name == "codex"
                         else run_headless(sys.argv[1:]))
    except (RuntimeError, OSError, subprocess.TimeoutExpired) as exc:
        print(f"Pilot guard: {exc}", file=sys.stderr)
        raise SystemExit(2)
