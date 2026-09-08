#!/usr/bin/env python3
"""Post-freeze source proofs and exact scored traces for the stopped E1-R run."""
import ast
import json

from e1r_backend import E1, ROOT
from policy import load_policy
from audit_e1r import trace_encounter


def diagnose():
    frozen = json.loads((E1 / "training_selections_frozen.json").read_text())
    audit = json.loads((E1 / "audit.json").read_text())
    assert frozen["statuses"]["A101"] == "complete"
    diagnoses = {}
    for run_id, run in audit["runs"].items():
        for row in run["slots"][1:]:
            if not row.get("source"):
                continue
            tree = ast.parse(row["complete_source"])
            key = f"{run_id}/{row['slot']}"
            entry = {"source": row["source"], "sha256": row["sha256"],
                     "nodes": len(list(ast.walk(tree))), "bytes": len(row["complete_source"].encode()),
                     "valid": row["correct"], "probe_compatible": row.get("recognition", {}).get("matches_tft_probes")}
            if entry["probe_compatible"]:
                assert len(tree.body) == 1 and len(tree.body[0].body) == 1
                assert isinstance(tree.body[0].body[0], ast.Return)
                expression = ast.unparse(tree.body[0].body[0].value)
                assert expression in [
                    "0 if len(opponent_history) == 0 else opponent_history[-1]",
                    "0 if not opponent_history else opponent_history[-1]",
                    "0 if not opponent_history else 1 if opponent_history[-1] == 1 else 0"], expression
                entry["source_established_tft_equivalence"] = (
                    "For every finite legal paired binary history: empty opponent history returns integer 0; "
                    "otherwise returns exactly the last opponent action. In the final conditional form, a binary "
                    "value equals 1 iff it is 1, otherwise it is 0. No other dependencies or branches.")
            diagnoses[key] = entry
    source = frozen["selections"]["A101"]["source"]
    candidate = load_policy(ROOT / source)
    traces = {opponent: trace_encounter(candidate, "holdout", opponent, 211)
              for opponent in ("suspicious_tit_for_tat", "alternator", "random_80")}
    (E1 / "source_diagnoses.json").write_text(json.dumps(diagnoses, indent=2) + "\n")
    (E1 / "interpretation_traces.json").write_text(json.dumps(traces, indent=2) + "\n")
    return diagnoses


if __name__ == "__main__":
    result = diagnose()
    print(json.dumps({"generated_sources": len(result),
                      "source_established_tft": sum("source_established_tft_equivalence" in r for r in result.values())}))
