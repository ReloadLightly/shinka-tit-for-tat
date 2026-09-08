# Shinka Tit-for-Tat

**Can ShinkaEvolve generate tit-for-tat behavior when selection rewards only a player's own payoff in the iterated Prisoner's Dilemma?**

## Abstract

This project tests operational rediscovery of tit-for-tat (TFT) with LLM-guided program evolution. Starting from unconditional defection, ShinkaEvolve may change a deterministic policy that observes both players' past actions. A fixed evaluator returns average own payoff against a frozen opponent panel. Identification of TFT is a separate post-search analysis and supplies no fitness bonus. The environment, payoff matrix, observations, opponents, stopping rule, and evaluator are outside candidate control.

**Status, 2026-09-08:** [**E1: ShinkaEvolve versus independent generation — full report**](results/e1/E1_REPORT.md). E1 stopped at **44/60 external proposal invocations** after a subscription metadata timeout. Four runs completed, A303 is incomplete, and B303 never started. The two available paired holdout differences (A minus B) are 0.000000 and −0.110196; the third is unavailable. This partial readout shows no observed search advantage and does not complete the planned three-pair experiment. The earlier five-invocation unblinded pilot remains preserved.

## Research question and predictions

Record three distinct outcomes: whether TFT-compatible behavior appears in any generated valid candidate; whether it is the best candidate under training payoff; and how the payoff-selected candidate performs on held-out encounters. A non-TFT winner is an informative outcome, not grounds to change opponents until TFT wins.

An LLM may already know TFT. Recovering its behavior demonstrates operational rediscovery under this interface, not invention from an uninformed prior. E1 compares the combined Shinka search procedure with independent same-model generation at equal proposal opportunities; it does not isolate numerical feedback alone. Its unfinished third pair and infrastructure failures prevent a completed three-pair comparison. Exhaustive enumeration below is a separate comparator.

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
| `audit_e1.py` / `render_e1.py` / `write_e1_report.py` | Terminal selection freeze, offline audit, catalogue, trajectories and self-contained E1 report |
| `check_e1_restrictions.py` / `diagnose_e1_failures.py` | Zero-external-call native tool checks and infrastructure failure reproductions |
| `audit_pilot.py` | Post-search comparison of candidate files, live database/archive records, and usage |
| `recognize.py` | Offline behavioral probes and holdout evaluation for one candidate |
| `analyze_archive.py` | Offline report across generated candidate files |
| `baseline.py` | Hand-written references and exhaustive memory-one comparator |

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

## E1: evolutionary search versus independent generation

The protocol was frozen in commit `e0ca3f3`, before calls. It planned ten opportunities in each of A101, B101, B202, A202, A303, B303. A uses real Shinka parent selection, accumulated programs and training feedback. B uses the same native backend, parser, limits and evaluator, with a fresh session and the byte-identical initial task/seed/feedback prompt each time. Both use `gpt-5.6-terra`, low reasoning effort, through the existing ChatGPT Pro login. Local seeds do not control remote-model randomness.

| Run | Training-selected slot | Training | Development holdout | Status |
|---|---:|---:|---:|---|
| A101 | 1 | 2.536238 | 2.544314 | Complete |
| B101 | 1 | 2.536238 | 2.544314 | Complete; one opportunity lost to evaluator timing |
| B202 | 2 | 2.536238 | 2.544314 | Complete |
| A202 | 5 | **2.570925** | 2.434118 | Complete |
| A303 | 1, provisional | 2.536238 | Unavailable | Incomplete, four proposals |
| B303 | None | Unavailable | Unavailable | Unstarted |

All terminal selection identities/statuses were frozen before holdout or recognition; incomplete entries contribute no primary outcome. Exact ties use earliest appearance, which can differ from Shinka's later tied best-program pointer. The paired holdout differences are **0.000000**, **−0.110196**, and **unavailable**. The two-pair descriptive mean is −0.055098 (sample SD 0.077920). These are run-level comparisons, not 44 independent replicates.

The first three completed selections implement TFT. A202's selected policy copies the last opponent action except that it defects after apparent repeating mixed-action blocks of lengths 2–6. Its training gain arose entirely against fair random; on holdout, sustained mutual defection against suspicious TFT outweighed gains elsewhere. It remains below reference grim on training and below TFT, grim and ordinary WSLS on holdout. The [main report](results/e1/E1_REPORT.md) gives every selected source, branch explanations, scored traces and opponent breakdowns.

Forty-four files were generated and stored in Shinka: 40 live-valid/archived, two interpreter rejections, and two without evaluator results because upstream incorrectly included proposal time in the evaluation timeout. Nineteen valid programs passed the fixed TFT probes; eighteen have source-based TFT equivalence arguments. B202 slot 5 passes those probes but defects every 32 rounds, illustrating finite agreement without universal equivalence. The [proposal catalogue](results/e1/PROPOSALS.md) preserves all 60 planned opportunities, marking unattempted slots explicitly.

Supported per-process controls removed file, search, MCP, plugin and agent retrieval capabilities. Forced localhost tests verified tool refusal, and all 44 live native contexts matched the expected information with no tool calls observed. This is a tested native tool boundary, not an OS confidentiality container or knowledge-free invention. The original evaluator and scientific protocol are unchanged.

The terminal subscription metadata timeout prevented a 45th launch. Launch stopping worked, but cleanup needed a targeted interrupt; all partial evidence is saved and the ledger is closed with 16 unspent invocations. Local checks reproduce an RPC buffering vulnerability and the upstream timer defect. No retry, resampling, replacement, API-key authentication, paid API fallback, purchased credits, or GitHub Actions was used.

Usage records distinguish 44 external invocations, 44 completed Codex turn events and 44 native model-response records; those counts coincide here but are different concepts. Input tokens were 254,296 (137,216 cached); output 39,039 (31,394 reasoning). Credit balance remained 90.6853810000; account-wide rounded subscription use moved from 3% to 4%, also including supervisor use. The $0.7300712 list-price estimate is not a charge. [Audit](results/e1/audit.json), [usage](results/e1/usage_summary.json), [failure reproductions](results/e1/setup/failure_reproductions.json), and [36 passing final tests](results/e1/setup/tests_post_stop.txt) support this partial result.

## Preserved subscription pilot

The earlier [five-invocation integration pilot](results/PILOT_001.md), reviewed at `fe5e130a4b2f3428b4b2bc482bd0378214672ea4`, remains intact with its exhausted ledger. It produced three valid archived policies and one invalid tuple-based TFT expression after a pre-model configuration failure. Its selected guarded-WSLS policy scored 2.533136 training / 2.444314 holdout. That pilot allowed broad file reads and remains explicitly **unblinded**; E1 does not retroactively change that characterization.

## Run locally

The reference experiment and tests require only Python 3.10 or later:

```bash
python3 -m unittest discover -s tests -v
python3 baseline.py --output results/baseline_local.json
python3 run_evo.py --preflight
# E1 preflight needs the pinned optional dependency; it makes no proposal calls.
.venv/bin/python run_e1.py --preflight
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

The pilot passed its 26 tests; the final E1 suite passes 36, including mocked native A/B runs, terminal-state handling, and failure reproductions. Both default launchers are zero-call. E1's historical execution command was `.venv/bin/python run_e1.py --execute`; its existing closed ledger prevents reuse. Prompts, candidate sources, feedback, failures, usage, configuration, logs and databases are retained after credential review. The original scientific source files remain unchanged. No GitHub Actions workflows are installed.

## Sources and deviations

1. Robert Axelrod, *The Evolution of Cooperation*, uploaded revised-edition scan: printed p.8 (payoffs); pp.10, 13–16 (horizon, TFT definition, opponent-dependent success); pp.30–33 (first tournament); pp.38–39 (other rules could outperform TFT); pp.41–43 and p.217, chapter 2 note 5 (second tournament stopping rule). We borrow the payoff matrix and stopping probability, but use our own panel, seeds, and normalized scoring. Uploaded PDF SHA-256: `e816ca61aebd84159747d248fedd6d5ff318c471c36bcc31b1ac6bf9aebcd3c1`. The copyrighted PDF is not distributed here.
2. Lange, Imajuku, and Cetin (2025), [*ShinkaEvolve: Towards Open-Ended and Sample-Efficient Program Evolution*](https://arxiv.org/abs/2509.19349), uploaded v1, section 3: archive sampling, LLM mutation, execution/feedback. Uploaded PDF SHA-256: `ee287343c53240126e16a444d5ade2cd0ad0f290a400e78b97a040b93d965087`. The five-proposal, one-model pilot uses a reduced configuration; it does not exercise every mechanism in the paper.
3. Official [SakanaAI/ShinkaEvolve](https://github.com/SakanaAI/ShinkaEvolve/tree/9912af12d423504b8d580f4179fd15f5f88b8c50), pinned commit `9912af12d423504b8d580f4179fd15f5f88b8c50`: inspected `shinka/core/config.py`, `shinka/core/async_runner.py`, `shinka/launch/scheduler.py`, `shinka/llm/constants.py`, `shinka/llm/kwargs.py`, and `pyproject.toml` for the current API and limits.

## Next bounded milestone

Repair RPC buffering, measure evaluator time from actual evaluation start, and finalize stopped runners after draining work. First prove those fixes and a full six-run rehearsal with local mocks and zero external calls. Then repeat the same E1 design under a new, separately authorized 60-invocation ledger: three pairs, ten opportunities per run, the same model/effort, order, seed program, interpreter, panels and payoff-only selection. The intended change is the execution harness. Do not reopen either existing ledger or reuse E1's remaining 16 slots. The [E1 report](results/e1/E1_REPORT.md) provides the concrete implementation prompt; this follow-up has not been executed.
