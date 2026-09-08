# Project status — 2026-09-08

## E1-R protocol frozen; execution next

The new [E1-R protocol](results/e1_r/protocol/PROTOCOL.md) repeats the same six-run comparison under a separate 60-invocation allowance. Metadata buffering, evaluation-only timing and terminal finalization have been repaired using versioned per-run adapters; installed Shinka and the fixed evaluator remain unchanged. The initial prompt is byte-identical to E1's. Model gpt-5.6-terra / low and ChatGPT Pro access were verified; six forced localhost checks re-established retrieval restrictions.

The final suite passed 52 tests. The complete [release rehearsal](results/e1_r/setup/rehearsal_release/summary.json) and all metadata/backend/quota stopped paths passed with zero external proposals and no manual interruption. The old native finalization hang was reproduced separately. E1-R has zero external proposals at protocol freeze; the authorized next action is its one serial execution. [Implementation](results/e1_r/setup/IMPLEMENTATION.md) and [commands](results/e1_r/setup/COMMANDS.md) retain local failure history. Prior E1 and pilot ledgers remain closed and unchanged.

## E1 stopped; the planned experiment remains incomplete

The principal deliverable is [E1_REPORT.md](results/e1/E1_REPORT.md): a self-contained account of the design, every run, selected sources, branches, scored traces, opponent breakdowns, failures, usage, commands and next step.

The protocol and executable controls were frozen at `e0ca3f3` before calls. E1 planned A101, B101, B202, A202, A303, B303, ten opportunities each. A used the real Shinka search loop. B used the same native backend/parser/evaluator with fresh sessions and byte-identical initial task/seed/feedback. Model: `gpt-5.6-terra`, low reasoning, native Headless 0.6.1 / Codex 0.153.4, existing ChatGPT Pro login. No substitution occurred.

Four runs completed. A303 generated four proposals, then its slot-5 subscription metadata check timed out before another proposal launch. B303 never started. The E1 ledger is **closed at 44/60**, preserving all counters and 16 unspent invocations. No retry, replacement, resampling or reset occurred.

| Run | Training-selected slot | Training | Development holdout |
|---|---:|---:|---:|
| A101 | 1 | 2.536238 | 2.544314 |
| B101 | 1 | 2.536238 | 2.544314 |
| B202 | 2 | 2.536238 | 2.544314 |
| A202 | 5 | 2.570925 | 2.434118 |
| A303, incomplete | 1, provisional | 2.536238 | Unavailable |
| B303, unstarted | None | Unavailable | Unavailable |

All terminal selection identities/statuses were frozen before holdout or recognition. B303's seed entry is a placeholder, not a run result. Neither unfinished entry contributes a primary outcome. Earliest appearance breaks exact ties, independently of Shinka's later tied best pointer. Paired A-minus-B differences are 0.000000, −0.110196 and unavailable; the two available pairs have descriptive mean −0.055098 and sample SD 0.077920. This partial readout shows no observed search advantage and does not complete the three-pair experiment or establish a general effect.

## Scientific and operational findings

All 44 generated sources have Shinka database rows: **40 live-valid/archived, two interpreter rejections and two without evaluator results**. A202 slot 7 exceeded the 400-node limit (438); slot 9 contained a forbidden tuple (394 nodes). Neither was repaired. B101 slot 3 and A303 slot 4 were killed because the pinned scheduler included proposal time in its evaluation timeout. Their database score 0 is a failure placeholder, not measured payoff. Post-stop training diagnoses (2.295967 and 2.117879) did not alter selection or archives.

A202 extended TFT with defection after apparent repeating mixed-action blocks of lengths 2–6. Its training gain arose entirely against fair random. On holdout, sustained mutual defection against suspicious TFT outweighed gains elsewhere. It remains below reference grim on training and below TFT, grim and ordinary WSLS on holdout.

Nineteen live-valid proposals passed the frozen TFT probes. Eighteen have simple source arguments establishing TFT on legal binary histories. B202 slot 5 is not equivalent: its defection every 32 rounds is missed by the finite probes; a scored round-33 counterexample is preserved. Recognition never supplied fitness.

Forced localhost checks established native tool restrictions before calls: file/search/MCP/plugin/agent retrieval disabled, with inert code-mode entrypoints failing closed. No tool call was observed in 44 fresh sessions; actual base/permission/user contexts matched the audited information. This is a tested native tool boundary, not an OS confidentiality container or knowledge-free invention.

The stop latch blocked further launches, but cleanup waited on a separate finalization event. A targeted SIGINT to the stopped A303 child let its finally block save the partial summary and the parent close the ledger. Local fixtures reproduce the timer defect and an RPC buffering vulnerability. The exact live cause of the metadata timeout is not proven; a post-stop read-only check succeeded with no evidence of quota exhaustion. The as-executed code is preserved; these defects must be fixed before another run.

## Usage, checks and evidence

There were 44 external proposal invocations, 44 completed Codex turn events and 44 native model-response usage records; their equality here does not make them equivalent units. Input: 254,296 tokens, including 137,216 cached. Output: 39,039, including 31,394 reasoning. Codex runtime: 1,304.1 seconds; five started Shinka runs: 1,726.0 seconds including checks/evaluation/cleanup. Credit balance stayed 90.6853810000; account-wide rounded use moved 3%→4%, also including supervisor use. The $0.7300712 list-price estimate is not a subscription charge.

No paid API calls, API-key authentication, API fallback, purchased-credit continuation, auxiliary models, embeddings or GitHub Actions were used. Default launchers remain zero-call. The pre-call suite passed 31 tests; the final suite passed 36. Prompts, sources, native contexts, scores, failures, archives, configuration and usage are retained after credential review.

- [Protocol](results/e1/protocol/PROTOCOL.md) and [source freeze](results/e1/protocol/freeze.json).
- [Every planned opportunity](results/e1/PROPOSALS.md), including blocked/unattempted slots.
- [Terminal selection freeze](results/e1/training_selections_frozen.json) and [audit](results/e1/audit.json).
- [Closed ledger](results/e1/ledger.json), [usage](results/e1/usage_summary.json) and [failure reproductions](results/e1/setup/failure_reproductions.json).
- [Final tests](results/e1/setup/tests_post_stop.txt) and [commands](results/e1/setup/COMMANDS.md).

## Preserved pilot and next bounded step

The reviewed pilot commit `fe5e130a4b2f3428b4b2bc482bd0378214672ea4`, its completed five-invocation ledger, candidates, report and audit remain intact. It remains an unblinded integration pilot, with selected guarded-WSLS payoff 2.533136 training / 2.444314 holdout. The original seed, interpreter, evaluator, task, payoffs, panels and stopping rule have not changed.

Next: repair buffered RPC handling, evaluation timing and terminal finalization; prove them and a full six-run rehearsal with zero-call mocks. Then repeat the same A/B design under a **new, separately authorized 60-invocation ledger**, three pairs and ten opportunities each. Change only the execution harness; keep model, effort, order, seeds and scientific conditions fixed. Do not reopen either ledger or reuse E1's remaining 16 invocations. The main report contains the implementation prompt. No follow-up experiment was executed.
