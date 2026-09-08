"""Usage/authentication boundaries; all tests make zero model calls."""
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest import mock

import subscription_guard as guard
from subscription_status import require_subscription_capacity, sanitize_limits


class SubscriptionBoundaryTests(unittest.TestCase):
    def test_sixth_invocation_and_restart_after_failure_are_refused(self):
        state = {"limit": 5, "invocations": [], "stopped": False}
        with tempfile.TemporaryDirectory() as tmp:
            ledger = Path(tmp) / "invocations.json"
            for _ in range(5):
                guard.reserve(state)
                guard.write_json(ledger, state)
                state = json.loads(ledger.read_text())
            with self.assertRaisesRegex(RuntimeError, "exhausted"):
                guard.reserve(state)
        with self.assertRaisesRegex(RuntimeError, "stopped"):
            guard.reserve({"limit": 5, "invocations": [], "stopped": True})

    def test_environment_drops_keys_endpoints_and_parent_context(self):
        with mock.patch.dict(os.environ, {"OPENAI_API_KEY": "fake", "CODEX_API_KEY": "fake",
                                         "OPENAI_BASE_URL": "fake", "CODEX_THREAD_ID": "fake"}):
            env = guard.child_environment()
        self.assertFalse(set(env) & {"OPENAI_API_KEY", "CODEX_API_KEY", "OPENAI_BASE_URL", "CODEX_THREAD_ID"})

    def test_native_command_keeps_read_only_and_forces_subscription(self):
        args = ["--sandbox", "read-only", "--ask-for-approval", "never", "--search",
                "exec", "--model", guard.MODEL, "--json", "-"]
        with mock.patch.dict(os.environ, {"PILOT_REAL_CODEX": "/usr/bin/codex"}):
            command = guard.codex_command(args)
            with self.assertRaises(RuntimeError):
                guard.codex_command([*args, "resume"])
        self.assertNotIn("--search", command)
        self.assertIn('forced_login_method="chatgpt"', command)
        self.assertIn("model_providers.shinka_subscription.request_max_retries=0", command)
        self.assertIn("model_providers.shinka_subscription.stream_max_retries=0", command)
        self.assertIn('model_providers.shinka_subscription.base_url="https://chatgpt.com/backend-api/codex"', command)
        self.assertIn("read-only", command)

    def test_quota_exhaustion_or_unknown_quota_never_uses_credits(self):
        status = {"account": {"type": "chatgpt", "planType": "pro"},
                  "limits": {"rateLimits": {"primary": {"usedPercent": 1},
                                            "credits": {"hasCredits": True}}}}
        require_subscription_capacity(status)
        for percent in (90, 100):
            status["limits"]["rateLimits"]["primary"]["usedPercent"] = percent
            with self.assertRaises(RuntimeError):
                require_subscription_capacity(status)
        status["limits"]["rateLimits"] = {}
        with self.assertRaises(RuntimeError):
            require_subscription_capacity(status)

    def test_account_identifiers_not_saved(self):
        clean = sanitize_limits({"accountId": "private", "rateLimitResetCredits": {"id": "private"},
                                 "rateLimits": {"primary": {"usedPercent": 1}}})
        self.assertNotIn("private", json.dumps(clean))

    def test_subprocess_timeout_returns_failure(self):
        rc, _, stderr = guard.bounded_run(
            ["python3", "-c", "import time; time.sleep(10)"],
            timeout=0.05, env=guard.child_environment())
        self.assertEqual(rc, 124)
        self.assertIn("process group killed", stderr)
