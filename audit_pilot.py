"""Post-search comparison of canonical files, live SQLite records, and usage.

Read-only SQLite access; candidate code is interpreted by analyze_archive.
Never imports or executes candidate source. Run only after search has ended.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sqlite3

from analyze_archive import analyze_archive


def digest(source):
    return hashlib.sha256(source.encode()).hexdigest()


def audit_run(root):
    diagnostic = analyze_archive(root)
    with sqlite3.connect(f"file:{root.resolve()}/programs.sqlite?mode=ro", uri=True) as db:
        db.row_factory = sqlite3.Row
        rows = [dict(r) for r in db.execute("SELECT * FROM programs ORDER BY generation, timestamp")]
        archive = {r[0] for r in db.execute("SELECT program_id FROM archive")}
        best_row = db.execute("SELECT value FROM metadata_store WHERE key='best_program_id'").fetchone()
        best_id = best_row[0] if best_row else None
        attempts = [dict(r) for r in db.execute("SELECT * FROM attempt_log ORDER BY id")]
        events = [dict(r) for r in db.execute("SELECT * FROM generation_event_log ORDER BY id")]
    candidates = []
    for record in diagnostic["candidates"]:
        matches = [r for r in rows if r["generation"] == record["generation"]]
        record["database_rows"] = [{"id": r["id"], "parent_id": r["parent_id"],
                                    "correct": bool(r["correct"]), "combined_score": r["combined_score"],
                                    "code_sha256": digest(r["code"]),
                                    "canonical_source_matches": digest(r["code"]) == record["sha256"],
                                    "retained_in_archive": r["id"] in archive,
                                    "shinka_best": r["id"] == best_id} for r in matches]
        candidates.append(record)
    selected = next((r for r in rows if r["id"] == best_id), None)
    valid = [r for r in rows if r["correct"]]
    highest_score = max((r["combined_score"] for r in valid), default=None)
    if selected and selected["combined_score"] != highest_score:
        raise ValueError("Shinka best differs from highest valid training score")
    # Attempt responses are counted independently of canonical candidates.
    responses = []
    for path in sorted(root.glob("gen_*/attempts/**/llm_response.txt")):
        patch = path.with_name("patch.txt")
        responses.append({"response_path": str(path.relative_to(root)),
                          "response_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                          "patch_file_present": patch.is_file(),
                          "canonical_program_present": (path.parents[4] / "main.py").is_file()})
    for collection in (attempts, events):
        for row in collection:
            row["details"] = json.loads(row["details"] or "{}")
    best = None if selected is None else {
        "id": selected["id"], "generation": selected["generation"],
        "training_payoff": selected["combined_score"], "complete_executable_source": selected["code"],
        "source_sha256": digest(selected["code"]), "retained_in_archive": selected["id"] in archive,
    }
    if best:
        record = next(r for r in candidates if r["generation"] == best["generation"])
        best["holdout_payoff"] = record.get("holdout", {}).get("mean_payoff")
        best["recognition"] = record.get("recognition")
    return {"run": str(root), "analysis": diagnostic, "shinka_best": best,
            "database_program_rows": len(rows), "archive_members": len(archive),
            "attempt_responses": responses, "attempt_log": attempts, "generation_event_log": events}


def audit_usage(root):
    ledger = json.loads((root / "invocations.json").read_text())
    totals = {}
    completed_events = 0
    tool_items = []
    for record in ledger["invocations"]:
        for usage in record.get("turn_usage", []):
            for key, value in (usage or {}).items():
                if type(value) is int:
                    totals[key] = totals.get(key, 0) + value
        completed_events += record.get("completed_codex_turn_events", 0)
        trace = root / f"invocation_{record['invocation']}" / "codex.jsonl"
        for line in trace.read_text().splitlines():
            event = json.loads(line)
            item = event.get("item") or {}
            if item.get("type") not in (None, "agent_message", "reasoning"):
                tool_items.append({"invocation": record["invocation"], "event": event})
    return {"ledger": ledger, "external_proposal_invocations": len(ledger["invocations"]),
            "completed_codex_turn_events": completed_events, "internal_model_requests": None,
            "codex_turn_usage_sum": totals, "non_message_trace_items": tool_items,
            "count_limit": "Codex turn.completed events are not internal model request counts"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", action="append", type=Path, required=True)
    parser.add_argument("--usage-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error("Refusing to overwrite audit evidence")
    report = {"runs": [audit_run(root) for root in args.run], "usage": audit_usage(args.usage_dir)}
    with args.output.open("x") as handle:
        json.dump(report, handle, indent=2, allow_nan=False)
        handle.write("\n")
    print(json.dumps({"best_by_run": [r["shinka_best"] for r in report["runs"]],
                      "invocations": report["usage"]["external_proposal_invocations"]}, indent=2))
