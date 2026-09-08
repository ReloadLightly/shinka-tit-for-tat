# First real ShinkaEvolve subscription pilot — 2026-09-08

The native Shinka search completed after a configuration repair, within the
original five-invocation allowance. Four candidate files were generated and
evaluated; three were valid and retained. No valid candidate matched the TFT
probes. The final rejected file expresses TFT under ordinary Python semantics,
but contains a forbidden tuple literal and is not an admissible evolved policy.

## Method and failures

The detailed [method and access audit](pilot_001_setup/METHOD.md) records the
pinned upstream provider inspection. Shinka 0.0.7 at commit
`9912af12d423504b8d580f4179fd15f5f88b8c50` used Headless 0.6.1, Codex 0.153.4,
and `headless/codex@gpt-5.6-terra?effort=low` with the existing ChatGPT Pro login.
The original seed, evaluator, panels, payoff matrix, stopping rule, and
payoff-only fitness were unchanged. Search and evaluation were serial; all
auxiliary models, embeddings, retries, resampling, and fallback were disabled.

Invocation 1 failed before a model turn because Codex prohibits overriding
reserved provider ID `openai`. Shinka preserved five failed proposal slots in
[`pilot_001`](pilot_001): the first reached Codex, while the remaining four
were refused by the local stop latch. Only the seed was evaluated and stored.
No generated candidate was lost. The original launcher sources and hashes are
preserved in that run. A zero-call configuration-loading check then validated
the corrected local provider entry, using native ChatGPT authentication and an
explicit subscription endpoint. The one-time repair kept invocation 1 in the
ledger and allowed four remaining invocations in
[`pilot_001_repaired`](pilot_001_repaired). This is one integration milestone
with a repaired launch, not two independent evolutionary replicates.

This is an **unblinded integration pilot**. The native wrapper grants broad
read-only file access, and merely changing directories does not hide the
repository. This run disabled web search and automatic project instructions;
explicit prompts supplied the permitted task, generated programs, and training
feedback. Codex still injected generic skill, plugin, and agent instructions,
which are preserved in `native_context.json`. No file/search/tool call was
observed in any of the four successful sessions. This observation does not
establish enforced blinding, nor exclude model prior knowledge.

## Every generated candidate

Generation numbers below belong to the repaired run. Training/holdout means
use the unchanged 7,092/5,100 total rounds. Selection was frozen by training
payoff before recognition and holdout diagnostics.

| External invocation | Generation / generated name | Training | Holdout | Live outcome |
|---|---|---:|---:|---|
| — | 0 / original defection seed | 2.331077 | 2.001569 | Valid, archived |
| 2 | [1 / guarded_win_stay](pilot_001_repaired/gen_1/main.py) | **2.533136** | **2.444314** | Valid, archived, Shinka best |
| 3 | [2 / adaptive_probe_tft](pilot_001_repaired/gen_2/main.py) | 1.966159 | 2.187647 | Valid, archived |
| 4 | [3 / echo_probe](pilot_001_repaired/gen_3/main.py) | 2.226029 | 2.255098 | Valid, archived |
| 5 | [4 / forgiving_tft](pilot_001_repaired/gen_4/main.py) | -1 validity sentinel | Not run | Invalid, stored in DB, excluded from archive |

- **Generation 1:** win-stay, lose-shift with a guard: after at least three
  opponent actions, defect if the opponent has never cooperated. Otherwise
  repeat own action after opponent cooperation and flip it after defection.
  It fails the TFT probes, including history `own=(1,), opponent=(0,)` where it
  returns 1 and TFT returns 0. It improves the seed but falls slightly below the
  pre-existing TFT reference's training payoff, 2.536238.
- **Generation 2:** cooperates for four rounds, periodically defects against
  an opponent that has always cooperated, and otherwise uses a forgiving
  retaliation rule. Its generated name contains TFT, but names are not
  recognition evidence. After `own=(0,), opponent=(1,)` it returns 0 instead
  of TFT's 1. Its training payoff is below the seed.
- **Generation 3:** combines early cooperation, a defection probe, an
  opponent-echo condition, and retaliation. After three mutual cooperations it
  defects; TFT cooperates. It also scores below the seed.
- **Generation 4:** its AST has 50 nodes; the unsupported node is `Tuple` in
  `(1, 1, 1)`. The fixed interpreter rejects it before match simulation, and
  both live and offline checks agree. Its full source is preserved below.
  Static inspection shows the three-defection branch is redundant: if the
  last three opponent actions are 1, the last opponent action is already 1.
  Thus, for finite binary histories, this ordinary Python expression is TFT.
  The model's prose claim of "permanent defection" is false: an ensuing
  cooperation would be copied. No candidate import, `exec`, syntax repair, or
  extra live proposal was used to obtain this conclusion. It cannot count as
  an evaluator-valid TFT rediscovery.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else 1 if len(opponent_history) > 2 and opponent_history[-3:] == (1, 1, 1) else opponent_history[-1]
# EVOLVE-BLOCK-END
```

Each valid mutation failed at least one of the 1,640 TFT probes. Finite probe
agreement would not by itself prove equivalence on every history; the rejected
source's equivalence observation above is a separate, narrow source argument.

## Payoff-selected policy: complete executable source

Shinka's `best_program_id` is `da4c43bd-228f-4da9-b5ab-7e756c217185`, generation 1.
The source SHA-256 is
`6f8f8b32a1fcd9c6507551f57d2c847d66fe5e029e173ecd59e86c6d1d9a751b`.
Its database source, canonical file, saved evaluation, and offline rescore agree.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else 1 if len(opponent_history) > 2 and opponent_history.count(0) == 0 else own_history[-1] if opponent_history[-1] == 0 else 1 - own_history[-1]
# EVOLVE-BLOCK-END
```

The [database and offline audit](pilot_001_audit.json) verifies five repaired-run
program rows, four archive members including the seed, and the payoff-selected
winner. Four generated files and four model response files are present. The
invalid fourth proposal has a database row with `correct=false`, but no archive
membership. The copied `best/` files are not additional proposals.

## Usage and verification

The [usage ledger](subscription_pilot_001_usage/invocations.json) records five
external proposal launches: one pre-model configuration failure and four
successful sessions. There are four Codex `turn.completed` events and four
native model-response usage records, each with a distinct response ID. These
are separate counts: an invocation can contain multiple internal model turns.

Codex reports 50,334 input tokens, including 15,872 cached input tokens, and
4,783 output tokens, including 3,998 reasoning tokens. Do not add subset counts
again. Headless/Shinka record an **API list-price estimate** of $0.1294944; it is
not a bill or subscription charge. The reported credit balance stayed exactly
90.6853810000 before and after. Account-wide subscription usage moved from 1%
to 2%; integer rounding and concurrent supervisor usage prevent assigning that
entire change to this pilot. No credit purchase/continuation, API-key request,
API fallback, or GitHub Actions workflow was used. See the
[usage summary](subscription_pilot_001_usage/usage_summary.json).

All 26 unit tests passed before launch and after the configuration repair; both
zero-call preflights passed. The complete evidence includes prompts, native
context and usage, Codex/Headless outputs, all failure records, source snapshots,
environment versions, configurations, evaluation logs, and SQLite databases.

Commands executed, after inspecting GitHub and installing the pinned dependency:

```bash
uv venv .venv
uv pip install --python .venv/bin/python -r requirements-shinka.txt
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python run_evo.py --preflight
timeout --signal=INT --kill-after=15s 1500s .venv/bin/python run_evo.py --execute --mutations 5 --results-dir results/pilot_001
# Configuration failure preserved; one invocation consumed, no model turn.
timeout --signal=INT --kill-after=15s 1200s .venv/bin/python run_evo.py --execute --mutations 4 --continue-after-config-failure --results-dir results/pilot_001_repaired
.venv/bin/python audit_pilot.py --run results/pilot_001 --run results/pilot_001_repaired --usage-dir results/subscription_pilot_001_usage --output results/pilot_001_audit.json
.venv/bin/python subscription_status.py --output results/subscription_pilot_001_usage/subscription_after.json
```

## Interpretation and next bounded experiment

The real native search loop and subscription integration work. This small run
produced an improved admissible policy and a rejected TFT expression; it did
not produce a valid TFT-compatible archive member. There is no basis for
attributing an outcome specifically to evolutionary feedback or claiming
knowledge-free invention, historical tournament replication, or a global
optimum.

Next, establish and locally test an enforced mutation information boundary,
then run **one five-invocation blinded replication** with this same model,
seed, interpreter, panels, and fitness. Retain the tuple rejection as a real
failure; do not relax the evaluator in response. A feedback-free control and
multiple independent seeds remain later work, not additional conditions in
this milestone.
