# Shinka Tit-for-Tat

**Can ShinkaEvolve generate tit-for-tat behavior when selection rewards only a player's own payoff in the iterated Prisoner's Dilemma?**

## Abstract

This project tests operational rediscovery of tit-for-tat (TFT) with LLM-guided program evolution. Starting from unconditional defection, ShinkaEvolve may change a deterministic policy that observes both players' past actions. A fixed evaluator returns average own payoff against a frozen opponent panel. Identification of TFT is a separate post-search analysis and supplies no fitness bonus. The environment, payoff matrix, observations, opponents, stopping rule, and evaluator are outside candidate control.

**Status, 2026-09-08:** reference experiments, exhaustive comparison of 32 deterministic memory-one policies, and zero-call preflight have run. No ShinkaEvolve mutation has run in this environment: the dependency and API credential are absent. The live launcher uses the inspected, pinned upstream API, but its live integration remains untested here. This is a small prospective pilot, not a reconstruction of either historical Axelrod tournament.

## Research question and predictions

Record three distinct outcomes: whether TFT-compatible behavior appears in any generated valid candidate; whether it is the best candidate under training payoff; and how the payoff-selected candidate performs on held-out encounters. A non-TFT winner is an informative outcome, not grounds to change opponents until TFT wins.

An LLM may already know TFT. Recovering its behavior demonstrates operational rediscovery under this interface, not invention from an uninformed prior. This first five-proposal pilot cannot attribute success specifically to evolutionary feedback. That claim needs multiple independent runs and a same-model, equal-budget control receiving no evolutionary feedback. Exhaustive enumeration below is a comparator, not that control.

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
| `initial.py` | Evolved program; initially always defects |
| `environment.py` | Fixed game, opponents, seeds, horizons, and payoff measurement |
| `policy.py` | Validates and interprets candidate decision code without executing arbitrary Python |
| `evaluate.py` | Shinka adapter; writes payoff-only `metrics.json` and validity `correct.json` |
| `task_prompt.txt` | Exact task-specific model instruction; contains no target strategy or opponent names |
| `run_evo.py` | Zero-call preflight and real upstream ShinkaEvolve launcher |
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

Evidence: [`results/baseline.json`](results/baseline.json), [`results/preflight.json`](results/preflight.json), and [`results/tests.txt`](results/tests.txt). The baseline records source hashes, individual matches, and all 32 comparator scores. Zero API calls were made; there is no evolved policy or live archive yet.

## Run locally

The reference experiment and tests require only Python 3.10 or later:

```bash
python3 -m unittest discover -s tests -v
python3 baseline.py --output results/baseline_local.json
python3 run_evo.py --preflight
```

Each baseline/report command refuses to overwrite its existing evidence file. Choose a new output name for another run.

For the actual ShinkaEvolve pilot, create a local environment and install the pinned dependency. `OPENAI_API_KEY` must be exported in your local shell; never commit the credential.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-shinka.txt
python run_evo.py --preflight
python run_evo.py --execute --mutations 5 --max-api-cost 0.50 --results-dir results/pilot_001
python analyze_archive.py --results-dir results/pilot_001 --output results/pilot_001/diagnostics.json
```

The pilot uses `gpt-5-mini`, five mutation proposals plus the initial seed (six Shinka generations), one concurrent proposal/evaluation, and 4,096 maximum output tokens per request. Provider retry controls are bounded; embeddings, novelty calls, meta calls, and prompt evolution are disabled. The **$0.50 setting is a soft scheduling threshold, not a hard spending cap**: an in-flight call can exceed it. The default command makes zero model calls; `--execute` launches paid calls. Shinka is pinned by Git commit, while transitive dependencies are recorded with `pip freeze` for each launch rather than fully locked.

Inspect rejected candidates and logs as well as successful outputs. A completed runner does not prove rediscovery. Archive diagnostics are a separate rescore of generated files; they must not be mistaken for proof of what the live database evaluated or retained. The launcher records source hashes, search seed, environment, and status. Remote model outputs need not reproduce bit-for-bit even with identical seeds. Before sharing live results, review logs and preserve prompts, generated sources, validity, scores, and costs. No GitHub Actions workflows are installed.

## Sources and deviations

1. Robert Axelrod, *The Evolution of Cooperation*, uploaded revised-edition scan: printed p.8 (payoffs); pp.10, 13–16 (horizon, TFT definition, opponent-dependent success); pp.30–33 (first tournament); pp.38–39 (other rules could outperform TFT); pp.41–43 and p.217, chapter 2 note 5 (second tournament stopping rule). We borrow the payoff matrix and stopping probability, but use our own panel, seeds, and normalized scoring. Uploaded PDF SHA-256: `e816ca61aebd84159747d248fedd6d5ff318c471c36bcc31b1ac6bf9aebcd3c1`. The copyrighted PDF is not distributed here.
2. Lange, Imajuku, and Cetin (2025), [*ShinkaEvolve: Towards Open-Ended and Sample-Efficient Program Evolution*](https://arxiv.org/abs/2509.19349), uploaded v1, section 3: archive sampling, LLM mutation, execution/feedback. Uploaded PDF SHA-256: `ee287343c53240126e16a444d5ade2cd0ad0f290a400e78b97a040b93d965087`. The five-proposal, one-model pilot uses a reduced configuration; it does not exercise every mechanism in the paper.
3. Official [SakanaAI/ShinkaEvolve](https://github.com/SakanaAI/ShinkaEvolve/tree/9912af12d423504b8d580f4179fd15f5f88b8c50), pinned commit `9912af12d423504b8d580f4179fd15f5f88b8c50`: inspected `shinka/core/config.py`, `shinka/core/async_runner.py`, `shinka/launch/scheduler.py`, `shinka/llm/constants.py`, `shinka/llm/kwargs.py`, and `pyproject.toml` for the current API and limits.

## Next bounded milestone

Run the five-proposal live pilot in a configured environment, preserve the archive, and inspect every valid candidate. Report whether TFT-compatible behavior appeared, its training payoff and generation, the payoff-selected winner, and holdout performance. Only after that decide whether the experiment warrants replicated search and no-feedback controls. The result may be TFT, a TFT variant, another strategy, or no useful mutation.
