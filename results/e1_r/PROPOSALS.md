# Every E1-R proposal opportunity

There were 60 planned opportunities nested in six runs, not 60 independent experimental replicates. Statuses and measured outcomes below are derived from E1-R evidence. Unattempted opportunities and a prelaunch block are not invalid programs or zero-payoff observations. Slot 0 is the unchanged seed. Validity and payoff are fixed-evaluator results. An AST duplicate ignores formatting/comments and compares with earlier sources in the same run, including seed; it consumes its slot. Archive means actual final SQLite archive membership, separate from a generated file or database row. Full-precision context scores below are archival values; native prompts format payoff to two decimals. Use the prompt links to inspect exactly what the proposer received.

## A101 — complete

| Slot | Source | Parent | Inspirations | Validity | Training | Best so far | New best | AST duplicate of | Archived |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | [slot 1](runs/A101/gen_1/main.py) | 0 | none | rejected | -1.000000 | 2.331077 | no | — | no |
| 2 | [slot 2](runs/A101/gen_2/main.py) | 0 | none | valid | 2.037366 | 2.331077 | no | — | yes |
| 3 | [slot 3](runs/A101/gen_3/main.py) | 0 | 2 | valid | 2.003384 | 2.331077 | no | — | yes |
| 4 | [slot 4](runs/A101/gen_4/main.py) | 0 | 2 | valid | 2.655386 | 2.655386 | yes | — | yes |
| 5 | [slot 5](runs/A101/gen_5/main.py) | 4 | 0 | valid | 2.289481 | 2.655386 | no | — | yes |
| 6 | [slot 6](runs/A101/gen_6/main.py) | 4 | 0 | valid | 2.536238 | 2.655386 | no | — | yes |
| 7 | [slot 7](runs/A101/gen_7/main.py) | 4 | 6 | valid | 2.087563 | 2.655386 | no | — | yes |
| 8 | [slot 8](runs/A101/gen_8/main.py) | 6 | 4 | valid | 2.655386 | 2.655386 | no | 4 | yes |
| 9 | [slot 9](runs/A101/gen_9/main.py) | 0 | 4 | valid | 2.655386 | 2.655386 | no | 4 | yes |
| 10 | [slot 10](runs/A101/gen_10/main.py) | 9 | 4 | valid | 2.536238 | 2.655386 | no | 6 | yes |

### A101, proposal 1

[Exact rendered prompt](runs/A101/invocations/01/prompt.md) · [native output](runs/A101/invocations/01/codex.jsonl) · [supplied context](runs/A101/gen_1/supplied_context.json).

[Evaluation records](runs/A101/gen_1/results/).

Training: **-1.000000**; validity: **False**; current best: 2.331077; database rows: 1.

Rejection/failure: `PolicyError: Unsupported syntax or more than 400 AST nodes`. Unsupported AST types: ['Tuple']. No repair or replacement.

Source size: 263 bytes; 48 AST nodes (limits 16,000 bytes / 400 nodes).

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    if len(opponent_history) < 3:
        return 0
    if opponent_history.count(1) == 0:
        return 1
    if opponent_history[-3:] == (1, 1, 1):
        return 1
    return 0
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

[Exact rendered prompt](runs/A101/invocations/02/prompt.md) · [native output](runs/A101/invocations/02/codex.jsonl) · [supplied context](runs/A101/gen_2/supplied_context.json).

[Evaluation records](runs/A101/gen_2/results/).

Training: **2.037366**; validity: **True**; current best: 2.331077; database rows: 1.

Source size: 198 bytes; 31 AST nodes (limits 16,000 bytes / 400 nodes).

Frozen TFT probes: **fail**, 1640 checks, computed after the terminal selection freeze. Finite agreement alone is not equivalence.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    if len(opponent_history) < 3:
        return 0 if len(opponent_history) else 1
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

### A101, proposal 3

[Exact rendered prompt](runs/A101/invocations/03/prompt.md) · [native output](runs/A101/invocations/03/codex.jsonl) · [supplied context](runs/A101/gen_3/supplied_context.json).

[Evaluation records](runs/A101/gen_3/results/).

Training: **2.003384**; validity: **True**; current best: 2.331077; database rows: 1.

Source size: 183 bytes; 29 AST nodes (limits 16,000 bytes / 400 nodes).

Frozen TFT probes: **fail**, 1640 checks, computed after the terminal selection freeze. Finite agreement alone is not equivalence.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    if len(opponent_history) >= 4 and opponent_history.count(1) == 0:
        return 0
    return 1
# EVOLVE-BLOCK-END
```

**Parent: generation 0**, training 2.331077; public feedback `{"mean_payoff": 2.3310772701635645}`; text feedback ``.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 1
# EVOLVE-BLOCK-END
```

**Inspiration: generation 2**, training 2.037366; public feedback `{"mean_payoff": 2.037366046249295}`; text feedback ``.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    if len(opponent_history) < 3:
        return 0 if len(opponent_history) else 1
    return opponent_history[-1]
# EVOLVE-BLOCK-END
```

### A101, proposal 4

[Exact rendered prompt](runs/A101/invocations/04/prompt.md) · [native output](runs/A101/invocations/04/codex.jsonl) · [supplied context](runs/A101/gen_4/supplied_context.json).

[Evaluation records](runs/A101/gen_4/results/).

Training: **2.655386**; validity: **True**; current best: 2.655386; database rows: 1.

Source size: 167 bytes; 28 AST nodes (limits 16,000 bytes / 400 nodes).

Frozen TFT probes: **fail**, 1640 checks, computed after the terminal selection freeze. Finite agreement alone is not equivalence.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 or opponent_history.count(1) == 0 else 1
# EVOLVE-BLOCK-END
```

**Parent: generation 0**, training 2.331077; public feedback `{"mean_payoff": 2.3310772701635645}`; text feedback ``.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 1
# EVOLVE-BLOCK-END
```

**Inspiration: generation 2**, training 2.037366; public feedback `{"mean_payoff": 2.037366046249295}`; text feedback ``.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    if len(opponent_history) < 3:
        return 0 if len(opponent_history) else 1
    return opponent_history[-1]
# EVOLVE-BLOCK-END
```

### A101, proposal 5

[Exact rendered prompt](runs/A101/invocations/05/prompt.md) · [native output](runs/A101/invocations/05/codex.jsonl) · [supplied context](runs/A101/gen_5/supplied_context.json).

[Evaluation records](runs/A101/gen_5/results/).

Training: **2.289481**; validity: **True**; current best: 2.655386; database rows: 1.

Source size: 351 bytes; 82 AST nodes (limits 16,000 bytes / 400 nodes).

Frozen TFT probes: **fail**, 1640 checks, computed after the terminal selection freeze. Finite agreement alone is not equivalence.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) < 3 else (1 if len(opponent_history) == 3 else (0 if len(opponent_history) == 4 else (1 if len(opponent_history) == 5 and opponent_history[-1] == 0 else (1 if opponent_history.count(1) == 0 or opponent_history[-1] == 1 else 0))))
# EVOLVE-BLOCK-END
```

**Parent: generation 4**, training 2.655386; public feedback `{"mean_payoff": 2.655386350817823}`; text feedback ``.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 or opponent_history.count(1) == 0 else 1
# EVOLVE-BLOCK-END
```

**Inspiration: generation 0**, training 2.331077; public feedback `{"mean_payoff": 2.3310772701635645}`; text feedback ``.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 1
# EVOLVE-BLOCK-END
```

### A101, proposal 6

[Exact rendered prompt](runs/A101/invocations/06/prompt.md) · [native output](runs/A101/invocations/06/codex.jsonl) · [supplied context](runs/A101/gen_6/supplied_context.json).

[Evaluation records](runs/A101/gen_6/results/).

Training: **2.536238**; validity: **True**; current best: 2.655386; database rows: 1.

Source size: 152 bytes; 23 AST nodes (limits 16,000 bytes / 400 nodes).

Frozen TFT probes: **pass**, 1640 checks, computed after the terminal selection freeze. Finite agreement alone is not equivalence.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else opponent_history[-1]
# EVOLVE-BLOCK-END
```

**Parent: generation 4**, training 2.655386; public feedback `{"mean_payoff": 2.655386350817823}`; text feedback ``.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 or opponent_history.count(1) == 0 else 1
# EVOLVE-BLOCK-END
```

**Inspiration: generation 0**, training 2.331077; public feedback `{"mean_payoff": 2.3310772701635645}`; text feedback ``.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 1
# EVOLVE-BLOCK-END
```

### A101, proposal 7

[Exact rendered prompt](runs/A101/invocations/07/prompt.md) · [native output](runs/A101/invocations/07/codex.jsonl) · [supplied context](runs/A101/gen_7/supplied_context.json).

[Evaluation records](runs/A101/gen_7/results/).

Training: **2.087563**; validity: **True**; current best: 2.655386; database rows: 1.

Source size: 239 bytes; 52 AST nodes (limits 16,000 bytes / 400 nodes).

Frozen TFT probes: **fail**, 1640 checks, computed after the terminal selection freeze. Finite agreement alone is not equivalence.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) < 12 else (1 if opponent_history.count(1) == 0 else (1 if own_history[-1] == 1 and opponent_history[-1] == 0 else 0))
# EVOLVE-BLOCK-END
```

**Parent: generation 4**, training 2.655386; public feedback `{"mean_payoff": 2.655386350817823}`; text feedback ``.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 or opponent_history.count(1) == 0 else 1
# EVOLVE-BLOCK-END
```

**Inspiration: generation 6**, training 2.536238; public feedback `{"mean_payoff": 2.5362380146644106}`; text feedback ``.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else opponent_history[-1]
# EVOLVE-BLOCK-END
```

### A101, proposal 8

[Exact rendered prompt](runs/A101/invocations/08/prompt.md) · [native output](runs/A101/invocations/08/codex.jsonl) · [supplied context](runs/A101/gen_8/supplied_context.json).

[Evaluation records](runs/A101/gen_8/results/).

Training: **2.655386**; validity: **True**; current best: 2.655386; database rows: 1.

Source size: 167 bytes; 28 AST nodes (limits 16,000 bytes / 400 nodes).

Frozen TFT probes: **fail**, 1640 checks, computed after the terminal selection freeze. Finite agreement alone is not equivalence.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 or opponent_history.count(1) == 0 else 1
# EVOLVE-BLOCK-END
```

**Parent: generation 6**, training 2.536238; public feedback `{"mean_payoff": 2.5362380146644106}`; text feedback ``.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else opponent_history[-1]
# EVOLVE-BLOCK-END
```

**Inspiration: generation 4**, training 2.655386; public feedback `{"mean_payoff": 2.655386350817823}`; text feedback ``.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 or opponent_history.count(1) == 0 else 1
# EVOLVE-BLOCK-END
```

### A101, proposal 9

[Exact rendered prompt](runs/A101/invocations/09/prompt.md) · [native output](runs/A101/invocations/09/codex.jsonl) · [supplied context](runs/A101/gen_9/supplied_context.json).

[Evaluation records](runs/A101/gen_9/results/).

Training: **2.655386**; validity: **True**; current best: 2.655386; database rows: 1.

Source size: 167 bytes; 28 AST nodes (limits 16,000 bytes / 400 nodes).

Frozen TFT probes: **fail**, 1640 checks, computed after the terminal selection freeze. Finite agreement alone is not equivalence.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 or opponent_history.count(1) == 0 else 1
# EVOLVE-BLOCK-END
```

**Parent: generation 0**, training 2.331077; public feedback `{"mean_payoff": 2.3310772701635645}`; text feedback ``.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 1
# EVOLVE-BLOCK-END
```

**Inspiration: generation 4**, training 2.655386; public feedback `{"mean_payoff": 2.655386350817823}`; text feedback ``.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 or opponent_history.count(1) == 0 else 1
# EVOLVE-BLOCK-END
```

### A101, proposal 10

[Exact rendered prompt](runs/A101/invocations/10/prompt.md) · [native output](runs/A101/invocations/10/codex.jsonl) · [supplied context](runs/A101/gen_10/supplied_context.json).

[Evaluation records](runs/A101/gen_10/results/).

Training: **2.536238**; validity: **True**; current best: 2.655386; database rows: 1.

Source size: 152 bytes; 23 AST nodes (limits 16,000 bytes / 400 nodes).

Frozen TFT probes: **pass**, 1640 checks, computed after the terminal selection freeze. Finite agreement alone is not equivalence.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else opponent_history[-1]
# EVOLVE-BLOCK-END
```

**Parent: generation 9**, training 2.655386; public feedback `{"mean_payoff": 2.655386350817823}`; text feedback ``.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 or opponent_history.count(1) == 0 else 1
# EVOLVE-BLOCK-END
```

**Inspiration: generation 4**, training 2.655386; public feedback `{"mean_payoff": 2.655386350817823}`; text feedback ``.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 or opponent_history.count(1) == 0 else 1
# EVOLVE-BLOCK-END
```

## B101 — incomplete

| Slot | Source | Parent | Inspirations | Validity | Training | Best so far | New best | AST duplicate of | Archived |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | [slot 1](runs/B101/gen_1/main.py) | 0 | none | valid | 2.536238 | 2.536238 | yes | — | yes |
| 2 | [slot 2](runs/B101/gen_2/main.py) | 0 | none | valid | 2.655386 | 2.655386 | yes | — | yes |
| 3 | [slot 3](runs/B101/gen_3/main.py) | 0 | none | valid | 2.369007 | 2.655386 | no | — | yes |
| 4 | [slot 4](runs/B101/gen_4/main.py) | 0 | none | valid | 2.474055 | 2.655386 | no | — | yes |
| 5 | [slot 5](runs/B101/gen_5/main.py) | 0 | none | valid | 2.536238 | 2.655386 | no | — | yes |
| 6 | [slot 6](runs/B101/gen_6/main.py) | 0 | none | valid | 2.432459 | 2.655386 | no | — | yes |
| 7 | [slot 7](runs/B101/gen_7/main.py) | 0 | none | valid | 2.536238 | 2.655386 | no | — | yes |
| 8 | [slot 8](runs/B101/gen_8/main.py) | 0 | none | valid | 2.536238 | 2.655386 | no | 5 | yes |
| 9 | [slot 9](runs/B101/gen_9/main.py) | 0 | none | valid | 2.536238 | 2.655386 | no | 5 | yes |
| 10 | no canonical file | 0 | none | failed_or_unparsed | unavailable | unavailable | no | — | no |

### B101, proposal 1

[Exact rendered prompt](runs/B101/invocations/01/prompt.md) · [native output](runs/B101/invocations/01/codex.jsonl) · [supplied context](runs/B101/gen_1/supplied_context.json).

[Evaluation records](runs/B101/gen_1/results/).

Training: **2.536238**; validity: **True**; current best: 2.536238; database rows: 1.

Source size: 146 bytes; 19 AST nodes (limits 16,000 bytes / 400 nodes).

Frozen TFT probes: **pass**, 1640 checks, computed after the terminal selection freeze. Finite agreement alone is not equivalence.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if not opponent_history else opponent_history[-1]
# EVOLVE-BLOCK-END
```

Fresh session; unchanged seed-only information. The backend enforces byte equality with the [frozen initial prompt](protocol/initial_prompt.md), and the native-session audit checks the only user message against that prompt. No prior candidate, score, validity, recognition, or holdout result is supplied.

### B101, proposal 2

[Exact rendered prompt](runs/B101/invocations/02/prompt.md) · [native output](runs/B101/invocations/02/codex.jsonl) · [supplied context](runs/B101/gen_2/supplied_context.json).

[Evaluation records](runs/B101/gen_2/results/).

Training: **2.655386**; validity: **True**; current best: 2.655386; database rows: 1.

Source size: 132 bytes; 15 AST nodes (limits 16,000 bytes / 400 nodes).

Frozen TFT probes: **fail**, 1640 checks, computed after the terminal selection freeze. Finite agreement alone is not equivalence.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 1 if opponent_history.count(1) else 0
# EVOLVE-BLOCK-END
```

Fresh session; unchanged seed-only information. The backend enforces byte equality with the [frozen initial prompt](protocol/initial_prompt.md), and the native-session audit checks the only user message against that prompt. No prior candidate, score, validity, recognition, or holdout result is supplied.

### B101, proposal 3

[Exact rendered prompt](runs/B101/invocations/03/prompt.md) · [native output](runs/B101/invocations/03/codex.jsonl) · [supplied context](runs/B101/gen_3/supplied_context.json).

[Evaluation records](runs/B101/gen_3/results/).

Training: **2.369007**; validity: **True**; current best: 2.655386; database rows: 1.

Source size: 385 bytes; 76 AST nodes (limits 16,000 bytes / 400 nodes).

Frozen TFT probes: **fail**, 1640 checks, computed after the terminal selection freeze. Finite agreement alone is not equivalence.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    if len(opponent_history) == 0:
        return 1
    if len(opponent_history) == 1:
        return 0
    if len(opponent_history) == 2 and opponent_history[0] == 0 and opponent_history[1] == 1:
        return 0
    if opponent_history.count(1) == 0:
        return 1
    return opponent_history[-1]
# EVOLVE-BLOCK-END
```

Fresh session; unchanged seed-only information. The backend enforces byte equality with the [frozen initial prompt](protocol/initial_prompt.md), and the native-session audit checks the only user message against that prompt. No prior candidate, score, validity, recognition, or holdout result is supplied.

### B101, proposal 4

[Exact rendered prompt](runs/B101/invocations/04/prompt.md) · [native output](runs/B101/invocations/04/codex.jsonl) · [supplied context](runs/B101/gen_4/supplied_context.json).

[Evaluation records](runs/B101/gen_4/results/).

Training: **2.474055**; validity: **True**; current best: 2.655386; database rows: 1.

Source size: 213 bytes; 42 AST nodes (limits 16,000 bytes / 400 nodes).

Frozen TFT probes: **fail**, 1640 checks, computed after the terminal selection freeze. Finite agreement alone is not equivalence.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    if len(opponent_history) < 2:
        return 0
    return 1 if opponent_history[-1] == 1 and opponent_history[-2] == 1 else 0
# EVOLVE-BLOCK-END
```

Fresh session; unchanged seed-only information. The backend enforces byte equality with the [frozen initial prompt](protocol/initial_prompt.md), and the native-session audit checks the only user message against that prompt. No prior candidate, score, validity, recognition, or holdout result is supplied.

### B101, proposal 5

[Exact rendered prompt](runs/B101/invocations/05/prompt.md) · [native output](runs/B101/invocations/05/codex.jsonl) · [supplied context](runs/B101/gen_5/supplied_context.json).

[Evaluation records](runs/B101/gen_5/results/).

Training: **2.536238**; validity: **True**; current best: 2.655386; database rows: 1.

Source size: 152 bytes; 23 AST nodes (limits 16,000 bytes / 400 nodes).

Frozen TFT probes: **pass**, 1640 checks, computed after the terminal selection freeze. Finite agreement alone is not equivalence.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else opponent_history[-1]
# EVOLVE-BLOCK-END
```

Fresh session; unchanged seed-only information. The backend enforces byte equality with the [frozen initial prompt](protocol/initial_prompt.md), and the native-session audit checks the only user message against that prompt. No prior candidate, score, validity, recognition, or holdout result is supplied.

### B101, proposal 6

[Exact rendered prompt](runs/B101/invocations/06/prompt.md) · [native output](runs/B101/invocations/06/codex.jsonl) · [supplied context](runs/B101/gen_6/supplied_context.json).

[Evaluation records](runs/B101/gen_6/results/).

Training: **2.432459**; validity: **True**; current best: 2.655386; database rows: 1.

Source size: 223 bytes; 49 AST nodes (limits 16,000 bytes / 400 nodes).

Frozen TFT probes: **fail**, 1640 checks, computed after the terminal selection freeze. Finite agreement alone is not equivalence.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 1 if len(opponent_history) == 0 or opponent_history[-1] == 0 or (len(opponent_history) > 1 and opponent_history[-2] == 1) else 0
# EVOLVE-BLOCK-END
```

Fresh session; unchanged seed-only information. The backend enforces byte equality with the [frozen initial prompt](protocol/initial_prompt.md), and the native-session audit checks the only user message against that prompt. No prior candidate, score, validity, recognition, or holdout result is supplied.

### B101, proposal 7

[Exact rendered prompt](runs/B101/invocations/07/prompt.md) · [native output](runs/B101/invocations/07/codex.jsonl) · [supplied context](runs/B101/gen_7/supplied_context.json).

[Evaluation records](runs/B101/gen_7/results/).

Training: **2.536238**; validity: **True**; current best: 2.655386; database rows: 1.

Source size: 165 bytes; 25 AST nodes (limits 16,000 bytes / 400 nodes).

Frozen TFT probes: **pass**, 1640 checks, computed after the terminal selection freeze. Finite agreement alone is not equivalence.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if not opponent_history else (1 if opponent_history[-1] == 1 else 0)
# EVOLVE-BLOCK-END
```

Fresh session; unchanged seed-only information. The backend enforces byte equality with the [frozen initial prompt](protocol/initial_prompt.md), and the native-session audit checks the only user message against that prompt. No prior candidate, score, validity, recognition, or holdout result is supplied.

### B101, proposal 8

[Exact rendered prompt](runs/B101/invocations/08/prompt.md) · [native output](runs/B101/invocations/08/codex.jsonl) · [supplied context](runs/B101/gen_8/supplied_context.json).

[Evaluation records](runs/B101/gen_8/results/).

Training: **2.536238**; validity: **True**; current best: 2.655386; database rows: 1.

Source size: 152 bytes; 23 AST nodes (limits 16,000 bytes / 400 nodes).

Frozen TFT probes: **pass**, 1640 checks, computed after the terminal selection freeze. Finite agreement alone is not equivalence.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else opponent_history[-1]
# EVOLVE-BLOCK-END
```

Fresh session; unchanged seed-only information. The backend enforces byte equality with the [frozen initial prompt](protocol/initial_prompt.md), and the native-session audit checks the only user message against that prompt. No prior candidate, score, validity, recognition, or holdout result is supplied.

### B101, proposal 9

[Exact rendered prompt](runs/B101/invocations/09/prompt.md) · [native output](runs/B101/invocations/09/codex.jsonl) · [supplied context](runs/B101/gen_9/supplied_context.json).

[Evaluation records](runs/B101/gen_9/results/).

Training: **2.536238**; validity: **True**; current best: 2.655386; database rows: 1.

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

[Exact rendered prompt](runs/B101/invocations/10/prompt.md) · [native output](runs/B101/invocations/10/codex.jsonl) · [supplied context](runs/B101/gen_10/supplied_context.json).

[Evaluation records](runs/B101/gen_10/results/).

[Native failure record](runs/B101/gen_10/failure.json). This external invocation consumed a slot but supplied no canonical policy or measured payoff.

Training: **unavailable**; validity: **False**; current best: 2.655386; database rows: 0.

Rejection/failure: `No canonical generated source; inspect raw response/failure`. Unsupported AST types: []. No repair or replacement.

```python
# No canonical source; raw response and failure retained.
```

Fresh session; unchanged seed-only information. The backend enforces byte equality with the [frozen initial prompt](protocol/initial_prompt.md), and the native-session audit checks the only user message against that prompt. No prior candidate, score, validity, recognition, or holdout result is supplied.

## B202 — not_started

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

### B202, proposal 1

**not_attempted**. No external proposal, generated source, or measured payoff. The stopped ledger was not reset.

### B202, proposal 2

**not_attempted**. No external proposal, generated source, or measured payoff. The stopped ledger was not reset.

### B202, proposal 3

**not_attempted**. No external proposal, generated source, or measured payoff. The stopped ledger was not reset.

### B202, proposal 4

**not_attempted**. No external proposal, generated source, or measured payoff. The stopped ledger was not reset.

### B202, proposal 5

**not_attempted**. No external proposal, generated source, or measured payoff. The stopped ledger was not reset.

### B202, proposal 6

**not_attempted**. No external proposal, generated source, or measured payoff. The stopped ledger was not reset.

### B202, proposal 7

**not_attempted**. No external proposal, generated source, or measured payoff. The stopped ledger was not reset.

### B202, proposal 8

**not_attempted**. No external proposal, generated source, or measured payoff. The stopped ledger was not reset.

### B202, proposal 9

**not_attempted**. No external proposal, generated source, or measured payoff. The stopped ledger was not reset.

### B202, proposal 10

**not_attempted**. No external proposal, generated source, or measured payoff. The stopped ledger was not reset.

## A202 — not_started

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

### A202, proposal 1

**not_attempted**. No external proposal, generated source, or measured payoff. The stopped ledger was not reset.

### A202, proposal 2

**not_attempted**. No external proposal, generated source, or measured payoff. The stopped ledger was not reset.

### A202, proposal 3

**not_attempted**. No external proposal, generated source, or measured payoff. The stopped ledger was not reset.

### A202, proposal 4

**not_attempted**. No external proposal, generated source, or measured payoff. The stopped ledger was not reset.

### A202, proposal 5

**not_attempted**. No external proposal, generated source, or measured payoff. The stopped ledger was not reset.

### A202, proposal 6

**not_attempted**. No external proposal, generated source, or measured payoff. The stopped ledger was not reset.

### A202, proposal 7

**not_attempted**. No external proposal, generated source, or measured payoff. The stopped ledger was not reset.

### A202, proposal 8

**not_attempted**. No external proposal, generated source, or measured payoff. The stopped ledger was not reset.

### A202, proposal 9

**not_attempted**. No external proposal, generated source, or measured payoff. The stopped ledger was not reset.

### A202, proposal 10

**not_attempted**. No external proposal, generated source, or measured payoff. The stopped ledger was not reset.

## A303 — not_started

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

### A303, proposal 1

**not_attempted**. No external proposal, generated source, or measured payoff. The stopped ledger was not reset.

### A303, proposal 2

**not_attempted**. No external proposal, generated source, or measured payoff. The stopped ledger was not reset.

### A303, proposal 3

**not_attempted**. No external proposal, generated source, or measured payoff. The stopped ledger was not reset.

### A303, proposal 4

**not_attempted**. No external proposal, generated source, or measured payoff. The stopped ledger was not reset.

### A303, proposal 5

**not_attempted**. No external proposal, generated source, or measured payoff. The stopped ledger was not reset.

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
