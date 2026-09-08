# Project status — 2026-09-08

## Current milestone: E3 paused before external model calls

[E3_REPORT.md](results/e3/E3_REPORT.md) is the principal current record. E3 generated **no new strategy**: 0 external proposal invocations, 3 failed local wrapper attempts, zero reservations, 0/3 completed runs. S101's only measured/archive program is the byte-identical earlier grim seed (2.655386350817823 original training); S202 and S303 are unstarted. The scientific question is unanswered, and all fresh-transfer outcomes are unavailable. No final selections, recognition or transfer evaluation were performed.

The protocol, exact seed, fresh manifests, implementation and hashes were committed and remotely verified at `3288b90e625daf0f02e684eb32d791c4f3f261a1` before `python run_e3.py --execute`. Local/remote recovery started at the reviewed `9564d2125d5b818e24df1aa2b958938dc2f843f6` with a clean tree and no active experiment. Six native retrieval checks, four real-loop mock failure/resume scenarios, seven focused tests and 70 full-suite tests passed before launch, but the mocks bypassed the actual commit guard and missed its working-directory/import-order defects.

S101 slot 1 was sampled from the seed. The commit guard ran Git from the isolated mutation directory and failed before metadata, reservation or external Codex. Shinka had already captured its default three query attempts because upstream hash validation imported it before environment controls. Three local attempts therefore failed with the same Git error. The terminal database checkpoint is intact, but native next_generation_to_submit=2 disagrees with consumed=0. The launcher paused the same experiment automatically; no workers remain and no transient recovery allowance was used. [Audit and zero-call reproduction](results/e3/prelaunch_failure_audit.json); [ledger](results/e3/ledger.json); [checkpoint](results/e3/runs/S101/checkpoint.json).

Post-pause repairs set retry controls before imports and pass cwd=ROOT to Git. Nine focused regression checks pass. The original freeze/checkpoints remain unchanged, and [repair source hashes](results/e3/setup/repair_source_hashes.json) distinguish current repairs from as-executed code. The original freeze rejects those repaired bytes, so no accidental live restart is possible. Zero reservations must not be treated as a reset 60-call allowance; failed local launch/slot accounting requires explicit reconciliation before a continuation freeze. Do not rerun slot 1, relabel retries, reset the ledger or restart from the best policy alone.

Final verification is qualified: the post-repair 72-test suite failed an unchanged 0.1-second subprocess-startup fixture. The 16-test recheck repeated that failure and also timed out the unchanged 0.25-second partial-UTF-8 fixture. No historical test/bound was modified; logs are preserved. Nine E3-focused tests, both zero-call preflights and publication source/prompt/ledger checks pass. The post-repair full suite is not green.

The bounded proposed next step is a zero-call reconciliation review and isolated-backend failure fixture for this same E3, with no new call authorization or other experiment. E2's evaluation-only follow-up remains unexecuted. All initial.py, earlier scientific sources, historical results and closed ledgers remain unchanged.

## Preserved E2 strategy transfer complete

[E2_REPORT.md](results/e2/E2_REPORT.md) is the current principal deliverable. It contains the setup, original focal sources, branch explanations, six scored traces and exact reproduction commands. [CATALOGUE.md](results/e2/CATALOGUE.md) covers every source/origin, exclusion and per-opponent result; [summary.json](results/e2/summary.json) and [per_match.jsonl](results/e2/per_match.jsonl) provide machine-readable evidence.

Recovery found a clean tree and GitHub at `fd19af5dd0f168f14b82dd5e2f5b1e68b210fe33`, no E2 files/runtime/checkpoints and no host-visible E2 process. The implementation, protocol, all source hashes and encounter manifest were frozen and remotely verified at `6adb42eb2e924a8b54c843d89cdcd28cb2412100` before fresh evaluation.

The inventory verifies 40 E1 and 18 E1-R live-valid occurrences, deduplicated into 35 ASTs while retaining all provenance and original incomplete-run statuses. It excludes three rejected sources, two originally unevaluated generated sources and all absent slots. Adding the original always-defect seed, four other named references and 32 memory-one policies gives 72 entries. No generated source was repaired or executed outside policy.py.

All **86,400/86,400 matches succeeded**, with no policy or infrastructure failures in main evaluation, no retries and **zero experimental model calls**. Each entry faced all six opponents × 100 seeds per panel: training 100001–100100 and development 200001–200100. Frozen CLOCK_BOOTTIME accounting is **2497.819 seconds (41.63 minutes)**; UTC timestamps span **2644.755 seconds (44.08 minutes)**. Their 146.936-second discrepancy has an unestablished host-clock cause; both recorded spans are below 45 minutes. [Clock audit](results/e2/runtime_clock_audit.json) retains all 76 detected discontinuities without altering the original runtime. Serial 300-second worker bounds were retained. The single runtime ledger and append-only match starts/results are preserved; execution is closed.

Grim scored **2.660859 training / 2.655990 development**, beating TFT by **+0.121902 / +0.106837**. The period detector scored **2.575313 / 2.440402**, **+0.036356 / −0.108751** vs TFT and below grim on both. Six generated ASTs beat TFT on training; three on development; none exceeds grim. Grim's training gain is entirely against fair random. The detector's development loss is concentrated against suspicious TFT. E1 A101 slot 9's two initial cooperations yield a new exploratory development score of **2.630670**, rank 3 of 35; it was not the historical winner. Original development scores exist for only four ASTs and are not backfilled for other sources.

Verification: eight focused frozen checks and 14 exact historical panel replays passed before fresh evaluation; zero-call preflight validated the seed. The dependency-enabled full suite passed 60 tests, and three subsequent analysis checks passed. A sandbox mock-harness stall, one non-reproducing host child-death test failure and a caught/fixed report-merge bug are preserved separately from scientific results. Final export/trace/source checks are recorded in [VERIFICATION.md](results/e2/setup/VERIFICATION.md), with exact commands in [COMMANDS.md](results/e2/COMMANDS.md).

E2 is post-search descriptive screening on the same public panels. Historical winners, original scientific implementations, pilot/E1/E1-R evidence and closed ledgers remain intact. E2 does not complete missing A/B outcomes, establish universal policy equivalence from probes, or demonstrate knowledge-free invention or transfer beyond the panels.

One proposed follow-up, **not executed**: a separate zero-call robustness protocol with the two focal sources, TFT and E1 A101 slot 9; six training opponents × 20 new seeds × ordinary/one-error conditions = 960 matches, a 10-minute cap, no evolution or reselection. Test whether cooperation recovers after one opponent-action error at round 10 when the independent horizon reaches it. This is motivated by the observed retaliation/recovery contrast. The prior E1-R transport proposal remains historical and unexecuted.

## Preserved E1-R status

## E1-R stopped automatically; comparative outcome remains unanswered

The E1-R principal deliverable is [E1_R_REPORT.md](results/e1_r/E1_R_REPORT.md), a
self-contained report of the design, every run, all paired outcomes, original
selected sources, branches, scored traces, opponent breakdowns, actual parent/
inspiration context, failures, usage, commands and next bounded step.

The new protocol and execution fixes were committed as
`b6647198e07df4eba7f23b0507dda0ea3d6e322a` before external proposals, and that
commit was pushed and verified on GitHub. E1-R retained
E1's scientific design: three paired local seeds 101/202/303, ten opportunities
per run, serial order A101/B101/B202/A202/A303/B303, gpt-5.6-terra with low reasoning,
original seed/interpreter/evaluator/panels/fitness and exact initial prompt.
The model and ChatGPT Pro access were verified without substitution. B's ten
fresh sessions received the identical initial prompt, never earlier outputs or
feedback. A retained real native Shinka parent selection and accumulated records.

The separate ledger is **closed at 20/60 external invocations**. B101 slot 10
failed with **“Connection failed: error sending request”** after 13.471 seconds.
It consumed its slot, supplied no policy, and recorded no completed model turn
or native response-usage record. No retry, replacement or restart occurred.
The remaining **40 invocations cannot be reused**.

| Run | Status | Training-selected slot | Training | Development holdout |
|---|---|---:|---:|---:|
| A101 | Complete, 10 invocations | 4 | 2.655386 | 2.649804 |
| B101 | Incomplete, 10 invocations; final launch failed | 2, provisional | 2.655386 | Unavailable |
| B202 | Unstarted | — | Unavailable | Unavailable |
| A202 | Unstarted | — | Unavailable | Unavailable |
| A303 | Unstarted | — | Unavailable | Unavailable |
| B303 | Unstarted | — | Unavailable | Unavailable |

The pre-call completion rule requires all ten consumed opportunities and a
successful child exit. All six terminal statuses and source hashes were frozen
at 14:33:54.708 UTC before E1-R holdout or recognition. The four unstarted seed
identities are placeholders, not evaluations. B101 has no computed primary
holdout result. Paired differences for 101, 202 and 303 are all unavailable:
**n=0 completed pairs**, so mean, median, range and sample SD are undefined.
Do not pool E1 and E1-R or substitute missing outcomes with zero.

## Scientific evidence

Nineteen generated sources were evaluated: **18 valid and archived, one rejected**.
A101 slot 1 has 48 AST nodes but contains a forbidden tuple literal. It was not
repaired. B101 slot 10 has no generated source, evaluator result, program row or
archive entry; native Shinka's downstream missing-output label is explained as
a transport failure. Including two seeds, there are 21 database rows and 20
archive members. Five AST duplicates consume their slots and overlap validity.
Each started run has nine valid proposals out of ten consumed opportunities;
B101 has nine valid programs out of nine actually generated files.

Exact TFT appears at A101 slots 6/10 and B101 slots 1/5/7/8/9. All seven pass the
1,640 frozen probes and have source arguments covering every legal binary
history. The known E1 periodic-defection counterexample remains a warning that
probe agreement alone does not prove equivalence.

TFT was not selected. A101's selected slot 4 and B101's provisional slot 2 both
implement grim trigger: cooperate until the opponent first defects, then defect
forever. Source inspection establishes their equivalence. Grim improves training
over TFT solely against fair random. Its measured A101 holdout payoff is higher
than reference TFT, with gains against alternator/random outweighing a large
loss against suspicious TFT. Independent generation produced the same behavior
without accumulated feedback. The incomplete paired experiment cannot estimate
whether evolutionary search improves expected selected-policy holdout payoff.

The actual A101 slot-6 → slot-8 step changes TFT to grim (+0.119148 training),
but grim slot 4 was already supplied as an inspiration and the child repeats it.
It is neither a new best nor a new discovery at slot 8. The report distinguishes
measured code/context relationships from speculation about model reasoning.

## Operational result and verification

The publication audit independently reproduced the archived analysis, all 20
native contexts, usage, source proofs and scored traces. All 52 tests and both
zero-call preflights passed; the known sandbox test stall and successful rerun
are recorded in [PUBLICATION_AUDIT.md](results/e1_r/setup/PUBLICATION_AUDIT.md).
No additional live invocation occurred during publication work.

The fixed evaluator and installed pinned Shinka remain unchanged. Versioned,
hash-checked per-run adapters repair buffered metadata reading, start evaluation
timeouts at actual evaluation start, and finalize stopped runners after bounded
draining. Ledger replacement fsyncs the file and directory; nested subprocesses
have time bounds and parent-death cleanup. Database and proposal retries are
disabled. The default launcher remains zero-call.

The release suite passed 52 tests, a full six-run mocked rehearsal and metadata/
backend/quota stop paths before calls. Forced localhost checks re-established
native retrieval restrictions. Legacy buffering, timer and actual native stop
failures were reproduced separately. Early local sandbox/fixture failures remain
preserved and are not scientific proposals.

In live E1-R, every generated candidate received an evaluator result. The
terminal drain took 0.051 seconds, and closure needed no manual interruption.
The new connection error's low-level cause remains unresolved; the logs do not
establish a DNS, TLS, service or quota cause. A post-stop read-only metadata
check succeeded. Account-wide rounded usage was 6% before/after; credit balance
stayed 90.6853810000. No quota exhaustion was observed.

Usage: **20 external invocations, 19 completed Codex turn events, 19 available
native model-response records**. Input tokens 108,683 (34,048 cached subset);
output 15,469 (13,048 reasoning subset); total 124,152. Codex runtime 698.031
seconds; Shinka run runtime 925.373 seconds. The $0.3417076 API-list-price estimate
is not a subscription charge. Failed-call remote processing cannot be inferred
from absent usage. All 20 native sessions were fresh; no tool call was observed.
No paid API, API-key authentication/fallback, purchased-credit continuation,
auxiliary model, embeddings or GitHub Actions was used.

- [Protocol](results/e1_r/protocol/PROTOCOL.md) and [source freeze](results/e1_r/protocol/freeze.json).
- [Terminal selections](results/e1_r/training_selections_frozen.json), [audit](results/e1_r/audit.json), [source proofs](results/e1_r/source_diagnoses.json).
- [Every opportunity and original source](results/e1_r/PROPOSALS.md), [closed ledger](results/e1_r/ledger.json), [usage](results/e1_r/usage_summary.json).
- [Implementation and local failure history](results/e1_r/setup/IMPLEMENTATION.md), [release rehearsal](results/e1_r/setup/rehearsal_release/summary.json), [tests](results/e1_r/setup/tests_release.txt), [commands](results/e1_r/setup/COMMANDS.md).

## Preserved findings and proposed next step

The pilot at reviewed commit `fe5e130a4b2f3428b4b2bc482bd0378214672ea4` remains an
unblinded five-invocation integration pilot; selected guarded WSLS scored
2.533136 training / 2.444314 holdout. Its exhausted ledger and evidence remain
unchanged. E1 at `42b163193e0a0da4030e6c5917a1c17f1cab6e3d` remains closed at 44/60,
with four complete runs and two available paired differences, 0 and −0.110196.
Its mean −0.055098 showed no observed advantage in that partial readout. The
original code, failures and unused 16 slots are preserved; E1-R did not reuse them.

At E1-R closure, the proposed next step was one transport-reliability diagnostic with **at most three newly
authorized subscription invocations**, a fixed non-game prompt, the same model,
restrictions, serial bounds and no retries. Record sanitized transport timing
and error identifiers; stop on the first failure. First exercise the failure
locally. This addresses the new execution uncertainty and does not complete the
scientific comparison. [Full bounded proposal](results/e1_r/FOLLOWUP.md).
**No follow-up or additional scientific condition was executed.**
