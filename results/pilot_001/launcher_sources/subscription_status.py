"""Read Codex account/model/quota metadata without starting a model turn."""
import argparse
import json
import os
from pathlib import Path
import selectors
import subprocess
import time


def sanitize_limits(limits):
    """Keep usage windows/balance, omit account and reset-credit identifiers."""
    allowed = ("limitId", "limitName", "primary", "secondary", "credits",
               "spendControlReached", "planType", "rateLimitReachedType")
    return {"rateLimits": {k: limits.get("rateLimits", {}).get(k) for k in allowed},
            "rateLimitsByLimitId": {
                name: {k: value.get(k) for k in allowed}
                for name, value in (limits.get("rateLimitsByLimitId") or {}).items()}}


def require_subscription_capacity(status):
    if status["account"] != {"type": "chatgpt", "planType": "pro"}:
        raise RuntimeError("Existing ChatGPT Pro authentication required")
    limits = status["limits"]["rateLimits"]
    if limits.get("spendControlReached") or limits.get("rateLimitReachedType"):
        raise RuntimeError("Subscription quota unavailable; credit continuation forbidden")
    windows = [limits.get(k) for k in ("primary", "secondary") if limits.get(k)]
    # Conservative margin avoids approaching the account's automatic credit
    # continuation boundary. No purchasing, reset, or continuation API is used.
    if not windows or any(w.get("usedPercent", 100) >= 90 for w in windows):
        raise RuntimeError("Subscription quota insufficient for this small pilot")


def read_status(codex="codex"):
    env = {k: v for k, v in os.environ.items()
           if k in {"HOME", "PATH", "CODEX_HOME", "LANG", "TMPDIR", "SSL_CERT_FILE"}}
    proc = subprocess.Popen([codex, "app-server", "--stdio"], env=env,
                            stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                            stderr=subprocess.DEVNULL, text=True, bufsize=1)
    selector = selectors.DefaultSelector()
    selector.register(proc.stdout, selectors.EVENT_READ)

    def request(number, method, params):
        proc.stdin.write(json.dumps(dict(id=number, method=method, params=params)) + "\n")
        proc.stdin.flush()
        deadline = time.monotonic() + 30
        while time.monotonic() < deadline:
            if not selector.select(timeout=max(0, deadline - time.monotonic())):
                break
            line = proc.stdout.readline()
            if not line:
                raise RuntimeError("Codex app-server closed")
            reply = json.loads(line)
            if reply.get("id") == number:
                if "error" in reply:
                    raise RuntimeError(str(reply["error"]))
                return reply["result"]
        raise TimeoutError("Codex metadata request timed out")

    try:
        request(1, "initialize", {"clientInfo": {"name": "shinka-pilot", "version": "1"},
                                  "capabilities": {"experimentalApi": True}})
        proc.stdin.write('{"method":"initialized"}\n')
        proc.stdin.flush()
        account = request(2, "account/read", {"refreshToken": False})
        limits = request(3, "account/rateLimits/read", {})
        models = request(4, "model/list", {"includeHidden": False})
        # Explicit allowlist: no tokens, account IDs, email, or full auth payload.
        return {"model_turns": 0,
                "account": {k: (account.get("account") or {}).get(k)
                            for k in ("type", "planType")},
                "limits": sanitize_limits(limits),
                "models": [{k: m.get(k) for k in
                            ("id", "model", "displayName", "supportedReasoningEfforts")}
                           for m in models.get("data", [])]}
    finally:
        selector.close()
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    with args.output.open("x") as handle:
        json.dump(read_status(), handle, indent=2)
        handle.write("\n")
