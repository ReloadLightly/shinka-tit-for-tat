#!/usr/bin/env python3
"""Render E1-R only after its frozen selections and measured offline audit."""
import difflib
import json

from e1r_backend import E1, ORDER
from render_e1r import table, number


def write_report():
    audit = json.loads((E1 / "audit.json").read_text())
    usage = json.loads((E1 / "usage_summary.json").read_text())
    ledger = json.loads((E1 / "ledger.json").read_text())
    assert ledger["closed"]
    stats = audit["paired_descriptive_summary"]
    completed = sum(r["status"] == "complete" for r in audit["runs"].values())
    measured = (E1 / "MEASURED_EVIDENCE.md").read_text()
    interpretation = (E1 / "INTERPRETATION.md").read_text()
    method = (E1 / "METHOD_TEXT.md").read_text().replace("PROTOCOL_COMMIT", ledger["protocol_commit"])
    parts = ["# E1-R: ShinkaEvolve versus independent generation\n\n2026-09-08\n",
             f"**Completion: {completed}/6 runs, {usage['external_invocations']}/60 external proposal invocations; ledger closed.** "
             + ("All three planned pairs are available.\n" if completed == 6 else
                f"Execution stopped: {ledger.get('stop_reason')}. Incomplete/unstarted runs have no primary outcome.\n"),
             interpretation, method,
             "## Game rounds versus search iterations\n\n"
             "A game round is one simultaneous action by each player. A proposal/search iteration asks the model for one candidate program; "
             "an admissible program is then scored across 30 training matches containing 7,092 game rounds. "
             "Each match resets its action histories. The ten proposal opportunities per run are separate from those game rounds. "
             "A receives earlier training information across search iterations; B's fresh sessions always receive the original information. "
             "A Codex invocation may contain multiple model requests or turns; none of these units are interchangeable.\n",
             "## Every run, paired outcomes, selected sources and scored traces\n\n"
             "The following tables are derived from the archived live evaluator records and post-freeze analysis. "
             "All three paired differences are run-level A minus B; missing pairs are excluded, never set to zero. "
             "The descriptive sample SD uses only available pairs. E1-R is reported separately from E1: the previous 44 proposals "
             "and this repetition are not pooled as additional independent replicates.\n",
             measured.removeprefix("# E1-R measured evidence\n"),
             "## Training trajectories\n\n![Best admissible training payoff by proposal opportunity](training_trajectories.svg)\n\n"
             "The trajectory includes the original seed at opportunity zero and retains invalid/duplicate opportunities. "
             "The [complete catalogue](PROPOSALS.md) gives every planned slot, original source, exact prompt, supplied "
             "parent/inspirations, score, validity, failure, database and archive membership. "
             "Generated files, evaluator acceptance, database rows and archive membership are separate facts. "
             "A copied `best/` file is not another proposal. Earliest-tie selections can differ from Shinka's best pointer.\n"]
    links = []
    for run_id in ORDER:
        if not run_id.startswith("A"):
            continue
        for row in audit["runs"][run_id]["slots"][1:]:
            parent = (row.get("supplied_context") or {}).get("parent")
            if row["correct"] and parent and parent["generation"] > 0:
                links.append((row["training"] - parent["combined_score"], run_id, row, parent))
    if links:
        delta, run_id, child, parent = max(links, key=lambda item: item[0])
        slot = child["slot"]
        context = child["supplied_context"]
        inspirations = context["archive_inspirations"] + context["top_k_inspirations"]
        parts.extend(["## One actual evolutionary parent-to-child step\n",
            f"**{run_id}, parent generation {parent['generation']} → child opportunity {slot}.** "
            f"The parent training payoff was {parent['combined_score']:.12f}; the child earned {child['training']:.12f}; "
            f"change **{delta:+.12f}**. This step was chosen for explanation after all selections were frozen, "
            "as the largest measured parent-to-child gain among A proposals with a generated parent. "
            "It did not influence search or selection.\n",
            f"[Exact prompt](runs/{run_id}/invocations/{slot:02d}/prompt.md) · "
            f"[original context record](runs/{run_id}/gen_{slot}/supplied_context.json). "
            f"The parent public metrics were `{json.dumps(parent['public_metrics'])}` and text feedback "
            f"`{parent.get('text_feedback', '')}`. Native prompts render numeric payoff to two decimal places; "
            "archival scores here retain full precision.\n",
            "**Complete supplied parent:**\n\n```python\n" + parent["code"].rstrip() + "\n```\n"])
        for inspiration in inspirations:
            parts.append(f"**Supplied inspiration, generation {inspiration['generation']}, training "
                         f"{inspiration['combined_score']:.12f}:**\n\n```python\n" + inspiration["code"].rstrip() + "\n```\n")
        if not inspirations:
            parts.append("No inspiration program was supplied in this step.\n")
        parts.extend(["**Complete generated child:**\n\n```python\n" + child["complete_source"].rstrip() + "\n```\n",
            "**Original code change:**\n\n```diff\n" + "".join(difflib.unified_diff(
                parent["code"].splitlines(keepends=True), child["complete_source"].splitlines(keepends=True),
                fromfile="supplied_parent.py", tofile="generated_child.py")) + "\n```\n",
            "This establishes which code and feedback preceded a measured change. It does not establish the model's "
            "internal reasoning or a causal effect of numerical feedback alone. Selection, inherited programs and inspirations "
            "all differ between A and B.\n"])
    parts.extend(["## Execution repairs, usage and limitations\n",
        "The scientific source files and old ledgers remain unchanged. The [versioned runtime adapters](setup/IMPLEMENTATION.md) "
        "fix byte-buffered metadata reading, use actual evaluation start for the 60-second limit, and finalize stopped native "
        "runners after bounded draining. The installed pinned Shinka dependency is unchanged and hash-checked. "
        "The 52-test pre-call suite, full six-run mock rehearsal, forced metadata/backend/quota stops and old-failure "
        "reproductions passed before the protocol commit. Earlier local fixture failures are preserved and are not experimental proposals.\n",
        f"Available usage records distinguish **{usage['external_invocations']} external invocations**, "
        f"**{usage['completed_codex_turn_events']} completed Codex turn events** and "
        f"**{usage['native_model_response_records']} native response-usage records**. "
        f"Tokens: `{json.dumps(usage['tokens'])}`; Codex runtime **{usage['codex_runtime_seconds']:.1f} seconds**. "
        "Cached input and reasoning output are subsets. Equal proposal counts do not imply equal token or runtime consumption. "
        "Native Headless does not enforce max_tokens. API-list-price estimates are not subscription charges.\n",
        "Fresh-session native user/base/permission contexts are checked against the frozen prompt and forced local fixture. "
        "Retrieval restrictions use supported per-process controls, not a changed directory alone; no global credentials or permissions "
        "were changed. This is a tested native tool boundary, not an OS confidentiality container. Model prior knowledge remains; "
        "operational rediscovery is not knowledge-free invention.\n",
        "Three paired runs are exploratory. The fixed already-public development encounters are reused; this is not an untouched "
        "confirmatory holdout. Local seeds do not make remote model outputs deterministic. Fixed encounter lengths and opponent "
        "mixtures can reward sample-specific behavior. Finite probe agreement alone is not equivalence: E1's "
        "[B202 slot-5 periodic-defection counterexample](../e1/runs/B202/gen_5/main.py) passes all 1,640 frozen probes yet "
        "defects after 32 prior cooperations. E1-R retains those probes for comparability and separately inspects source. "
        "No target-strategy reward, manual candidate repair, evaluator relaxation or additional scientific condition was introduced.\n",
        (E1 / "FOLLOWUP.md").read_text(),
        "## Evidence and commands\n\n"
        "Publication verification independently reproduced the archived audit, source proofs, scored traces and usage, "
        "checked all 20 native contexts and both SQLite databases, and confirmed unchanged frozen sources and ledger. "
        "The final 52-test suite and both zero-call preflights passed. "
        "The [publication audit](setup/PUBLICATION_AUDIT.md) records these checks and the preserved local sandbox test stall.\n\n"
        "[Protocol](protocol/PROTOCOL.md) · [configuration](protocol/protocol.json) · [source freeze](protocol/freeze.json) · "
        "[closed ledger](ledger.json) · [all selections frozen](training_selections_frozen.json) · [audit](audit.json) · "
        "[usage](usage_summary.json) · [every proposal](PROPOSALS.md) · [commands and local failure history](setup/COMMANDS.md). "
        "Candidate programs were interpreted through policy.py, never imported or exec'd. "
        "Prompts, generated sources, failures, scores, native contexts and archives are preserved without credentials.\n\n"
        "```bash\n.venv/bin/python -m unittest discover -s tests -v\n"
        ".venv/bin/python run_e1r.py --preflight\n"
        ".venv/bin/python check_e1r_restrictions.py --output results/e1_r/setup/restriction_checks_verified.json\n"
        ".venv/bin/python rehearse_e1r.py --root results/e1_r/setup/rehearsal_release\n"
        ".venv/bin/python run_e1r.py --freeze\n"
        "# Protocol, fixes, configuration, source hashes and zero-call ledger committed before calls.\n"
        ".venv/bin/python run_e1r.py --execute > results/e1_r/setup/live_console.txt 2>&1\n"
        ".venv/bin/python e1r_status.py --output results/e1_r/setup/subscription_after.json\n"
        ".venv/bin/python audit_e1r.py > results/e1_r/setup/audit_console.txt 2>&1\n"
        "MPLCONFIGDIR=/tmp/e1r_matplotlib .venv/bin/python render_e1r.py\n"
        ".venv/bin/python write_e1r_report.py\n```\n\n"
        "Default launcher is zero-call. Freeze/evidence paths are single-use; the closed ledger refuses execution again. "
        "No paid API calls, API-key authentication/fallback, purchased-credit continuation, auxiliary models or GitHub Actions were used.\n"])
    (E1 / "E1_R_REPORT.md").write_text("\n".join(parts))


if __name__ == "__main__":
    write_report()
