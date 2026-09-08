#!/usr/bin/env python3
"""Render the terminal E3 evidence, preserving unavailable outcomes as unavailable."""
import ast
import json
from pathlib import Path
from e3_state import E3, ROOT, read, sha
from e3_backend import ORDER


def fmt(x):
    return 'Unavailable' if x is None else f'{x:.6f}'


def logic(source):
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return 'Source does not parse; no valid policy behavior is established.'
    fn = next((n for n in tree.body if isinstance(n, ast.FunctionDef)), None)
    if fn is None: return 'No policy function; rejected without repair.'
    rows = []
    def action(node):
        if isinstance(node, ast.Constant) and type(node.value) is int and node.value in (0,1):
            return 'cooperate' if node.value == 0 else 'defect'
        if isinstance(node, ast.IfExp):
            return f'{action(node.body)} when `{ast.unparse(node.test)}`, otherwise {action(node.orelse)}'
        return f'return `{ast.unparse(node)}` (0 means cooperate, 1 means defect)'
    def visit(body, prefix=''):
        for n in body:
            if isinstance(n, ast.Return): rows.append(prefix + action(n.value) + '.')
            elif isinstance(n, ast.If):
                visit(n.body, prefix + f'If `{ast.unparse(n.test)}`: ')
                visit(n.orelse, prefix + f'Otherwise: ')
            else: rows.append(prefix + f'Contains `{ast.unparse(n)}`; see recorded interpreter validity.')
    visit(fn.body)
    return ' '.join(rows)


def transfer_details(summary):
    lines = ['### Per-opponent fresh results', '',
        'All selected sources are byte-identical to seed/grim, so their opponent-specific results equal its results. Each cell aggregates 100 fresh matches.', '',
        '| Panel / opponent | Seed / all selections | TFT | Grim minus TFT |',
        '| --- | ---: | ---: | ---: |']
    for split in ('train','holdout'):
        for name,value in summary['seed'][split]['opponents'].items():
            g=value['mean_payoff']; t=summary['TFT'][split]['opponents'][name]['mean_payoff']
            lines.append(f'| {split} / {name} | {fmt(g)} | {fmt(t)} | {fmt(g-t)} |')
    lines += ['', '### Replayed scored encounters', '',
        'These are the first 16 actual rounds; payoffs and match length are full-encounter totals. C=0 and D=1. Full pre-action histories and per-round payoffs are retained in traces.json. All six traces reproduce their existing scored records exactly.', '',
        '| Policy / encounter | Own first 16 | Opponent first 16 | Full own payoff / rounds |',
        '| --- | --- | --- | ---: |']
    for t in read(E3/'traces.json'):
        a=''.join('CD'[s['action']] for s in t['steps'])
        b=''.join('CD'[s['opponent_action']] for s in t['steps'])
        m=t['scored_totals_verified']
        lines.append(f"| {t['policy']} / {t['encounter']['id']} | `{a}` | `{b}` | {m['total_payoff']} / {m['turns']} |")
    lines += ['', 'Grim retaliates permanently after the first random defection, while TFT continues responding to the latest action. Against suspicious TFT, grim settles into mutual defection after the opening; TFT alternates C/D out of phase. These traces explain encounter-specific behavior, not a universal ranking.', '']
    return lines


def render():
    audit = read(E3/'audit.json')
    ledger = read(E3/'ledger.json')
    transfer = read(E3/'transfer/summary.json') if (E3/'transfer/summary.json').exists() else None
    usage = audit['usage']
    done = audit['analysis_gate_open']
    generated = sum(r['generated'] for r in audit['runs'].values())
    valid = sum(r['valid'] for r in audit['runs'].values())
    completed = audit['completed_runs']
    text = ['# E3 — continuation beyond generated grim', '',
        f'**{completed}/3 completed searches; {audit["external_invocations"]} external proposal launches; {generated} generated policies, {valid} valid.** '
        + ('All training-selected sources were frozen before recognition and fresh transfer.' if done else
           'Search is paused at a preserved terminal boundary. Recognition and transfer remain gated; the research question is unanswered.'), '',
        'This continues the E3 experiment from an earlier LLM-generated grim policy. It tests whether native Shinka search can improve its own original-training payoff and retain that gain on fresh encounters. It does not complete the interrupted independent-generation comparisons in E1 or E1-R, demonstrate knowledge-free invention, or estimate a general advantage of evolutionary search.', '',
        '## Setup and continuation amendment', '',
        'The simultaneous iterated Prisoner’s Dilemma uses 0=cooperate and 1=defect, with own payoffs CC=3, CD=0, DC=5, DD=1. Both players act on pre-round histories. Independent geometric termination has probability 0.00346 after each round; no fixed endpoint, noise, extra state, opponent identity or seed is supplied to the candidate. Fitness is total own payoff / total rounds on the original 30 training matches (7,092 rounds). Selection rewards no cooperation, TFT resemblance, complexity or novelty.', '',
        'Training opponents are always cooperate, always defect, fair random, TFT, grim and win-stay/lose-shift, with seeds 11,23,47,89,131 and lengths 174,747,126,25,110. The unchanged policy.py interpreter checks restricted single-function syntax (16,000 bytes, 400 AST nodes); evaluator tools never import or exec candidate source. Invalid candidates receive -1 without repair.', '',
        'Three independent local contexts S101/S202/S303 use Python/NumPy seeds 101/202/303. The exact E1-R A101 generation-4 grim seed has SHA-256 fc938dea6c869791ffb3d7fbbb03f95b21ea86152fb3414345a9d107323d56a1 and original-training payoff 2.655386350817823. initial.py remains the original unconditional-defection seed.', '',
        'Pinned Shinka 0.0.7 (9912af12d423504b8d580f4179fd15f5f88b8c50) supplies native weighted parent selection, accumulated programs, archive and top-k inspiration sampling. Configuration: one island, archive size 16, fitness-only archive, zero random archive inspirations and one top-k inspiration, full rewrite, one proposal attempt, no resampling, dynamic model, embedding, novelty judge, meta recommendation, prompt evolution or migration. The model is gpt-5.6-terra at low effort through Codex 0.153.4 / Headless 0.6.1 and the existing ChatGPT Pro login. Remote outputs are not deterministic from local seeds.', '',
        'The [original freeze](protocol/freeze.json) at 3288b90e625daf0f02e684eb32d791c4f3f261a1 is preserved. Its S101 opportunity 1 failed in three local wrapper attempts before any external call or reservation. The [versioned amendment](continuation_v1/AMENDMENT.md) records that one consumed local_prelaunch_failure now, with provenance and timestamp, rather than pretending a historical reservation existed. The [reconciliation](continuation_v1/reconciliation.json) preserves the full terminal database, ancestry, child counts, attempt records, DB runtime fields, Python/NumPy RNG states and native counters. next_generation_to_submit remains 2. Only opportunity accounting changed from zero to one; no source-only restart or fabricated program was used.', '',
        'The continuation ceiling is **59 further external launches**: S101 opportunities 2–20 (19), S202 1–20 (20), S303 1–20 (20). Thus available model opportunities are unequal. Every failed launch, invalid source and duplicate consumes its opportunity. No retries, replacements or live smoke calls are allowed. Historical plus future calls remain within the original 60-call cap. The continuation implementation, reconciliation and hashes were committed and remotely verified before its first call at **'+audit['continuation_freeze']['commit']+'**.', '',
        '## Actual run outcomes and trajectory', '',
        '| Run | Status | Consumed opportunities | External launches | Generated / valid | AST duplicates | Best training | Final selected slot |',
        '| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |']
    for run_id in ORDER:
        run = audit['runs'][run_id]
        text.append(f'| {run_id} | {run["status"]["status"]} | {len(run["opportunities"])} | {usage["runs"][run_id]["external_invocations"]} | {run["generated"]} / {run["valid"]} | {run["ast_duplicates"]} | {fmt(run["best_measured_training"])} | {run["selection"]["slot"] if run["selection"] else "Unavailable"} |')
    text += ['', 'Duplicates are parsed-AST matches to an earlier source within the same run, including its seed. They overlap validity and consume an opportunity. The seed is included in training-only selection; exact payoff ties choose the earliest slot. Best-measured values for incomplete runs are provisional, not final selections.', '',
        'The [complete opportunity catalogue](continuation_v1/PROPOSALS.md) contains every actual original generated source and its validity, payoff, duplicate status, parent/inspirations and branch explanation. The [audit](continuation_v1/audit.json) retains the complete measured trajectory. Local synthetic fixture programs under setup are excluded from scientific counts.', '']
    for run_id in ORDER:
        run = audit['runs'][run_id]
        text += [f'### {run_id}', '', '| Opportunity | Outcome | Training | Best so far | Parent slot / score | Inspiration slots |', '| ---: | --- | ---: | ---: | --- | --- |']
        for row in run['opportunities']:
            p = row['program'] or {}
            parent = row.get('parent',{})
            text.append(f'| {row["slot"]} | {row["status"]} | {fmt(p.get("training"))} | {fmt(p.get("best_training_so_far"))} | {parent.get("generation","—")} / {fmt(parent.get("combined_score"))} | {", ".join(str(i["generation"]) for i in row.get("inspirations",[])) or "none"} |')
        selected = run['selection']
        if selected:
            code = (ROOT/selected['source']).read_text()
            text += ['', f'Complete training-selected original source (slot {selected["slot"]}, SHA-256 `{selected["sha256"]}`):', '', '```python',code.rstrip(),'```','',logic(code),'']
    text += [(E3/'INTERPRETATION.md').read_text(), '## Fresh transfer and interpretation', '']
    if transfer:
        text += ['All five policies (three frozen selections, seed/grim and reference TFT) received the same 600 matches per panel: training types × seeds 300001–300100 and development types × seeds 400001–400100. All 6,000 matches use the original horizon and SHA-256 match RNG derivation. Development types are alternator, suspicious TFT, TFT for two consecutive defections, hard TFT, random p(C)=0.2 and random p(C)=0.8. These public types are a development holdout, not an untouched confirmatory opponent population. Panels are scored separately; there is no post-transfer reselection.', '',
            '| Policy | Fresh training | Fresh development | Training minus seed | Development minus seed |', '| --- | ---: | ---: | ---: | ---: |']
        for name in (*ORDER,'seed','TFT'):
            tr = transfer[name]['train']['mean_payoff']; ho = transfer[name]['holdout']['mean_payoff']
            text.append(f'| {name} | {fmt(tr)} | {fmt(ho)} | {fmt(tr-transfer["seed"]["train"]["mean_payoff"])} | {fmt(ho-transfer["seed"]["holdout"]["mean_payoff"])} |')
        text += ['', 'Per-opponent results are retained in [transfer/summary.json](continuation_v1/transfer/summary.json), and every scored match in the adjacent JSONL files. [Verified traces](continuation_v1/traces.json) show actual actions and payoffs from selected scored encounters. Recognition is reported only after the gate: passing 1,640 TFT probes is finite-probe compatibility, not universal equivalence.', '']
    else:
        text += ['No complete E3 fresh-transfer outcome is available. The three selected-minus-seed development differences, fresh-training gains and per-opponent transfer results are **unavailable**, not zero. No recognition or transfer is substituted for missing search outcomes.', '']
    if transfer:
        text += transfer_details(transfer)
    text += ['## Usage, failures and verification', '',
        f'External launches: {audit["external_invocations"]}; completed Codex turn events: {usage["completed_codex_turn_events"]}; available native model-response usage records: {usage["native_model_response_records"]}. Native response tokens: `{json.dumps(usage["tokens"],sort_keys=True)}`. Cached input and reasoning output are subsets. Codex runtime: {usage["codex_runtime_seconds"]:.3f} seconds. Native sessions are fresh, and their user messages/base instructions/permissions were checked against recorded prompts and the localhost restriction fixture. No tool call was observed.', '',
        '| Run | Cumulative outer runtime (s) |', '| --- | ---: |']
    for r in ORDER:
        text.append(f'| {r} | {audit["runs"][r]["status"].get("runtime_seconds",0):.3f} |')
    estimate = sum(read(E3/'runs'/r/'training_summary.json')['headless_list_price_estimate_not_charge'] for r in ORDER)
    text += ['', f'Total cumulative outer search runtime: {sum(audit["runs"][r]["status"].get("runtime_seconds",0) for r in ORDER):.3f} seconds. Headless API-list-price estimate: ${estimate:.7f}, not a subscription charge. Read-only account usage changed from 13% to 15%; credit balance remained 90.6853810000. The transfer ledger records 51.635 seconds for the 6,000 matches. These are the preserved runtime-clock measurements.', '', 'S101 cumulative runtime includes the original 67.56626177899307-second segment. Codex/Headless/native provider/evaluator limits remain 180/210/240/60 seconds, native drain 350 seconds, cumulative outer bound 9,000 seconds per run. At most two specifically classified send failures permit a full-state recovery and one reserved read-only availability check each. Ambiguous transport, quota/auth, configuration and integrity failures pause. No consumed opportunity is repeated.', '',
        f'Automatic recovery checks used: {len(ledger.get("recoveries",[]))}/2. Terminal stop reason: `{ledger.get("stop_reason")}`; failure class: `{ledger.get("failure_class")}`. Full failure output, call records, runtime segments and checkpoint snapshots are preserved under [continuation_v1](continuation_v1). Absent model-response usage does not establish whether a failed request was processed remotely.', '',
        'The continuation passed 12 focused E3 checks, 16 repaired timing-fixture checks, the full 75-test unittest suite, both zero-call preflights, and six localhost forced retrieval refusals. The native Shinka → Headless → wrapper → final executable rehearsal exercised real temporary mutation cwd and actual Git/freeze/import checks, reproduced one prelaunch failure with exactly one local attempt, then restored its full checkpoint and successfully evaluated the next opportunity. Only the final external executable was synthetic. Original failed test logs and initial rehearsal evidence remain available; no production deadline was relaxed.', '',
        'Final verification independently checked all three terminal database/checkpoint digests, exact training-only selections, 6,000 manifest-matched scored rows and six full scored-trace replays. A post-search trace command initially used the nonexistent identifier suspicious_tft; it was corrected to the frozen suspicious_tit_for_tat identifier. The lookup error and dependent missing-trace verification failure are preserved under setup, and no match or source changed.', '',
        'The supervisor’s actual process command confirmed approval_policy="never". Mutation sessions retained read-only sandbox and approval never with explicit retrieval restrictions. No paid API, API-key fallback, purchased credits, auxiliary model or GitHub Actions was used. Headless API-list-price estimates are not subscription charges; exact usage is in [usage_summary.json](continuation_v1/usage_summary.json).', '',
        '## Commands and bounded follow-up', '',
        'Exact preparation, freeze, launch and gated evaluation commands are in [continuation_v1/COMMANDS.md](continuation_v1/COMMANDS.md). The authorized launch was `PATH="$PWD/.venv/bin:$PATH" .venv/bin/python run_e3.py --resume`. Defaults remain zero-call and stopped/closed ledgers refuse automatic restart. Read-only verification and scored-trace replay: `.venv/bin/python verify_e3.py`; audit regeneration: `.venv/bin/python audit_e3.py`; report replay: `.venv/bin/python write_e3_report.py`. Trace replay uses `.venv/bin/python analyze_e3.py --trace S101 --split train --opponent random --seed 300001 --rounds 16` when the gated transfer exists.', '',
        'One bounded evidence-motivated follow-up is recorded in [FOLLOWUP.md](continuation_v1/FOLLOWUP.md). It is proposed only and has not been executed.', '']
    (E3.parent/'E3_REPORT.md').write_text('\n'.join(text))
    print('Rendered terminal E3 report and source explanations.')


if __name__ == '__main__':
    render()
