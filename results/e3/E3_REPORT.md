# E3 — continuation beyond generated grim: paused before model calls

**The research question is unanswered. E3 produced no new strategy.** S101
paused during its first proposal's local launcher setup; S202 and S303 are
unstarted. There were **0 external model invocations, 3 failed local wrapper
attempts, 0 generated policies and 0/3 completed runs**. No transfer evaluation
or recognition was performed. This is failed preparation/execution-boundary
evidence, not an evolutionary result or evidence that grim cannot be improved.

The user required configuration mismatches and ambiguous checkpoint integrity
to pause execution. Both occurred. Native generation state advanced to 2 after
assigning slot 1, but the external-invocation ledger contains zero reservations.
The actual database and saved database agree; the slot/ledger relationship does
not. It would be misleading to repair this by pretending a reservation preceded
the failed launches, relabeling retries as new opportunities, resetting the
ledger, or resuming from the best source alone. No such action was taken.

## Intended scientific design

Question: starting from the strongest previously generated policy, can the
genuine pinned ShinkaEvolve loop generate a higher-original-training-payoff
policy whose advantage survives fresh encounters? This is continuation from
evolved grim, not discovery from unconditional defection or an uninformed prior.
Three exploratory searches cannot establish Shinka's advantage over independent
generation because E3 has no such comparison condition. E3 is not pooled with
E1 or E1-R and does not execute E2's proposed evaluation-only follow-up.

The fixed game is the simultaneous iterated Prisoner's Dilemma. Actions are
0=cooperate and 1=defect; own payoffs are CC=3, CD=0, DC=5 and DD=1. Both decisions
use histories before the current round. Policies receive only own/opponent
histories, with no opponent identity, source, current action, encounter seed or
endpoint. Independent geometric stopping probability is 0.00346, without a fixed
cutoff. There is no noise, new opponent, cooperation reward or extra state.

Original training uses always-cooperate, always-defect, fair random, TFT, grim
and win-stay/lose-shift with seeds 11,23,47,89,131, yielding match lengths
174,747,126,25,110. Fitness is total own payoff / total rounds over 30 matches
(7,092 rounds). Candidate validity is determined by unchanged policy.py, which
interprets the restricted one-function source rather than importing or exec'ing
it. Limits remain 16,000 bytes and 400 AST nodes; invalid candidates score -1.

| Setting | Frozen value |
| --- | --- |
| Run order | S101, S202, S303 |
| Local Python/NumPy seeds | 101, 202, 303 |
| Opportunities | 20 per run; hard 60 total including failed launches |
| Model/backend | gpt-5.6-terra, low effort; ChatGPT Pro subscription, Codex 0.153.4 / Headless 0.6.1 |
| Shinka | 0.0.7, commit 9912af12d423504b8d580f4179fd15f5f88b8c50 |
| Search | Native weighted parent sampling, accumulated programs, archive size 16, one island, fitness-only archive |
| Inspirations | Zero random archive inspirations; one native top-k inspiration |
| Proposal | Native FULL_SYS_FORMATS[0], full rewrite, intended one attempt with no retry/resample |
| Disabled | Dynamic models, embeddings, novelty judge, meta recommendations, prompt evolution, migration/dynamic islands |
| Bounds | Codex 180 s; Headless wrapper 210 s; native provider 240 s; evaluator 60 s; drain 350 s; cumulative child runtime 9,000 s/run |
| Intended recovery | At most two classified send failures, each followed by full checkpoint and one bounded read-only availability check |

Local seeds do not make remote outputs deterministic. The native parent sampler
retains its existing child-count weighting; this is not an additional fitness
reward. E3 does not claim to exercise every Shinka paper mechanism. The effective
local retry count differed from the intended configuration, as documented below.

The [full protocol](protocol/PROTOCOL.md), [configuration](protocol/protocol.json),
[exact initial prompt](protocol/initial_prompt.md), [source freeze](protocol/freeze.json)
and [fresh encounter manifest](protocol/encounters.json) were committed and
remotely verified at **3288b90e625daf0f02e684eb32d791c4f3f261a1** before launch.
The reviewed starting main was 9564d2125d5b818e24df1aa2b958938dc2f843f6.

## Original seed and the actual attempted sequence

The exact earlier generated source at `results/e1_r/runs/A101/gen_4/main.py` was
copied byte-for-byte into [protocol/seed.py](protocol/seed.py). The SHA-256 is
`fc938dea6c869791ffb3d7fbbb03f95b21ea86152fb3414345a9d107323d56a1` and matches the
earlier frozen E1-R selection. `initial.py` remains unconditional defection.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 or opponent_history.count(1) == 0 else 1
# EVOLVE-BLOCK-END
```

This is grim by direct source logic: cooperate while the opponent has never
defected; after its first defection, the count of recorded defections can never
return to zero, so defect forever. Own history is unused. It is a familiar
strategy recovered in E1-R and reused here, not a new E3 discovery.

S101's native archive contains exactly one program, the seed. Its new training
evaluation reproduced **2.655386350817823**. Slot 1 sampled that program as its
parent and supplied no inspirations, because there were no other programs.
The [actual supplied context](runs/S101/gen_1/supplied_context.json) contains that
source and scalar mean payoff, with empty private metrics and text feedback.
Three preserved [Headless prompt files](runs/S101/headless_prompts) record the
local attempts; none was delivered to an external model. No proposal response,
changed source, measured child policy or evolutionary improvement exists.

| Run/slot | Actual outcome | Measured proposal payoff | Best training payoff |
| --- | --- | --- | --- |
| S101 seed, slot 0 | Valid seed evaluated and archived | 2.655386350817823 | 2.655386350817823 |
| S101 slot 1 | Assigned; three local wrapper failures before external launch/reservation | Unavailable | 2.655386350817823 |
| S101 slots 2–20 | Not reached; no generated source or evaluation | Unavailable | No subsequent trajectory |
| S202 slots 1–20 | Run unstarted | Unavailable | Not measured in this run |
| S303 slots 1–20 | Run unstarted | Unavailable | Not measured in this run |

There are zero valid or invalid generated proposals and zero generated
duplicates. A valid-proposal rate is undefined because no external proposal was
made, rather than evidence of a 0% model validity rate. The seed-only interim
`training_summary.json` is not a final selection. No three-selection freeze file
exists. There are no selected new original sources to explain or publish.

## Failure diagnosis and checkpoints

The supervising launcher entered native S101. Its isolated mutation working
directory was `/tmp/e3_mutation_ljrjcww4`. The newly added committed-source guard
called `git rev-parse HEAD` without `cwd=ROOT`. Git therefore failed outside the
checkout, before subscription metadata, durable reservation or external Codex
launch. The [raw final wrapper stderr](runs/S101/invocations/01/headless.stderr.txt)
retains `fatal: not a git repository` and the complete traceback.

A second implementation defect loaded Shinka while checking upstream source
hashes, before setting its retry environment. Shinka captured the default
`MAX_RETRIES=3`; setting the environment later did not change that imported
constant. The [console](runs/S101/console.log) records `1/3`, `2/3` and `3/3` local
query failures with the same Git error. All three failed before invoking the
real external Codex process. The native downstream `LLM response content was
None` / `llm_output_invalid` label is a consequence of those local failures,
not a model-generated invalid policy.

All three prompt files survive and match the frozen initial prompt byte-for-byte.
The per-slot wrapper stdout/stderr paths were reused by the three failed local
attempts, so those files retain only the last attempt; the unmodified console
retains all three tracebacks. No missing earlier raw file is reconstructed.

The [read-only audit](prelaunch_failure_audit.json) reproduces the original import
order as `3 0` (Shinka attempts / OpenAI retries) and the repaired order as `1 0`.
It verifies one actual program row, one archive member, one failed generation
attempt record and zero invocation reservations. Its original and saved database
digests agree. The terminal checkpoint has `consumed=0` but
`next_generation_to_submit=2`; the launcher rejected that disagreement and
preserved **stopped=true, closed=false** in the [ledger](ledger.json).

Both [pre-proposal](runs/S101/checkpoints/000_boundary_00/state.json) and
[terminal](runs/S101/checkpoints/001_terminal_00/state.json) checkpoints retain
full SQLite backups, RNGs, native generation/accounting fields, DB runtime
metadata, ledger snapshots and configuration hashes. The [terminal drain](runs/S101/terminal_finalization.json)
completed in 0.083334 seconds without cancellation or manual interruption.
A host process check after exit found no surviving E3 proposal/evaluator worker.
No automatic transient recovery was used: this was a configuration/integrity
failure, not the specifically permitted send failure.

The zero-reservation ledger must **not** be interpreted as a fresh unrestricted
60-call allowance. The three failed local launches expose an accounting defect
at the boundary. Their relationship to the assigned opportunity must be resolved
explicitly before any continuation; this report does not retroactively assign
new slot numbers, invent reservations or rerun slot 1.

## Verification and post-pause repairs

Before launch, six localhost forced-tool checks passed with no authentication
header and no canary access. The restricted model catalog matches locally cached
model metadata except intentional removal of apply_patch registration. Fresh
mutation tools cannot retrieve repository, opponent/evaluator/reference code,
reports, development/recognition information or outside experiment material.
This is a supported native tool boundary, not an OS confidentiality container.
No supervising conversation or report was given to a mutation model.

The pre-launch native-loop rehearsals passed normal, first-slot, middle-slot
and final-slot failures; first/middle cases resumed the same full archive and
RNG checkpoint to 20 synthetic opportunities. Seven focused checks and the
70-test full unittest suite passed. **Those tests mocked the proposal interface
and bypassed the new commit guard, so they missed both live-entrypoint defects.**
Test success did not establish end-to-end readiness. Earlier sandbox/local
fixture failures are preserved in [preparation evidence](setup/IMPLEMENTATION.md)
and the compressed byte-preserving rehearsal archives.

Post-pause repairs set retry controls before the first Shinka import and run
both Git guard commands with `cwd=ROOT`. Two new regression tests exercise the
guard from outside the checkout and its retry constants in a fresh process.
All nine focused checks pass. [Repair hashes](setup/repair_source_hashes.json)
distinguish these edits from the as-executed implementation. The original
protocol freeze, raw execution evidence and checkpoints are unchanged; the
original freeze deliberately rejects these subsequently repaired source bytes.
No new live protocol or experiment was started. Original and E3 zero-call
preflights pass after repair.

The first post-repair full suite reached 72 tests but failed the preserved
E1-R 0.1-second subprocess fixture: the child timed out before printing `fixture`.
That [failure log](setup/tests_full_repairs.txt) remains intact, and no historical
test or subprocess bound was changed. The [16-test focused recheck](setup/tests_process_recheck.txt)
also failed that check and timed out the existing 0.25-second partial-UTF-8
fixture. The planned subsequent full rerun was therefore not launched. These
results are consistent with timing-sensitive fixture startup under current host
conditions; the precise scheduling cause is unestablished. The post-repair full
suite is **not green**. Nine E3-focused checks and both zero-call preflights pass;
the earlier pre-launch 70-test pass remains a separate result.

## Transfer, traces and scientific interpretation

The frozen future panels are original training types × seeds 300001–300100 and
original development types × seeds 400001–400100. The latter types are alternator,
suspicious TFT, TFT for two consecutive defections, hard TFT, random p(C)=0.2 and
random p(C)=0.8. Ranges are disjoint from original encounter seeds and E2's
100001–100100/200001–200100. Horizon and SHA-256 match-stream derivation are
unchanged. Three selected policies, seed/grim and TFT were intended to receive
identical encounters: 6,000 matches total, panels scored separately.

**Actual fresh matches: 0/6,000.** All three primary selected-minus-seed
development outcomes, fresh-training improvements and per-opponent transfer
results are unavailable. There are no scored E3 transfer traces to replay.
No recognition or interim transfer was exposed to a future mutation session.

The planned distinctions—no training improvement, training gain failing to
transfer, and gain retained on both fresh panels—cannot yet be applied. This
execution produced no child policy to compare. Source and behavior both remain
the earlier grim seed; there is no E3 novelty claim and no finite-probe claim of
universal equivalence. Earlier E2 transfer findings remain historical evidence,
not substitute E3 outcomes.

## Computation and reproducible evidence

| Quantity | Actual E3 result |
| --- | ---: |
| External proposal/model invocations | 0 |
| Failed local wrapper attempts before external launch | 3 |
| Durable invocation reservations | 0 — integrity discrepancy, not reset allowance |
| Completed external model turns / native response usage records | 0 / 0 |
| External proposal tokens / subscription charges | 0 / 0 |
| Generated sources / successful generations | 0 / 0 |
| Completed runs | 0/3 |
| S101 child-segment runtime, outer measurement | 67.566262 s |
| Native runner runtime, inner measurement | 44.260495 s |
| Seed evaluator recorded compute time | 0.505195 s |
| Headless API-list-price estimate | $0.00; not a subscription charge |
| Automatic recovery checks used | 0/2 |

Outer and inner times measure different scopes; neither is substituted for the
other. The pre-call read-only account check reported ChatGPT Pro, the requested
model/low effort, 11% rounded account usage and credit balance 90.6853810000.
No paid API, API-key fallback, purchased-credit continuation, auxiliary model,
embedding, judge call or GitHub Actions was used.

Safe exact commands from the repository (no external proposals):

```bash
source .venv/bin/activate
python diagnose_e3_prelaunch.py
python -m unittest discover -s tests -p test_e3.py -v
python run_e3.py --preflight
python run_evo.py --preflight
python - <<'PY'
from policy import load_policy
p = load_policy('results/e3/protocol/seed.py')
for own, other in [((), ()), ((0,), (0,)), ((0,), (1,)), ((0,1), (1,0))]:
    print(own, other, '->', p(own, other))
PY
```

The last command reproduces the seed's choices `0, 0, 1, 1` through policy.py.
These are explicit history examples, **not scored E3 encounter traces**. The
as-executed source can be inspected with
`git show 3288b90e625daf0f02e684eb32d791c4f3f261a1:run_e3.py`.
[COMMANDS.md](COMMANDS.md) preserves the actual preparation/launch commands and
clearly gates the currently unexecuted transfer commands.

One bounded follow-up proposal, **not executed**: a zero-call reconciliation
review of this same E3 archive, both checkpoints and all three local wrapper
attempts. Exercise the real isolated backend entrypoint with a localhost-only
failure fixture and decide the failed-launch/slot accounting before a reviewed
continuation freeze. Do not grant new calls, reset a ledger, repeat a consumed
opportunity or start a new experiment as part of that review.
