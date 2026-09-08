"""Scientific and evaluator-boundary checks; run with unittest discovery."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import environment
from environment import PAYOFFS, evaluate_policy, play, reference_policy
from evaluate import evaluate_file
from policy import PolicyError, load_policy, parse_policy
from recognize import analyze_policy


TFT_SOURCE = (
    "def policy(own_history, opponent_history):\n"
    "    return opponent_history[-1] if opponent_history else 0\n"
)


class MatchRulesTests(unittest.TestCase):
    def setUp(self):
        self.tft = parse_policy(TFT_SOURCE)

    def test_payoff_matrix_and_simultaneous_histories(self):
        self.assertEqual(PAYOFFS, {(0, 0): 3, (0, 1): 0, (1, 0): 5, (1, 1): 1})
        candidate_inputs, opponent_inputs = [], []

        def candidate(own, other):
            candidate_inputs.append((own, other))
            return len(own) % 2

        def opponent(name, own, other, rng):
            opponent_inputs.append((own, other))
            return 1

        with mock.patch.object(environment, "reference", side_effect=opponent):
            result = play(candidate, "observed", 3, 17)
        self.assertEqual(candidate_inputs, [((), ()), ((0,), (1,)), ((0, 1), (1, 1))])
        self.assertEqual(opponent_inputs, [(other, own) for own, other in candidate_inputs])
        self.assertEqual(result["total_payoff"], 1)
        self.assertTrue(all(isinstance(history, tuple) for pair in candidate_inputs for history in pair))

    def test_tft_against_cooperator_and_itself(self):
        for opponent in ("always_cooperate", "tit_for_tat"):
            with self.subTest(opponent=opponent):
                result = play(self.tft, opponent, 5, 17)
                self.assertEqual(result["total_payoff"], 15)
                self.assertEqual(result["opponent_total_payoff"], 15)
                self.assertEqual(result["cooperations"], 5)

    def test_tft_against_defector(self):
        # First round C/D earns 0/5, followed by four rounds of D/D at 1/1.
        result = play(self.tft, "always_defect", 5, 17)
        self.assertEqual(result["total_payoff"], 4)
        self.assertEqual(result["opponent_total_payoff"], 9)
        self.assertEqual(result["mean_payoff"], 0.8)
        self.assertEqual(result["cooperations"], 1)

    def test_tft_against_alternator(self):
        # TFT C,C,D,C,D faces C,D,C,D,C: payoffs 3,0,5,0,5.
        result = play(self.tft, "alternator", 5, 17)
        self.assertEqual(result["total_payoff"], 13)
        self.assertEqual(result["opponent_total_payoff"], 13)
        self.assertEqual(result["cooperations"], 3)

    def test_win_stay_lose_shift_covers_four_outcomes(self):
        wsls = reference_policy("win_stay_lose_shift")
        self.assertEqual(wsls((), ()), 0)
        for (own, other), expected in {(0, 0): 0, (0, 1): 1, (1, 0): 1, (1, 1): 0}.items():
            with self.subTest(own=own, other=other):
                self.assertEqual(wsls((own,), (other,)), expected)

    def test_random_opponent_replay_and_history_reset(self):
        self.assertEqual(play(self.tft, "random", 97, 17), play(self.tft, "random", 97, 17))
        # Prior matches cannot leave hidden state in an interpreted candidate.
        play(self.tft, "always_defect", 23, 17)
        self.assertEqual(play(self.tft, "always_cooperate", 3, 17)["total_payoff"], 9)

    def test_invalid_match_action_and_turn_count_rejected(self):
        for action in (True, False, None, 0.0, 2, -1):
            with self.subTest(action=repr(action)):
                with self.assertRaises(ValueError):
                    play(lambda own, other: action, "always_cooperate", 1, 17)
        for turns in (True, 0, -1, 1.0):
            with self.subTest(turns=repr(turns)):
                with self.assertRaises(ValueError):
                    play(self.tft, "always_cooperate", turns, 17)


class PolicyBoundaryTests(unittest.TestCase):
    def test_load_policy_and_history_dependent_program(self):
        source = (
            "def policy(own_history, opponent_history):\n"
            "    if len(opponent_history) < 2:\n"
            "        return 0\n"
            "    return 1 if opponent_history[-2:].count(1) == 2 else 0\n"
        )
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "candidate.py"
            path.write_text(source)
            candidate = load_policy(path)
        self.assertEqual(candidate((), ()), 0)
        self.assertEqual(candidate((0, 0), (1, 1)), 1)
        self.assertEqual(candidate((0, 0), (1, 0)), 0)

    def test_boolean_and_non_action_returns_rejected(self):
        for expression in ("True", "False", "2", "-1", "own_history", "'0'"):
            with self.subTest(expression=expression):
                with self.assertRaises(PolicyError):
                    parse_policy("def policy(own_history, opponent_history):\n    return " + expression)((), ())

    def test_runtime_errors_become_policy_errors(self):
        for expression in ("opponent_history[-1]", "min(own_history)", "1 % 0", "own_history[::0]"):
            with self.subTest(expression=expression):
                candidate = parse_policy("def policy(own_history, opponent_history):\n    return " + expression)
                with self.assertRaises(PolicyError):
                    candidate((), ())

    def test_import_filesystem_and_introspection_forbidden(self):
        sources = [
            "import os\ndef policy(own_history, opponent_history):\n    return 0",
            "def policy(own_history, opponent_history):\n    return __import__('os')",
            "def policy(own_history, opponent_history):\n    return open('/tmp/forbidden')",
            "def policy(own_history, opponent_history):\n    return own_history.__class__",
            "def policy(own_history, opponent_history):\n    return getattr(own_history)",
        ]
        for source in sources:
            with self.subTest(source=source):
                with self.assertRaises(PolicyError):
                    parse_policy(source)

    def test_unbounded_or_stateful_language_features_forbidden(self):
        sources = [
            "def policy(own_history, opponent_history):\n    while True:\n        pass",
            "def policy(own_history, opponent_history):\n    return policy(own_history, opponent_history)",
            "def policy(own_history, opponent_history):\n    own_history[0] = 1\n    return 0",
            "def policy(own_history, opponent_history):\n    return [x for x in opponent_history]",
            "@len\ndef policy(own_history, opponent_history):\n    return 0",
            "def policy(own_history=0, opponent_history=0):\n    return 0",
        ]
        for source in sources:
            with self.subTest(source=source):
                with self.assertRaises(PolicyError):
                    parse_policy(source)

    def test_source_and_ast_size_limits(self):
        with self.assertRaises(PolicyError):
            parse_policy("#" * 16001)
        many_branches = "def policy(own_history, opponent_history):\n" + "    if own_history:\n        return 0\n" * 100
        with self.assertRaises(PolicyError):
            parse_policy(many_branches)


class EvaluationContractTests(unittest.TestCase):
    def test_train_and_holdout_replay_use_disjoint_opponents_and_seeds(self):
        self.assertFalse(set(environment.TRAIN_OPPONENTS) & set(environment.HOLDOUT_OPPONENTS))
        self.assertFalse(set(environment.TRAIN_SEEDS) & set(environment.HOLDOUT_SEEDS))
        candidate = parse_policy(TFT_SOURCE)
        for split in ("train", "holdout"):
            with self.subTest(split=split):
                first = evaluate_policy(candidate, split)
                self.assertEqual(first, evaluate_policy(candidate, split))
                self.assertEqual(first["mean_payoff"], sum(row["total_payoff"] for row in first["rows"]) / sum(row["turns"] for row in first["rows"]))
        with self.assertRaises(ValueError):
            evaluate_policy(candidate, "invalid")

    def test_geometric_lengths_are_positive_and_equal_across_opponents(self):
        report = evaluate_policy(parse_policy(TFT_SOURCE))
        for seed in environment.TRAIN_SEEDS:
            turns = {row["turns"] for row in report["rows"] if row["seed"] == seed}
            self.assertEqual(turns, {environment.horizon(seed)})
            self.assertGreater(next(iter(turns)), 0)

    def test_fitness_is_raw_training_payoff_without_recognition_bonus(self):
        with tempfile.TemporaryDirectory() as tmp:
            candidate_path = Path(tmp) / "candidate.py"
            candidate_path.write_text(TFT_SOURCE)
            metrics, correct = evaluate_file(candidate_path, Path(tmp) / "result")
            # Sum the match outcomes directly; no recognition score is included.
            report = evaluate_policy(parse_policy(TFT_SOURCE))
            raw_mean = sum(row["total_payoff"] for row in report["rows"]) / sum(row["turns"] for row in report["rows"])
            self.assertTrue(correct["correct"])
            self.assertEqual(metrics["combined_score"], raw_mean)
            self.assertEqual(metrics["public"], {"mean_payoff": raw_mean})
            self.assertEqual(metrics["private"], {})

    def test_invalid_evaluation_cli_writes_invalid_record(self):
        with tempfile.TemporaryDirectory() as tmp:
            candidate = Path(tmp) / "invalid.py"
            candidate.write_text("def policy(own_history, opponent_history):\n    return True\n")
            results = Path(tmp) / "results"
            completed = subprocess.run(
                [sys.executable, str(ROOT / "evaluate.py"), "--program_path", str(candidate), "--results_dir", str(results)],
                cwd=ROOT, capture_output=True, text=True, timeout=30, check=False,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            correctness = json.loads((results / "correct.json").read_text())
            metrics = json.loads((results / "metrics.json").read_text())
            self.assertIs(correctness["correct"], False)
            self.assertIn("PolicyError", correctness["error"])
            self.assertEqual(metrics, {"combined_score": -1.0, "public": {}, "private": {}})


class RecognitionTests(unittest.TestCase):
    def test_canonical_and_alternative_tft_expressions_match(self):
        alternative = "def policy(own_history, opponent_history):\n    return sum(opponent_history[-1:])\n"
        for source in (TFT_SOURCE, alternative):
            with self.subTest(source=source):
                report = analyze_policy(parse_policy(source))
                self.assertIs(report["matches_tft_probes"], True)
                self.assertEqual(report["probe_count"], 1640)
                self.assertEqual(report["first_mismatches"], [])

    def test_defection_grim_and_endgame_variants_are_distinguished(self):
        variants = [
            "return 1",
            "return 1 if opponent_history.count(1) > 0 else 0",
            "return 1 if len(own_history) == 199 else (opponent_history[-1] if opponent_history else 0)",
        ]
        for body in variants:
            with self.subTest(body=body):
                candidate = parse_policy("def policy(own_history, opponent_history):\n    " + body)
                report = analyze_policy(candidate)
                self.assertIs(report["matches_tft_probes"], False)
                self.assertGreater(len(report["first_mismatches"]), 0)

    def test_unprobed_history_difference_is_not_claimed_as_proof(self):
        candidate = parse_policy(
            "def policy(own_history, opponent_history):\n"
            "    return 1 if len(own_history) == 1001 else (opponent_history[-1] if opponent_history else 0)\n"
        )
        report = analyze_policy(candidate)
        self.assertTrue(report["matches_tft_probes"])
        self.assertIn("not proof", report["claim"])
        self.assertEqual(candidate((0,) * 1001, (0,) * 1001), 1)


if __name__ == "__main__":
    unittest.main()
