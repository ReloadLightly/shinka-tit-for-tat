# E1-R measured evidence

| Run | Training-selected source | Training | Development holdout | Valid/rejected-or-failed/unevaluated/duplicate | TFT-probe-compatible slots | Improved after first? |
| --- | --- | --- | --- | --- | --- | --- |
| A101 (complete) | [slot 4](runs/A101/gen_4/main.py) | 2.655386 | 2.649804 | 9/1/0/3 | 6, 10 | yes |
| B101 (incomplete) | [slot 2](runs/B101/gen_2/main.py) | 2.655386 | unavailable | 9/1/0/2 | 1, 5, 7, 8, 9 | yes |
| B202 (not_started) | none; seed placeholder only | unavailable | unavailable | 0/0/0/0 | none | unavailable |
| A202 (not_started) | none; seed placeholder only | unavailable | unavailable | 0/0/0/0 | none | unavailable |
| A303 (not_started) | none; seed placeholder only | unavailable | unavailable | 0/0/0/0 | none | unavailable |
| B303 (not_started) | none; seed placeholder only | unavailable | unavailable | 0/0/0/0 | none | unavailable |

Duplicates overlap validity counts; they are not an additional class. Seed 0 is eligible, but not included in the ten-proposal validity denominator.

Validity means live evaluator acceptance; duplicates overlap validity. Incomplete/unstarted runs have no primary outcome. Missing results are never zero payoff.

| Run | Generated sources | Live-valid | Interpreter rejections | No-source failed invocation | Valid / consumed opportunities |
| --- | --- | --- | --- | --- | --- |
| A101 | 10 | 9 | 1 | 0 | 9/10 |
| B101 | 9 | 9 | 0 | 1 | 9/10 |
| B202 | 0 | 0 | 0 | 0 | unavailable |
| A202 | 0 | 0 | 0 | 0 | unavailable |
| A303 | 0 | 0 | 0 | 0 | unavailable |
| B303 | 0 | 0 | 0 | 0 | unavailable |

E1-R applies the frozen earliest-appearance tie rule. Shinka can record a later tied program as its own best; that pointer does not override E1-R's predeclared selection. Both records are retained:

| Run | E1-R selected slot | Shinka recorded best slot | DB rows including seed | Archive members including seed |
| --- | --- | --- | --- | --- |
| A101 | 4 | 9 | 11 | 10 |
| B101 | 2 | 2 | 10 | 10 |
| B202 | 0 | None | 0 | 0 |
| A202 | 0 | None | 0 | 0 |
| A303 | 0 | None | 0 | 0 |
| B303 | 0 | None | 0 | 0 |

| Paired local seed | A holdout | B holdout | A minus B |
| --- | --- | --- | --- |
| 101 | 2.649804 | unavailable | unavailable |
| 202 | unavailable | unavailable | unavailable |
| 303 | unavailable | unavailable | unavailable |

Descriptive paired summary: n=0.

There are zero available completed pairs. Mean, median, range and sample SD are undefined; no effect estimate can be computed.

## Usage

| Run | Invocations | Codex turn events | Model response records | Input | Cached subset | Output | Reasoning subset | Codex seconds | Tool calls |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A101 | 10 | 10 | 10 | 57590 | 19456 | 9025 | 7699 | 413.0 | 0 |
| B101 | 10 | 9 | 9 | 51093 | 14592 | 6444 | 5349 | 285.0 | 0 |
| B202 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0.0 | 0 |
| A202 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0.0 | 0 |
| A303 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0.0 | 0 |
| B303 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0.0 | 0 |

Invocations can contain multiple model requests; equal invocation budgets do not imply equal tokens or runtime. Cached/reasoning counts are subsets. Native Headless list-price cost estimates are not subscription charges.

## Complete selected source: A101

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 or opponent_history.count(1) == 0 else 1
# EVOLVE-BLOCK-END
```

Source SHA-256: `fc938dea6c869791ffb3d7fbbb03f95b21ea86152fb3414345a9d107323d56a1`.

Trace test key: **T1** = `len(opponent_history) == 0 or opponent_history.count(1) == 0`.

### Scored encounter trace: train / always_defect / seed 11

First 8 rounds of the actual 174-round evaluated encounter; full-match candidate payoff 173. C=0, D=1. Tests are listed in actual interpreter execution order; true/false identifies the executed branch. The replay's full totals are asserted equal to the unchanged evaluator.

| Round | Own history | Opponent history | Executed tests | Actions own/other | Payoff own/other | Cumulative own/other |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | empty | empty | T1=true | 0/1 | 0/5 | 0/5 |
| 2 | 0 | 1 | T1=false | 1/1 | 1/1 | 1/6 |
| 3 | 01 | 11 | T1=false | 1/1 | 1/1 | 2/7 |
| 4 | 011 | 111 | T1=false | 1/1 | 1/1 | 3/8 |
| 5 | 0111 | 1111 | T1=false | 1/1 | 1/1 | 4/9 |
| 6 | 01111 | 11111 | T1=false | 1/1 | 1/1 | 5/10 |
| 7 | 011111 | 111111 | T1=false | 1/1 | 1/1 | 6/11 |
| 8 | 0111111 | 1111111 | T1=false | 1/1 | 1/1 | 7/12 |

### Scored encounter trace: train / random / seed 11

First 8 rounds of the actual 174-round evaluated encounter; full-match candidate payoff 521. C=0, D=1. Tests are listed in actual interpreter execution order; true/false identifies the executed branch. The replay's full totals are asserted equal to the unchanged evaluator.

| Round | Own history | Opponent history | Executed tests | Actions own/other | Payoff own/other | Cumulative own/other |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | empty | empty | T1=true | 0/0 | 3/3 | 3/3 |
| 2 | 0 | 0 | T1=true | 0/0 | 3/3 | 6/6 |
| 3 | 00 | 00 | T1=true | 0/1 | 0/5 | 6/11 |
| 4 | 000 | 001 | T1=false | 1/0 | 5/0 | 11/11 |
| 5 | 0001 | 0010 | T1=false | 1/1 | 1/1 | 12/12 |
| 6 | 00011 | 00101 | T1=false | 1/1 | 1/1 | 13/13 |
| 7 | 000111 | 001011 | T1=false | 1/1 | 1/1 | 14/14 |
| 8 | 0001111 | 0010111 | T1=false | 1/1 | 1/1 | 15/15 |

### Scored encounter trace: train / tit_for_tat / seed 11

First 8 rounds of the actual 174-round evaluated encounter; full-match candidate payoff 522. C=0, D=1. Tests are listed in actual interpreter execution order; true/false identifies the executed branch. The replay's full totals are asserted equal to the unchanged evaluator.

| Round | Own history | Opponent history | Executed tests | Actions own/other | Payoff own/other | Cumulative own/other |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | empty | empty | T1=true | 0/0 | 3/3 | 3/3 |
| 2 | 0 | 0 | T1=true | 0/0 | 3/3 | 6/6 |
| 3 | 00 | 00 | T1=true | 0/0 | 3/3 | 9/9 |
| 4 | 000 | 000 | T1=true | 0/0 | 3/3 | 12/12 |
| 5 | 0000 | 0000 | T1=true | 0/0 | 3/3 | 15/15 |
| 6 | 00000 | 00000 | T1=true | 0/0 | 3/3 | 18/18 |
| 7 | 000000 | 000000 | T1=true | 0/0 | 3/3 | 21/21 |
| 8 | 0000000 | 0000000 | T1=true | 0/0 | 3/3 | 24/24 |

### Scored encounter trace: holdout / alternator / seed 211

First 8 rounds of the actual 241-round evaluated encounter; full-match candidate payoff 722. C=0, D=1. Tests are listed in actual interpreter execution order; true/false identifies the executed branch. The replay's full totals are asserted equal to the unchanged evaluator.

| Round | Own history | Opponent history | Executed tests | Actions own/other | Payoff own/other | Cumulative own/other |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | empty | empty | T1=true | 0/0 | 3/3 | 3/3 |
| 2 | 0 | 0 | T1=true | 0/1 | 0/5 | 3/8 |
| 3 | 00 | 01 | T1=false | 1/0 | 5/0 | 8/8 |
| 4 | 001 | 010 | T1=false | 1/1 | 1/1 | 9/9 |
| 5 | 0011 | 0101 | T1=false | 1/0 | 5/0 | 14/9 |
| 6 | 00111 | 01010 | T1=false | 1/1 | 1/1 | 15/10 |
| 7 | 001111 | 010101 | T1=false | 1/0 | 5/0 | 20/10 |
| 8 | 0011111 | 0101010 | T1=false | 1/1 | 1/1 | 21/11 |

### Opponent payoff and cooperation

Cells show own payoff per round and own cooperation percentage, aggregated across the five scored matches for that opponent. All comparators use identical encounters.

**train**

| Opponent | Selected | Seed | TFT | Grim | Ordinary WSLS |
| --- | --- | --- | --- | --- | --- |
| always_cooperate | 3.0000 (100.0%) | 5.0000 (0.0%) | 3.0000 (100.0%) | 3.0000 (100.0%) | 3.0000 (100.0%) |
| always_defect | 0.9958 (0.4%) | 1.0000 (0.0%) | 0.9958 (0.4%) | 0.9958 (0.4%) | 0.4992 (50.1%) |
| random | 2.9365 (0.8%) | 2.9492 (0.0%) | 2.2217 (48.9%) | 2.9365 (0.8%) | 2.2073 (50.0%) |
| tit_for_tat | 3.0000 (100.0%) | 1.0169 (0.0%) | 3.0000 (100.0%) | 3.0000 (100.0%) | 3.0000 (100.0%) |
| grim | 3.0000 (100.0%) | 1.0169 (0.0%) | 3.0000 (100.0%) | 3.0000 (100.0%) | 3.0000 (100.0%) |
| win_stay_lose_shift | 3.0000 (100.0%) | 3.0034 (0.0%) | 3.0000 (100.0%) | 3.0000 (100.0%) | 3.0000 (100.0%) |

**holdout**

| Opponent | Selected | Seed | TFT | Grim | Ordinary WSLS |
| --- | --- | --- | --- | --- | --- |
| alternator | 2.9918 (1.2%) | 3.0094 (0.0%) | 2.5000 (50.4%) | 2.9918 (1.2%) | 2.2529 (50.4%) |
| suspicious_tit_for_tat | 1.0176 (0.6%) | 1.0000 (0.0%) | 2.4882 (50.2%) | 1.0176 (0.6%) | 1.9953 (33.6%) |
| tit_for_two_tats | 3.0000 (100.0%) | 1.0471 (0.0%) | 3.0000 (100.0%) | 3.0000 (100.0%) | 3.0000 (100.0%) |
| hard_tit_for_tat | 3.0000 (100.0%) | 1.0235 (0.0%) | 3.0000 (100.0%) | 3.0000 (100.0%) | 3.0000 (100.0%) |
| random_20 | 1.7918 (0.7%) | 1.8000 (0.0%) | 1.5494 (20.6%) | 1.7918 (0.7%) | 1.1718 (51.5%) |
| random_80 | 4.0976 (1.9%) | 4.1294 (0.0%) | 2.7282 (78.4%) | 4.0976 (1.9%) | 3.2459 (49.6%) |

## Complete selected source: B101 (partial)

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 1 if opponent_history.count(1) else 0
# EVOLVE-BLOCK-END
```

Source SHA-256: `68b703128085b98c09b5ff66507e9d3e1ba1ff0b49201bfb6b72c0c4b475acf1`.

Trace test key: **T1** = `opponent_history.count(1)`.

### Scored encounter trace: train / always_defect / seed 11

First 8 rounds of the actual 174-round evaluated encounter; full-match candidate payoff 173. C=0, D=1. Tests are listed in actual interpreter execution order; true/false identifies the executed branch. The replay's full totals are asserted equal to the unchanged evaluator.

| Round | Own history | Opponent history | Executed tests | Actions own/other | Payoff own/other | Cumulative own/other |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | empty | empty | T1=false | 0/1 | 0/5 | 0/5 |
| 2 | 0 | 1 | T1=true | 1/1 | 1/1 | 1/6 |
| 3 | 01 | 11 | T1=true | 1/1 | 1/1 | 2/7 |
| 4 | 011 | 111 | T1=true | 1/1 | 1/1 | 3/8 |
| 5 | 0111 | 1111 | T1=true | 1/1 | 1/1 | 4/9 |
| 6 | 01111 | 11111 | T1=true | 1/1 | 1/1 | 5/10 |
| 7 | 011111 | 111111 | T1=true | 1/1 | 1/1 | 6/11 |
| 8 | 0111111 | 1111111 | T1=true | 1/1 | 1/1 | 7/12 |

### Scored encounter trace: train / random / seed 11

First 8 rounds of the actual 174-round evaluated encounter; full-match candidate payoff 521. C=0, D=1. Tests are listed in actual interpreter execution order; true/false identifies the executed branch. The replay's full totals are asserted equal to the unchanged evaluator.

| Round | Own history | Opponent history | Executed tests | Actions own/other | Payoff own/other | Cumulative own/other |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | empty | empty | T1=false | 0/0 | 3/3 | 3/3 |
| 2 | 0 | 0 | T1=false | 0/0 | 3/3 | 6/6 |
| 3 | 00 | 00 | T1=false | 0/1 | 0/5 | 6/11 |
| 4 | 000 | 001 | T1=true | 1/0 | 5/0 | 11/11 |
| 5 | 0001 | 0010 | T1=true | 1/1 | 1/1 | 12/12 |
| 6 | 00011 | 00101 | T1=true | 1/1 | 1/1 | 13/13 |
| 7 | 000111 | 001011 | T1=true | 1/1 | 1/1 | 14/14 |
| 8 | 0001111 | 0010111 | T1=true | 1/1 | 1/1 | 15/15 |

### Scored encounter trace: train / tit_for_tat / seed 11

First 8 rounds of the actual 174-round evaluated encounter; full-match candidate payoff 522. C=0, D=1. Tests are listed in actual interpreter execution order; true/false identifies the executed branch. The replay's full totals are asserted equal to the unchanged evaluator.

| Round | Own history | Opponent history | Executed tests | Actions own/other | Payoff own/other | Cumulative own/other |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | empty | empty | T1=false | 0/0 | 3/3 | 3/3 |
| 2 | 0 | 0 | T1=false | 0/0 | 3/3 | 6/6 |
| 3 | 00 | 00 | T1=false | 0/0 | 3/3 | 9/9 |
| 4 | 000 | 000 | T1=false | 0/0 | 3/3 | 12/12 |
| 5 | 0000 | 0000 | T1=false | 0/0 | 3/3 | 15/15 |
| 6 | 00000 | 00000 | T1=false | 0/0 | 3/3 | 18/18 |
| 7 | 000000 | 000000 | T1=false | 0/0 | 3/3 | 21/21 |
| 8 | 0000000 | 0000000 | T1=false | 0/0 | 3/3 | 24/24 |

### Opponent payoff and cooperation

Cells show own payoff per round and own cooperation percentage, aggregated across the five scored matches for that opponent. All comparators use identical encounters.

**train**

| Opponent | Selected | Seed | TFT | Grim | Ordinary WSLS |
| --- | --- | --- | --- | --- | --- |
| always_cooperate | 3.0000 (100.0%) | 5.0000 (0.0%) | 3.0000 (100.0%) | 3.0000 (100.0%) | 3.0000 (100.0%) |
| always_defect | 0.9958 (0.4%) | 1.0000 (0.0%) | 0.9958 (0.4%) | 0.9958 (0.4%) | 0.4992 (50.1%) |
| random | 2.9365 (0.8%) | 2.9492 (0.0%) | 2.2217 (48.9%) | 2.9365 (0.8%) | 2.2073 (50.0%) |
| tit_for_tat | 3.0000 (100.0%) | 1.0169 (0.0%) | 3.0000 (100.0%) | 3.0000 (100.0%) | 3.0000 (100.0%) |
| grim | 3.0000 (100.0%) | 1.0169 (0.0%) | 3.0000 (100.0%) | 3.0000 (100.0%) | 3.0000 (100.0%) |
| win_stay_lose_shift | 3.0000 (100.0%) | 3.0034 (0.0%) | 3.0000 (100.0%) | 3.0000 (100.0%) | 3.0000 (100.0%) |

holdout evaluation unavailable: Run incomplete/unstarted; no primary holdout result computed.
