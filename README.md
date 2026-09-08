# Shinka Tit-for-Tat

**Can ShinkaEvolve generate tit-for-tat behavior when selection rewards only a player's own payoff in the iterated Prisoner's Dilemma?**

## Abstract

This project tests operational rediscovery of tit-for-tat (TFT) with LLM-guided program evolution. Starting from unconditional defection, ShinkaEvolve may change a deterministic policy that observes both players' past actions. A fixed evaluator returns average own payoff against a frozen opponent panel. Identification of TFT is a separate post-search analysis and supplies no fitness bonus. The environment, payoff matrix, observations, opponents, stopping rule, and evaluator are outside candidate control.

**E3 in preparation:** Three serial 20-opportunity Shinka searches will start from the exact E1-R generated grim source, with faithful failure recovery and fresh transfer manifests. [Frozen design](results/e3/protocol/PROTOCOL.md). No E3 proposal has been invoked yet.

**Previous status, 2026-09-08:** [**E2: strategy transfer — full report**](results/e2/E2_REPORT.md) completed all **86,400 fresh matches with zero experimental model calls**. Grim retained its advantage over TFT on both original panels. The selected period detector retained a training advantage but remained worse on development holdout. E2 is separate post-search screening; the preserved [E1](results/e1/E1_REPORT.md) and [E1-R](results/e1_r/E1_R_REPORT.md) comparisons remain incomplete with closed ledgers.

## Research question and predictions

Record three distinct outcomes: whether TFT-compatible behavior appears in any generated valid candidate; whether it is the best candidate under training payoff; and how the payoff-selected candidate performs on held-out encounters. A non-TFT winner is an informative outcome, not grounds to change opponents until TFT wins.

An LLM may already know TFT. Recovering its behavior demonstrates operational rediscovery under this interface, not invention from an uninformed prior. E1 compares the combined Shinka search procedure with independent same-model generation at equal proposal opportunities; it does not isolate numerical feedback alone. Neither E1 nor E1-R completed its three-pair comparison; their results are reported separately. Exhaustive enumeration below is a separate comparator.

## Method

Actions are `0 = cooperate` and `1 = defect`. The table gives the candidate's payoff; the other player receives the corresponding transposed entry.

| Candidate action | Opponent cooperates | Opponent defects |
|---|---:|---:|
| Cooperate | 3 | 0 |
| Defect | 5 | 1 |

Both decisions use histories from before the current round. The match independently ends after each round with probability **0.00346**, giving a geometric length with no fixed cutoff. The evaluator samples its length independently in advance; the candidate sees neither this length nor the seed, opponent identity, or current opponent action. Candidate decisions cannot affect termination. There is no action noise, communication, or extra state.

For reproducible comparisons, five fixed seeds generate the same lengths for every training opponent. Distinct seeds and opponent types define the held-out panel. Reusing finite samples can still permit overfitting; hidden random termination removes a disclosed final-round opportunity, not every possible sampling artifact.

| Split | Opponents | Realized lengths shared across opponents |
|---|---|---|
| Training | Always cooperate; always defect; fair random; TFT; grim trigger; win-stay, lose-shift | 174, 747, 126, 25, 110 |
| Holdout | Alternator; suspicious TFT; TFT for two consecutive defections; hard TFT; random with cooperation probability 0.2; random with cooperation probability 0.8 | 241, 293, 199, 55, 62 |

TFT cooperates initially and then copies the opponent's previous action. Grim cooperates until the opponent defects, then defects forever. Win-stay, lose-shift starts with cooperation, repeats its action after payoff 3 or 5, and switches after 0 or 1. Alternator starts with cooperation. Suspicious TFT starts with defection. TFT for two consecutive defections cooperates for the first two rounds. Hard TFT cooperates initially and defects if either of the opponent's last two available actions was defection. Random choices use independent reproducible per-match streams. This illustrative panel includes modern comparators and is not Axelrod's submission roster; there is no additional candidate self-play encounter.

Fitness is **total own payoff / total rounds** across the 30 training matches. All opponents receive equal aggregate weight because they share lengths; individual matches are weighted by their number of rounds. There is no cooperation, simplicity, equality, winning-margin, or TFT-similarity bonus. The held-out panel is excluded from selection. Its baseline results are already public, so it is a fixed development holdout, not an untouched final confirmatory test.

## Programs and search space

| File | Role |
|---|---|
| `initial.py` | Preserved original unconditional-defection seed |
| `environment.py` | Fixed game, opponents, seeds, horizons, and payoff measurement |
| `policy.py` | Validates and interprets candidate decision code without executing arbitrary Python |
| `evaluate.py` | Shinka adapter; writes payoff-only `metrics.json` and validity `correct.json` |
| `task_prompt.txt` | Exact task-specific model instruction; contains no target strategy or opponent names |
| `run_evo.py` | Zero-call preflight and real upstream ShinkaEvolve subscription launcher |
| `subscription_guard.py` / `subscription_status.py` | Invocation ledger, native Codex process controls, and read-only account/quota checks |
| `run_e1.py` / `e1_backend.py` | Frozen A/B harness, restricted native Codex sessions, separate closed 60-call ledger |
| `audit_e1.py` / `render_e1.py` / `write_e1_report.py` | Preserved E1 analysis and report |
| `run_e1r.py` / `e1r_backend.py` / `e1r_runtime.py` | Separate E1-R launcher, durable accounting and versioned native runtime adapters |
| `e1r_status.py` / `e1r_process.py` / `e1r_io.py` | Buffered metadata, bounded nested subprocesses, fsynced ledger writes |
| `audit_e1r.py` / `diagnose_e1r.py` / `render_e1r.py` / `write_e1r_report.py` | E1-R audit, source proofs, scored traces, catalogue and report |
| `check_e1_restrictions.py` / `diagnose_e1_failures.py` | Zero-external-call native tool checks and infrastructure failure reproductions |
| `audit_pilot.py` | Post-search comparison of candidate files, live database/archive records, and usage |
| `recognize.py` | Offline behavioral probes and holdout evaluation for one candidate |
| `analyze_archive.py` | Offline report across generated candidate files |
| `baseline.py` | Hand-written references and exhaustive memory-one comparator |
| `run_e2.py` / `e2_common.py` / `analyze_e2.py` / `write_e2_report.py` | Separate frozen zero-call transfer evaluation, checkpoints, verified traces and report |

The candidate is ordinary runnable Python restricted to one `policy(own_history, opponent_history)` function. The evaluator interprets its syntax: `if/elif/else`, `return`, integer actions, comparisons, Boolean expressions, integer `+`, `-`, `%`, history indexes/slices, `len`, `sum`, `min`, `max`, and `.count`. There are no assignments, loops, imports, file access, functions created by the candidate, or external calls. Histories permit rules based on the whole past; the search is not restricted to memory one. Limits are 16,000 source bytes and 400 syntax-tree nodes. Invalid actions, including Boolean returns, invalidate the candidate and receive score -1.

For a separate, exactly enumerable comparator, a deterministic memory-one policy consists of five bits: its initial action, then its responses after CC, CD, DC, DD (own previous action first). There are 32 such policies. TFT is `00101`; the winning `00111` rule behaves as grim trigger on its reachable histories. Enumeration compares this restricted class only and does not establish a global optimum over the full-history program space.

Recognition exhaustively checks all paired binary histories through length 5, then adds 275 long probes, for **1,640 checks**. Passing means *TFT-compatible on these probes*. It does not prove equivalence on every possible history; a successful candidate needs subsequent code inspection or a proof based on its actual dependencies. Recognition and holdout data are never returned to the mutation model by `evaluate.py`.

## Measured baseline results

These are recorded reference measurements, **not evolved discoveries**. Each strategy plays 30 training matches / 7,092 rounds and 30 held-out matches / 5,100 rounds. Values are payoff per round.

| Hand-written policy | Training | Holdout |
|---|---:|---:|
| Always cooperate | 2.243655 | 2.239412 |
| Always defect (initial program) | 2.331077 | 2.001569 |
| TFT | 2.536238 | 2.544314 |
| Grim trigger | **2.655386** | **2.649804** |
| Win-stay, lose-shift | 2.451072 | 2.444314 |

The exhaustive memory-one comparison places TFT **2nd of 32**, with `00111` first. In this panel, grim earns more against the random opponent while preserving cooperation against cooperative references. A higher-payoff policy need not be TFT. Scores describe these specified encounters, with no uncertainty estimate or claim of universal optimality.

Evidence: [`results/baseline.json`](results/baseline.json), [`results/preflight.json`](results/preflight.json), and [`results/tests.txt`](results/tests.txt). The baseline records source hashes, individual matches, and all 32 comparator scores. These baseline/preflight artifacts made zero model calls; live evolution evidence is reported separately below.

## E2: transfer of fixed generated strategies

E2 froze its protocol, implementation, source inventory and encounters at `6adb42eb2e924a8b54c843d89cdcd28cb2412100` before evaluation. All **40 E1 + 18 E1-R live-valid occurrences** map to 35 parsed ASTs, retaining every origin, including incomplete runs. Five named references (including the seed) and all 32 memory-one policies bring the total to 72 entries. Rejected, missing and originally unevaluated sources remain excluded without repair.

Every entry played 600 matches on each unchanged panel: training seeds 100001–100100 and development seeds 200001–200100. The original horizon/RNG derivation and interpreter were unchanged. All 86,400 matches succeeded without model calls or retries. Frozen CLOCK_BOOTTIME accounting is **41.63 minutes**; recorded UTC timestamps span **44.08 minutes**. Their 146.936-second discrepancy has an unestablished host-clock cause; both recorded spans are below the 45-minute limit. [Clock audit](results/e2/runtime_clock_audit.json).

| Fixed policy | Fresh training | Δ TFT | Fresh development | Δ TFT |
|---|---:|---:|---:|---:|
| TFT reference | 2.538957 | 0 | 2.549153 | 0 |
| E1-R A101 selected grim | 2.660859 | +0.121902 | 2.655990 | +0.106837 |
| E1 A202 selected period detector | 2.575313 | +0.036356 | 2.440402 | −0.108751 |
| E1 A101 slot 9: two initial cooperations, then TFT | 2.538001 | −0.000957 | 2.630670 | +0.081517 |

Six generated ASTs exceed TFT on fresh training and three on development; none exceeds grim. Training gains for grim and the four period-detector variants persist. The focal detector's development loss is concentrated against suspicious TFT: extra defection ends in mutual defection. Two initial cooperations instead restore cooperation against that opponent; this newly measured development result is exploratory, not a historical selection. Only four ASTs have archived development scores; missing historical outcomes stay unavailable. Equal scores or finite probes are not universal equivalence proofs.

The [self-contained report](results/e2/E2_REPORT.md) includes original focal sources, branches and six scored traces with exact reproduction commands. The [catalogue](results/e2/CATALOGUE.md), [per-match records](results/e2/per_match.jsonl), [summary](results/e2/summary.json) and [commands](results/e2/COMMANDS.md) retain provenance, panel-specific ranks, cooperation, opponent breakdowns and failures. E2 does not complete either historical A/B comparison or establish transfer beyond these panels.

## E1-R: repaired comparison, stopped at 20/60

E1-R froze the same design in commit `b6647198e07df4eba7f23b0507dda0ea3d6e322a`: three pairs, ten opportunities per run, order A101, B101, B202, A202, A303, B303; `gpt-5.6-terra`, low effort, existing ChatGPT Pro login. A uses genuine Shinka parent selection, accumulated programs and training feedback. B receives the byte-identical original task/seed/feedback prompt in a fresh session each time. Both use the same backend, parser, limits and evaluator. Local seeds do not make remote outputs deterministic.

| Run | Status | Training-selected slot | Training | Development holdout |
|---|---|---:|---:|---:|
| A101 | Complete, 10 invocations | 4 | 2.655386 | 2.649804 |
| B101 | Incomplete, 10 invocations; last failed | 2, provisional | 2.655386 | Unavailable |
| B202 | Unstarted | — | Unavailable | Unavailable |
| A202 | Unstarted | — | Unavailable | Unavailable |
| A303 | Unstarted | — | Unavailable | Unavailable |
| B303 | Unstarted | — | Unavailable | Unavailable |

All six terminal statuses and source identities were frozen before holdout or recognition. A complete run requires ten consumed opportunities and a successful child exit. Seed placeholders for unstarted runs are not results. All three paired A-minus-B differences are unavailable; n=0 completed pairs, so descriptive effect statistics are undefined. E1-R is exploratory and is not pooled with E1.

Nineteen programs were generated and evaluated: 18 valid/archived and one forbidden-tuple rejection. The failed twentieth invocation supplied no program and consumed its slot. Five AST duplicates were retained. Seven admissible sources implement TFT by direct source arguments, beyond agreement on the unchanged 1,640 probes. TFT was not selected. A101's winner and B101's provisional winner both implement grim: cooperate until any opponent defection, then defect forever. Complete original sources, branch explanations, scored traces and every proposal appear in the [principal report](results/e1_r/E1_R_REPORT.md).

Grim's training advantage over TFT (+0.119148) arose entirely against fair random. A101's holdout advantage over reference TFT (+0.105490) combines gains against alternator and random opponents with a substantial loss against suspicious TFT. Independent B101 generated grim at slot 2 without earlier feedback. This observed behavior did not require evolutionary feedback to appear, but the incomplete comparison cannot estimate a general search advantage.

The three E1 defects were repaired with hash-checked runtime adapters around unchanged pinned Shinka: explicit buffered JSON-RPC reading, evaluation timing from actual evaluation start, and bounded terminal finalization. Fifty-two tests, a complete six-run mock rehearsal, forced failure/stop paths and native retrieval checks passed before calls. No generated E1-R candidate lost its evaluation, and the terminal stop finalized without manual interruption. The new transport error was **“Connection failed: error sending request”**; its lower-level cause is unresolved. A post-stop read-only check succeeded with 6% account usage and unchanged credit balance. The ledger is closed; its remaining 40 invocations cannot be reused.

Usage distinguishes **20 external invocations, 19 completed Codex turn events and 19 native response-usage records**. Available tokens: 108,683 input (34,048 cached subset), 15,469 output (13,048 reasoning subset); total 124,152. Codex runtime: 698.031 seconds; two Shinka runs: 925.373 seconds. The $0.3417076 API-list-price estimate is not a subscription charge. All 20 sessions were fresh, no tool call was observed, and controls prevented native file/search retrieval. This is a tested native tool boundary, not an OS confidentiality container or knowledge-free invention. No paid API, API-key fallback, purchased-credit continuation, auxiliary model or GitHub Actions was used.

Evidence: [protocol](results/e1_r/protocol/PROTOCOL.md), [audit](results/e1_r/audit.json), [closed ledger](results/e1_r/ledger.json), [usage](results/e1_r/usage_summary.json), [source diagnoses](results/e1_r/source_diagnoses.json), [implementation and local failures](results/e1_r/setup/IMPLEMENTATION.md).

## Preserved E1 comparison

[E1](results/e1/E1_REPORT.md) stopped at 44/60 after a metadata timeout: four runs completed, A303 remained incomplete and B303 unstarted. Its two available paired differences were 0 and −0.110196; the third was unavailable. The partial mean −0.055098 showed no observed search advantage. Forty-four sources included 40 valid policies, two rejections and two evaluator timing losses. A202's periodic-pattern policy improved training but transferred poorly. Nineteen proposals passed finite TFT probes; eighteen had source-based equivalence arguments. The periodic-defection false positive remains a warning against treating probe agreement as proof. E1's cleanup required a targeted interrupt; its exact as-executed code, report, failures, sources and closed ledger remain unchanged. Its unused 16 slots are not reused by E1-R.

## Preserved subscription pilot

The earlier [five-invocation integration pilot](results/PILOT_001.md), reviewed at `fe5e130a4b2f3428b4b2bc482bd0378214672ea4`, remains intact with its exhausted ledger. It produced three valid archived policies and one invalid tuple-based TFT expression after a pre-model configuration failure. Its selected guarded-WSLS policy scored 2.533136 training / 2.444314 holdout. That pilot allowed broad file reads and remains explicitly **unblinded**; E1 does not retroactively change that characterization.

## Run locally

The reference experiment and tests require only Python 3.10 or later:

```bash
python3 -m unittest discover -s tests -v
python3 analyze_e2.py --verify  # Read-only E2 verification, including six scored trace replays
python3 baseline.py --output results/baseline_local.json
python3 run_evo.py --preflight
# E1 preflight needs the pinned optional dependency; it makes no proposal calls.
.venv/bin/python run_e1.py --preflight
.venv/bin/python run_e1r.py --preflight
```

Each baseline/report command refuses to overwrite its existing evidence file. Choose a new output name for another run.

The subscription workflow uses the pinned dependency in a local environment:

```bash
uv venv .venv
uv pip install --python .venv/bin/python -r requirements-shinka.txt
.venv/bin/python run_evo.py --preflight
# The completed first milestone used these commands; its ledger prevents reruns.
.venv/bin/python run_evo.py --execute --mutations 5 --results-dir results/pilot_001
# After the recorded pre-model configuration repair, only four slots remained:
.venv/bin/python run_evo.py --execute --mutations 4 --continue-after-config-failure --results-dir results/pilot_001_repaired
.venv/bin/python audit_pilot.py --run results/pilot_001 --run results/pilot_001_repaired --usage-dir results/subscription_pilot_001_usage --output results/pilot_001_audit.json
```

The default remains zero-call. `--execute` requires existing ChatGPT Pro authentication and checks the explicitly configured model and subscription quota. It does not require `OPENAI_API_KEY` or a dollar threshold. The local guard forces native ChatGPT authentication, fixes the subscription endpoint, strips API-key/endpoint environment overrides, and changes no global credentials or permissions. A durable first-milestone ledger limits external proposal invocations to five and refuses automatic restarts; the explicit configuration-repair route retained the failed invocation. A later milestone needs a separately reviewed allowance.

Proposals/evaluations are serial. Each Codex process has a 180-second timeout; Headless has 210 seconds and the native provider 240 seconds. Request/stream retries, patch resampling, embeddings, novelty/meta calls, prompt evolution, and provider fallback are disabled. Quota checks before each proposal refuse unknown/exhausted quota or at least 90% window usage, with backend failures stopping further external calls. Native Headless ignores `max_tokens`, so no token cap is claimed. Shinka is Git-pinned; installed transitive dependency versions are recorded per run. Remote outputs are not bit-for-bit reproducible from the local search seed.

The pilot passed 26 tests; E1 passed 36; E1-R's pre-call and final suites pass 52. All default launchers remain zero-call. The historical execution commands `.venv/bin/python run_e1.py --execute` and `.venv/bin/python run_e1r.py --execute` now refuse their closed ledgers. E1-R's [command record](results/e1_r/setup/COMMANDS.md) includes local rehearsals, freeze, execution, failure diagnosis and analysis. Prompts, sources, feedback, failures, usage, configurations and databases are retained after credential review. No GitHub Actions workflows are installed.

## Sources and deviations

1. Robert Axelrod, *The Evolution of Cooperation*, uploaded revised-edition scan: printed p.8 (payoffs); pp.10, 13–16 (horizon, TFT definition, opponent-dependent success); pp.30–33 (first tournament); pp.38–39 (other rules could outperform TFT); pp.41–43 and p.217, chapter 2 note 5 (second tournament stopping rule). We borrow the payoff matrix and stopping probability, but use our own panel, seeds, and normalized scoring. Uploaded PDF SHA-256: `e816ca61aebd84159747d248fedd6d5ff318c471c36bcc31b1ac6bf9aebcd3c1`. The copyrighted PDF is not distributed here.
2. Lange, Imajuku, and Cetin (2025), [*ShinkaEvolve: Towards Open-Ended and Sample-Efficient Program Evolution*](https://arxiv.org/abs/2509.19349), uploaded v1, section 3: archive sampling, LLM mutation, execution/feedback. Uploaded PDF SHA-256: `ee287343c53240126e16a444d5ade2cd0ad0f290a400e78b97a040b93d965087`. The five-proposal, one-model pilot uses a reduced configuration; it does not exercise every mechanism in the paper.
3. Official [SakanaAI/ShinkaEvolve](https://github.com/SakanaAI/ShinkaEvolve/tree/9912af12d423504b8d580f4179fd15f5f88b8c50), pinned commit `9912af12d423504b8d580f4179fd15f5f88b8c50`: inspected `shinka/core/config.py`, `shinka/core/async_runner.py`, `shinka/launch/scheduler.py`, `shinka/llm/constants.py`, `shinka/llm/kwargs.py`, and `pyproject.toml` for the current API and limits.

## Next bounded milestone

Propose a separate **zero-call, 960-match, 10-minute** robustness study of the two focal policies, TFT and E1 A101 slot 9. Against the six training opponents on 20 new seeds, compare ordinary play with one forced opponent-action error at round 10, only if the independent horizon reaches it. Measure payoff loss and recovery of cooperation; no evolution or reselection. Grim's permanent retaliation and the two-opening-cooperation variant's suspicious-TFT recovery motivate the question. **Not executed.** The earlier [E1-R transport diagnostic proposal](results/e1_r/FOLLOWUP.md) is preserved historically and was not executed or authorized by E2.
