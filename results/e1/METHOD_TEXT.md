## Question and design

E1 asks whether **ShinkaEvolve's combined search procedure improves the
development-holdout payoff of a candidate selected solely by training payoff**,
compared with independent generation from the same model at equal proposal
opportunities. Consistently positive paired differences would support that
hypothesis; negative differences would weaken it; small, inconsistent, or
invalidity-dominated differences would leave the comparison uncertain. There
were three runs planned per condition, not sixty independent experimental replicates.

The [protocol](protocol/PROTOCOL.md), [machine-readable configuration](protocol/protocol.json),
and [source hashes](protocol/freeze.json) were frozen in commit `e0ca3f3` before
calls. The predefined order was **A101, B101, B202, A202, A303, B303**: A first
in two pairs and B first in one, the closest possible balance with three pairs.
Each run had ten proposal opportunities. Local RNG seeds 101, 202, and 303 seed
local search sampling; they do **not** make remote outputs deterministic or
control remote randomness within pairs.

| Common elements | Condition A | Condition B |
|---|---|---|
| Native Shinka full-rewrite prompt/parser, interpreter, evaluator, model, limits, initial policy | Real Shinka weighted parent selection, accumulated programs and training feedback; one top-k inspiration when available | Context sampler returns the original seed and no inspirations at every opportunity |
| Existing ChatGPT Pro via Headless 0.6.1 / Codex 0.153.4; `gpt-5.6-terra`, low reasoning | New native Codex session per proposal | New native Codex session per proposal; byte-identical frozen initial prompt |
| One native proposal-format variant, no retries/resampling/replacements; serial execution | Fitness archive and parent selection influence later information | Common harness stores results but never supplies earlier candidates, scores or validity feedback to later proposals |

A's first prompt in each run equals B's prompt. Both start with the original
always-defect *program*, which is distinct from the random-number seeds:

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 1
# EVOLVE-BLOCK-END
```

The selected candidate is the highest-training-payoff admissible program
within its run, including this seed; exact ties choose the earliest appearance.
“Selected” does not mean it beats reference TFT or grim. All six source identities
were frozen in [training_selections_frozen.json](training_selections_frozen.json)
before holdout evaluation or TFT recognition. This compares evolutionary search
with independent generation; it does **not** isolate numerical feedback alone.

## Game and candidate interface

The candidate receives immutable tuples of its own and its opponent's completed
actions and returns integer `0` (cooperate, C) or `1` (defect, D), never a Boolean.
Both players choose using histories before the current round; their choices
are simultaneous. Histories reset to empty at the start of every match. There
is no action noise, external state, communication, opponent identity, revealed
ending time, or access to the opponent's current action.

| Own action | Other C | Other D |
|---|---:|---:|
| C | 3 | 0 |
| D | 5 | 1 |

The other player's payoff is the transposed entry. Each match independently
ends after a round with probability **0.00346**. The evaluator samples this
geometric length independently before play; candidate actions cannot change
it, and it is hidden from the policy. There is no fixed disclosed final round.

| Panel | Fixed seeds | Realized lengths, reused for each opponent | Matches / rounds |
|---|---|---|---|
| Training | 11, 23, 47, 89, 131 | 174, 747, 126, 25, 110 | 30 / 7,092 |
| Development holdout | 211, 307, 401, 503, 601 | 241, 293, 199, 55, 62 | 30 / 5,100 |

Each opponent plays five matches. Random opponents use reproducible match
streams from the first eight bytes of SHA-256 of `split/opponent/seed`, interpreted
as a big-endian integer. This fixes each scored encounter across policies.

| Panel | Opponent | Rule | Random? |
|---|---|---|---|
| Train | Always cooperate | C every round | No |
| Train | Always defect | D every round | No |
| Train | Fair random | Independent C with probability 0.5 | Yes |
| Train | TFT | C first, then copy the opponent's last action | No |
| Train | Grim trigger | C until any opponent D, then D forever | No |
| Train | Ordinary win-stay, lose-shift (WSLS) | C first; repeat own action after payoff 3 or 5, switch after 0 or 1 | No |
| Holdout | Alternator | C first, alternate C/D | No |
| Holdout | Suspicious TFT | D first, then copy the opponent's last action | No |
| Holdout | TFT for two tats | D only after two consecutive opponent defections; C for the first two rounds | No |
| Holdout | Hard TFT | D if either of the last two available opponent actions was D; C first | No |
| Holdout | Random 20 | Independent C with probability 0.2 | Yes |
| Holdout | Random 80 | Independent C with probability 0.8 | Yes |

Candidates never play one another or themselves. This is **our custom opponent-panel
experiment**, not a reconstruction of Axelrod's tournaments. Fitness is total
own training payoff divided by 7,092 rounds. Opponents have equal aggregate
weight; individual matches are weighted by their length. There is no cooperation,
TFT-similarity, simplicity, or winning-margin bonus. The already-public holdout
is a **development holdout**, not an untouched confirmatory test.

The fixed interpreter accepts one unannotated function, conditionals and returns,
integer constants, history indexes/slices, comparisons, Boolean expressions,
integer `+`, `-`, `%`, `len`, `sum`, `min`, `max`, and history `.count`. It rejects
assignments, loops, imports, literal tuples, arbitrary calls, and outside state.
Limits are 16,000 source bytes and 400 syntax-tree nodes. Code may depend on the
entire history. Evaluation interprets candidate syntax; it never imports or
executes a candidate as arbitrary Python. Invalid proposals receive the fixed
−1 sentinel and cannot be selected. Invalids and duplicates consume their slots.
An AST duplicate ignores formatting/comments and compares with earlier sources
in the same run, including the seed; it is not a claim of behavioral equivalence.

## Information and resource boundaries

The [effective local checks](setup/restriction_checks_verified.json) forced shell,
file-edit, MCP-read, agent-spawn, file-image-read and code-mode calls through the
installed Codex binary against a **localhost-only fixture**. No real model was
queried, no authentication header was sent, every call was refused, and an
outside-directory canary was neither retrieved nor modified. Search and project
instructions were disabled. Tools, MCP, skills, plugins, apps, memory and agents
were disabled with supported per-process controls. Model metadata changed only
`apply_patch_tool_type` to null to remove the file-edit tool registration.
The residual code-mode entrypoints have no nested tools and their host is
disabled. The [implementation audit](setup/IMPLEMENTATION.md) explains the controls
and tests, including the expected fail-closed startup warning.

The supervisor could read experiment files, while fresh mutation sessions
received only generic native instructions plus the permitted task, supplied
programs, training feedback and proposal format. This is an enforced and tested
native tool boundary, **not an OS confidentiality container**. A changed working
directory alone would not suffice. Pretrained knowledge remains; LLM rediscovery
is not knowledge-free invention. The original pilot remains explicitly unblinded.

The separate [E1 ledger](ledger.json) enforces at most 60 external proposal
invocations, ten per run, with reservations before launch, serial execution,
unique slots and fixed order. The exhausted pilot ledger is unchanged. There
is no automatic retry, resampling, replacement, API fallback, API-key
authentication, paid API call, purchased-credit continuation, embedding,
auxiliary model call, or GitHub Actions. Native Codex/Headless/provider bounds
are 180/210/240 seconds, plus 2,600 seconds per run. Quota checks precede launches;
backend failure stops the experiment without resetting counters. Native Headless
does not enforce `max_tokens`; equal proposal budgets are not equal computation.

The primary outcome is selected-candidate development-holdout payoff. Secondary
outcomes are training payoff, validity rate, best-training trajectory and the
appearance time of admissible TFT-compatible behavior. The existing recognition
routine checks 1,640 finite probes; passing alone proves no universal equivalence.
