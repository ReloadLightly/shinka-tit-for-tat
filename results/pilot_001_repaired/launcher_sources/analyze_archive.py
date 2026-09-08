"""Offline diagnosis of canonical Shinka candidate files, including seed 0.

Verified upstream layout: gen_N/main.py (not best/ copies or attempt text).
All training rescoring and selection finish before recognition or holdout runs.
This command does not read Shinka's database and cannot certify its live winner.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import re

from environment import evaluate_policy
from policy import parse_policy
from recognize import analyze_policy


GENERATION = re.compile(r"gen_(0|[1-9][0-9]*)\Z")
MAX_GENERATION_DIRECTORIES = 101
MAX_READ_BYTES = 1_000_000


def recorded_evaluation(generation_dir: Path) -> dict:
    """Describe saved artifacts without treating their contents as verified provenance."""
    paths = [generation_dir / "results" / name for name in ("metrics.json", "correct.json")]
    report = {"files_present": all(path.is_file() for path in paths),
              "live_evaluation_or_database_retention_verified": False}
    if report["files_present"]:
        try:
            if any(path.stat().st_size > MAX_READ_BYTES for path in paths):
                raise ValueError("Saved evaluation artifact exceeds read limit")
            metrics, correct = [json.loads(path.read_text(encoding="utf-8")) for path in paths]
            report["reported_correct"] = correct.get("correct")
            report["reported_combined_score"] = metrics.get("combined_score")
        except (OSError, ValueError, AttributeError) as exc:
            report["read_error"] = f"{type(exc).__name__}: {exc}"
    return report


def analyze_archive(results_dir: Path) -> dict:
    root = results_dir.resolve()
    if not root.is_dir():
        raise ValueError("--results-dir must be an existing Shinka results directory")
    generations = sorted(
        (int(match.group(1)), child)
        for child in root.iterdir()
        if (match := GENERATION.fullmatch(child.name)) and child.is_dir()
    )
    if not generations:
        raise ValueError("No canonical gen_N directories found")
    if len(generations) > MAX_GENERATION_DIRECTORIES:
        raise ValueError(f"Analysis is bounded to {MAX_GENERATION_DIRECTORIES} generation directories")

    records, valid_candidates = [], {}
    # Pass 1: training only. No recognition or holdout call occurs in this pass.
    for number, directory in generations:
        path = directory / "main.py"
        record = {"generation": number, "is_seed": number == 0,
                  "program_path": str(path), "relative_program_path": str(path.relative_to(root)),
                  "sha256": None, "valid_for_training": False,
                  "recorded_evaluation": recorded_evaluation(directory)}
        records.append(record)
        if not path.is_file():
            record.update(status="missing_program", error="Canonical main.py was not written")
            continue
        try:
            if path.stat().st_size > MAX_READ_BYTES:
                raise ValueError("Candidate exceeds bounded read limit; hash not computed")
            source_bytes = path.read_bytes()
            record["sha256"] = hashlib.sha256(source_bytes).hexdigest()
            candidate = parse_policy(source_bytes.decode("utf-8"))
            train = evaluate_policy(candidate, "train")
            score = train["mean_payoff"]
            if not isinstance(score, (int, float)) or not math.isfinite(score):
                raise ValueError("Non-finite training score")
            record.update(status="valid_for_training", valid_for_training=True, train=train)
            valid_candidates[number] = candidate
            old_score = record["recorded_evaluation"].get("reported_combined_score")
            if isinstance(old_score, (int, float)) and math.isfinite(old_score):
                record["recorded_evaluation"]["agrees_with_offline_training_score"] = math.isclose(
                    old_score, score, rel_tol=0.0, abs_tol=1e-12)
        except Exception as exc:
            record.update(status="invalid_program_or_training_failure",
                          error=f"{type(exc).__name__}: {exc}")

    eligible = [record for record in records if record["valid_for_training"]]
    # Earliest generation wins exact training-payoff ties. Seed is eligible.
    selected = max(eligible, key=lambda item: (item["train"]["mean_payoff"], -item["generation"]),
                   default=None)
    selected_generation = selected["generation"] if selected else None

    # Pass 2: post-selection diagnostics. Neither result can change selected_generation.
    for record in eligible:
        candidate = valid_candidates[record["generation"]]
        try:
            record["recognition"] = analyze_policy(candidate)
        except Exception as exc:
            record["recognition_error"] = f"{type(exc).__name__}: {exc}"
        try:
            record["holdout"] = evaluate_policy(candidate, "holdout")
            record["valid_on_holdout"] = True
        except Exception as exc:
            record["valid_on_holdout"] = False
            record["holdout_error"] = f"{type(exc).__name__}: {exc}"

    matches = [record for record in eligible
               if record.get("recognition", {}).get("matches_tft_probes") is True]
    mutation_matches = [record for record in matches if not record["is_seed"]]
    selected_record = next((r for r in records if r["generation"] == selected_generation), None)

    def identity(record):
        if record is None:
            return None
        return {key: record[key] for key in
                ("generation", "is_seed", "relative_program_path", "program_path", "sha256")}

    diagnostic_sources = [Path(__file__), *(Path(__file__).parent / name for name in
                                         ("environment.py", "policy.py", "recognize.py"))]
    return {
        "analysis_kind": "offline_rescoring_of_canonical_candidate_files",
        "results_dir": str(root), "generated_utc": datetime.now(timezone.utc).isoformat(),
        "upstream_layout": "gen_N/main.py; N=0 is seed; best/ and attempts/ are excluded",
        "generation_directories": len(records),
        "candidate_files": sum(record["status"] != "missing_program" for record in records),
        "valid_training_candidates": len(eligible),
        "valid_training_mutations": sum(not record["is_seed"] for record in eligible),
        "selection_rule": "Highest offline training mean payoff; exact ties choose earliest generation; seed eligible",
        "selection_frozen_before_recognition_and_holdout": True,
        "shinka_database_winner_verified": False,
        "training_payoff_selected_generation": selected_generation,
        "training_payoff_selected_candidate": selected_record,
        "first_tft_probe_matching_candidate_including_seed": identity(matches[0]) if matches else None,
        "first_tft_probe_matching_mutation": identity(mutation_matches[0]) if mutation_matches else None,
        "tft_probe_matching_mutation_generations": [record["generation"] for record in mutation_matches],
        "claim_limits": [
            "Finite probe agreement is not proof of tit-for-tat equivalence on every history.",
            "Offline rescoring does not prove a file was live-evaluated, retained in the archive, or generated by an LLM.",
            "The seed does not count as a discovered mutation.",
            "Holdout scores are diagnostics and do not select the reported winner.",
        ],
        "diagnostic_source_sha256": {path.name: hashlib.sha256(path.read_bytes()).hexdigest()
                                     for path in diagnostic_sources},
        "candidates": records,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results-dir", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    if args.output.exists():
        parser.error("Refusing to overwrite existing diagnostic output")
    try:
        report = analyze_archive(args.results_dir)
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    # Exclusive creation also protects against a concurrent writer.
    with args.output.open("x", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2, allow_nan=False)
        handle.write("\n")
    selected = report["training_payoff_selected_candidate"]
    print(json.dumps({
        "analysis_kind": report["analysis_kind"],
        "valid_training_mutations": report["valid_training_mutations"],
        "first_tft_probe_matching_mutation": report["first_tft_probe_matching_mutation"],
        "training_payoff_selected_generation": report["training_payoff_selected_generation"],
        "selected_candidate_matches_tft_probes":
            selected.get("recognition", {}).get("matches_tft_probes") if selected else None,
        "output": str(args.output.resolve()),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
