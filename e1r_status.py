"""E1-R metadata transport: bounded byte-buffered JSON-RPC, no model turns."""
import argparse
import json
import os
from pathlib import Path
import selectors
import subprocess
import time

from subscription_status import sanitize_limits, require_subscription_capacity


class JsonLinesRPC:
    def __init__(self, process, timeout=30):
        self.process, self.timeout = process, timeout
        self.buffer = b""
        self.selector = selectors.DefaultSelector()
        self.selector.register(process.stdout, selectors.EVENT_READ)
        self.diagnostics = []

    def send(self, message):
        self.process.stdin.write((json.dumps(message) + "\n").encode())
        self.process.stdin.flush()

    def request(self, number, method, params):
        start = time.monotonic()
        deadline = start + self.timeout
        record = {"method": method, "notifications": 0, "unmatched_responses": 0}
        self.diagnostics.append(record)
        try:
            self.send(dict(id=number, method=method, params=params))
            while True:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise TimeoutError(f"Codex metadata deadline: {method}; buffered_bytes={len(self.buffer)}")
                # Consume ALL complete buffered lines before polling the fd again.
                if b"\n" in self.buffer:
                    line, self.buffer = self.buffer.split(b"\n", 1)
                    if not line.strip():
                        continue
                    reply = json.loads(line)
                    if reply.get("id") == number:
                        if "error" in reply:
                            # Do not include arbitrary server payloads or credentials.
                            raise RuntimeError(f"Codex metadata RPC error: {method}")
                        record["outcome"] = "response"
                        return reply["result"]
                    record["notifications" if "id" not in reply else "unmatched_responses"] += 1
                    continue
                if not self.selector.select(remaining):
                    continue
                chunk = os.read(self.process.stdout.fileno(), 65536)
                if not chunk:
                    raise EOFError(f"Codex metadata EOF: {method}; partial_bytes={len(self.buffer)}")
                self.buffer += chunk
                if len(self.buffer) > 4_000_000:
                    raise RuntimeError(f"Codex metadata response too large: {method}")
        except BaseException as exc:
            record["outcome"] = type(exc).__name__
            raise
        finally:
            record["runtime_seconds"] = time.monotonic() - start


def read_status(codex="codex", *, timeout=30, diagnostics=None):
    env = {k: v for k, v in os.environ.items()
           if k in {"HOME", "PATH", "CODEX_HOME", "LANG", "TMPDIR", "SSL_CERT_FILE"}}
    proc = subprocess.Popen([codex, "app-server", "--stdio"], env=env,
                            stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                            stderr=subprocess.DEVNULL, bufsize=0)
    rpc = JsonLinesRPC(proc, timeout)
    try:
        rpc.request(1, "initialize", {"clientInfo": {"name": "shinka-e1r", "version": "1"},
                                      "capabilities": {"experimentalApi": True}})
        rpc.send({"method": "initialized"})
        account = rpc.request(2, "account/read", {"refreshToken": False})
        limits = rpc.request(3, "account/rateLimits/read", {})
        models = rpc.request(4, "model/list", {"includeHidden": False})
        return {"model_turns": 0,
                "account": {k: (account.get("account") or {}).get(k) for k in ("type", "planType")},
                "limits": sanitize_limits(limits),
                "models": [{k: m.get(k) for k in
                            ("id", "model", "displayName", "supportedReasoningEfforts")}
                           for m in models.get("data", [])],
                "rpc_diagnostics": rpc.diagnostics}
    finally:
        if diagnostics is not None:
            diagnostics.extend(rpc.diagnostics)
        rpc.selector.close()
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait(timeout=5)
        proc.stdin.close()
        proc.stdout.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = read_status()
    with args.output.open("x") as handle:
        json.dump(result, handle, indent=2)
        handle.write("\n")
