#!/usr/bin/env python3
"""Render the authored interpretation of this terminal, partial E1 record."""
import json
from pathlib import Path
import re

from audit_e1 import by_opponent
from e1_backend import E1
from render_e1 import table


def trace_table(trace, periodic=False):
    rows = []
    for r in trace["rows"]:
        history = lambda h: "".join(map(str, h)) if len(h) <= 12 else "…" + "".join(map(str, h[-12:]))
        tests = r["branch_tests_in_execution_order"]
        if tests and tests[0]["result"]:
            branch = "first move → C"
        elif periodic and any(t["result"] for t in tests[1:]):
            test = next(t["test"] for t in tests[1:] if t["result"])
            period = int(re.search(r">= (\d+)", test).group(1)) // 2
            branch = f"period {period} → D"
        else:
            branch = "copy last opponent action"
        rows.append([r["round"], history(r["own_history"]) or "empty", history(r["opponent_history"]) or "empty",
                     branch, f"{r['action']}/{r['opponent_action']}", f"{r['payoff']}/{r['opponent_payoff']}",
                     f"{r['cumulative_payoff']}/{r['opponent_cumulative_payoff']}"])
    return table(["Round", "Own past", "Other past", "Executed branch", "Actions own/other", "Payoff own/other", "Cumulative own/other"], rows)


def opponent_table(audit, selected):
    rows = []
    for split in ("train", "holdout"):
        own = by_opponent(selected[split])
        refs = {name: by_opponent(r[split]) for name, r in audit["references"].items()}
        cell = lambda v: f"{v['payoff']:.4f} / {100*v['cooperation_rate']:.1f}%"
        for name, value in own.items():
            rows.append([split, name, cell(value), *(cell(refs[r][name]) for r in refs)])
    return table(["Panel", "Opponent", "Selected", "Seed", "TFT", "Grim", "Ordinary WSLS"], rows)


def main():
    audit = json.loads((E1 / "audit.json").read_text())
    usage = json.loads((E1 / "usage_summary.json").read_text())
    traces = json.loads((E1 / "interpretation_traces.json").read_text())
    assert usage["external_invocations"] == 44
    assert audit["paired_descriptive_summary"]["n"] == 2
    measured = (E1 / "MEASURED_EVIDENCE.md").read_text()
    tables = measured.split("## Complete selected source:")[0].replace("# E1 measured evidence", "## Every run and the partial comparison")
    methods = (E1 / "METHOD_TEXT.md").read_text()
    methods = methods.replace("All six source identities\nwere frozen in [training_selections_frozen.json](training_selections_frozen.json)\nbefore holdout evaluation or TFT recognition.",
        "After the terminal stop, [the selection-state freeze](training_selections_frozen.json)\nlocked four completed-run selections, A303's partial best-so-far and the unchanged\nseed as an explicit placeholder for unstarted B303, before any holdout or TFT\nanalysis. The placeholder is not a B303 result. Neither unfinished run receives\na primary holdout value. This terminal handling does not complete the originally\nplanned three-pair design.")
    parts = ["# E1: ShinkaEvolve versus independent generation — partial, stopped\n\n2026-09-08\n",
        "**E1 did not complete its planned three replicate pairs.** It stopped at **44 of 60 external proposal invocations**: "
        "A101, B101, B202 and A202 completed ten opportunities each; A303 generated four proposals; B303 never started. "
        "The closed ledger retains the unused allowance and cannot be reset.\n\n"
        "The available paired holdout differences, A minus B, are **0.000000**, **−0.110196**, and **unavailable**. "
        "Their two-pair descriptive mean is **−0.055098** payoff per round. This partial readout provides no observed "
        "advantage for ShinkaEvolve. Its strongest training improvement transferred poorly to holdout. "
        "Two pairs and infrastructure failures do not establish a general negative effect or complete the E1 hypothesis test.\n\n"
        "There were 44 generated sources: **40 live-valid, two interpreter rejections, and two without live evaluator results**. "
        "All 44 have Shinka database rows; 40 generated policies were retained in archives. Seed rows and `best/` copies "
        "are additional records, not proposals. Nineteen valid proposals passed the frozen TFT probes; source inspection "
        "establishes the TFT rule for eighteen, while one periodic defector exposes a finite-probe false positive.\n\n"
        "[Every opportunity, exact prompts, generated sources and supplied contexts](PROPOSALS.md) · "
        "[machine-readable audit](audit.json) · [frozen protocol](protocol/PROTOCOL.md) · "
        "[closed ledger](ledger.json) · [commands](setup/COMMANDS.md).\n",
        methods,
        "## What stopped the experiment\n\n"
        "The subscription metadata read before A303 slot 5 timed out. The stop latch prevented a 45th proposal; "
        "there was no retry, replacement, quota override or reset. A read-only post-stop check succeeded and showed "
        "4% account-wide window use with the same credit balance, so there is no evidence of quota exhaustion. "
        "The precise RPC stage of the live timeout was not logged. A local fixture reproduces a concrete vulnerability: "
        "`TextIOWrapper.readline()` can buffer a requested reply after a notification, while the next `select()` waits "
        "on an empty OS pipe. An explicit byte-buffer control receives both messages. This explains a possible failure "
        "mechanism; it does not prove the exact live cause.\n\n"
        "A separate pinned-upstream timer defect affected **B101 slot 3 and A303 slot 4**. `AsyncRunningJob.start_time` "
        "is the proposal start, and the local scheduler compares it against the 60-second evaluation limit. Those Codex "
        "proposals took 63.5 and 82.1 seconds; their evaluators were killed about a second after submission. No metrics "
        "or correctness file was produced. Shinka stored `correct=False, score=0.0`; **0.0 is a failure placeholder, "
        "not measured payoff**. Later interpreter-only training diagnoses gave 2.295967 and 2.117879 respectively. "
        "These diagnoses did not change selections or archive membership. Neither exceeds the seed.\n\n"
        "The stop flag halted launches, but the runner remained waiting for its separate finalization event. "
        "The supervisor sent SIGINT only to the stopped A303 child; its `finally` block saved the partial summary "
        "and the parent closed the ledger. Thus automatic launch stopping worked, while automatic cleanup needed "
        "intervention. The as-executed launcher and dependency were preserved. "
        "[Local failure reproductions](setup/failure_reproductions.json) and the [implementation audit](setup/IMPLEMENTATION.md) "
        "document these limitations. Earlier live aggregate updates overstated B101 validity; the final audited count is nine valid and one unevaluated.\n\n"
        "A202 slot 7 was a genuine interpreter rejection: **438 AST nodes exceeded 400**. Slot 9 had **394 nodes but a forbidden tuple literal**. "
        "Their original sources and −1 sentinels remain intact. No candidate was repaired.\n",
        tables,
        "The 303 row is unavailable, not zero and not a third comparison. The reported mean, median, range and sample SD "
        "use only the two completed pairs and are descriptive. B101's consumed unevaluated opportunity is an infrastructure "
        "limitation of even that partial readout. Live acceptance rates are A101 10/10, B101 9/10, B202 10/10, A202 8/10, "
        "and A303 3/4 observed proposals; B303 has no rate. Duplicates overlap those counts.\n\n"
        "Total usage was **44 external invocations, 44 completed Codex turn events and 44 native model-response usage records**. "
        "The equality is observed here, not a definition: an invocation can contain several model requests. Tokens total "
        "254,296 input including 137,216 cached, and 39,039 output including 31,394 reasoning. Codex subprocesses used "
        "1,304.1 seconds; five started Shinka runs used 1,726.0 seconds including checks, evaluation and cleanup. The "
        "$0.7300712 Headless list-price estimate is not a subscription charge. Credit balance stayed **90.6853810000**; "
        "rounded account-wide subscription use went from 3% to 4%, including concurrent supervisor use. "
        "All 44 sessions had unique native thread IDs, the requested model/effort, the expected generic base/permission "
        "instructions and exactly the recorded user prompt; no tool call was observed. "
        "[Usage evidence](usage_summary.json) preserves those separate measures.\n\n"
        "![Observed best-training trajectories](training_trajectories.svg)\n\n"
        "A303 ends after its fourth generated opportunity and B303 is absent. No unattempted trajectory is filled in.\n",
        "## A concrete search walkthrough\n\n"
        "A202 slot 2 received its slot-1 TFT parent at training 2.536238 and the original defection seed as inspiration "
        "at 2.331077. The exact prompt displayed rounded feedback 2.54 and 2.33. It produced this executable period-2 override:\n\n"
        "```python\n" + audit["runs"]["A202"]["slots"][2]["complete_source"].rstrip() + "\n```\n\n"
        "This cooperates first, defects after two repetitions of an alternating two-action pattern, and otherwise copies "
        "the opponent's last action. Its training payoff was 2.550761. Slot 3 extended the override to period 3 (2.561619); "
        "slot 4 extended it to period 4 (2.568951). Slot 5 received slot 4 as parent and slot 3 as inspiration, with "
        "displayed feedback 2.57 and 2.56. It added periods 5 and 6, reaching 2.570925. Its complete source appears below. "
        "The parent/inspiration programs and exact prompts are preserved in the [proposal catalogue](PROPOSALS.md).\n\n"
        "The observed training gain from slot 1 to slot 5 was 0.034687, entirely against fair random; the other five training "
        "opponents had unchanged payoff. This is a concrete path of accumulated code and training feedback. It does not "
        "identify the model's internal reasoning, or isolate the effect of numerical feedback from parent/inspiration context. "
        "A101 did not improve after its first proposal. B202 improved on its first opportunity's best-so-far by independently "
        "generating TFT at slot 2, without receiving prior results.\n",
        "## Selected programs, branches and scored encounters\n\n"
        "All sources below are exactly as generated. Actions and histories use C=0, D=1. Traces replay scored evaluator "
        "encounters with their original opponent, split, seed and match length; no extra encounter condition was added. "
        "Branch labels are derived from actual calls through the unchanged interpreter, and full-match payoff totals were "
        "checked against `environment.play`. Histories longer than 12 actions show their final 12 with `…`; full histories "
        "are in [the trace evidence](interpretation_traces.json).\n\n"
        "### TFT: A101 and B101, and the alternate source selected in B202\n\n"
        "A101 and B101 selected their first proposal:\n\n```python\n" + audit["runs"]["A101"]["slots"][1]["complete_source"].rstrip() + "\n```\n\n"
        "B202 selected slot 2; this same source is also A303's provisional slot-1 best:\n\n```python\n" + audit["runs"]["B202"]["slots"][2]["complete_source"].rstrip() + "\n```\n\n"
        "Both functions cooperate on empty history and then return the last opponent action: C after C, D after D. "
        "They ignore own history and all earlier opponent actions. For every legal binary history these two branches "
        "are exactly the TFT definition; this source argument establishes equivalence on that domain independently "
        "of the finite probes. The code is not evidence of knowledge-free invention.\n\n"
        "Against always-defect, training seed 11, the first eight of 174 scored rounds show the initial concession and subsequent retaliation:\n\n",
        trace_table(audit["runs"]["A101"]["selected_traces"][0]),
        "Against fair random with the same training seed, the following are the actual first eight rounds; each choice responds to the previous action, not the simultaneous current action:\n\n",
        trace_table(audit["runs"]["A101"]["selected_traces"][1]),
        "Cells below are **own payoff per round / own cooperation percentage**, pooled over the five matches per opponent. "
        "This table applies to both equivalent source forms.\n\n",
        opponent_table(audit, audit["runs"]["A101"]["slots"][1]),
        "### Period-detection defector: A202 slot 5\n\n```python\n" + audit["runs"]["A202"]["slots"][5]["complete_source"].rstrip() + "\n```\n\n"
        "It cooperates first. Thereafter it checks, in order, for two consecutive equal blocks of lengths 2, 3, 4, 5 or 6. "
        "The block must contain both actions: period 2 is explicitly alternating, and longer blocks require a defection "
        "count strictly between zero and block length. On the first matching test it defects; otherwise it copies the "
        "last opponent action. Thus it always defects after D, and defects after C only when one of these repeat tests "
        "fires. It ignores own history and uses at most the last 12 opponent actions. Detected repetition need not indicate "
        "a truly periodic opponent.\n\n"
        "The next scored training trace uses fair random, seed 11, rounds 33–40 of 174, around the first actual departure "
        "from copying the last action. The repeated pattern is accidental in this stochastic encounter:\n\n",
        trace_table(traces["A202_train_random_override"], periodic=True),
        "Against holdout alternator, seed 211, the first eight of 241 rounds show the override turning into sustained defection:\n\n",
        trace_table(traces["A202"]["alternator"], periodic=True),
        "Against holdout suspicious TFT with seed 211, the same period-2 test changes round 5 from the C that ordinary TFT "
        "would choose to D. The opponent also defects. Subsequent copying of D locks this encounter into mutual defection:\n\n",
        trace_table(traces["A202"]["suspicious_tit_for_tat"], periodic=True),
        "Payoff and cooperation against every fixed opponent, using the same reference encounters:\n\n",
        opponent_table(audit, audit["runs"]["A202"]["slots"][5]),
        "Relative to TFT, training fair-random payoff increased by **0.208122** per round; the other five opponents were unchanged. "
        "On holdout, gains against alternator (+0.485882), random-20 (+0.065882) and random-80 (+0.240000) were outweighed "
        "by the suspicious-TFT loss (−1.452941). The other two holdout payoffs were unchanged. Equal opponent weights "
        "make the net difference −0.110196. These code and trace mechanisms explain the measured transfers without "
        "claiming what the model intended.\n\n"
        "The selected period policy exceeds the seed, ordinary WSLS and TFT on training, but remains below grim's 2.655386. "
        "Its holdout 2.434118 exceeds the seed's 2.001569 but is below ordinary WSLS (2.444314), TFT (2.544314) and grim "
        "(2.649804). The selected TFT programs beat the seed and WSLS on both panels and also remain below grim. "
        "Selection therefore did not identify a universal optimum, or even the strongest fixed reference.\n",
        "## Finite recognition and its explicit counterexample\n\n"
        "The table records the frozen 1,640-probe result without retrospectively changing that recognizer. Nineteen "
        "live-valid sources pass. Seventeen directly use one of the two TFT forms above; A101 slot 7 is also equivalent "
        "on legal binary histories: if the last actions agree it returns its own action, otherwise `1-own_last` equals "
        "the opponent's last action. These eighteen have a source-based equivalence argument.\n\n"
        "**B202 slot 5 is a counterexample to treating probe agreement as proof.** It copies the last action except that "
        "it defects when history length is a positive multiple of 32. On the actual training always-cooperate encounter "
        "with seed 11, after 32 mutual cooperations it defects in round 33 while TFT would cooperate. Its training payoff "
        "is 2.052171, although all frozen probes pass. The [source](runs/B202/gen_5/main.py) and scored round-33 "
        "counterexample are retained in the trace evidence. It is called *probe-compatible*, not universally TFT-equivalent. "
        "No probe result, source recognition, reference payoff or holdout result was supplied to mutation sessions or used for selection.\n",
        "## Verification, limitations and next bounded step\n\n"
        "The original seed, interpreter, evaluator, payoff matrix, panels, seeds, termination rule and task file match "
        "the reviewed pilot commit. The five-slot pilot ledger remains byte-identical and exhausted. Before live work "
        "the localhost restriction checks and 31-test suite passed; the final suite has **36 passing tests**, including "
        "terminal-state handling and local failure reproductions. No external smoke was used. The 45th *opportunity's* "
        "metadata check failed before a proposal launch; 44 proposal invocations, one prelaunch block and 15 never-attempted "
        "opportunities account for the planned 60 slots. The ledger retains all 16 unspent external invocations and stays closed.\n\n"
        "The principal limitations are the unfinished third pair; two infrastructure losses; manual stop cleanup; "
        "only two available completed pairs; shared fixed development encounters; model prior knowledge; unequal token/runtime "
        "consumption; and a tested native tool boundary rather than an OS confidentiality container. The direct answer "
        "is **no observed Shinka advantage in this partial readout**, with insufficient evidence for a general conclusion. "
        "The training gains alone do not establish better transfer.\n\n"
        "The next bounded step is to repair the demonstrated harness defects and repeat the **same** A/B design, "
        "not add noise, horizon or opponent-mixture conditions. The remaining uncertainty is whether a completed, "
        "reliably executed three-pair comparison shows a search advantage. The hypothesis remains that A improves "
        "training-selected development-holdout payoff. The only intended change is the execution harness: buffered "
        "RPC handling, an evaluation-only clock and reliable terminal finalization. Keep model/effort, task, seed policy, "
        "local seeds, order, parser, interpreter, panels, fitness and ten opportunities per run fixed. First require "
        "zero-call failure tests and a full six-run mocked rehearsal; then a separately authorized, new ledger may "
        "allow at most **60** live invocations (three pairs × two conditions × ten), including any smoke or failed launch. "
        "Consistently positive paired differences would support benefit; flat/negative differences would weaken it; "
        "another infrastructure stop would leave it unresolved. Do not reuse E1's remaining 16 slots.\n\n"
        "**Implementation prompt for a future milestone (not executed):** “Implement E1-R with the same frozen scientific "
        "design and native subscription model. Preserve E1 and both closed ledgers. Fix explicit byte-buffer JSON-RPC "
        "reading, separate evaluation time from proposal time, and finalize stopped runners after draining work. "
        "Prove the fixes and all six runs with local mocks before any proposal call. Freeze a new protocol and separate "
        "60-invocation ledger, with ten per run and order A101, B101, B202, A202, A303, B303. Keep all information restrictions "
        "and payoff-only selection. Execute only under that new milestone's authorization.”\n\n"
        "Primary commands actually used (full setup and failed local-test history are in the linked command log):\n\n"
        "```bash\n"
        ".venv/bin/python check_e1_restrictions.py --output results/e1/setup/restriction_checks_verified.json\n"
        "timeout 180 .venv/bin/python -m unittest discover -s tests -v > results/e1/setup/tests_final.txt 2>&1\n"
        ".venv/bin/python run_e1.py --preflight > results/e1/setup/preflight.json\n"
        ".venv/bin/python run_e1.py --freeze > results/e1/setup/freeze_console.txt 2>&1\n"
        ".venv/bin/python run_e1.py --execute > results/e1/setup/live_console.txt 2>&1\n"
        "# After the terminal stop: interrupt only the stopped A303 child; no restart.\n"
        "kill -INT 1271638\n"
        ".venv/bin/python subscription_status.py --output results/e1/setup/subscription_after.json\n"
        ".venv/bin/python audit_e1.py --freeze-terminal\n"
        ".venv/bin/python audit_e1.py > results/e1/setup/audit_console.txt 2>&1\n"
        ".venv/bin/python diagnose_e1_failures.py > results/e1/setup/failure_reproductions_verified_console.txt 2>&1\n"
        "MPLCONFIGDIR=/tmp/e1_matplotlib .venv/bin/python render_e1.py\n"
        ".venv/bin/python write_e1_report.py\n"
        "timeout 180 .venv/bin/python -m unittest discover -s tests -v > results/e1/setup/tests_post_stop.txt 2>&1\n"
        "```\n\n"
        "E1 execution returned status 2 after stopping, not success. The analysis and rendering commands use only "
        "preserved data and interpreter-based diagnostics, with no proposal or judge-model calls. Files that are "
        "single-use evidence refuse overwrite; the live launcher refuses any existing ledger.\n"
    ]
    (E1 / "E1_REPORT.md").write_text("\n".join(parts))


if __name__ == "__main__":
    main()
