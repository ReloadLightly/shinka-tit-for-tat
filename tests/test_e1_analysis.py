import tempfile
import json
from pathlib import Path
import unittest
from unittest.mock import patch

import audit_e1
from policy import parse_policy


class AnalysisTests(unittest.TestCase):
    def test_terminal_freeze_marks_incomplete_and_unstarted_not_complete(self):
        baseline = {"slot": 0, "source": "initial.py", "sha256": audit_e1.sha(audit_e1.ROOT / "initial.py"),
                    "correct": True, "error": None, "training": 2.3310772701635645}
        calls = [{"run_id": name} for name in audit_e1.ORDER[:4] for _ in range(10)] + [{"run_id": "A303"} for _ in range(4)]
        with tempfile.TemporaryDirectory() as tmp, patch.object(audit_e1, "E1", Path(tmp)), patch.object(audit_e1, "training_records", side_effect=lambda name: [] if name == "B303" else [dict(baseline)]):
            Path(tmp, "ledger.json").write_text(json.dumps({"closed": True, "stopped": True, "invocations": calls}))
            audit_e1.freeze_terminal_states()
            frozen = json.loads(Path(tmp, "training_selections_frozen.json").read_text())
            self.assertFalse(frozen["complete_design"])
            self.assertEqual(frozen["statuses"]["A303"], "incomplete")
            self.assertEqual(frozen["statuses"]["B303"], "not_started")
            self.assertEqual(sum(v == "complete" for v in frozen["statuses"].values()), 4)
            with self.assertRaises(RuntimeError):
                audit_e1.freeze_terminal_states()

    def test_analysis_gate_refuses_missing_six_selections(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(audit_e1, "E1", Path(tmp)):
            with self.assertRaisesRegex(RuntimeError, "All six"):
                audit_e1.audit()

    def test_trace_uses_fixed_interpreter_and_actual_scored_rng(self):
        candidate = parse_policy("def policy(own_history, opponent_history):\n    return 0 if len(own_history) == 0 else 1\n")
        trace = audit_e1.trace_encounter(candidate, "train", "always_defect", 11, count=3)
        self.assertEqual([r["action"] for r in trace["rows"]], [0, 1, 1])
        self.assertEqual([r["payoff"] for r in trace["rows"]], [0, 1, 1])
        self.assertEqual(trace["rows"][0]["branch_tests_in_execution_order"], [{"test": "len(own_history) == 0", "result": True}])
        self.assertEqual(trace["rows"][1]["branch_tests_in_execution_order"][0]["result"], False)
        self.assertEqual(trace["full_match"]["total_payoff"], 173)


if __name__ == "__main__":
    unittest.main()
