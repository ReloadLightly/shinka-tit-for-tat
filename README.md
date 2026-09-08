# Shinka Tit-for-Tat

**Can ShinkaEvolve generate tit-for-tat behavior when selection rewards only a player's own payoff in the iterated Prisoner's Dilemma?**

## Abstract

This project tests operational rediscovery of tit-for-tat (TFT) with LLM-guided program evolution. Starting from unconditional defection, ShinkaEvolve may change a deterministic policy that observes both players' past actions. A fixed evaluator returns average own payoff against a frozen opponent panel. Identification of TFT is a separate post-search analysis and supplies no fitness bonus. The environment, payoff matrix, observations, opponents, stopping rule, and evaluator are outside candidate control.

**Status, 2026-09-08:** the first real native ShinkaEvolve/Headless/Codex pilot completed through the existing ChatGPT Pro login. Five external invocation slots yielded one pre-model configuration failure and four generated files: three valid archived policies and one rejected TFT expression. The best valid policy scored 2.533136 on training and 2.444314 on holdout. No valid mutation passed the TFT probes. This is an **unblinded integration pilot**, not discovery under enforced hidden information or a historical tournament reconstruction.

## Research question and predictions

Record three distinct outcomes: whether TFT-compatible behavior appears in any generated valid candidate; whether it is the best candidate under training payoff; and how the payoff-selected candidate performs on held-out encounters. A non-TFT winner is an informative outcome, not grounds to change opponents until TFT wins.

An LLM may already know TFT. Recovering its behavior demonstrates operational rediscovery under this interface, not invention from an uninformed prior. This first five-invocation pilot cannot attribute success specifically to evolutionary feedback. That claim needs multiple independent runs and a same-model, equal-budget control receiving no evolutionary feedback. Exhaustive enumeration below is a comparator, not that control.

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

## Measured subscription pilot

The pinned native search used `headless/codex@gpt-5.6-terra?effort=low`, Headless 0.6.1, Codex 0.153.4, and ChatGPT Pro authentication. One initial launch failed before a model turn because Codex disallows overriding a reserved provider ID. After a local configuration repair, the remaining four invocation slots ran through Shinka's real parent sampling, mutation, evaluation, and archive loop. Both run directories and all failures are retained; this is one integration milestone, not two independent replicates.

| Repaired-run generation | Policy | Training | Holdout | Shinka outcome |
|---|---|---:|---:|---|
| 0 | Original defection seed | 2.331077 | 2.001569 | Archived |
| 1 | Guarded win-stay, lose-shift | **2.533136** | **2.444314** | **Payoff-selected best**, archived |
| 2 | Periodic probing and forgiving retaliation | 1.966159 | 2.187647 | Archived |
| 3 | Echo detection and defection probing | 2.226029 | 2.255098 | Archived |
| 4 | TFT expression with redundant branch | -1 validity sentinel | Not run | Invalid; DB row, no archive membership |

All three valid mutations failed the 1,640 TFT probes. Generation 4 contains a forbidden tuple literal, so the fixed interpreter rejected it before simulation. Static inspection shows its ordinary Python rule is TFT: start with 0, otherwise copy the last opponent action; its additional branch returns 1 only when that last action is already 1. This source observation is separate from finite probing and **does not constitute a valid evolved TFT policy**. The model's accompanying claim of permanent defection does not match its code.

The complete executable source of the payoff-selected generation 1 is:

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else 1 if len(opponent_history) > 2 and opponent_history.count(0) == 0 else own_history[-1] if opponent_history[-1] == 0 else 1 - own_history[-1]
# EVOLVE-BLOCK-END
```

It uses win-stay, lose-shift except that it defects after at least three opponent actions if the opponent has never cooperated. It improves on the seed but remains below the TFT reference on training. The [database/offline audit](results/pilot_001_audit.json) verifies source hashes, live evaluations, archive membership, and Shinka's best-program record. Four generated files were evaluated, three were valid/archived, and one was invalid; `best/` copies are not additional proposals. Holdout results did not select the winner.

The native read-only wrapper allows broad file reads; it also normally enables web search. This run disabled search and automatic project instructions and requested use of only supplied task/programs/training feedback. Generic native skill/plugin instructions still appeared and are preserved. No file/search/tool call was observed in the successful traces, but confidentiality was not enforced. Accordingly, this is an **unblinded integration pilot**. It neither establishes discovery under hidden information nor separates evolutionary-feedback benefits from LLM prior knowledge.

The [usage records](results/subscription_pilot_001_usage/usage_summary.json) distinguish **five invocations**, **four successful Codex turns**, and **four native model-response usage records**. An invocation can contain multiple model requests. Reported tokens were 50,334 input (15,872 cached) and 4,783 output (3,998 reasoning); cached/reasoning counts are subsets. Headless's $0.1294944 API list-price estimate is not a charge. The account credit balance was unchanged at 90.6853810000, while account-wide subscription usage moved from 1% to 2%; concurrent supervisor use and rounding prevent exclusive attribution. No API-key authentication, paid API fallback, credit purchase, or GitHub Actions was used.

See [the full pilot report](results/PILOT_001.md) for every candidate's diagnosis, the rejected source, commands, failure provenance, access limits, and evidence links.

## Run locally

The reference experiment and tests require only Python 3.10 or later:

```bash
python3 -m unittest discover -s tests -v
python3 baseline.py --output results/baseline_local.json
python3 run_evo.py --preflight
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

All 26 local unit tests and both zero-call preflights passed. Prompts, source snapshots, candidate sources, feedback, failed attempts, usage, configurations, logs, and databases are retained after credential review. The original `initial.py` and evaluator remain unchanged. No GitHub Actions workflows are installed.

## Sources and deviations

1. Robert Axelrod, *The Evolution of Cooperation*, uploaded revised-edition scan: printed p.8 (payoffs); pp.10, 13–16 (horizon, TFT definition, opponent-dependent success); pp.30–33 (first tournament); pp.38–39 (other rules could outperform TFT); pp.41–43 and p.217, chapter 2 note 5 (second tournament stopping rule). We borrow the payoff matrix and stopping probability, but use our own panel, seeds, and normalized scoring. Uploaded PDF SHA-256: `e816ca61aebd84159747d248fedd6d5ff318c471c36bcc31b1ac6bf9aebcd3c1`. The copyrighted PDF is not distributed here.
2. Lange, Imajuku, and Cetin (2025), [*ShinkaEvolve: Towards Open-Ended and Sample-Efficient Program Evolution*](https://arxiv.org/abs/2509.19349), uploaded v1, section 3: archive sampling, LLM mutation, execution/feedback. Uploaded PDF SHA-256: `ee287343c53240126e16a444d5ade2cd0ad0f290a400e78b97a040b93d965087`. The five-proposal, one-model pilot uses a reduced configuration; it does not exercise every mechanism in the paper.
3. Official [SakanaAI/ShinkaEvolve](https://github.com/SakanaAI/ShinkaEvolve/tree/9912af12d423504b8d580f4179fd15f5f88b8c50), pinned commit `9912af12d423504b8d580f4179fd15f5f88b8c50`: inspected `shinka/core/config.py`, `shinka/core/async_runner.py`, `shinka/launch/scheduler.py`, `shinka/llm/constants.py`, `shinka/llm/kwargs.py`, and `pyproject.toml` for the current API and limits.

## Next bounded milestone

Establish and locally verify an enforced mutation information boundary, then run one five-invocation blinded replication using the same model, seed program, interpreter, panels, and payoff-only fitness. Keep the invalid tuple proposal as evidence and do not relax the evaluator in response. Independent replicated seeds and an equal-budget feedback-free control remain later work; neither was added to this first pilot.
