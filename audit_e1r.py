#!/usr/bin/env python3
"""Post-selection E1 audit. Candidate programs are only interpreted by policy.py."""
import argparse
import ast
from collections import Counter
import hashlib
import json
from pathlib import Path
import random
import sqlite3
import statistics
import sys

from e1r_backend import E1, ORDER, ROOT, utc
from run_e1r import select, sha, training_records
from subscription_guard import write_json


def freeze_terminal_states():
    from run_e1r import freeze_selections
    return freeze_selections()


def collect_usage():
    ledger = json.loads((E1 / "ledger.json").read_text())
    protocol = json.loads((E1 / "protocol" / "protocol.json").read_text())
    assert sha(E1 / "protocol" / "initial_prompt.md") == protocol["initial_prompt_sha256"]
    fixture = json.loads((E1 / "setup" / "restriction_checks_verified.json").read_text())["records"][0]["requests"][0]
    fixture_base = fixture["input"][1]["content"][0]["text"]
    fixture_permissions = fixture["input"][2]["content"]
    sessions = list((Path.home() / ".codex" / "sessions").rglob("*.jsonl"))
    total = Counter()
    runs = {}
    all_threads = []
    for run_id in ORDER:
        records = [r for r in ledger["invocations"] if r["run_id"] == run_id]
        totals = Counter()
        response_count = 0
        tool_calls = []
        native_sessions = []
        for record in records:
            folder = E1 / "runs" / run_id / "invocations" / f"{record['slot']:02d}"
            extracted = {"invocation": record["invocation"], "model_response_usage_records": [], "contexts": [], "messages": [], "tool_calls": []}
            for thread_id in record.get("thread_ids", []):
                paths = [p for p in sessions if thread_id in p.name]
                if len(paths) != 1:
                    raise RuntimeError(f"Expected one native session for E1 invocation {record['invocation']}")
                path = paths[0]
                native_sessions.append(thread_id)
                all_threads.append(thread_id)
                extracted["native_transcript_sha256"] = sha(path)
                for line in path.read_text().splitlines():
                    event = json.loads(line)
                    payload = event.get("payload") or {}
                    kind = event.get("type")
                    if kind == "session_meta":
                        extracted["native_base_instructions"] = payload.get("base_instructions")
                    elif kind == "token_usage_record":
                        extracted["model_response_usage_records"].append({"timestamp": event.get("timestamp"),
                            "response_id": payload.get("response_id"), "usage": payload.get("usage")})
                    elif kind == "turn_context":
                        extracted["contexts"].append({k: payload.get(k) for k in
                            ("model", "model_provider", "cwd", "effort", "reasoning_effort", "sandbox_policy", "approval_policy")})
                    elif kind == "response_item" and payload.get("type") == "message" and payload.get("role") in ("developer", "user"):
                        extracted["messages"].append(payload)
                    elif kind == "response_item" and payload.get("type") in ("function_call", "custom_tool_call", "web_search_call"):
                        extracted["tool_calls"].append(payload)
            if extracted["contexts"]:
                assert all(c["model"] == "gpt-5.6-terra" and c["effort"] == "low" for c in extracted["contexts"])
            if record.get("status") == "completed":
                assert extracted["native_base_instructions"]["text"] == fixture_base
                developers = [m for m in extracted["messages"] if m.get("role") == "developer"]
                assert len(developers) == 1 and developers[0]["content"] == fixture_permissions, "Unexpected ambient developer context"
                user_messages = [m for m in extracted["messages"] if m.get("role") == "user"]
                assert len(user_messages) == 1, "Mutation session inherited prior user context"
                text = "".join(c.get("text", "") for c in user_messages[0].get("content", []))
                assert text == (folder / "prompt.md").read_text(), "Native session user information differs from recorded prompt"
            for entry in extracted["model_response_usage_records"]:
                totals.update({k: v for k, v in (entry["usage"] or {}).items() if type(v) is int})
            response_count += len(extracted["model_response_usage_records"])
            tool_calls.extend(extracted["tool_calls"])
            if folder.exists():
                write_json(folder / "native_context_usage.json", extracted)
        runs[run_id] = {"external_invocations": len(records), "completed_codex_turn_events": sum(r.get("completed_codex_turn_events", 0) for r in records),
                        "native_model_response_records": response_count, "tokens": dict(totals),
                        "codex_runtime_seconds": sum(r.get("runtime_seconds", 0) for r in records),
                        "tool_calls_observed": len(tool_calls), "tool_calls": tool_calls,
                        "fresh_unique_threads": len(set(native_sessions)), "thread_count": len(native_sessions)}
        total.update(totals)
    assert len(all_threads) == len(set(all_threads)), "A mutation session was reused"
    report = {"generated_utc": utc(), "runs": runs, "tokens": dict(total),
              "unique_native_threads": len(set(all_threads)),
              "native_base_and_permissions_match_local_fixture": True,
              "native_user_messages_match_recorded_prompts": True,
              "external_invocations": len(ledger["invocations"]),
              "native_model_response_records": sum(r["native_model_response_records"] for r in runs.values()),
              "completed_codex_turn_events": sum(r["completed_codex_turn_events"] for r in runs.values()),
              "codex_runtime_seconds": sum(r["codex_runtime_seconds"] for r in runs.values()),
              "semantics": "One invocation may contain multiple model requests. Native response records count available model usage records; completed Codex turns are separate. Cached input and reasoning output are subsets, not additional tokens."}
    write_json(E1 / "usage_summary.json", report)
    return report


def trace_encounter(candidate, split, opponent, seed, count=8):
    """Replay a scored encounter through the unchanged interpreter, tracing branches."""
    from environment import reference, horizon, PAYOFFS, play
    match_seed = int.from_bytes(hashlib.sha256(f"{split}/{opponent}/{seed}".encode()).digest()[:8], "big")
    rng = random.Random(match_seed)
    own, other = (), ()
    rows = []
    total = opponent_total = 0
    for round_number in range(1, horizon(seed) + 1):
        conditions = []

        def tracer(frame, event, value):
            if event == "return" and frame.f_code.co_name == "expression" and frame.f_code.co_filename == str(ROOT / "policy.py"):
                node = frame.f_locals.get("n")
                parent = frame.f_back.f_locals.get("n") if frame.f_back else None
                if isinstance(parent, (ast.If, ast.IfExp)) and node is parent.test:
                    conditions.append({"test": ast.unparse(node), "result": bool(value)})
            return tracer

        previous_trace = sys.gettrace()
        if round_number <= count:
            sys.settrace(tracer)
        try:
            action = candidate(own, other)
        finally:
            sys.settrace(previous_trace)
        enemy = reference(opponent, other, own, rng)
        reward, enemy_reward = PAYOFFS[action, enemy], PAYOFFS[enemy, action]
        total += reward
        opponent_total += enemy_reward
        if round_number <= count:
            rows.append({"round": round_number, "own_history": list(own), "opponent_history": list(other),
                         "branch_tests_in_execution_order": conditions, "action": action, "opponent_action": enemy,
                         "payoff": reward, "opponent_payoff": enemy_reward,
                         "cumulative_payoff": total, "opponent_cumulative_payoff": opponent_total})
        own += (action,)
        other += (enemy,)
    original = play(candidate, opponent, horizon(seed), match_seed)
    assert original["total_payoff"] == total and original["opponent_total_payoff"] == opponent_total
    return {"split": split, "opponent": opponent, "seed": seed, "match_seed": match_seed,
            "match_turns": horizon(seed), "scored_encounter": True, "full_match": original, "rows": rows}


def by_opponent(result):
    groups = {}
    for row in result["rows"]:
        group = groups.setdefault(row["opponent"], Counter())
        for key in ("total_payoff", "cooperations", "turns"):
            group[key] += row[key]
    return {name: {**g, "payoff": g["total_payoff"] / g["turns"], "cooperation_rate": g["cooperations"] / g["turns"]} for name, g in groups.items()}


def audit():
    frozen_path = E1 / "training_selections_frozen.json"
    if not frozen_path.exists():
        raise RuntimeError("All six training selections must be frozen before holdout/recognition")
    frozen = json.loads(frozen_path.read_text())
    assert set(frozen["selections"]) == set(ORDER)
    # First validate ALL selections and source identities before importing diagnostics.
    for run_id in ORDER:
        records = training_records(run_id)
        if records:
            assert select(records) == frozen["selections"][run_id]
        else:
            assert frozen.get("statuses", {}).get(run_id) == "not_started"
            assert frozen["selections"][run_id]["source"] == "initial.py"
        assert sha(ROOT / frozen["selections"][run_id]["source"]) == frozen["selections"][run_id]["sha256"]
    from policy import load_policy, ALLOWED
    from environment import evaluate_policy, reference_policy
    from recognize import analyze_policy
    ledger = json.loads((E1 / "ledger.json").read_text())
    assert ledger["closed"]
    report = {"analysis_started_utc": utc(), "selection_freeze_sha256": sha(frozen_path), "runs": {}}
    for run_id in ORDER:
        folder = E1 / "runs" / run_id
        status = frozen.get("statuses", {}).get(run_id, "complete")
        programs, archived, events, attempts, db_best = [], set(), [], [], None
        if (folder / "programs.sqlite").exists():
          with sqlite3.connect(f"file:{folder}/programs.sqlite?mode=ro", uri=True) as db:
            db.row_factory = sqlite3.Row
            programs = [dict(r) for r in db.execute("SELECT * FROM programs ORDER BY generation,timestamp")]
            archived = {r[0] for r in db.execute("SELECT program_id FROM archive")}
            best_row = db.execute("SELECT value FROM metadata_store WHERE key='best_program_id'").fetchone()
            db_best = best_row[0] if best_row else None
            events = [dict(r) for r in db.execute("SELECT * FROM generation_event_log ORDER BY id")]
            attempts = [dict(r) for r in db.execute("SELECT * FROM attempt_log ORDER BY id")]
        records = {r["slot"]: r for r in training_records(run_id)}
        if not records:
            records[0] = dict(frozen["selections"][run_id], baseline_placeholder=True)
        best = records[0]
        seen = {}
        slots = []
        for slot in range(11):
            record = records.get(slot, {"slot": slot, "source": None, "correct": False, "training": None, "error": "No canonical generated source; inspect raw response/failure"})
            record["duplicate_of_slot"] = None
            record["new_best"] = False
            record["opportunity_status"] = ("baseline" if slot == 0 else
                "valid" if record["correct"] else "rejected" if record.get("training") is not None else
                "evaluation_missing" if record["source"] else
                "failed_or_unparsed" if any(r["run_id"] == run_id and r["slot"] == slot for r in ledger["invocations"]) else
                "blocked_before_external_launch" if (folder / "invocations" / f"{slot:02d}").exists() else "not_attempted")
            if record["source"]:
                source = (ROOT / record["source"]).read_text()
                record["complete_source"] = source
                try:
                    tree = ast.parse(source)
                    signature = ast.dump(tree, include_attributes=False)
                    record["duplicate_of_slot"] = seen.get(signature)
                    seen.setdefault(signature, slot)
                    record["unsupported_ast_types"] = sorted({type(n).__name__ for n in ast.walk(tree) if not isinstance(n, ALLOWED)})
                except SyntaxError:
                    pass
            matching = [p for p in programs if p["generation"] == slot]
            record["database_rows"] = [{"id": p["id"], "parent_id": p["parent_id"],
                "correct": bool(p["correct"]), "training": p["combined_score"],
                "source_sha256": hashlib.sha256(p["code"].encode()).hexdigest(),
                "archived": p["id"] in archived, "shinka_best": p["id"] == db_best,
                "archive_inspiration_ids": p["archive_inspiration_ids"], "top_k_inspiration_ids": p["top_k_inspiration_ids"]} for p in matching]
            for row in record["database_rows"]:
                if record["source"]:
                    assert row["source_sha256"] == record["sha256"]
                    assert row["correct"] == record["correct"]
                    if record["training"] is not None:
                        assert row["training"] == record["training"]
                    else:
                        record["database_failure_score_not_measured_payoff"] = row["training"]
            context = folder / f"gen_{slot}" / "supplied_context.json"
            record["supplied_context"] = json.loads(context.read_text()) if context.exists() else None
            if record["correct"]:
                candidate = load_policy(ROOT / record["source"])
                train = evaluate_policy(candidate, "train")
                assert train["mean_payoff"] == record["training"]
                record["train"] = train
                record["recognition"] = analyze_policy(candidate)
                if record["training"] > best["training"]:
                    best = record
                    record["new_best"] = True
            elif record["source"] and record["training"] is None:
                # Diagnose an infrastructure failure offline, never insert it
                # into the live archive or alter the already frozen selection.
                try:
                    diagnostic = evaluate_policy(load_policy(ROOT / record["source"]), "train")
                    record["offline_training_diagnostic"] = diagnostic
                    record["offline_diagnostic_note"] = "Post-stop only; no live evaluator result; not eligible for retrospective selection or admissible-appearance counts"
                except Exception as exc:
                    record["offline_diagnostic_error"] = f"{type(exc).__name__}: {exc}"
            record["best_training_so_far"] = best["training"]
            slots.append(record)
        selected = slots[frozen["selections"][run_id]["slot"]]
        candidate = load_policy(ROOT / selected["source"])
        if status == "complete":
            try:
                selected["holdout"] = evaluate_policy(candidate, "holdout")
            except Exception as exc:
                selected["holdout_error"] = f"{type(exc).__name__}: {exc}"
        else:
            selected["holdout_error"] = "Run incomplete/unstarted; no primary holdout result computed"
        traces = [trace_encounter(candidate, split, opponent, seed)
                  for split, opponent, seed in (("train", "always_defect", 11), ("train", "random", 11),
                                                ("train", "tit_for_tat", 11), ("holdout", "alternator", 211))
                  if status == "complete" or (status == "incomplete" and split == "train")]
        proposals = slots[1:]
        report["runs"][run_id] = {"slots": slots, "selected_slot": selected["slot"], "status": status,
            "valid_proposals": sum(r["correct"] for r in proposals),
            "invalid_or_unparsed_proposals": sum(r["opportunity_status"] in ("rejected", "failed_or_unparsed") for r in proposals),
            "unevaluated_generated_proposals": sum(r["opportunity_status"] == "evaluation_missing" for r in proposals),
            "not_attempted_opportunities": sum(r["opportunity_status"] == "not_attempted" for r in proposals),
            "blocked_before_launch": sum(r["opportunity_status"] == "blocked_before_external_launch" for r in proposals),
            "duplicate_proposals": sum(r["duplicate_of_slot"] is not None for r in proposals),
            "tft_compatible_slots": [r["slot"] for r in proposals if r.get("recognition", {}).get("matches_tft_probes")],
            "improved_after_first": max(r["best_training_so_far"] for r in proposals) > proposals[0]["best_training_so_far"],
            "selected_traces": traces, "archive_ids": sorted(archived), "database_best_id": db_best,
            "database_best_slot": next((p["generation"] for p in programs if p["id"] == db_best), None),
            "database_rows": len(programs), "generation_events": events, "attempt_log": attempts}
    references = {}
    for name in ("always_defect", "tit_for_tat", "grim", "win_stay_lose_shift"):
        references[name] = {split: evaluate_policy(reference_policy(name), split) for split in ("train", "holdout")}
    report["references"] = references
    deltas = []
    for seed in (101, 202, 303):
        a, b = report["runs"][f"A{seed}"], report["runs"][f"B{seed}"]
        av = a["slots"][a["selected_slot"]].get("holdout", {}).get("mean_payoff")
        bv = b["slots"][b["selected_slot"]].get("holdout", {}).get("mean_payoff")
        deltas.append({"seed": seed, "A": av, "B": bv, "A_minus_B": av - bv if av is not None and bv is not None else None})
    report["paired_holdout"] = deltas
    values = [r["A_minus_B"] for r in deltas if r["A_minus_B"] is not None]
    report["paired_descriptive_summary"] = {"n": len(values), "mean": statistics.mean(values),
        "median": statistics.median(values), "min": min(values), "max": max(values),
        "sample_sd": statistics.stdev(values) if len(values) > 1 else None} if values else {"n": 0}
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--usage-only", action="store_true")
    parser.add_argument("--freeze-terminal", action="store_true")
    args = parser.parse_args()
    if args.freeze_terminal:
        freeze_terminal_states()
        print("All terminal selection identities/statuses frozen; incomplete/unstarted entries excluded from primary outcomes.")
        raise SystemExit(0)
    usage = collect_usage()
    if not args.usage_only:
        if (E1 / "audit.json").exists():
            raise SystemExit("Refusing to overwrite completed scientific audit")
        report = audit()
        write_json(E1 / "audit.json", report)
        print(json.dumps(report["paired_holdout"], indent=2))
    else:
        print(json.dumps({"invocations": usage["external_invocations"], "model_response_records": usage["native_model_response_records"]}))
