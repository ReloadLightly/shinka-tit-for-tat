import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import e1_backend
import run_e1


class AccountingTests(unittest.TestCase):
    def test_total_per_run_order_and_no_replacement(self):
        state = {"invocations": []}
        for run in e1_backend.ORDER:
            for slot in range(1, 11):
                e1_backend.reserve(state, run, slot)
                with self.assertRaises(RuntimeError):
                    e1_backend.reserve(state, run, slot)
        self.assertEqual(len(state["invocations"]), 60)
        with self.assertRaises(RuntimeError):
            e1_backend.reserve(state, "B303", 10)

    def test_stopped_and_out_of_order_refused(self):
        for state, run, slot in [({"invocations": [], "stopped": True}, "A101", 1),
                                  ({"invocations": []}, "B101", 1),
                                  ({"invocations": []}, "A101", 2)]:
            with self.assertRaises(RuntimeError):
                e1_backend.reserve(state, run, slot)

    def test_selection_seed_eligible_exact_earliest_tie(self):
        rows = [{"slot": 0, "correct": True, "training": 2},
                {"slot": 1, "correct": False, "training": 99},
                {"slot": 2, "correct": True, "training": 2}]
        self.assertEqual(run_e1.select(rows)["slot"], 0)
        rows.append({"slot": 3, "correct": True, "training": 3})
        self.assertEqual(run_e1.select(rows)["slot"], 3)

    def test_environment_drops_keys_and_supervisor_context(self):
        with patch.dict(os.environ, {"OPENAI_API_KEY": "local-test-only", "CODEX_THREAD_ID": "supervisor", "MCP_TOKEN": "test"}):
            clean = e1_backend.clean_environment()
        self.assertNotIn("OPENAI_API_KEY", clean)
        self.assertNotIn("CODEX_THREAD_ID", clean)
        self.assertNotIn("MCP_TOKEN", clean)


@unittest.skipUnless(run_e1.dependency_status()["installed"], "Pinned optional Shinka dependency required")
class NativeHarnessTests(unittest.TestCase):
    def test_two_opportunities_each_arm_no_external_backend(self):
        run_e1.configure_imports()
        from shinka.core import EvolutionConfig
        from shinka.llm import AsyncLLMClient
        from shinka.llm.providers import QueryResult
        from shinka.llm.providers.headless import _render_prompt
        original_env = dict(os.environ)
        try:
            with tempfile.TemporaryDirectory(prefix="e1_unit_", dir=run_e1.ROOT) as tmp, patch.object(run_e1, "E1", Path(tmp)), patch.object(run_e1, "verify_freeze"):
                Path(tmp, "ledger.json").write_text('{"invocations": [], "stopped": false}')
                for run in ("A101", "B101"):
                    prompts = []

                    async def fake_query(self, msg, system_msg, msg_history, **kwargs):
                        prompts.append(_render_prompt(msg=msg, system_msg=system_msg, msg_history=msg_history))
                        # Local fixtures only: a constant cooperator followed by a forbidden tuple.
                        value = "0" if len(prompts) == 1 else "(0, 1)[0]"
                        content = f"<NAME>local_fixture</NAME>\n<DESCRIPTION>Local fixture</DESCRIPTION>\n```python\n# EVOLVE-BLOCK-START\ndef policy(own_history, opponent_history):\n    return {value}\n# EVOLVE-BLOCK-END\n```"
                        return QueryResult(content, msg, system_msg, [], e1_backend.MODEL, {}, 0, 1, cost=0)

                    def short_config(**kwargs):
                        kwargs["num_generations"] = 3
                        return EvolutionConfig(**kwargs)

                    with patch.object(AsyncLLMClient, "query", fake_query), patch("shinka.core.EvolutionConfig", short_config):
                        self.assertEqual(run_e1.run_one(run), 0)
                    self.assertEqual(len(prompts), 2, "Invalid proposal must not trigger replacement")
                    self.assertEqual(prompts[0], run_e1.initial_prompt())
                    if run.startswith("B"):
                        self.assertEqual(prompts[0], prompts[1])
                        context = json.loads(Path(tmp, "runs", run, "gen_2", "supplied_context.json").read_text())
                        self.assertEqual(context["parent"]["generation"], 0)
                        self.assertEqual(context["top_k_inspirations"], [])
                    rows = run_e1.training_records(run)
                    self.assertEqual(len(rows), 3)
                    self.assertTrue(rows[1]["correct"])
                    self.assertFalse(rows[2]["correct"])
                    self.assertIn("Unsupported syntax", rows[2]["error"])
                    os.environ.clear()
                    os.environ.update(original_env)
        finally:
            os.environ.clear()
            os.environ.update(original_env)


if __name__ == "__main__":
    unittest.main()
