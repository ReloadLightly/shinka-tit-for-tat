#!/usr/bin/env python3
"""Render preserved E1 evidence; no model calls and no candidate execution."""
import json
import ast
from pathlib import Path

from audit_e1 import by_opponent
from e1_backend import E1, ORDER, ROOT


def number(value):
    return "unavailable" if value is None else f"{value:.6f}"


def table(headers, rows):
    return "\n".join(["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |",
                      *("| " + " | ".join(str(v).replace("|", "\\|").replace("\n", " ") for v in row) + " |" for row in rows)]) + "\n"


def source_link(record):
    return "no canonical file" if not record.get("source") else f"[slot {record['slot']}]({record['source'].removeprefix('results/e1/')})"


def catalogue(audit):
    parts = ["# Every E1 proposal opportunity\n",
             "There were 60 planned opportunities nested in six runs, not 60 independent experimental replicates. "
             "E1 stopped at 44 external proposals: four complete runs, A303 incomplete, B303 unstarted. "
             "Unattempted opportunities and a prelaunch block are not invalid programs or zero-payoff observations. "
             "Slot 0 is the unchanged seed. Validity and payoff are fixed-evaluator results. "
             "An AST duplicate ignores formatting/comments and compares with earlier sources in the same run, including seed; it consumes its slot. "
             "Archive means actual final SQLite archive membership, separate from a generated file or database row. "
             "Full-precision context scores below are archival values; native prompts format payoff to two decimals. "
             "Use the prompt links to inspect exactly what the proposer received.\n"]
    for run_id in ORDER:
        run = audit["runs"][run_id]
        parts.append(f"## {run_id} — {run['status']}\n")
        rows = []
        for record in run["slots"][1:]:
            context = record["supplied_context"] or {}
            parent = context.get("parent", {})
            inspirations = context.get("archive_inspirations", []) + context.get("top_k_inspirations", [])
            rows.append([record["slot"], source_link(record), parent.get("generation", "—"),
                         ", ".join(str(p["generation"]) for p in inspirations) or "none",
                         record["opportunity_status"], number(record["training"]),
                         number(record["best_training_so_far"]) if record["source"] else "unavailable", "yes" if record["new_best"] else "no",
                         record["duplicate_of_slot"] if record["duplicate_of_slot"] is not None else "—",
                         "yes" if any(p["archived"] for p in record["database_rows"]) else "no"])
        parts.append(table(["Slot", "Source", "Parent", "Inspirations", "Validity", "Training", "Best so far", "New best", "AST duplicate of", "Archived"], rows))
        for record in run["slots"][1:]:
            slot = record["slot"]
            parts.append(f"### {run_id}, proposal {slot}\n")
            if record["opportunity_status"] in ("not_attempted", "blocked_before_external_launch"):
                parts.append(f"**{record['opportunity_status']}**. No external proposal, generated source, or measured payoff. "
                             + (f"[Preserved boundary failure](runs/{run_id}/invocations/{slot:02d}/headless.stderr.txt) · [actual native prompt prepared before the block](runs/{run_id}/invocations/{slot:02d}/prompt.md).\n" if record["opportunity_status"] == "blocked_before_external_launch" else "The stopped ledger was not reset.\n"))
                continue
            parts.append(f"[Exact rendered prompt](runs/{run_id}/invocations/{slot:02d}/prompt.md) · "
                         f"[native output](runs/{run_id}/invocations/{slot:02d}/codex.jsonl) · "
                         f"[supplied context](runs/{run_id}/gen_{slot}/supplied_context.json) · "
                         f"[evaluation records](runs/{run_id}/gen_{slot}/results/).\n")
            parts.append(f"Training: **{number(record['training'])}**; validity: **{record['correct']}**; "
                         f"current best: {number(record['best_training_so_far'])}; database rows: {len(record['database_rows'])}.\n")
            if record.get("error"):
                parts.append(f"Rejection/failure: `{record['error']}`. Unsupported AST types: {record.get('unsupported_ast_types', [])}. No repair or replacement.\n")
            if record.get("complete_source"):
                try:
                    nodes = len(list(ast.walk(ast.parse(record["complete_source"]))))
                    parts.append(f"Source size: {len(record['complete_source'].encode())} bytes; {nodes} AST nodes (limits 16,000 bytes / 400 nodes).\n")
                except SyntaxError:
                    pass
            if record.get("recognition"):
                parts.append(f"Frozen TFT probes: **{'pass' if record['recognition']['matches_tft_probes'] else 'fail'}**, {record['recognition']['probe_count']} checks, computed after the terminal selection freeze. Finite agreement alone is not equivalence.\n")
                if run_id == "B202" and slot == 5:
                    parts.append("Known false positive: this policy defects after positive multiples of 32 history actions. The actual round-33 training counterexample is documented in the main report.\n")
            if record.get("offline_training_diagnostic"):
                parts.append(f"Post-stop interpreter diagnosis: admissible, training payoff {number(record['offline_training_diagnostic']['mean_payoff'])}. "
                             "This is not a live evaluator result and did not alter selection or archive membership. Shinka's database failure score 0 is not measured payoff.\n")
            parts.append("```python\n" + record.get("complete_source", "# No canonical source; raw response and failure retained.").rstrip() + "\n```\n")
            context = record["supplied_context"] or {}
            if run_id.startswith("B"):
                parts.append("Fresh session; unchanged seed-only information. The backend enforces byte equality with the "
                             "[frozen initial prompt](protocol/initial_prompt.md), and the native-session audit checks the only user message against that prompt. "
                             "No prior candidate, score, validity, recognition, or holdout result is supplied.\n")
            else:
                supplied = [("Parent", context.get("parent"))] + [("Inspiration", p) for p in context.get("archive_inspirations", []) + context.get("top_k_inspirations", [])]
                for role, program in supplied:
                    if program:
                        parts.append(f"**{role}: generation {program['generation']}**, training {number(program['combined_score'])}; "
                                     f"public feedback `{json.dumps(program['public_metrics'])}`; text feedback `{program.get('text_feedback', '')}`.\n")
                        parts.append("```python\n" + program["code"].rstrip() + "\n```\n")
    (E1 / "PROPOSALS.md").write_text("\n".join(parts))


def report_tables(audit, usage):
    parts = ["# E1 measured evidence\n"]
    rows = []
    for run_id in ORDER:
        run = audit["runs"][run_id]
        selected = run["slots"][run["selected_slot"]]
        rows.append([run_id + " (" + run["status"] + ")", source_link(selected) if run["status"] != "not_started" else "none; seed placeholder only", number(selected["training"]) if run["status"] != "not_started" else "unavailable",
                     number(selected.get("holdout", {}).get("mean_payoff")),
                     f"{run['valid_proposals']}/{run['invalid_or_unparsed_proposals']}/{run['unevaluated_generated_proposals']}/{run['duplicate_proposals']}",
                     ", ".join(map(str, run["tft_compatible_slots"])) or "none",
                     "yes" if run["improved_after_first"] else "no" if run["status"] != "not_started" else "unavailable"])
    parts.append(table(["Run", "Training-selected source", "Training", "Development holdout", "Valid/invalid/unevaluated/duplicate", "TFT-probe-compatible slots", "Improved after first?"], rows))
    parts.append("Duplicates overlap validity counts; they are not an additional class. Seed 0 is eligible, but not included in the ten-proposal validity denominator.\n")
    parts.append("B101 slot 3 and A303 slot 4 lack live evaluator results because of the upstream timer defect. A303 additionally has one blocked prelaunch check and five unattempted opportunities. B303 has ten unattempted opportunities. A303's training selection is provisional; neither unfinished run contributes a primary holdout result. Validity here means live evaluator acceptance, not a pure measure of generated syntax quality.\n")
    parts.append("E1 applies the frozen earliest-appearance tie rule. Shinka can record a later tied program as its own best; that pointer does not override E1's predeclared selection. Both records are retained:\n")
    parts.append(table(["Run", "E1 selected slot", "Shinka recorded best slot", "DB rows including seed", "Archive members including seed"],
                       [[name, r["selected_slot"], r["database_best_slot"], r["database_rows"], len(r["archive_ids"])] for name, r in audit["runs"].items()]))
    parts.append(table(["Paired local seed", "A holdout", "B holdout", "A minus B"],
                       [[r["seed"], number(r["A"]), number(r["B"]), number(r["A_minus_B"])] for r in audit["paired_holdout"]]))
    stats = audit["paired_descriptive_summary"]
    parts.append("Descriptive paired summary: " + "; ".join(f"{k}={number(v)}" for k, v in stats.items()) + ".\n")
    rows = []
    for run_id in ORDER:
        value = usage["runs"][run_id]
        token = value["tokens"]
        rows.append([run_id, value["external_invocations"], value["completed_codex_turn_events"], value["native_model_response_records"],
                     token.get("input_tokens", 0), token.get("cached_input_tokens", 0), token.get("output_tokens", 0),
                     token.get("reasoning_output_tokens", 0), f"{value['codex_runtime_seconds']:.1f}", value["tool_calls_observed"]])
    parts.append("## Usage\n")
    parts.append(table(["Run", "Invocations", "Codex turn events", "Model response records", "Input", "Cached subset", "Output", "Reasoning subset", "Codex seconds", "Tool calls"], rows))
    parts.append("Invocations can contain multiple model requests; equal invocation budgets do not imply equal tokens or runtime. Cached/reasoning counts are subsets. Native Headless list-price cost estimates are not subscription charges.\n")
    emitted = set()
    for run_id in ORDER:
        run = audit["runs"][run_id]
        if run["status"] == "not_started":
            continue
        selected = run["slots"][run["selected_slot"]]
        digest = selected["sha256"]
        if digest in emitted:
            continue
        emitted.add(digest)
        same = [name + (" (partial)" if r["status"] == "incomplete" else "") for name, r in audit["runs"].items() if r["status"] != "not_started" and r["slots"][r["selected_slot"]]["sha256"] == digest]
        parts.append(f"## Complete selected source: {', '.join(same)}\n")
        parts.append("```python\n" + selected["complete_source"].rstrip() + "\n```\n")
        parts.append(f"Source SHA-256: `{digest}`.\n")
        tests_by_label = {}
        for trace in run["selected_traces"][:2]:
            for row in trace["rows"]:
                for test in row["branch_tests_in_execution_order"]:
                    tests_by_label.setdefault(test["test"], f"T{len(tests_by_label) + 1}")
        parts.append("Trace test key: " + "; ".join(f"**{label}** = `{test}`" for test, label in tests_by_label.items()) + ".\n")
        for trace in run["selected_traces"][:2]:
            parts.append(f"### Scored encounter trace: {trace['split']} / {trace['opponent']} / seed {trace['seed']}\n")
            parts.append(f"First {len(trace['rows'])} rounds of the actual {trace['match_turns']}-round evaluated encounter; full-match candidate payoff {trace['full_match']['total_payoff']}. "
                         "C=0, D=1. Tests are listed in actual interpreter execution order; true/false identifies the executed branch. "
                         "The replay's full totals are asserted equal to the unchanged evaluator.\n")
            trace_rows = []
            for row in trace["rows"]:
                tests = "; ".join(f"{tests_by_label[c['test']]}={str(c['result']).lower()}" for c in row["branch_tests_in_execution_order"]) or "unconditional return"
                trace_rows.append([row["round"], "".join(map(str, row["own_history"])) or "empty",
                                   "".join(map(str, row["opponent_history"])) or "empty", tests,
                                   f"{row['action']}/{row['opponent_action']}", f"{row['payoff']}/{row['opponent_payoff']}",
                                   f"{row['cumulative_payoff']}/{row['opponent_cumulative_payoff']}"])
            parts.append(table(["Round", "Own history", "Opponent history", "Executed tests", "Actions own/other", "Payoff own/other", "Cumulative own/other"], trace_rows))
        parts.append("### Opponent payoff and cooperation\n")
        parts.append("Cells show own payoff per round and own cooperation percentage, aggregated across the five scored matches for that opponent. All comparators use identical encounters.\n")
        for split in ("train", "holdout"):
            if split not in selected:
                parts.append(f"{split} evaluation unavailable: {selected.get('holdout_error')}.\n")
                continue
            groups = by_opponent(selected[split])
            refs = {name: by_opponent(value[split]) for name, value in audit["references"].items()}
            values = []
            for opponent, group in groups.items():
                cell = lambda g: f"{g['payoff']:.4f} ({100*g['cooperation_rate']:.1f}%)"
                values.append([opponent, cell(group), *(cell(refs[name][opponent]) for name in refs)])
            parts.append(f"**{split}**\n")
            parts.append(table(["Opponent", "Selected", "Seed", "TFT", "Grim", "Ordinary WSLS"], values))
    (E1 / "MEASURED_EVIDENCE.md").write_text("\n".join(parts))


def plot_trajectories(audit):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.3), sharey=True)
    colors = ("#2166ac", "#d95f02", "#1b7837")
    styles = ("-", "--", ":")
    for axis, condition in zip(axes, ("A", "B")):
        for seed, color, style in zip((101, 202, 303), colors, styles):
            run = audit["runs"][f"{condition}{seed}"]
            if run["status"] == "not_started":
                continue
            observed = [r for r in run["slots"] if r["source"]]
            axis.plot([r["slot"] for r in observed], [r["best_training_so_far"] for r in observed],
                      label=str(seed) + (" partial" if run["status"] == "incomplete" else ""), color=color, linestyle=style, marker=".")
        axis.axhline(audit["references"]["tit_for_tat"]["train"]["mean_payoff"], color="#555555", linewidth=.8, linestyle="--")
        axis.axhline(audit["references"]["grim"]["train"]["mean_payoff"], color="#999999", linewidth=.8, linestyle=":")
        axis.set_title("A: ShinkaEvolve" if condition == "A" else "B: Independent generation")
        axis.set_xlabel("Proposal opportunity (0 = seed)")
        axis.set_xticks(range(0, 11, 2))
        axis.grid(alpha=.15)
        axis.legend(title="Local seed", loc="lower right", fontsize=8, title_fontsize=8)
    axes[0].set_ylabel("Best admissible training payoff so far")
    fig.text(.5, .01, "Gray reference lines: TFT (dashed), grim trigger (dotted). Selection uses training only.", ha="center", fontsize=8)
    fig.tight_layout(rect=(0, .05, 1, 1))
    fig.savefig(E1 / "training_trajectories.svg")
    plt.close(fig)


if __name__ == "__main__":
    audit = json.loads((E1 / "audit.json").read_text())
    usage = json.loads((E1 / "usage_summary.json").read_text())
    catalogue(audit)
    report_tables(audit, usage)
    plot_trajectories(audit)
