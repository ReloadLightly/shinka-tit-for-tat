# E3 — continuation beyond generated grim

**3/3 completed searches; 59 external proposal launches; 59 generated policies, 57 valid.** All training-selected sources were frozen before recognition and fresh transfer.

This continues the E3 experiment from an earlier LLM-generated grim policy. It tests whether native Shinka search can improve its own original-training payoff and retain that gain on fresh encounters. It does not complete the interrupted independent-generation comparisons in E1 or E1-R, demonstrate knowledge-free invention, or estimate a general advantage of evolutionary search.

## Setup and continuation amendment

The simultaneous iterated Prisoner’s Dilemma uses 0=cooperate and 1=defect, with own payoffs CC=3, CD=0, DC=5, DD=1. Both players act on pre-round histories. Independent geometric termination has probability 0.00346 after each round; no fixed endpoint, noise, extra state, opponent identity or seed is supplied to the candidate. Fitness is total own payoff / total rounds on the original 30 training matches (7,092 rounds). Selection rewards no cooperation, TFT resemblance, complexity or novelty.

Training opponents are always cooperate, always defect, fair random, TFT, grim and win-stay/lose-shift, with seeds 11,23,47,89,131 and lengths 174,747,126,25,110. The unchanged policy.py interpreter checks restricted single-function syntax (16,000 bytes, 400 AST nodes); evaluator tools never import or exec candidate source. Invalid candidates receive -1 without repair.

Three independent local contexts S101/S202/S303 use Python/NumPy seeds 101/202/303. The exact E1-R A101 generation-4 grim seed has SHA-256 fc938dea6c869791ffb3d7fbbb03f95b21ea86152fb3414345a9d107323d56a1 and original-training payoff 2.655386350817823. initial.py remains the original unconditional-defection seed.

Pinned Shinka 0.0.7 (9912af12d423504b8d580f4179fd15f5f88b8c50) supplies native weighted parent selection, accumulated programs, archive and top-k inspiration sampling. Configuration: one island, archive size 16, fitness-only archive, zero random archive inspirations and one top-k inspiration, full rewrite, one proposal attempt, no resampling, dynamic model, embedding, novelty judge, meta recommendation, prompt evolution or migration. The model is gpt-5.6-terra at low effort through Codex 0.153.4 / Headless 0.6.1 and the existing ChatGPT Pro login. Remote outputs are not deterministic from local seeds.

The [original freeze](protocol/freeze.json) at 3288b90e625daf0f02e684eb32d791c4f3f261a1 is preserved. Its S101 opportunity 1 failed in three local wrapper attempts before any external call or reservation. The [versioned amendment](continuation_v1/AMENDMENT.md) records that one consumed local_prelaunch_failure now, with provenance and timestamp, rather than pretending a historical reservation existed. The [reconciliation](continuation_v1/reconciliation.json) preserves the full terminal database, ancestry, child counts, attempt records, DB runtime fields, Python/NumPy RNG states and native counters. next_generation_to_submit remains 2. Only opportunity accounting changed from zero to one; no source-only restart or fabricated program was used.

The continuation ceiling is **59 further external launches**: S101 opportunities 2–20 (19), S202 1–20 (20), S303 1–20 (20). Thus available model opportunities are unequal. Every failed launch, invalid source and duplicate consumes its opportunity. No retries, replacements or live smoke calls are allowed. Historical plus future calls remain within the original 60-call cap. The continuation implementation, reconciliation and hashes were committed and remotely verified before its first call at **58e9733ff0a177cb48a4c7bdfacc3e11e7ee1713**.

## Actual run outcomes and trajectory

| Run | Status | Consumed opportunities | External launches | Generated / valid | AST duplicates | Best training | Final selected slot |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| S101 | completed | 20 | 19 | 19 / 18 | 14 | 2.655386 | 0 |
| S202 | completed | 20 | 20 | 20 / 19 | 11 | 2.655386 | 0 |
| S303 | completed | 20 | 20 | 20 / 20 | 12 | 2.655386 | 0 |

Duplicates are parsed-AST matches to an earlier source within the same run, including its seed. They overlap validity and consume an opportunity. The seed is included in training-only selection; exact payoff ties choose the earliest slot. Best-measured values for incomplete runs are provisional, not final selections.

The [complete opportunity catalogue](continuation_v1/PROPOSALS.md) contains every actual original generated source and its validity, payoff, duplicate status, parent/inspirations and branch explanation. The [audit](continuation_v1/audit.json) retains the complete measured trajectory. Local synthetic fixture programs under setup are excluded from scientific counts.

### S101

| Opportunity | Outcome | Training | Best so far | Parent slot / score | Inspiration slots |
| ---: | --- | ---: | ---: | --- | --- |
| 1 | local_prelaunch_failure | Unavailable | Unavailable | 0 / 2.655386 | none |
| 2 | completed | 2.654258 | 2.655386 | 0 / 2.655386 | none |
| 3 | completed | 2.536238 | 2.655386 | 0 / 2.655386 | 2 |
| 4 | completed | 2.651720 | 2.655386 | 0 / 2.655386 | 2 |
| 5 | completed | 2.653553 | 2.655386 | 2 / 2.654258 | 0 |
| 6 | completed | 2.536238 | 2.655386 | 2 / 2.654258 | 0 |
| 7 | completed | 2.655386 | 2.655386 | 2 / 2.654258 | 0 |
| 8 | completed | 2.536238 | 2.655386 | 7 / 2.655386 | 0 |
| 9 | completed | 2.536238 | 2.655386 | 0 / 2.655386 | 7 |
| 10 | completed | 2.655386 | 2.655386 | 5 / 2.653553 | 0 |
| 11 | completed | 2.536238 | 2.655386 | 10 / 2.655386 | 0 |
| 12 | completed | 2.536238 | 2.655386 | 0 / 2.655386 | 7 |
| 13 | completed | 2.536238 | 2.655386 | 4 / 2.651720 | 0 |
| 14 | completed | 2.655386 | 2.655386 | 8 / 2.536238 | 0 |
| 15 | completed | 2.536238 | 2.655386 | 14 / 2.655386 | 0 |
| 16 | completed | 2.536238 | 2.655386 | 14 / 2.655386 | 0 |
| 17 | completed | 2.536238 | 2.655386 | 7 / 2.655386 | 0 |
| 18 | completed | 2.655386 | 2.655386 | 17 / 2.536238 | 0 |
| 19 | completed | -1.000000 | 2.655386 | 18 / 2.655386 | 0 |
| 20 | completed | 2.536238 | 2.655386 | 7 / 2.655386 | 0 |

Complete training-selected original source (slot 0, SHA-256 `fc938dea6c869791ffb3d7fbbb03f95b21ea86152fb3414345a9d107323d56a1`):

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 or opponent_history.count(1) == 0 else 1
# EVOLVE-BLOCK-END
```

cooperate when `len(opponent_history) == 0 or opponent_history.count(1) == 0`, otherwise defect.

### S202

| Opportunity | Outcome | Training | Best so far | Parent slot / score | Inspiration slots |
| ---: | --- | ---: | ---: | --- | --- |
| 1 | completed | 2.330936 | 2.655386 | 0 / 2.655386 | none |
| 2 | completed | 2.536238 | 2.655386 | 0 / 2.655386 | 1 |
| 3 | completed | 2.651720 | 2.655386 | 2 / 2.536238 | 0 |
| 4 | completed | 2.655386 | 2.655386 | 3 / 2.651720 | 0 |
| 5 | completed | 2.536238 | 2.655386 | 4 / 2.655386 | 0 |
| 6 | completed | 2.640299 | 2.655386 | 4 / 2.655386 | 0 |
| 7 | completed | 2.536238 | 2.655386 | 3 / 2.651720 | 0 |
| 8 | completed | 2.536238 | 2.655386 | 4 / 2.655386 | 0 |
| 9 | completed | 2.655386 | 2.655386 | 5 / 2.536238 | 0 |
| 10 | completed | 2.655386 | 2.655386 | 3 / 2.651720 | 0 |
| 11 | completed | 2.536238 | 2.655386 | 9 / 2.655386 | 0 |
| 12 | completed | 2.651720 | 2.655386 | 6 / 2.640299 | 0 |
| 13 | completed | 2.536238 | 2.655386 | 10 / 2.655386 | 0 |
| 14 | completed | 2.536238 | 2.655386 | 12 / 2.651720 | 0 |
| 15 | completed | 2.596588 | 2.655386 | 14 / 2.536238 | 0 |
| 16 | completed | 2.536238 | 2.655386 | 9 / 2.655386 | 0 |
| 17 | completed | 2.625917 | 2.655386 | 4 / 2.655386 | 0 |
| 18 | completed | 2.336717 | 2.655386 | 0 / 2.655386 | 4 |
| 19 | completed | 2.655386 | 2.655386 | 3 / 2.651720 | 0 |
| 20 | completed | -1.000000 | 2.655386 | 9 / 2.655386 | 0 |

Complete training-selected original source (slot 0, SHA-256 `fc938dea6c869791ffb3d7fbbb03f95b21ea86152fb3414345a9d107323d56a1`):

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 or opponent_history.count(1) == 0 else 1
# EVOLVE-BLOCK-END
```

cooperate when `len(opponent_history) == 0 or opponent_history.count(1) == 0`, otherwise defect.

### S303

| Opportunity | Outcome | Training | Best so far | Parent slot / score | Inspiration slots |
| ---: | --- | ---: | ---: | --- | --- |
| 1 | completed | 2.536238 | 2.655386 | 0 / 2.655386 | none |
| 2 | completed | 2.474055 | 2.655386 | 0 / 2.655386 | 1 |
| 3 | completed | 2.655386 | 2.655386 | 1 / 2.536238 | 0 |
| 4 | completed | 2.084743 | 2.655386 | 0 / 2.655386 | 3 |
| 5 | completed | 2.655386 | 2.655386 | 1 / 2.536238 | 0 |
| 6 | completed | 2.536238 | 2.655386 | 5 / 2.655386 | 0 |
| 7 | completed | 2.536238 | 2.655386 | 0 / 2.655386 | 3 |
| 8 | completed | 2.655386 | 2.655386 | 6 / 2.536238 | 0 |
| 9 | completed | 2.067541 | 2.655386 | 0 / 2.655386 | 3 |
| 10 | completed | 2.655386 | 2.655386 | 8 / 2.655386 | 0 |
| 11 | completed | 2.655386 | 2.655386 | 2 / 2.474055 | 0 |
| 12 | completed | 2.536238 | 2.655386 | 0 / 2.655386 | 3 |
| 13 | completed | 2.474055 | 2.655386 | 12 / 2.536238 | 0 |
| 14 | completed | 2.536238 | 2.655386 | 11 / 2.655386 | 0 |
| 15 | completed | 2.655386 | 2.655386 | 7 / 2.536238 | 0 |
| 16 | completed | 2.655386 | 2.655386 | 6 / 2.536238 | 0 |
| 17 | completed | 2.084743 | 2.655386 | 10 / 2.655386 | 0 |
| 18 | completed | 2.536238 | 2.655386 | 3 / 2.655386 | 0 |
| 19 | completed | 2.536238 | 2.655386 | 10 / 2.655386 | 0 |
| 20 | completed | 2.536238 | 2.655386 | 8 / 2.655386 | 0 |

Complete training-selected original source (slot 0, SHA-256 `fc938dea6c869791ffb3d7fbbb03f95b21ea86152fb3414345a9d107323d56a1`):

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 or opponent_history.count(1) == 0 else 1
# EVOLVE-BLOCK-END
```

cooperate when `len(opponent_history) == 0 or opponent_history.count(1) == 0`, otherwise defect.

## What the generated policies do

The 59 generated sources contain **20 parsed ASTs, 18 valid**. Within-run AST
duplicates, including comparison to each seed, total 37 (S101 14, S202 11,
S303 12); global AST deduplication is a different count (39 repeated occurrences).
All generated candidates received an evaluation. There are 62 native program
rows including the three seeds, and 48 final archive members (16 per run).

**27 generated occurrences implement familiar TFT**, in three source forms.
The direct `opponent_history[-1]` form and its equivalent Boolean conditional
cooperate initially and copy the opponent thereafter. S303/18 has a redundant
own-history expression: if the previous actions agree, returning own equals
returning opponent; if they differ, `1-own` equals opponent for binary actions.
All 27 pass the frozen 1,640 probes. These source arguments establish TFT for
these particular programs on equal-length binary histories, independently of
finite-probe agreement. **15 occurrences implement familiar grim**, in two source
forms. The seed and both generated grim forms cooperate precisely while the
opponent's defection count is zero; that count cannot decrease, so retaliation
is permanent. These are recovered implementations of known strategies, not
novel discoveries.

The table groups every remaining source by its actual decision rule. Full code,
all duplicate origins and per-opportunity branch expressions are in the complete
source catalogue. C means cooperation and D defection; round numbers start at 1.

| Source occurrence(s) | Actual behavior | Original training |
| --- | --- | ---: |
| S101/2 | Grim with an exception: cooperate when there have been exactly two opponent defections and the last opponent action was C. At three total defections, retaliation is permanent. | 2.654258 |
| S101/4; S202/3,12 | Cooperate until the opponent's second **total** defection, then defect forever. This differs from counting consecutive defections. | 2.651720 |
| S101/5 | Grim with an exception after exactly one opponent defection when its latest action is C; a second total defection removes forgiveness. | 2.653553 |
| S202/1 | Open C,D. Thereafter, only opponents whose first two actions were C,C can receive cooperation, and only while their total defection count is exactly one. All other cases defect. | 2.330936 |
| S202/6 | Grim, but cooperate whenever history length modulo 50 is 0 or 1: rounds 1–2, 51–52, 101–102, etc. | 2.640299 |
| S202/15 | Grim, with cooperation restored whenever the opponent's last two actions were both C. | 2.596588 |
| S202/17 | Grim, with cooperation restored whenever the opponent's last three actions were all C. | 2.625917 |
| S202/18 | Cooperate only through round 6 while the opponent has never defected; defect from round 7 onward, or earlier after any defection. | 2.336717 |
| S303/2,13 | Familiar tit-for-two-tats: cooperate initially; defect exactly after two consecutive opponent defections. | 2.474055 |
| S303/4 | From its own reachable histories, cooperate through round 8, then defect against a never-defecting opponent; once the opponent defects, cooperate permanently. Its redundant own-action branch differs on some unreachable input histories. | 2.084743 |
| S303/9 | Open C; normally copy the opponent. Override with D after an entirely cooperative history of length divisible by 83; override with C after mutual D. This is a periodic-defection/forgiveness hybrid, not exact TFT. | 2.067541 |
| S303/17 | Cooperate through round 8; thereafter defect only if the opponent has never defected. Cooperate permanently after its first defection. Same reachable behavior as S303/4 by the preceding branch argument, despite a different AST. | 2.084743 |
| S101/19 | Rejected: a tuple literal `(1, 1, 1)` in a history comparison is outside the interpreter grammar. 62 AST nodes, below the size limit; no repaired version was evaluated. | −1 (invalid) |
| S202/20 | Rejected: a tuple literal `(0, 0, 0)` is outside the interpreter grammar. 53 AST nodes, below the size limit; no repaired version was evaluated. | −1 (invalid) |

The ten other valid variant occurrences combine delayed retaliation, limited
forgiveness or history-length triggers. Changed code and behavior are established;
worldwide novelty is not. Their measured training scores all fall below grim.
Only the three selected sources and fixed references received fresh transfer:
there is no fresh-development claim for an unselected variant.

## Actual evolutionary changes and stagnation

The incumbent trajectory is flat in all three runs: 2.655386350817823 from seed
to completion. Native parent selection still explored lower-scoring programs.
For example, S202/2 (TFT, 2.536238) → S202/3 (second-total-defection trigger,
2.651720) → S202/4 (grim, 2.655386) improves the sampled parent's score twice.
However, the exact grim seed was supplied as top-k inspiration in both steps.
This is recovery of an already available incumbent, not a new best or new
strategy. Likewise S101/7 returns from S101/2's limited-forgiveness variant to
the original grim source, with seed slot 0 supplied as inspiration. The full
parent/inspiration record supports these concrete relationships; no hidden
model reasoning is inferred.

The closest new variant was S101/2, **−0.001128** below the seed on original
training. The 27 TFT occurrences scored 2.536238, **−0.119148** below the seed.
Selection retained slot 0 in every run under the frozen earliest-tie rule.
The result is **no training improvement**, followed by zero selected-minus-seed
transfer differences. It does not establish global optimality of grim, prove
that a larger or differently configured search cannot improve it, or show that
all unselected variants would transfer poorly.

Three exploratory searches with 19/20/20 available model opportunities cannot
repair the unfinished independent-generation comparison. Public development
opponent types, fixed training samples, deterministic noiseless play, restricted
program syntax, small budgets and the LLM's prior knowledge limit the claim.
Native retrieval restrictions isolate the supplied mutation information; they
are not an OS confidentiality container or a knowledge-free starting point.

## Fresh transfer and interpretation

All five policies (three frozen selections, seed/grim and reference TFT) received the same 600 matches per panel: training types × seeds 300001–300100 and development types × seeds 400001–400100. All 6,000 matches use the original horizon and SHA-256 match RNG derivation. Development types are alternator, suspicious TFT, TFT for two consecutive defections, hard TFT, random p(C)=0.2 and random p(C)=0.8. These public types are a development holdout, not an untouched confirmatory opponent population. Panels are scored separately; there is no post-transfer reselection.

| Policy | Fresh training | Fresh development | Training minus seed | Development minus seed |
| --- | ---: | ---: | ---: | ---: |
| S101 | 2.665880 | 2.663790 | 0.000000 | 0.000000 |
| S202 | 2.665880 | 2.663790 | 0.000000 | 0.000000 |
| S303 | 2.665880 | 2.663790 | 0.000000 | 0.000000 |
| seed | 2.665880 | 2.663790 | 0.000000 | 0.000000 |
| TFT | 2.541541 | 2.551387 | -0.124339 | -0.112403 |

Per-opponent results are retained in [transfer/summary.json](continuation_v1/transfer/summary.json), and every scored match in the adjacent JSONL files. [Verified traces](continuation_v1/traces.json) show actual actions and payoffs from selected scored encounters. Recognition is reported only after the gate: passing 1,640 TFT probes is finite-probe compatibility, not universal equivalence.

### Per-opponent fresh results

All selected sources are byte-identical to seed/grim, so their opponent-specific results equal its results. Each cell aggregates 100 fresh matches.

| Panel / opponent | Seed / all selections | TFT | Grim minus TFT |
| --- | ---: | ---: | ---: |
| train / always_cooperate | 3.000000 | 3.000000 | 0.000000 |
| train / always_defect | 0.996579 | 0.996579 | 0.000000 |
| train / grim | 3.000000 | 3.000000 | 0.000000 |
| train / random | 2.998700 | 2.252668 | 0.746032 |
| train / tit_for_tat | 3.000000 | 3.000000 | 0.000000 |
| train / win_stay_lose_shift | 3.000000 | 3.000000 | 0.000000 |
| holdout / alternator | 2.993834 | 2.498157 | 0.495677 |
| holdout / hard_tit_for_tat | 3.000000 | 3.000000 | 0.000000 |
| holdout / random_20 | 1.790832 | 1.553549 | 0.237283 |
| holdout / random_80 | 4.188024 | 2.761477 | 1.426546 |
| holdout / suspicious_tit_for_tat | 1.010053 | 2.495141 | -1.485088 |
| holdout / tit_for_two_tats | 3.000000 | 3.000000 | 0.000000 |

### Replayed scored encounters

These are the first 16 actual rounds; payoffs and match length are full-encounter totals. C=0 and D=1. Full pre-action histories and per-round payoffs are retained in traces.json. All six traces reproduce their existing scored records exactly.

| Policy / encounter | Own first 16 | Opponent first 16 | Full own payoff / rounds |
| --- | --- | --- | ---: |
| S101 / train/random/300001 | `CDDDDDDDDDDDDDDD` | `DCCCDDCDCDCDCCDD` | 2467 / 824 |
| S101 / holdout/suspicious_tit_for_tat/400001 | `CDDDDDDDDDDDDDDD` | `DCDDDDDDDDDDDDDD` | 40 / 37 |
| seed / train/random/300001 | `CDDDDDDDDDDDDDDD` | `DCCCDDCDCDCDCCDD` | 2467 / 824 |
| seed / holdout/suspicious_tit_for_tat/400001 | `CDDDDDDDDDDDDDDD` | `DCDDDDDDDDDDDDDD` | 40 / 37 |
| TFT / train/random/300001 | `CDCCCDDCDCDCDCCD` | `DCCCDDCDCDCDCCDD` | 1862 / 824 |
| TFT / holdout/suspicious_tit_for_tat/400001 | `CDCDCDCDCDCDCDCD` | `DCDCDCDCDCDCDCDC` | 90 / 37 |

Grim retaliates permanently after the first random defection, while TFT continues responding to the latest action. Against suspicious TFT, grim settles into mutual defection after the opening; TFT alternates C/D out of phase. These traces explain encounter-specific behavior, not a universal ranking.

## Usage, failures and verification

External launches: 59; completed Codex turn events: 59; available native model-response usage records: 59. Native response tokens: `{"cache_write_input_tokens": 0, "cached_input_tokens": 233472, "input_tokens": 341644, "output_tokens": 42734, "reasoning_output_tokens": 35352, "total_tokens": 384378}`. Cached input and reasoning output are subsets. Codex runtime: 1016.854 seconds. Native sessions are fresh, and their user messages/base instructions/permissions were checked against recorded prompts and the localhost restriction fixture. No tool call was observed.

| Run | Cumulative outer runtime (s) |
| --- | ---: |
| S101 | 576.982 |
| S202 | 522.942 |
| S303 | 501.455 |

Total cumulative outer search runtime: 1601.378 seconds. Headless API-list-price estimate: $0.7758464, not a subscription charge. Read-only account usage changed from 13% to 15%; credit balance remained 90.6853810000. The transfer ledger records 51.635 seconds for the 6,000 matches. These are the preserved runtime-clock measurements.

S101 cumulative runtime includes the original 67.56626177899307-second segment. Codex/Headless/native provider/evaluator limits remain 180/210/240/60 seconds, native drain 350 seconds, cumulative outer bound 9,000 seconds per run. At most two specifically classified send failures permit a full-state recovery and one reserved read-only availability check each. Ambiguous transport, quota/auth, configuration and integrity failures pause. No consumed opportunity is repeated.

Automatic recovery checks used: 0/2. Terminal stop reason: `None`; failure class: `None`. Full failure output, call records, runtime segments and checkpoint snapshots are preserved under [continuation_v1](continuation_v1). Absent model-response usage does not establish whether a failed request was processed remotely.

The continuation passed 12 focused E3 checks, 16 repaired timing-fixture checks, the full 75-test unittest suite, both zero-call preflights, and six localhost forced retrieval refusals. The native Shinka → Headless → wrapper → final executable rehearsal exercised real temporary mutation cwd and actual Git/freeze/import checks, reproduced one prelaunch failure with exactly one local attempt, then restored its full checkpoint and successfully evaluated the next opportunity. Only the final external executable was synthetic. Original failed test logs and initial rehearsal evidence remain available; no production deadline was relaxed.

Final verification independently checked all three terminal database/checkpoint digests, exact training-only selections, 6,000 manifest-matched scored rows and six full scored-trace replays. A post-search trace command initially used the nonexistent identifier suspicious_tft; it was corrected to the frozen suspicious_tit_for_tat identifier. The lookup error and dependent missing-trace verification failure are preserved under setup, and no match or source changed.

The supervisor’s actual process command confirmed approval_policy="never". Mutation sessions retained read-only sandbox and approval never with explicit retrieval restrictions. No paid API, API-key fallback, purchased credits, auxiliary model or GitHub Actions was used. Headless API-list-price estimates are not subscription charges; exact usage is in [usage_summary.json](continuation_v1/usage_summary.json).

## Commands and bounded follow-up

Exact preparation, freeze, launch and gated evaluation commands are in [continuation_v1/COMMANDS.md](continuation_v1/COMMANDS.md). The authorized launch was `PATH="$PWD/.venv/bin:$PATH" .venv/bin/python run_e3.py --resume`. Defaults remain zero-call and stopped/closed ledgers refuse automatic restart. Read-only verification and scored-trace replay: `.venv/bin/python verify_e3.py`; audit regeneration: `.venv/bin/python audit_e3.py`; report replay: `.venv/bin/python write_e3_report.py`. Trace replay uses `.venv/bin/python analyze_e3.py --trace S101 --split train --opponent random --seed 300001 --rounds 16` when the gated transfer exists.

One bounded evidence-motivated follow-up is recorded in [FOLLOWUP.md](continuation_v1/FOLLOWUP.md). It is proposed only and has not been executed.
