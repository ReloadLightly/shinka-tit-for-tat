# Every E1 proposal opportunity

There were 60 planned opportunities nested in six runs, not 60 independent experimental replicates. E1 stopped at 44 external proposals: four complete runs, A303 incomplete, B303 unstarted. Unattempted opportunities and a prelaunch block are not invalid programs or zero-payoff observations. Slot 0 is the unchanged seed. Validity and payoff are fixed-evaluator results. An AST duplicate ignores formatting/comments and compares with earlier sources in the same run, including seed; it consumes its slot. Archive means actual final SQLite archive membership, separate from a generated file or database row. Full-precision context scores below are archival values; native prompts format payoff to two decimals. Use the prompt links to inspect exactly what the proposer received.

## A101 — complete

| Slot | Source | Parent | Inspirations | Validity | Training | Best so far | New best | AST duplicate of | Archived |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | [slot 1](runs/A101/gen_1/main.py) | 0 | none | valid | 2.536238 | 2.536238 | yes | — | yes |
| 2 | [slot 2](runs/A101/gen_2/main.py) | 1 | 0 | valid | 2.095601 | 2.536238 | no | — | yes |
| 3 | [slot 3](runs/A101/gen_3/main.py) | 1 | 0 | valid | 2.459250 | 2.536238 | no | — | yes |
| 4 | [slot 4](runs/A101/gen_4/main.py) | 3 | 1 | valid | 2.451072 | 2.536238 | no | — | yes |
| 5 | [slot 5](runs/A101/gen_5/main.py) | 4 | 1 | valid | 2.536238 | 2.536238 | no | 1 | yes |
| 6 | [slot 6](runs/A101/gen_6/main.py) | 5 | 1 | valid | 2.319515 | 2.536238 | no | — | yes |
| 7 | [slot 7](runs/A101/gen_7/main.py) | 1 | 5 | valid | 2.536238 | 2.536238 | no | — | yes |
| 8 | [slot 8](runs/A101/gen_8/main.py) | 7 | 1 | valid | 2.474055 | 2.536238 | no | — | yes |
| 9 | [slot 9](runs/A101/gen_9/main.py) | 1 | 5 | valid | 2.535110 | 2.536238 | no | — | yes |
| 10 | [slot 10](runs/A101/gen_10/main.py) | 9 | 1 | valid | 1.958263 | 2.536238 | no | — | yes |

### A101, proposal 1

[Exact rendered prompt](runs/A101/invocations/01/prompt.md) · [native output](runs/A101/invocations/01/codex.jsonl) · [supplied context](runs/A101/gen_1/supplied_context.json) · [evaluation records](runs/A101/gen_1/results/).

Training: **2.536238**; validity: **True**; current best: 2.536238; database rows: 1.

Source size: 152 bytes; 23 AST nodes (limits 16,000 bytes / 400 nodes).

Frozen TFT probes: **pass**, 1640 checks, computed after the terminal selection freeze. Finite agreement alone is not equivalence.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else opponent_history[-1]
# EVOLVE-BLOCK-END
```

**Parent: generation 0**, training 2.331077; public feedback `{"mean_payoff": 2.3310772701635645}`; text feedback ``.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 1
# EVOLVE-BLOCK-END
```

### A101, proposal 2

[Exact rendered prompt](runs/A101/invocations/02/prompt.md) · [native output](runs/A101/invocations/02/codex.jsonl) · [supplied context](runs/A101/gen_2/supplied_context.json) · [evaluation records](runs/A101/gen_2/results/).

Training: **2.095601**; validity: **True**; current best: 2.536238; database rows: 1.

Source size: 427 bytes; 122 AST nodes (limits 16,000 bytes / 400 nodes).

Frozen TFT probes: **fail**, 1640 checks, computed after the terminal selection freeze. Finite agreement alone is not equivalence.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else (1 if len(opponent_history) >= 3 and opponent_history[-3:].count(1) == 3 else (1 if opponent_history[-1] == 1 and own_history[-1] == 0 else (0 if opponent_history[-1] == 1 else (1 if len(opponent_history) >= 4 and opponent_history[-4:].count(0) == 4 and own_history[-4:].count(0) == 4 else 0))))
# EVOLVE-BLOCK-END
```

**Parent: generation 1**, training 2.536238; public feedback `{"mean_payoff": 2.5362380146644106}`; text feedback ``.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else opponent_history[-1]
# EVOLVE-BLOCK-END
```

**Inspiration: generation 0**, training 2.331077; public feedback `{"mean_payoff": 2.3310772701635645}`; text feedback ``.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 1
# EVOLVE-BLOCK-END
```

### A101, proposal 3

[Exact rendered prompt](runs/A101/invocations/03/prompt.md) · [native output](runs/A101/invocations/03/codex.jsonl) · [supplied context](runs/A101/gen_3/supplied_context.json) · [evaluation records](runs/A101/gen_3/results/).

Training: **2.459250**; validity: **True**; current best: 2.536238; database rows: 1.

Source size: 374 bytes; 94 AST nodes (limits 16,000 bytes / 400 nodes).

Frozen TFT probes: **fail**, 1640 checks, computed after the terminal selection freeze. Finite agreement alone is not equivalence.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else (1 if len(opponent_history) >= 12 and opponent_history.count(0) == len(opponent_history) else (0 if opponent_history[-1] == 1 and own_history[-1] == 1 and opponent_history[:-1].count(0) == len(opponent_history) - 1 else opponent_history[-1]))
# EVOLVE-BLOCK-END
```

**Parent: generation 1**, training 2.536238; public feedback `{"mean_payoff": 2.5362380146644106}`; text feedback ``.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else opponent_history[-1]
# EVOLVE-BLOCK-END
```

**Inspiration: generation 0**, training 2.331077; public feedback `{"mean_payoff": 2.3310772701635645}`; text feedback ``.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 1
# EVOLVE-BLOCK-END
```

### A101, proposal 4

[Exact rendered prompt](runs/A101/invocations/04/prompt.md) · [native output](runs/A101/invocations/04/codex.jsonl) · [supplied context](runs/A101/gen_4/supplied_context.json) · [evaluation records](runs/A101/gen_4/results/).

Training: **2.451072**; validity: **True**; current best: 2.536238; database rows: 1.

Source size: 180 bytes; 35 AST nodes (limits 16,000 bytes / 400 nodes).

Frozen TFT probes: **fail**, 1640 checks, computed after the terminal selection freeze. Finite agreement alone is not equivalence.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(own_history) == 0 else (0 if own_history[-1] == opponent_history[-1] else 1)
# EVOLVE-BLOCK-END
```

**Parent: generation 3**, training 2.459250; public feedback `{"mean_payoff": 2.459249858996052}`; text feedback ``.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else (1 if len(opponent_history) >= 12 and opponent_history.count(0) == len(opponent_history) else (0 if opponent_history[-1] == 1 and own_history[-1] == 1 and opponent_history[:-1].count(0) == len(opponent_history) - 1 else opponent_history[-1]))
# EVOLVE-BLOCK-END
```

**Inspiration: generation 1**, training 2.536238; public feedback `{"mean_payoff": 2.5362380146644106}`; text feedback ``.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else opponent_history[-1]
# EVOLVE-BLOCK-END
```

### A101, proposal 5

[Exact rendered prompt](runs/A101/invocations/05/prompt.md) · [native output](runs/A101/invocations/05/codex.jsonl) · [supplied context](runs/A101/gen_5/supplied_context.json) · [evaluation records](runs/A101/gen_5/results/).

Training: **2.536238**; validity: **True**; current best: 2.536238; database rows: 1.

Source size: 152 bytes; 23 AST nodes (limits 16,000 bytes / 400 nodes).

Frozen TFT probes: **pass**, 1640 checks, computed after the terminal selection freeze. Finite agreement alone is not equivalence.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else opponent_history[-1]
# EVOLVE-BLOCK-END
```

**Parent: generation 4**, training 2.451072; public feedback `{"mean_payoff": 2.4510716300056403}`; text feedback ``.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(own_history) == 0 else (0 if own_history[-1] == opponent_history[-1] else 1)
# EVOLVE-BLOCK-END
```

**Inspiration: generation 1**, training 2.536238; public feedback `{"mean_payoff": 2.5362380146644106}`; text feedback ``.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else opponent_history[-1]
# EVOLVE-BLOCK-END
```

### A101, proposal 6

[Exact rendered prompt](runs/A101/invocations/06/prompt.md) · [native output](runs/A101/invocations/06/codex.jsonl) · [supplied context](runs/A101/gen_6/supplied_context.json) · [evaluation records](runs/A101/gen_6/results/).

Training: **2.319515**; validity: **True**; current best: 2.536238; database rows: 1.

Source size: 287 bytes; 46 AST nodes (limits 16,000 bytes / 400 nodes).

Frozen TFT probes: **fail**, 1640 checks, computed after the terminal selection freeze. Finite agreement alone is not equivalence.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    if len(opponent_history) == 0:
        return 1
    elif len(opponent_history) == 1:
        return 0
    elif opponent_history[1] == 0:
        return 1
    else:
        return opponent_history[-1]
# EVOLVE-BLOCK-END
```

**Parent: generation 5**, training 2.536238; public feedback `{"mean_payoff": 2.5362380146644106}`; text feedback ``.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else opponent_history[-1]
# EVOLVE-BLOCK-END
```

**Inspiration: generation 1**, training 2.536238; public feedback `{"mean_payoff": 2.5362380146644106}`; text feedback ``.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else opponent_history[-1]
# EVOLVE-BLOCK-END
```

### A101, proposal 7

[Exact rendered prompt](runs/A101/invocations/07/prompt.md) · [native output](runs/A101/invocations/07/codex.jsonl) · [supplied context](runs/A101/gen_7/supplied_context.json) · [evaluation records](runs/A101/gen_7/results/).

Training: **2.536238**; validity: **True**; current best: 2.536238; database rows: 1.

Source size: 212 bytes; 50 AST nodes (limits 16,000 bytes / 400 nodes).

Frozen TFT probes: **pass**, 1640 checks, computed after the terminal selection freeze. Finite agreement alone is not equivalence.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(own_history) == 0 else (own_history[-1] if own_history[-1] == opponent_history[-1] else 1 - own_history[-1])
# EVOLVE-BLOCK-END
```

**Parent: generation 1**, training 2.536238; public feedback `{"mean_payoff": 2.5362380146644106}`; text feedback ``.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else opponent_history[-1]
# EVOLVE-BLOCK-END
```

**Inspiration: generation 5**, training 2.536238; public feedback `{"mean_payoff": 2.5362380146644106}`; text feedback ``.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else opponent_history[-1]
# EVOLVE-BLOCK-END
```

### A101, proposal 8

[Exact rendered prompt](runs/A101/invocations/08/prompt.md) · [native output](runs/A101/invocations/08/codex.jsonl) · [supplied context](runs/A101/gen_8/supplied_context.json) · [evaluation records](runs/A101/gen_8/results/).

Training: **2.474055**; validity: **True**; current best: 2.536238; database rows: 1.

Source size: 200 bytes; 41 AST nodes (limits 16,000 bytes / 400 nodes).

Frozen TFT probes: **fail**, 1640 checks, computed after the terminal selection freeze. Finite agreement alone is not equivalence.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) < 2 else (1 if opponent_history[-1] == 1 and opponent_history[-2] == 1 else 0)
# EVOLVE-BLOCK-END
```

**Parent: generation 7**, training 2.536238; public feedback `{"mean_payoff": 2.5362380146644106}`; text feedback ``.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(own_history) == 0 else (own_history[-1] if own_history[-1] == opponent_history[-1] else 1 - own_history[-1])
# EVOLVE-BLOCK-END
```

**Inspiration: generation 1**, training 2.536238; public feedback `{"mean_payoff": 2.5362380146644106}`; text feedback ``.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else opponent_history[-1]
# EVOLVE-BLOCK-END
```

### A101, proposal 9

[Exact rendered prompt](runs/A101/invocations/09/prompt.md) · [native output](runs/A101/invocations/09/codex.jsonl) · [supplied context](runs/A101/gen_9/supplied_context.json) · [evaluation records](runs/A101/gen_9/results/).

Training: **2.535110**; validity: **True**; current best: 2.536238; database rows: 1.

Source size: 151 bytes; 23 AST nodes (limits 16,000 bytes / 400 nodes).

Frozen TFT probes: **fail**, 1640 checks, computed after the terminal selection freeze. Finite agreement alone is not equivalence.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) < 2 else opponent_history[-1]
# EVOLVE-BLOCK-END
```

**Parent: generation 1**, training 2.536238; public feedback `{"mean_payoff": 2.5362380146644106}`; text feedback ``.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else opponent_history[-1]
# EVOLVE-BLOCK-END
```

**Inspiration: generation 5**, training 2.536238; public feedback `{"mean_payoff": 2.5362380146644106}`; text feedback ``.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else opponent_history[-1]
# EVOLVE-BLOCK-END
```

### A101, proposal 10

[Exact rendered prompt](runs/A101/invocations/10/prompt.md) · [native output](runs/A101/invocations/10/codex.jsonl) · [supplied context](runs/A101/gen_10/supplied_context.json) · [evaluation records](runs/A101/gen_10/results/).

Training: **1.958263**; validity: **True**; current best: 2.536238; database rows: 1.

Source size: 310 bytes; 73 AST nodes (limits 16,000 bytes / 400 nodes).

Frozen TFT probes: **fail**, 1640 checks, computed after the terminal selection freeze. Finite agreement alone is not equivalence.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else (1 if opponent_history.count(1) == 0 and len(opponent_history) % 20 == 0 else (1 if len(opponent_history) > 1 and opponent_history[-1] == 1 and opponent_history[-2] == 1 else 0))
# EVOLVE-BLOCK-END
```

**Parent: generation 9**, training 2.535110; public feedback `{"mean_payoff": 2.535109983079526}`; text feedback ``.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) < 2 else opponent_history[-1]
# EVOLVE-BLOCK-END
```

**Inspiration: generation 1**, training 2.536238; public feedback `{"mean_payoff": 2.5362380146644106}`; text feedback ``.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else opponent_history[-1]
# EVOLVE-BLOCK-END
```

## B101 — complete

| Slot | Source | Parent | Inspirations | Validity | Training | Best so far | New best | AST duplicate of | Archived |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | [slot 1](runs/B101/gen_1/main.py) | 0 | none | valid | 2.536238 | 2.536238 | yes | — | yes |
| 2 | [slot 2](runs/B101/gen_2/main.py) | 0 | none | valid | 2.536238 | 2.536238 | no | — | yes |
| 3 | [slot 3](runs/B101/gen_3/main.py) | 0 | none | evaluation_missing | unavailable | 2.536238 | no | — | no |
| 4 | [slot 4](runs/B101/gen_4/main.py) | 0 | none | valid | 2.536238 | 2.536238 | no | 1 | yes |
| 5 | [slot 5](runs/B101/gen_5/main.py) | 0 | none | valid | 2.536238 | 2.536238 | no | 2 | yes |
| 6 | [slot 6](runs/B101/gen_6/main.py) | 0 | none | valid | 2.536238 | 2.536238 | no | 1 | yes |
| 7 | [slot 7](runs/B101/gen_7/main.py) | 0 | none | valid | 2.536238 | 2.536238 | no | 1 | yes |
| 8 | [slot 8](runs/B101/gen_8/main.py) | 0 | none | valid | 2.536238 | 2.536238 | no | 2 | yes |
| 9 | [slot 9](runs/B101/gen_9/main.py) | 0 | none | valid | 2.536238 | 2.536238 | no | 1 | yes |
| 10 | [slot 10](runs/B101/gen_10/main.py) | 0 | none | valid | 1.897208 | 2.536238 | no | — | yes |

### B101, proposal 1

[Exact rendered prompt](runs/B101/invocations/01/prompt.md) · [native output](runs/B101/invocations/01/codex.jsonl) · [supplied context](runs/B101/gen_1/supplied_context.json) · [evaluation records](runs/B101/gen_1/results/).

Training: **2.536238**; validity: **True**; current best: 2.536238; database rows: 1.

Source size: 152 bytes; 23 AST nodes (limits 16,000 bytes / 400 nodes).

Frozen TFT probes: **pass**, 1640 checks, computed after the terminal selection freeze. Finite agreement alone is not equivalence.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else opponent_history[-1]
# EVOLVE-BLOCK-END
```

Fresh session; unchanged seed-only information. The backend enforces byte equality with the [frozen initial prompt](protocol/initial_prompt.md), and the native-session audit checks the only user message against that prompt. No prior candidate, score, validity, recognition, or holdout result is supplied.

### B101, proposal 2

[Exact rendered prompt](runs/B101/invocations/02/prompt.md) · [native output](runs/B101/invocations/02/codex.jsonl) · [supplied context](runs/B101/gen_2/supplied_context.json) · [evaluation records](runs/B101/gen_2/results/).

Training: **2.536238**; validity: **True**; current best: 2.536238; database rows: 1.

Source size: 167 bytes; 24 AST nodes (limits 16,000 bytes / 400 nodes).

Frozen TFT probes: **pass**, 1640 checks, computed after the terminal selection freeze. Finite agreement alone is not equivalence.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    if len(opponent_history) == 0:
        return 0
    return opponent_history[-1]
# EVOLVE-BLOCK-END
```

Fresh session; unchanged seed-only information. The backend enforces byte equality with the [frozen initial prompt](protocol/initial_prompt.md), and the native-session audit checks the only user message against that prompt. No prior candidate, score, validity, recognition, or holdout result is supplied.

### B101, proposal 3

[Exact rendered prompt](runs/B101/invocations/03/prompt.md) · [native output](runs/B101/invocations/03/codex.jsonl) · [supplied context](runs/B101/gen_3/supplied_context.json) · [evaluation records](runs/B101/gen_3/results/).

Training: **unavailable**; validity: **False**; current best: 2.536238; database rows: 1.

Rejection/failure: `No evaluator result`. Unsupported AST types: []. No repair or replacement.

Source size: 375 bytes; 67 AST nodes (limits 16,000 bytes / 400 nodes).

Post-stop interpreter diagnosis: admissible, training payoff 2.295967. This is not a live evaluator result and did not alter selection or archive membership. Shinka's database failure score 0 is not measured payoff.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    if len(opponent_history) < 4:
        return 0
    elif len(opponent_history) == 4:
        return 1
    elif len(opponent_history) == 5:
        return 1 if opponent_history[4] == 0 else 0
    elif opponent_history[4] == 0:
        return 1
    else:
        return opponent_history[-1]
# EVOLVE-BLOCK-END
```

Fresh session; unchanged seed-only information. The backend enforces byte equality with the [frozen initial prompt](protocol/initial_prompt.md), and the native-session audit checks the only user message against that prompt. No prior candidate, score, validity, recognition, or holdout result is supplied.

### B101, proposal 4

[Exact rendered prompt](runs/B101/invocations/04/prompt.md) · [native output](runs/B101/invocations/04/codex.jsonl) · [supplied context](runs/B101/gen_4/supplied_context.json) · [evaluation records](runs/B101/gen_4/results/).

Training: **2.536238**; validity: **True**; current best: 2.536238; database rows: 1.

Source size: 152 bytes; 23 AST nodes (limits 16,000 bytes / 400 nodes).

Frozen TFT probes: **pass**, 1640 checks, computed after the terminal selection freeze. Finite agreement alone is not equivalence.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else opponent_history[-1]
# EVOLVE-BLOCK-END
```

Fresh session; unchanged seed-only information. The backend enforces byte equality with the [frozen initial prompt](protocol/initial_prompt.md), and the native-session audit checks the only user message against that prompt. No prior candidate, score, validity, recognition, or holdout result is supplied.

### B101, proposal 5

[Exact rendered prompt](runs/B101/invocations/05/prompt.md) · [native output](runs/B101/invocations/05/codex.jsonl) · [supplied context](runs/B101/gen_5/supplied_context.json) · [evaluation records](runs/B101/gen_5/results/).

Training: **2.536238**; validity: **True**; current best: 2.536238; database rows: 1.

Source size: 167 bytes; 24 AST nodes (limits 16,000 bytes / 400 nodes).

Frozen TFT probes: **pass**, 1640 checks, computed after the terminal selection freeze. Finite agreement alone is not equivalence.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    if len(opponent_history) == 0:
        return 0
    return opponent_history[-1]
# EVOLVE-BLOCK-END
```

Fresh session; unchanged seed-only information. The backend enforces byte equality with the [frozen initial prompt](protocol/initial_prompt.md), and the native-session audit checks the only user message against that prompt. No prior candidate, score, validity, recognition, or holdout result is supplied.

### B101, proposal 6

[Exact rendered prompt](runs/B101/invocations/06/prompt.md) · [native output](runs/B101/invocations/06/codex.jsonl) · [supplied context](runs/B101/gen_6/supplied_context.json) · [evaluation records](runs/B101/gen_6/results/).

Training: **2.536238**; validity: **True**; current best: 2.536238; database rows: 1.

Source size: 152 bytes; 23 AST nodes (limits 16,000 bytes / 400 nodes).

Frozen TFT probes: **pass**, 1640 checks, computed after the terminal selection freeze. Finite agreement alone is not equivalence.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else opponent_history[-1]
# EVOLVE-BLOCK-END
```

Fresh session; unchanged seed-only information. The backend enforces byte equality with the [frozen initial prompt](protocol/initial_prompt.md), and the native-session audit checks the only user message against that prompt. No prior candidate, score, validity, recognition, or holdout result is supplied.

### B101, proposal 7

[Exact rendered prompt](runs/B101/invocations/07/prompt.md) · [native output](runs/B101/invocations/07/codex.jsonl) · [supplied context](runs/B101/gen_7/supplied_context.json) · [evaluation records](runs/B101/gen_7/results/).

Training: **2.536238**; validity: **True**; current best: 2.536238; database rows: 1.

Source size: 152 bytes; 23 AST nodes (limits 16,000 bytes / 400 nodes).

Frozen TFT probes: **pass**, 1640 checks, computed after the terminal selection freeze. Finite agreement alone is not equivalence.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else opponent_history[-1]
# EVOLVE-BLOCK-END
```

Fresh session; unchanged seed-only information. The backend enforces byte equality with the [frozen initial prompt](protocol/initial_prompt.md), and the native-session audit checks the only user message against that prompt. No prior candidate, score, validity, recognition, or holdout result is supplied.

### B101, proposal 8

[Exact rendered prompt](runs/B101/invocations/08/prompt.md) · [native output](runs/B101/invocations/08/codex.jsonl) · [supplied context](runs/B101/gen_8/supplied_context.json) · [evaluation records](runs/B101/gen_8/results/).

Training: **2.536238**; validity: **True**; current best: 2.536238; database rows: 1.

Source size: 167 bytes; 24 AST nodes (limits 16,000 bytes / 400 nodes).

Frozen TFT probes: **pass**, 1640 checks, computed after the terminal selection freeze. Finite agreement alone is not equivalence.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    if len(opponent_history) == 0:
        return 0
    return opponent_history[-1]
# EVOLVE-BLOCK-END
```

Fresh session; unchanged seed-only information. The backend enforces byte equality with the [frozen initial prompt](protocol/initial_prompt.md), and the native-session audit checks the only user message against that prompt. No prior candidate, score, validity, recognition, or holdout result is supplied.

### B101, proposal 9

[Exact rendered prompt](runs/B101/invocations/09/prompt.md) · [native output](runs/B101/invocations/09/codex.jsonl) · [supplied context](runs/B101/gen_9/supplied_context.json) · [evaluation records](runs/B101/gen_9/results/).

Training: **2.536238**; validity: **True**; current best: 2.536238; database rows: 1.

Source size: 152 bytes; 23 AST nodes (limits 16,000 bytes / 400 nodes).

Frozen TFT probes: **pass**, 1640 checks, computed after the terminal selection freeze. Finite agreement alone is not equivalence.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else opponent_history[-1]
# EVOLVE-BLOCK-END
```

Fresh session; unchanged seed-only information. The backend enforces byte equality with the [frozen initial prompt](protocol/initial_prompt.md), and the native-session audit checks the only user message against that prompt. No prior candidate, score, validity, recognition, or holdout result is supplied.

### B101, proposal 10

[Exact rendered prompt](runs/B101/invocations/10/prompt.md) · [native output](runs/B101/invocations/10/codex.jsonl) · [supplied context](runs/B101/gen_10/supplied_context.json) · [evaluation records](runs/B101/gen_10/results/).

Training: **1.897208**; validity: **True**; current best: 2.536238; database rows: 1.

Source size: 232 bytes; 51 AST nodes (limits 16,000 bytes / 400 nodes).

Frozen TFT probes: **fail**, 1640 checks, computed after the terminal selection freeze. Finite agreement alone is not equivalence.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 1 if len(opponent_history) == 0 else (0 if opponent_history[-1] == 0 or (len(opponent_history) > 1 and opponent_history[-2] == 0) else 1)
# EVOLVE-BLOCK-END
```

Fresh session; unchanged seed-only information. The backend enforces byte equality with the [frozen initial prompt](protocol/initial_prompt.md), and the native-session audit checks the only user message against that prompt. No prior candidate, score, validity, recognition, or holdout result is supplied.

## B202 — complete

| Slot | Source | Parent | Inspirations | Validity | Training | Best so far | New best | AST duplicate of | Archived |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | [slot 1](runs/B202/gen_1/main.py) | 0 | none | valid | 2.099690 | 2.331077 | no | — | yes |
| 2 | [slot 2](runs/B202/gen_2/main.py) | 0 | none | valid | 2.536238 | 2.536238 | yes | — | yes |
| 3 | [slot 3](runs/B202/gen_3/main.py) | 0 | none | valid | 2.536238 | 2.536238 | no | — | yes |
| 4 | [slot 4](runs/B202/gen_4/main.py) | 0 | none | valid | 2.046954 | 2.536238 | no | — | yes |
| 5 | [slot 5](runs/B202/gen_5/main.py) | 0 | none | valid | 2.052171 | 2.536238 | no | — | yes |
| 6 | [slot 6](runs/B202/gen_6/main.py) | 0 | none | valid | 2.536238 | 2.536238 | no | 3 | yes |
| 7 | [slot 7](runs/B202/gen_7/main.py) | 0 | none | valid | 2.046954 | 2.536238 | no | — | yes |
| 8 | [slot 8](runs/B202/gen_8/main.py) | 0 | none | valid | 2.536238 | 2.536238 | no | 3 | yes |
| 9 | [slot 9](runs/B202/gen_9/main.py) | 0 | none | valid | 2.456007 | 2.536238 | no | — | yes |
| 10 | [slot 10](runs/B202/gen_10/main.py) | 0 | none | valid | 2.536238 | 2.536238 | no | 3 | yes |

### B202, proposal 1

[Exact rendered prompt](runs/B202/invocations/01/prompt.md) · [native output](runs/B202/invocations/01/codex.jsonl) · [supplied context](runs/B202/gen_1/supplied_context.json) · [evaluation records](runs/B202/gen_1/results/).

Training: **2.099690**; validity: **True**; current best: 2.331077; database rows: 1.

Source size: 317 bytes; 75 AST nodes (limits 16,000 bytes / 400 nodes).

Frozen TFT probes: **fail**, 1640 checks, computed after the terminal selection freeze. Finite agreement alone is not equivalence.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else (0 if opponent_history[-1] == 1 else (1 if (len(opponent_history) % 31 == 0 and opponent_history.count(1) == 0) or (own_history.count(1) > 0 and opponent_history.count(1) == 0) else 0))
# EVOLVE-BLOCK-END
```

Fresh session; unchanged seed-only information. The backend enforces byte equality with the [frozen initial prompt](protocol/initial_prompt.md), and the native-session audit checks the only user message against that prompt. No prior candidate, score, validity, recognition, or holdout result is supplied.

### B202, proposal 2

[Exact rendered prompt](runs/B202/invocations/02/prompt.md) · [native output](runs/B202/invocations/02/codex.jsonl) · [supplied context](runs/B202/gen_2/supplied_context.json) · [evaluation records](runs/B202/gen_2/results/).

Training: **2.536238**; validity: **True**; current best: 2.536238; database rows: 1.

Source size: 167 bytes; 24 AST nodes (limits 16,000 bytes / 400 nodes).

Frozen TFT probes: **pass**, 1640 checks, computed after the terminal selection freeze. Finite agreement alone is not equivalence.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    if len(opponent_history) == 0:
        return 0
    return opponent_history[-1]
# EVOLVE-BLOCK-END
```

Fresh session; unchanged seed-only information. The backend enforces byte equality with the [frozen initial prompt](protocol/initial_prompt.md), and the native-session audit checks the only user message against that prompt. No prior candidate, score, validity, recognition, or holdout result is supplied.

### B202, proposal 3

[Exact rendered prompt](runs/B202/invocations/03/prompt.md) · [native output](runs/B202/invocations/03/codex.jsonl) · [supplied context](runs/B202/gen_3/supplied_context.json) · [evaluation records](runs/B202/gen_3/results/).

Training: **2.536238**; validity: **True**; current best: 2.536238; database rows: 1.

Source size: 152 bytes; 23 AST nodes (limits 16,000 bytes / 400 nodes).

Frozen TFT probes: **pass**, 1640 checks, computed after the terminal selection freeze. Finite agreement alone is not equivalence.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else opponent_history[-1]
# EVOLVE-BLOCK-END
```

Fresh session; unchanged seed-only information. The backend enforces byte equality with the [frozen initial prompt](protocol/initial_prompt.md), and the native-session audit checks the only user message against that prompt. No prior candidate, score, validity, recognition, or holdout result is supplied.

### B202, proposal 4

[Exact rendered prompt](runs/B202/invocations/04/prompt.md) · [native output](runs/B202/invocations/04/codex.jsonl) · [supplied context](runs/B202/gen_4/supplied_context.json) · [evaluation records](runs/B202/gen_4/results/).

Training: **2.046954**; validity: **True**; current best: 2.536238; database rows: 1.

Source size: 255 bytes; 43 AST nodes (limits 16,000 bytes / 400 nodes).

Frozen TFT probes: **fail**, 1640 checks, computed after the terminal selection freeze. Finite agreement alone is not equivalence.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    if len(opponent_history) == 0:
        return 0
    if opponent_history.count(1) == 0:
        return 1
    if opponent_history[-1] == 1:
        return 1
    return 0
# EVOLVE-BLOCK-END
```

Fresh session; unchanged seed-only information. The backend enforces byte equality with the [frozen initial prompt](protocol/initial_prompt.md), and the native-session audit checks the only user message against that prompt. No prior candidate, score, validity, recognition, or holdout result is supplied.

### B202, proposal 5

[Exact rendered prompt](runs/B202/invocations/05/prompt.md) · [native output](runs/B202/invocations/05/codex.jsonl) · [supplied context](runs/B202/gen_5/supplied_context.json) · [evaluation records](runs/B202/gen_5/results/).

Training: **2.052171**; validity: **True**; current best: 2.536238; database rows: 1.

Source size: 215 bytes; 42 AST nodes (limits 16,000 bytes / 400 nodes).

Frozen TFT probes: **pass**, 1640 checks, computed after the terminal selection freeze. Finite agreement alone is not equivalence.

Known false positive: this policy defects after positive multiples of 32 history actions. The actual round-33 training counterexample is documented in the main report.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else (1 if opponent_history[-1] == 1 else (1 if len(opponent_history) % 32 == 0 else 0))
# EVOLVE-BLOCK-END
```

Fresh session; unchanged seed-only information. The backend enforces byte equality with the [frozen initial prompt](protocol/initial_prompt.md), and the native-session audit checks the only user message against that prompt. No prior candidate, score, validity, recognition, or holdout result is supplied.

### B202, proposal 6

[Exact rendered prompt](runs/B202/invocations/06/prompt.md) · [native output](runs/B202/invocations/06/codex.jsonl) · [supplied context](runs/B202/gen_6/supplied_context.json) · [evaluation records](runs/B202/gen_6/results/).

Training: **2.536238**; validity: **True**; current best: 2.536238; database rows: 1.

Source size: 152 bytes; 23 AST nodes (limits 16,000 bytes / 400 nodes).

Frozen TFT probes: **pass**, 1640 checks, computed after the terminal selection freeze. Finite agreement alone is not equivalence.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else opponent_history[-1]
# EVOLVE-BLOCK-END
```

Fresh session; unchanged seed-only information. The backend enforces byte equality with the [frozen initial prompt](protocol/initial_prompt.md), and the native-session audit checks the only user message against that prompt. No prior candidate, score, validity, recognition, or holdout result is supplied.

### B202, proposal 7

[Exact rendered prompt](runs/B202/invocations/07/prompt.md) · [native output](runs/B202/invocations/07/codex.jsonl) · [supplied context](runs/B202/gen_7/supplied_context.json) · [evaluation records](runs/B202/gen_7/results/).

Training: **2.046954**; validity: **True**; current best: 2.536238; database rows: 1.

Source size: 219 bytes; 35 AST nodes (limits 16,000 bytes / 400 nodes).

Frozen TFT probes: **fail**, 1640 checks, computed after the terminal selection freeze. Finite agreement alone is not equivalence.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    if len(opponent_history) == 0:
        return 0
    if sum(opponent_history) == 0:
        return 1
    return opponent_history[-1]
# EVOLVE-BLOCK-END
```

Fresh session; unchanged seed-only information. The backend enforces byte equality with the [frozen initial prompt](protocol/initial_prompt.md), and the native-session audit checks the only user message against that prompt. No prior candidate, score, validity, recognition, or holdout result is supplied.

### B202, proposal 8

[Exact rendered prompt](runs/B202/invocations/08/prompt.md) · [native output](runs/B202/invocations/08/codex.jsonl) · [supplied context](runs/B202/gen_8/supplied_context.json) · [evaluation records](runs/B202/gen_8/results/).

Training: **2.536238**; validity: **True**; current best: 2.536238; database rows: 1.

Source size: 152 bytes; 23 AST nodes (limits 16,000 bytes / 400 nodes).

Frozen TFT probes: **pass**, 1640 checks, computed after the terminal selection freeze. Finite agreement alone is not equivalence.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else opponent_history[-1]
# EVOLVE-BLOCK-END
```

Fresh session; unchanged seed-only information. The backend enforces byte equality with the [frozen initial prompt](protocol/initial_prompt.md), and the native-session audit checks the only user message against that prompt. No prior candidate, score, validity, recognition, or holdout result is supplied.

### B202, proposal 9

[Exact rendered prompt](runs/B202/invocations/09/prompt.md) · [native output](runs/B202/invocations/09/codex.jsonl) · [supplied context](runs/B202/gen_9/supplied_context.json) · [evaluation records](runs/B202/gen_9/results/).

Training: **2.456007**; validity: **True**; current best: 2.536238; database rows: 1.

Source size: 259 bytes; 57 AST nodes (limits 16,000 bytes / 400 nodes).

Frozen TFT probes: **fail**, 1640 checks, computed after the terminal selection freeze. Finite agreement alone is not equivalence.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 1 if len(opponent_history) == 0 or opponent_history.count(1) == 0 else (0 if opponent_history[-1] == 1 and opponent_history.count(1) == 1 else opponent_history[-1])
# EVOLVE-BLOCK-END
```

Fresh session; unchanged seed-only information. The backend enforces byte equality with the [frozen initial prompt](protocol/initial_prompt.md), and the native-session audit checks the only user message against that prompt. No prior candidate, score, validity, recognition, or holdout result is supplied.

### B202, proposal 10

[Exact rendered prompt](runs/B202/invocations/10/prompt.md) · [native output](runs/B202/invocations/10/codex.jsonl) · [supplied context](runs/B202/gen_10/supplied_context.json) · [evaluation records](runs/B202/gen_10/results/).

Training: **2.536238**; validity: **True**; current best: 2.536238; database rows: 1.

Source size: 152 bytes; 23 AST nodes (limits 16,000 bytes / 400 nodes).

Frozen TFT probes: **pass**, 1640 checks, computed after the terminal selection freeze. Finite agreement alone is not equivalence.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else opponent_history[-1]
# EVOLVE-BLOCK-END
```

Fresh session; unchanged seed-only information. The backend enforces byte equality with the [frozen initial prompt](protocol/initial_prompt.md), and the native-session audit checks the only user message against that prompt. No prior candidate, score, validity, recognition, or holdout result is supplied.

## A202 — complete

| Slot | Source | Parent | Inspirations | Validity | Training | Best so far | New best | AST duplicate of | Archived |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | [slot 1](runs/A202/gen_1/main.py) | 0 | none | valid | 2.536238 | 2.536238 | yes | — | yes |
| 2 | [slot 2](runs/A202/gen_2/main.py) | 1 | 0 | valid | 2.550761 | 2.550761 | yes | — | yes |
| 3 | [slot 3](runs/A202/gen_3/main.py) | 2 | 1 | valid | 2.561619 | 2.561619 | yes | — | yes |
| 4 | [slot 4](runs/A202/gen_4/main.py) | 3 | 2 | valid | 2.568951 | 2.568951 | yes | — | yes |
| 5 | [slot 5](runs/A202/gen_5/main.py) | 4 | 3 | valid | 2.570925 | 2.570925 | yes | — | yes |
| 6 | [slot 6](runs/A202/gen_6/main.py) | 5 | 4 | valid | 2.330936 | 2.570925 | no | — | yes |
| 7 | [slot 7](runs/A202/gen_7/main.py) | 4 | 5 | rejected | -1.000000 | 2.570925 | no | — | no |
| 8 | [slot 8](runs/A202/gen_8/main.py) | 3 | 5 | valid | 2.570925 | 2.570925 | no | 5 | yes |
| 9 | [slot 9](runs/A202/gen_9/main.py) | 5 | 8 | rejected | -1.000000 | 2.570925 | no | — | no |
| 10 | [slot 10](runs/A202/gen_10/main.py) | 4 | 5 | valid | 2.120981 | 2.570925 | no | — | yes |

### A202, proposal 1

[Exact rendered prompt](runs/A202/invocations/01/prompt.md) · [native output](runs/A202/invocations/01/codex.jsonl) · [supplied context](runs/A202/gen_1/supplied_context.json) · [evaluation records](runs/A202/gen_1/results/).

Training: **2.536238**; validity: **True**; current best: 2.536238; database rows: 1.

Source size: 152 bytes; 23 AST nodes (limits 16,000 bytes / 400 nodes).

Frozen TFT probes: **pass**, 1640 checks, computed after the terminal selection freeze. Finite agreement alone is not equivalence.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else opponent_history[-1]
# EVOLVE-BLOCK-END
```

**Parent: generation 0**, training 2.331077; public feedback `{"mean_payoff": 2.3310772701635645}`; text feedback ``.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 1
# EVOLVE-BLOCK-END
```

### A202, proposal 2

[Exact rendered prompt](runs/A202/invocations/02/prompt.md) · [native output](runs/A202/invocations/02/codex.jsonl) · [supplied context](runs/A202/gen_2/supplied_context.json) · [evaluation records](runs/A202/gen_2/results/).

Training: **2.550761**; validity: **True**; current best: 2.550761; database rows: 1.

Source size: 291 bytes; 72 AST nodes (limits 16,000 bytes / 400 nodes).

Frozen TFT probes: **fail**, 1640 checks, computed after the terminal selection freeze. Finite agreement alone is not equivalence.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else 1 if len(opponent_history) >= 4 and opponent_history[-4:-2] == opponent_history[-2:] and opponent_history[-1] != opponent_history[-2] else opponent_history[-1]
# EVOLVE-BLOCK-END
```

**Parent: generation 1**, training 2.536238; public feedback `{"mean_payoff": 2.5362380146644106}`; text feedback ``.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else opponent_history[-1]
# EVOLVE-BLOCK-END
```

**Inspiration: generation 0**, training 2.331077; public feedback `{"mean_payoff": 2.3310772701635645}`; text feedback ``.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 1
# EVOLVE-BLOCK-END
```

### A202, proposal 3

[Exact rendered prompt](runs/A202/invocations/03/prompt.md) · [native output](runs/A202/invocations/03/codex.jsonl) · [supplied context](runs/A202/gen_3/supplied_context.json) · [evaluation records](runs/A202/gen_3/results/).

Training: **2.561619**; validity: **True**; current best: 2.561619; database rows: 1.

Source size: 451 bytes; 133 AST nodes (limits 16,000 bytes / 400 nodes).

Frozen TFT probes: **fail**, 1640 checks, computed after the terminal selection freeze. Finite agreement alone is not equivalence.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else 1 if len(opponent_history) >= 4 and opponent_history[-4:-2] == opponent_history[-2:] and opponent_history[-1] != opponent_history[-2] else 1 if len(opponent_history) >= 6 and opponent_history[-6:-3] == opponent_history[-3:] and sum(opponent_history[-3:]) > 0 and sum(opponent_history[-3:]) < 3 else opponent_history[-1]
# EVOLVE-BLOCK-END
```

**Parent: generation 2**, training 2.550761; public feedback `{"mean_payoff": 2.550761421319797}`; text feedback ``.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else 1 if len(opponent_history) >= 4 and opponent_history[-4:-2] == opponent_history[-2:] and opponent_history[-1] != opponent_history[-2] else opponent_history[-1]
# EVOLVE-BLOCK-END
```

**Inspiration: generation 1**, training 2.536238; public feedback `{"mean_payoff": 2.5362380146644106}`; text feedback ``.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else opponent_history[-1]
# EVOLVE-BLOCK-END
```

### A202, proposal 4

[Exact rendered prompt](runs/A202/invocations/04/prompt.md) · [native output](runs/A202/invocations/04/codex.jsonl) · [supplied context](runs/A202/gen_4/supplied_context.json) · [evaluation records](runs/A202/gen_4/results/).

Training: **2.568951**; validity: **True**; current best: 2.568951; database rows: 1.

Source size: 611 bytes; 194 AST nodes (limits 16,000 bytes / 400 nodes).

Frozen TFT probes: **fail**, 1640 checks, computed after the terminal selection freeze. Finite agreement alone is not equivalence.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else 1 if len(opponent_history) >= 4 and opponent_history[-4:-2] == opponent_history[-2:] and opponent_history[-1] != opponent_history[-2] else 1 if len(opponent_history) >= 6 and opponent_history[-6:-3] == opponent_history[-3:] and sum(opponent_history[-3:]) > 0 and sum(opponent_history[-3:]) < 3 else 1 if len(opponent_history) >= 8 and opponent_history[-8:-4] == opponent_history[-4:] and sum(opponent_history[-4:]) > 0 and sum(opponent_history[-4:]) < 4 else opponent_history[-1]
# EVOLVE-BLOCK-END
```

**Parent: generation 3**, training 2.561619; public feedback `{"mean_payoff": 2.5616187253243092}`; text feedback ``.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else 1 if len(opponent_history) >= 4 and opponent_history[-4:-2] == opponent_history[-2:] and opponent_history[-1] != opponent_history[-2] else 1 if len(opponent_history) >= 6 and opponent_history[-6:-3] == opponent_history[-3:] and sum(opponent_history[-3:]) > 0 and sum(opponent_history[-3:]) < 3 else opponent_history[-1]
# EVOLVE-BLOCK-END
```

**Inspiration: generation 2**, training 2.550761; public feedback `{"mean_payoff": 2.550761421319797}`; text feedback ``.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else 1 if len(opponent_history) >= 4 and opponent_history[-4:-2] == opponent_history[-2:] and opponent_history[-1] != opponent_history[-2] else opponent_history[-1]
# EVOLVE-BLOCK-END
```

### A202, proposal 5

[Exact rendered prompt](runs/A202/invocations/05/prompt.md) · [native output](runs/A202/invocations/05/codex.jsonl) · [supplied context](runs/A202/gen_5/supplied_context.json) · [evaluation records](runs/A202/gen_5/results/).

Training: **2.570925**; validity: **True**; current best: 2.570925; database rows: 1.

Source size: 935 bytes; 316 AST nodes (limits 16,000 bytes / 400 nodes).

Frozen TFT probes: **fail**, 1640 checks, computed after the terminal selection freeze. Finite agreement alone is not equivalence.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else 1 if len(opponent_history) >= 4 and opponent_history[-4:-2] == opponent_history[-2:] and opponent_history[-1] != opponent_history[-2] else 1 if len(opponent_history) >= 6 and opponent_history[-6:-3] == opponent_history[-3:] and sum(opponent_history[-3:]) > 0 and sum(opponent_history[-3:]) < 3 else 1 if len(opponent_history) >= 8 and opponent_history[-8:-4] == opponent_history[-4:] and sum(opponent_history[-4:]) > 0 and sum(opponent_history[-4:]) < 4 else 1 if len(opponent_history) >= 10 and opponent_history[-10:-5] == opponent_history[-5:] and sum(opponent_history[-5:]) > 0 and sum(opponent_history[-5:]) < 5 else 1 if len(opponent_history) >= 12 and opponent_history[-12:-6] == opponent_history[-6:] and sum(opponent_history[-6:]) > 0 and sum(opponent_history[-6:]) < 6 else opponent_history[-1]
# EVOLVE-BLOCK-END
```

**Parent: generation 4**, training 2.568951; public feedback `{"mean_payoff": 2.5689509306260576}`; text feedback ``.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else 1 if len(opponent_history) >= 4 and opponent_history[-4:-2] == opponent_history[-2:] and opponent_history[-1] != opponent_history[-2] else 1 if len(opponent_history) >= 6 and opponent_history[-6:-3] == opponent_history[-3:] and sum(opponent_history[-3:]) > 0 and sum(opponent_history[-3:]) < 3 else 1 if len(opponent_history) >= 8 and opponent_history[-8:-4] == opponent_history[-4:] and sum(opponent_history[-4:]) > 0 and sum(opponent_history[-4:]) < 4 else opponent_history[-1]
# EVOLVE-BLOCK-END
```

**Inspiration: generation 3**, training 2.561619; public feedback `{"mean_payoff": 2.5616187253243092}`; text feedback ``.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else 1 if len(opponent_history) >= 4 and opponent_history[-4:-2] == opponent_history[-2:] and opponent_history[-1] != opponent_history[-2] else 1 if len(opponent_history) >= 6 and opponent_history[-6:-3] == opponent_history[-3:] and sum(opponent_history[-3:]) > 0 and sum(opponent_history[-3:]) < 3 else opponent_history[-1]
# EVOLVE-BLOCK-END
```

### A202, proposal 6

[Exact rendered prompt](runs/A202/invocations/06/prompt.md) · [native output](runs/A202/invocations/06/codex.jsonl) · [supplied context](runs/A202/gen_6/supplied_context.json) · [evaluation records](runs/A202/gen_6/results/).

Training: **2.330936**; validity: **True**; current best: 2.570925; database rows: 1.

Source size: 1033 bytes; 350 AST nodes (limits 16,000 bytes / 400 nodes).

Frozen TFT probes: **fail**, 1640 checks, computed after the terminal selection freeze. Finite agreement alone is not equivalence.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else 1 if len(opponent_history) == 1 else 1 if own_history[-1] == 1 and opponent_history[-1] == 0 else 1 if len(opponent_history) >= 4 and opponent_history[-4:-2] == opponent_history[-2:] and opponent_history[-1] != opponent_history[-2] else 1 if len(opponent_history) >= 6 and opponent_history[-6:-3] == opponent_history[-3:] and sum(opponent_history[-3:]) > 0 and sum(opponent_history[-3:]) < 3 else 1 if len(opponent_history) >= 8 and opponent_history[-8:-4] == opponent_history[-4:] and sum(opponent_history[-4:]) > 0 and sum(opponent_history[-4:]) < 4 else 1 if len(opponent_history) >= 10 and opponent_history[-10:-5] == opponent_history[-5:] and sum(opponent_history[-5:]) > 0 and sum(opponent_history[-5:]) < 5 else 1 if len(opponent_history) >= 12 and opponent_history[-12:-6] == opponent_history[-6:] and sum(opponent_history[-6:]) > 0 and sum(opponent_history[-6:]) < 6 else opponent_history[-1]
# EVOLVE-BLOCK-END
```

**Parent: generation 5**, training 2.570925; public feedback `{"mean_payoff": 2.5709249858996053}`; text feedback ``.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else 1 if len(opponent_history) >= 4 and opponent_history[-4:-2] == opponent_history[-2:] and opponent_history[-1] != opponent_history[-2] else 1 if len(opponent_history) >= 6 and opponent_history[-6:-3] == opponent_history[-3:] and sum(opponent_history[-3:]) > 0 and sum(opponent_history[-3:]) < 3 else 1 if len(opponent_history) >= 8 and opponent_history[-8:-4] == opponent_history[-4:] and sum(opponent_history[-4:]) > 0 and sum(opponent_history[-4:]) < 4 else 1 if len(opponent_history) >= 10 and opponent_history[-10:-5] == opponent_history[-5:] and sum(opponent_history[-5:]) > 0 and sum(opponent_history[-5:]) < 5 else 1 if len(opponent_history) >= 12 and opponent_history[-12:-6] == opponent_history[-6:] and sum(opponent_history[-6:]) > 0 and sum(opponent_history[-6:]) < 6 else opponent_history[-1]
# EVOLVE-BLOCK-END
```

**Inspiration: generation 4**, training 2.568951; public feedback `{"mean_payoff": 2.5689509306260576}`; text feedback ``.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else 1 if len(opponent_history) >= 4 and opponent_history[-4:-2] == opponent_history[-2:] and opponent_history[-1] != opponent_history[-2] else 1 if len(opponent_history) >= 6 and opponent_history[-6:-3] == opponent_history[-3:] and sum(opponent_history[-3:]) > 0 and sum(opponent_history[-3:]) < 3 else 1 if len(opponent_history) >= 8 and opponent_history[-8:-4] == opponent_history[-4:] and sum(opponent_history[-4:]) > 0 and sum(opponent_history[-4:]) < 4 else opponent_history[-1]
# EVOLVE-BLOCK-END
```

### A202, proposal 7

[Exact rendered prompt](runs/A202/invocations/07/prompt.md) · [native output](runs/A202/invocations/07/codex.jsonl) · [supplied context](runs/A202/gen_7/supplied_context.json) · [evaluation records](runs/A202/gen_7/results/).

Training: **-1.000000**; validity: **False**; current best: 2.570925; database rows: 1.

Rejection/failure: `PolicyError: Unsupported syntax or more than 400 AST nodes`. Unsupported AST types: []. No repair or replacement.

Source size: 1259 bytes; 438 AST nodes (limits 16,000 bytes / 400 nodes).

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else 1 if len(opponent_history) >= 4 and opponent_history[-4:-2] == opponent_history[-2:] and opponent_history[-1] != opponent_history[-2] else 1 if len(opponent_history) >= 6 and opponent_history[-6:-3] == opponent_history[-3:] and sum(opponent_history[-3:]) > 0 and sum(opponent_history[-3:]) < 3 else 1 if len(opponent_history) >= 8 and opponent_history[-8:-4] == opponent_history[-4:] and sum(opponent_history[-4:]) > 0 and sum(opponent_history[-4:]) < 4 else 1 if len(opponent_history) >= 10 and opponent_history[-10:-5] == opponent_history[-5:] and sum(opponent_history[-5:]) > 0 and sum(opponent_history[-5:]) < 5 else 1 if len(opponent_history) >= 12 and opponent_history[-12:-6] == opponent_history[-6:] and sum(opponent_history[-6:]) > 0 and sum(opponent_history[-6:]) < 6 else 1 if len(opponent_history) >= 14 and opponent_history[-14:-7] == opponent_history[-7:] and sum(opponent_history[-7:]) > 0 and sum(opponent_history[-7:]) < 7 else 1 if len(opponent_history) >= 16 and opponent_history[-16:-8] == opponent_history[-8:] and sum(opponent_history[-8:]) > 0 and sum(opponent_history[-8:]) < 8 else opponent_history[-1]
# EVOLVE-BLOCK-END
```

**Parent: generation 4**, training 2.568951; public feedback `{"mean_payoff": 2.5689509306260576}`; text feedback ``.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else 1 if len(opponent_history) >= 4 and opponent_history[-4:-2] == opponent_history[-2:] and opponent_history[-1] != opponent_history[-2] else 1 if len(opponent_history) >= 6 and opponent_history[-6:-3] == opponent_history[-3:] and sum(opponent_history[-3:]) > 0 and sum(opponent_history[-3:]) < 3 else 1 if len(opponent_history) >= 8 and opponent_history[-8:-4] == opponent_history[-4:] and sum(opponent_history[-4:]) > 0 and sum(opponent_history[-4:]) < 4 else opponent_history[-1]
# EVOLVE-BLOCK-END
```

**Inspiration: generation 5**, training 2.570925; public feedback `{"mean_payoff": 2.5709249858996053}`; text feedback ``.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else 1 if len(opponent_history) >= 4 and opponent_history[-4:-2] == opponent_history[-2:] and opponent_history[-1] != opponent_history[-2] else 1 if len(opponent_history) >= 6 and opponent_history[-6:-3] == opponent_history[-3:] and sum(opponent_history[-3:]) > 0 and sum(opponent_history[-3:]) < 3 else 1 if len(opponent_history) >= 8 and opponent_history[-8:-4] == opponent_history[-4:] and sum(opponent_history[-4:]) > 0 and sum(opponent_history[-4:]) < 4 else 1 if len(opponent_history) >= 10 and opponent_history[-10:-5] == opponent_history[-5:] and sum(opponent_history[-5:]) > 0 and sum(opponent_history[-5:]) < 5 else 1 if len(opponent_history) >= 12 and opponent_history[-12:-6] == opponent_history[-6:] and sum(opponent_history[-6:]) > 0 and sum(opponent_history[-6:]) < 6 else opponent_history[-1]
# EVOLVE-BLOCK-END
```

### A202, proposal 8

[Exact rendered prompt](runs/A202/invocations/08/prompt.md) · [native output](runs/A202/invocations/08/codex.jsonl) · [supplied context](runs/A202/gen_8/supplied_context.json) · [evaluation records](runs/A202/gen_8/results/).

Training: **2.570925**; validity: **True**; current best: 2.570925; database rows: 1.

Source size: 935 bytes; 316 AST nodes (limits 16,000 bytes / 400 nodes).

Frozen TFT probes: **fail**, 1640 checks, computed after the terminal selection freeze. Finite agreement alone is not equivalence.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else 1 if len(opponent_history) >= 4 and opponent_history[-4:-2] == opponent_history[-2:] and opponent_history[-1] != opponent_history[-2] else 1 if len(opponent_history) >= 6 and opponent_history[-6:-3] == opponent_history[-3:] and sum(opponent_history[-3:]) > 0 and sum(opponent_history[-3:]) < 3 else 1 if len(opponent_history) >= 8 and opponent_history[-8:-4] == opponent_history[-4:] and sum(opponent_history[-4:]) > 0 and sum(opponent_history[-4:]) < 4 else 1 if len(opponent_history) >= 10 and opponent_history[-10:-5] == opponent_history[-5:] and sum(opponent_history[-5:]) > 0 and sum(opponent_history[-5:]) < 5 else 1 if len(opponent_history) >= 12 and opponent_history[-12:-6] == opponent_history[-6:] and sum(opponent_history[-6:]) > 0 and sum(opponent_history[-6:]) < 6 else opponent_history[-1]
# EVOLVE-BLOCK-END
```

**Parent: generation 3**, training 2.561619; public feedback `{"mean_payoff": 2.5616187253243092}`; text feedback ``.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else 1 if len(opponent_history) >= 4 and opponent_history[-4:-2] == opponent_history[-2:] and opponent_history[-1] != opponent_history[-2] else 1 if len(opponent_history) >= 6 and opponent_history[-6:-3] == opponent_history[-3:] and sum(opponent_history[-3:]) > 0 and sum(opponent_history[-3:]) < 3 else opponent_history[-1]
# EVOLVE-BLOCK-END
```

**Inspiration: generation 5**, training 2.570925; public feedback `{"mean_payoff": 2.5709249858996053}`; text feedback ``.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else 1 if len(opponent_history) >= 4 and opponent_history[-4:-2] == opponent_history[-2:] and opponent_history[-1] != opponent_history[-2] else 1 if len(opponent_history) >= 6 and opponent_history[-6:-3] == opponent_history[-3:] and sum(opponent_history[-3:]) > 0 and sum(opponent_history[-3:]) < 3 else 1 if len(opponent_history) >= 8 and opponent_history[-8:-4] == opponent_history[-4:] and sum(opponent_history[-4:]) > 0 and sum(opponent_history[-4:]) < 4 else 1 if len(opponent_history) >= 10 and opponent_history[-10:-5] == opponent_history[-5:] and sum(opponent_history[-5:]) > 0 and sum(opponent_history[-5:]) < 5 else 1 if len(opponent_history) >= 12 and opponent_history[-12:-6] == opponent_history[-6:] and sum(opponent_history[-6:]) > 0 and sum(opponent_history[-6:]) < 6 else opponent_history[-1]
# EVOLVE-BLOCK-END
```

### A202, proposal 9

[Exact rendered prompt](runs/A202/invocations/09/prompt.md) · [native output](runs/A202/invocations/09/codex.jsonl) · [supplied context](runs/A202/gen_9/supplied_context.json) · [evaluation records](runs/A202/gen_9/results/).

Training: **-1.000000**; validity: **False**; current best: 2.570925; database rows: 1.

Rejection/failure: `PolicyError: Unsupported syntax or more than 400 AST nodes`. Unsupported AST types: ['Tuple']. No repair or replacement.

Source size: 1158 bytes; 394 AST nodes (limits 16,000 bytes / 400 nodes).

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else 0 if len(own_history) >= 2 and own_history[-2:] == (1, 0) and opponent_history[-1] == 1 else 0 if own_history[-1] == 1 and sum(opponent_history) == 0 else 1 if len(opponent_history) >= 3 and sum(opponent_history) == 0 else 1 if len(opponent_history) >= 4 and opponent_history[-4:-2] == opponent_history[-2:] and opponent_history[-1] != opponent_history[-2] else 1 if len(opponent_history) >= 6 and opponent_history[-6:-3] == opponent_history[-3:] and sum(opponent_history[-3:]) > 0 and sum(opponent_history[-3:]) < 3 else 1 if len(opponent_history) >= 8 and opponent_history[-8:-4] == opponent_history[-4:] and sum(opponent_history[-4:]) > 0 and sum(opponent_history[-4:]) < 4 else 1 if len(opponent_history) >= 10 and opponent_history[-10:-5] == opponent_history[-5:] and sum(opponent_history[-5:]) > 0 and sum(opponent_history[-5:]) < 5 else 1 if len(opponent_history) >= 12 and opponent_history[-12:-6] == opponent_history[-6:] and sum(opponent_history[-6:]) > 0 and sum(opponent_history[-6:]) < 6 else opponent_history[-1]
# EVOLVE-BLOCK-END
```

**Parent: generation 5**, training 2.570925; public feedback `{"mean_payoff": 2.5709249858996053}`; text feedback ``.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else 1 if len(opponent_history) >= 4 and opponent_history[-4:-2] == opponent_history[-2:] and opponent_history[-1] != opponent_history[-2] else 1 if len(opponent_history) >= 6 and opponent_history[-6:-3] == opponent_history[-3:] and sum(opponent_history[-3:]) > 0 and sum(opponent_history[-3:]) < 3 else 1 if len(opponent_history) >= 8 and opponent_history[-8:-4] == opponent_history[-4:] and sum(opponent_history[-4:]) > 0 and sum(opponent_history[-4:]) < 4 else 1 if len(opponent_history) >= 10 and opponent_history[-10:-5] == opponent_history[-5:] and sum(opponent_history[-5:]) > 0 and sum(opponent_history[-5:]) < 5 else 1 if len(opponent_history) >= 12 and opponent_history[-12:-6] == opponent_history[-6:] and sum(opponent_history[-6:]) > 0 and sum(opponent_history[-6:]) < 6 else opponent_history[-1]
# EVOLVE-BLOCK-END
```

**Inspiration: generation 8**, training 2.570925; public feedback `{"mean_payoff": 2.5709249858996053}`; text feedback ``.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else 1 if len(opponent_history) >= 4 and opponent_history[-4:-2] == opponent_history[-2:] and opponent_history[-1] != opponent_history[-2] else 1 if len(opponent_history) >= 6 and opponent_history[-6:-3] == opponent_history[-3:] and sum(opponent_history[-3:]) > 0 and sum(opponent_history[-3:]) < 3 else 1 if len(opponent_history) >= 8 and opponent_history[-8:-4] == opponent_history[-4:] and sum(opponent_history[-4:]) > 0 and sum(opponent_history[-4:]) < 4 else 1 if len(opponent_history) >= 10 and opponent_history[-10:-5] == opponent_history[-5:] and sum(opponent_history[-5:]) > 0 and sum(opponent_history[-5:]) < 5 else 1 if len(opponent_history) >= 12 and opponent_history[-12:-6] == opponent_history[-6:] and sum(opponent_history[-6:]) > 0 and sum(opponent_history[-6:]) < 6 else opponent_history[-1]
# EVOLVE-BLOCK-END
```

### A202, proposal 10

[Exact rendered prompt](runs/A202/invocations/10/prompt.md) · [native output](runs/A202/invocations/10/codex.jsonl) · [supplied context](runs/A202/gen_10/supplied_context.json) · [evaluation records](runs/A202/gen_10/results/).

Training: **2.120981**; validity: **True**; current best: 2.570925; database rows: 1.

Source size: 852 bytes; 280 AST nodes (limits 16,000 bytes / 400 nodes).

Frozen TFT probes: **fail**, 1640 checks, computed after the terminal selection freeze. Finite agreement alone is not equivalence.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else 0 if own_history[-1] == 1 and opponent_history[-1] == 0 else 0 if len(own_history) >= 2 and own_history[-2] == 1 and own_history[-1] == 0 and opponent_history[-1] == 1 else 1 if len(opponent_history) >= 6 and sum(opponent_history) == 0 else 1 if len(opponent_history) >= 4 and opponent_history[-4:-2] == opponent_history[-2:] and opponent_history[-1] != opponent_history[-2] else 1 if len(opponent_history) >= 6 and opponent_history[-6:-3] == opponent_history[-3:] and sum(opponent_history[-3:]) > 0 and sum(opponent_history[-3:]) < 3 else 1 if len(opponent_history) >= 8 and opponent_history[-8:-4] == opponent_history[-4:] and sum(opponent_history[-4:]) > 0 and sum(opponent_history[-4:]) < 4 else opponent_history[-1]
# EVOLVE-BLOCK-END
```

**Parent: generation 4**, training 2.568951; public feedback `{"mean_payoff": 2.5689509306260576}`; text feedback ``.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else 1 if len(opponent_history) >= 4 and opponent_history[-4:-2] == opponent_history[-2:] and opponent_history[-1] != opponent_history[-2] else 1 if len(opponent_history) >= 6 and opponent_history[-6:-3] == opponent_history[-3:] and sum(opponent_history[-3:]) > 0 and sum(opponent_history[-3:]) < 3 else 1 if len(opponent_history) >= 8 and opponent_history[-8:-4] == opponent_history[-4:] and sum(opponent_history[-4:]) > 0 and sum(opponent_history[-4:]) < 4 else opponent_history[-1]
# EVOLVE-BLOCK-END
```

**Inspiration: generation 5**, training 2.570925; public feedback `{"mean_payoff": 2.5709249858996053}`; text feedback ``.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else 1 if len(opponent_history) >= 4 and opponent_history[-4:-2] == opponent_history[-2:] and opponent_history[-1] != opponent_history[-2] else 1 if len(opponent_history) >= 6 and opponent_history[-6:-3] == opponent_history[-3:] and sum(opponent_history[-3:]) > 0 and sum(opponent_history[-3:]) < 3 else 1 if len(opponent_history) >= 8 and opponent_history[-8:-4] == opponent_history[-4:] and sum(opponent_history[-4:]) > 0 and sum(opponent_history[-4:]) < 4 else 1 if len(opponent_history) >= 10 and opponent_history[-10:-5] == opponent_history[-5:] and sum(opponent_history[-5:]) > 0 and sum(opponent_history[-5:]) < 5 else 1 if len(opponent_history) >= 12 and opponent_history[-12:-6] == opponent_history[-6:] and sum(opponent_history[-6:]) > 0 and sum(opponent_history[-6:]) < 6 else opponent_history[-1]
# EVOLVE-BLOCK-END
```

## A303 — incomplete

| Slot | Source | Parent | Inspirations | Validity | Training | Best so far | New best | AST duplicate of | Archived |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | [slot 1](runs/A303/gen_1/main.py) | 0 | none | valid | 2.536238 | 2.536238 | yes | — | yes |
| 2 | [slot 2](runs/A303/gen_2/main.py) | 1 | 0 | valid | 2.051043 | 2.536238 | no | — | yes |
| 3 | [slot 3](runs/A303/gen_3/main.py) | 1 | 0 | valid | 2.451072 | 2.536238 | no | — | yes |
| 4 | [slot 4](runs/A303/gen_4/main.py) | 1 | 3 | evaluation_missing | unavailable | 2.536238 | no | — | no |
| 5 | no canonical file | 3 | 1 | blocked_before_external_launch | unavailable | unavailable | no | — | no |
| 6 | no canonical file | — | none | not_attempted | unavailable | unavailable | no | — | no |
| 7 | no canonical file | — | none | not_attempted | unavailable | unavailable | no | — | no |
| 8 | no canonical file | — | none | not_attempted | unavailable | unavailable | no | — | no |
| 9 | no canonical file | — | none | not_attempted | unavailable | unavailable | no | — | no |
| 10 | no canonical file | — | none | not_attempted | unavailable | unavailable | no | — | no |

### A303, proposal 1

[Exact rendered prompt](runs/A303/invocations/01/prompt.md) · [native output](runs/A303/invocations/01/codex.jsonl) · [supplied context](runs/A303/gen_1/supplied_context.json) · [evaluation records](runs/A303/gen_1/results/).

Training: **2.536238**; validity: **True**; current best: 2.536238; database rows: 1.

Source size: 167 bytes; 24 AST nodes (limits 16,000 bytes / 400 nodes).

Frozen TFT probes: **pass**, 1640 checks, computed after the terminal selection freeze. Finite agreement alone is not equivalence.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    if len(opponent_history) == 0:
        return 0
    return opponent_history[-1]
# EVOLVE-BLOCK-END
```

**Parent: generation 0**, training 2.331077; public feedback `{"mean_payoff": 2.3310772701635645}`; text feedback ``.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 1
# EVOLVE-BLOCK-END
```

### A303, proposal 2

[Exact rendered prompt](runs/A303/invocations/02/prompt.md) · [native output](runs/A303/invocations/02/codex.jsonl) · [supplied context](runs/A303/gen_2/supplied_context.json) · [evaluation records](runs/A303/gen_2/results/).

Training: **2.051043**; validity: **True**; current best: 2.536238; database rows: 1.

Source size: 375 bytes; 79 AST nodes (limits 16,000 bytes / 400 nodes).

Frozen TFT probes: **fail**, 1640 checks, computed after the terminal selection freeze. Finite agreement alone is not equivalence.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    if len(opponent_history) == 0:
        return 0
    if opponent_history.count(1) == 0:
        return 0 if len(opponent_history) < 3 else 1
    if opponent_history.count(1) == 1 and own_history.count(1) == 1 and opponent_history[-1] == 1:
        return 0
    return opponent_history[-1]
# EVOLVE-BLOCK-END
```

**Parent: generation 1**, training 2.536238; public feedback `{"mean_payoff": 2.5362380146644106}`; text feedback ``.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    if len(opponent_history) == 0:
        return 0
    return opponent_history[-1]
# EVOLVE-BLOCK-END
```

**Inspiration: generation 0**, training 2.331077; public feedback `{"mean_payoff": 2.3310772701635645}`; text feedback ``.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 1
# EVOLVE-BLOCK-END
```

### A303, proposal 3

[Exact rendered prompt](runs/A303/invocations/03/prompt.md) · [native output](runs/A303/invocations/03/codex.jsonl) · [supplied context](runs/A303/gen_3/supplied_context.json) · [evaluation records](runs/A303/gen_3/results/).

Training: **2.451072**; validity: **True**; current best: 2.536238; database rows: 1.

Source size: 231 bytes; 46 AST nodes (limits 16,000 bytes / 400 nodes).

Frozen TFT probes: **fail**, 1640 checks, computed after the terminal selection freeze. Finite agreement alone is not equivalence.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    if len(opponent_history) == 0:
        return 0
    if opponent_history[-1] == 0:
        return own_history[-1]
    return 1 - own_history[-1]
# EVOLVE-BLOCK-END
```

**Parent: generation 1**, training 2.536238; public feedback `{"mean_payoff": 2.5362380146644106}`; text feedback ``.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    if len(opponent_history) == 0:
        return 0
    return opponent_history[-1]
# EVOLVE-BLOCK-END
```

**Inspiration: generation 0**, training 2.331077; public feedback `{"mean_payoff": 2.3310772701635645}`; text feedback ``.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 1
# EVOLVE-BLOCK-END
```

### A303, proposal 4

[Exact rendered prompt](runs/A303/invocations/04/prompt.md) · [native output](runs/A303/invocations/04/codex.jsonl) · [supplied context](runs/A303/gen_4/supplied_context.json) · [evaluation records](runs/A303/gen_4/results/).

Training: **unavailable**; validity: **False**; current best: 2.536238; database rows: 1.

Rejection/failure: `No evaluator result`. Unsupported AST types: []. No repair or replacement.

Source size: 517 bytes; 134 AST nodes (limits 16,000 bytes / 400 nodes).

Post-stop interpreter diagnosis: admissible, training payoff 2.117879. This is not a live evaluator result and did not alter selection or archive membership. Shinka's database failure score 0 is not measured payoff.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    if len(opponent_history) == 0:
        return 0
    if opponent_history.count(1) == 0 and len(opponent_history) >= 12 and own_history[-1] == 0:
        return 1
    if own_history[-1] == 1 and opponent_history[-1] == 0:
        return 0
    if len(opponent_history) > 1 and own_history[-2] == 1 and opponent_history[-2] == 0 and own_history[-1] == 0 and opponent_history[-1] == 1:
        return 0
    return opponent_history[-1]
# EVOLVE-BLOCK-END
```

**Parent: generation 1**, training 2.536238; public feedback `{"mean_payoff": 2.5362380146644106}`; text feedback ``.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    if len(opponent_history) == 0:
        return 0
    return opponent_history[-1]
# EVOLVE-BLOCK-END
```

**Inspiration: generation 3**, training 2.451072; public feedback `{"mean_payoff": 2.4510716300056403}`; text feedback ``.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    if len(opponent_history) == 0:
        return 0
    if opponent_history[-1] == 0:
        return own_history[-1]
    return 1 - own_history[-1]
# EVOLVE-BLOCK-END
```

### A303, proposal 5

**blocked_before_external_launch**. No external proposal, generated source, or measured payoff. [Preserved boundary failure](runs/A303/invocations/05/headless.stderr.txt) · [actual native prompt prepared before the block](runs/A303/invocations/05/prompt.md).

### A303, proposal 6

**not_attempted**. No external proposal, generated source, or measured payoff. The stopped ledger was not reset.

### A303, proposal 7

**not_attempted**. No external proposal, generated source, or measured payoff. The stopped ledger was not reset.

### A303, proposal 8

**not_attempted**. No external proposal, generated source, or measured payoff. The stopped ledger was not reset.

### A303, proposal 9

**not_attempted**. No external proposal, generated source, or measured payoff. The stopped ledger was not reset.

### A303, proposal 10

**not_attempted**. No external proposal, generated source, or measured payoff. The stopped ledger was not reset.

## B303 — not_started

| Slot | Source | Parent | Inspirations | Validity | Training | Best so far | New best | AST duplicate of | Archived |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | no canonical file | — | none | not_attempted | unavailable | unavailable | no | — | no |
| 2 | no canonical file | — | none | not_attempted | unavailable | unavailable | no | — | no |
| 3 | no canonical file | — | none | not_attempted | unavailable | unavailable | no | — | no |
| 4 | no canonical file | — | none | not_attempted | unavailable | unavailable | no | — | no |
| 5 | no canonical file | — | none | not_attempted | unavailable | unavailable | no | — | no |
| 6 | no canonical file | — | none | not_attempted | unavailable | unavailable | no | — | no |
| 7 | no canonical file | — | none | not_attempted | unavailable | unavailable | no | — | no |
| 8 | no canonical file | — | none | not_attempted | unavailable | unavailable | no | — | no |
| 9 | no canonical file | — | none | not_attempted | unavailable | unavailable | no | — | no |
| 10 | no canonical file | — | none | not_attempted | unavailable | unavailable | no | — | no |

### B303, proposal 1

**not_attempted**. No external proposal, generated source, or measured payoff. The stopped ledger was not reset.

### B303, proposal 2

**not_attempted**. No external proposal, generated source, or measured payoff. The stopped ledger was not reset.

### B303, proposal 3

**not_attempted**. No external proposal, generated source, or measured payoff. The stopped ledger was not reset.

### B303, proposal 4

**not_attempted**. No external proposal, generated source, or measured payoff. The stopped ledger was not reset.

### B303, proposal 5

**not_attempted**. No external proposal, generated source, or measured payoff. The stopped ledger was not reset.

### B303, proposal 6

**not_attempted**. No external proposal, generated source, or measured payoff. The stopped ledger was not reset.

### B303, proposal 7

**not_attempted**. No external proposal, generated source, or measured payoff. The stopped ledger was not reset.

### B303, proposal 8

**not_attempted**. No external proposal, generated source, or measured payoff. The stopped ledger was not reset.

### B303, proposal 9

**not_attempted**. No external proposal, generated source, or measured payoff. The stopped ledger was not reset.

### B303, proposal 10

**not_attempted**. No external proposal, generated source, or measured payoff. The stopped ledger was not reset.
