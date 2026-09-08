# E1 measured evidence

| Run | Training-selected source | Training | Development holdout | Valid/invalid/unevaluated/duplicate | TFT-probe-compatible slots | Improved after first? |
| --- | --- | --- | --- | --- | --- | --- |
| A101 (complete) | [slot 1](runs/A101/gen_1/main.py) | 2.536238 | 2.544314 | 10/0/0/1 | 1, 5, 7 | no |
| B101 (complete) | [slot 1](runs/B101/gen_1/main.py) | 2.536238 | 2.544314 | 9/0/1/6 | 1, 2, 4, 5, 6, 7, 8, 9 | no |
| B202 (complete) | [slot 2](runs/B202/gen_2/main.py) | 2.536238 | 2.544314 | 10/0/0/3 | 2, 3, 5, 6, 8, 10 | yes |
| A202 (complete) | [slot 5](runs/A202/gen_5/main.py) | 2.570925 | 2.434118 | 8/2/0/1 | 1 | yes |
| A303 (incomplete) | [slot 1](runs/A303/gen_1/main.py) | 2.536238 | unavailable | 3/0/1/0 | 1 | no |
| B303 (not_started) | none; seed placeholder only | unavailable | unavailable | 0/0/0/0 | none | unavailable |

Duplicates overlap validity counts; they are not an additional class. Seed 0 is eligible, but not included in the ten-proposal validity denominator.

B101 slot 3 and A303 slot 4 lack live evaluator results because of the upstream timer defect. A303 additionally has one blocked prelaunch check and five unattempted opportunities. B303 has ten unattempted opportunities. A303's training selection is provisional; neither unfinished run contributes a primary holdout result. Validity here means live evaluator acceptance, not a pure measure of generated syntax quality.

E1 applies the frozen earliest-appearance tie rule. Shinka can record a later tied program as its own best; that pointer does not override E1's predeclared selection. Both records are retained:

| Run | E1 selected slot | Shinka recorded best slot | DB rows including seed | Archive members including seed |
| --- | --- | --- | --- | --- |
| A101 | 1 | 7 | 11 | 11 |
| B101 | 1 | 9 | 11 | 10 |
| B202 | 2 | 10 | 11 | 11 |
| A202 | 5 | 8 | 11 | 9 |
| A303 | 1 | 1 | 5 | 4 |
| B303 | 0 | None | 0 | 0 |

| Paired local seed | A holdout | B holdout | A minus B |
| --- | --- | --- | --- |
| 101 | 2.544314 | 2.544314 | 0.000000 |
| 202 | 2.434118 | 2.544314 | -0.110196 |
| 303 | unavailable | unavailable | unavailable |

Descriptive paired summary: n=2.000000; mean=-0.055098; median=-0.055098; min=-0.110196; max=0.000000; sample_sd=0.077920.

## Usage

| Run | Invocations | Codex turn events | Model response records | Input | Cached subset | Output | Reasoning subset | Codex seconds | Tool calls |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A101 | 10 | 10 | 10 | 57751 | 14592 | 8283 | 6774 | 285.5 | 0 |
| B101 | 10 | 10 | 10 | 56770 | 29184 | 7196 | 6016 | 268.4 | 0 |
| B202 | 10 | 10 | 10 | 56770 | 29184 | 6447 | 5193 | 253.3 | 0 |
| A202 | 10 | 10 | 10 | 59985 | 49664 | 11866 | 8842 | 336.6 | 0 |
| A303 | 4 | 4 | 4 | 23020 | 14592 | 5247 | 4569 | 160.1 | 0 |
| B303 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0.0 | 0 |

Invocations can contain multiple model requests; equal invocation budgets do not imply equal tokens or runtime. Cached/reasoning counts are subsets. Native Headless list-price cost estimates are not subscription charges.

## Complete selected source: A101, B101

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else opponent_history[-1]
# EVOLVE-BLOCK-END
```

Source SHA-256: `f10d41828a82b0716d21b12e3d60d2102411c4e51c935a7aa9d75a9658be4cb5`.

Trace test key: **T1** = `len(opponent_history) == 0`.

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

First 8 rounds of the actual 174-round evaluated encounter; full-match candidate payoff 396. C=0, D=1. Tests are listed in actual interpreter execution order; true/false identifies the executed branch. The replay's full totals are asserted equal to the unchanged evaluator.

| Round | Own history | Opponent history | Executed tests | Actions own/other | Payoff own/other | Cumulative own/other |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | empty | empty | T1=true | 0/0 | 3/3 | 3/3 |
| 2 | 0 | 0 | T1=false | 0/0 | 3/3 | 6/6 |
| 3 | 00 | 00 | T1=false | 0/1 | 0/5 | 6/11 |
| 4 | 000 | 001 | T1=false | 1/0 | 5/0 | 11/11 |
| 5 | 0001 | 0010 | T1=false | 0/1 | 0/5 | 11/16 |
| 6 | 00010 | 00101 | T1=false | 1/1 | 1/1 | 12/17 |
| 7 | 000101 | 001011 | T1=false | 1/1 | 1/1 | 13/18 |
| 8 | 0001011 | 0010111 | T1=false | 1/1 | 1/1 | 14/19 |

### Opponent payoff and cooperation

Cells show own payoff per round and own cooperation percentage, aggregated across the five scored matches for that opponent. All comparators use identical encounters.

**train**

| Opponent | Selected | Seed | TFT | Grim | Ordinary WSLS |
| --- | --- | --- | --- | --- | --- |
| always_cooperate | 3.0000 (100.0%) | 5.0000 (0.0%) | 3.0000 (100.0%) | 3.0000 (100.0%) | 3.0000 (100.0%) |
| always_defect | 0.9958 (0.4%) | 1.0000 (0.0%) | 0.9958 (0.4%) | 0.9958 (0.4%) | 0.4992 (50.1%) |
| random | 2.2217 (48.9%) | 2.9492 (0.0%) | 2.2217 (48.9%) | 2.9365 (0.8%) | 2.2073 (50.0%) |
| tit_for_tat | 3.0000 (100.0%) | 1.0169 (0.0%) | 3.0000 (100.0%) | 3.0000 (100.0%) | 3.0000 (100.0%) |
| grim | 3.0000 (100.0%) | 1.0169 (0.0%) | 3.0000 (100.0%) | 3.0000 (100.0%) | 3.0000 (100.0%) |
| win_stay_lose_shift | 3.0000 (100.0%) | 3.0034 (0.0%) | 3.0000 (100.0%) | 3.0000 (100.0%) | 3.0000 (100.0%) |

**holdout**

| Opponent | Selected | Seed | TFT | Grim | Ordinary WSLS |
| --- | --- | --- | --- | --- | --- |
| alternator | 2.5000 (50.4%) | 3.0094 (0.0%) | 2.5000 (50.4%) | 2.9918 (1.2%) | 2.2529 (50.4%) |
| suspicious_tit_for_tat | 2.4882 (50.2%) | 1.0000 (0.0%) | 2.4882 (50.2%) | 1.0176 (0.6%) | 1.9953 (33.6%) |
| tit_for_two_tats | 3.0000 (100.0%) | 1.0471 (0.0%) | 3.0000 (100.0%) | 3.0000 (100.0%) | 3.0000 (100.0%) |
| hard_tit_for_tat | 3.0000 (100.0%) | 1.0235 (0.0%) | 3.0000 (100.0%) | 3.0000 (100.0%) | 3.0000 (100.0%) |
| random_20 | 1.5494 (20.6%) | 1.8000 (0.0%) | 1.5494 (20.6%) | 1.7918 (0.7%) | 1.1718 (51.5%) |
| random_80 | 2.7282 (78.4%) | 4.1294 (0.0%) | 2.7282 (78.4%) | 4.0976 (1.9%) | 3.2459 (49.6%) |

## Complete selected source: B202, A303 (partial)

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    if len(opponent_history) == 0:
        return 0
    return opponent_history[-1]
# EVOLVE-BLOCK-END
```

Source SHA-256: `d18b36ca67036b2c2b081a349b9d963558d80e38a3df8334d63484cb7ffff22a`.

Trace test key: **T1** = `len(opponent_history) == 0`.

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

First 8 rounds of the actual 174-round evaluated encounter; full-match candidate payoff 396. C=0, D=1. Tests are listed in actual interpreter execution order; true/false identifies the executed branch. The replay's full totals are asserted equal to the unchanged evaluator.

| Round | Own history | Opponent history | Executed tests | Actions own/other | Payoff own/other | Cumulative own/other |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | empty | empty | T1=true | 0/0 | 3/3 | 3/3 |
| 2 | 0 | 0 | T1=false | 0/0 | 3/3 | 6/6 |
| 3 | 00 | 00 | T1=false | 0/1 | 0/5 | 6/11 |
| 4 | 000 | 001 | T1=false | 1/0 | 5/0 | 11/11 |
| 5 | 0001 | 0010 | T1=false | 0/1 | 0/5 | 11/16 |
| 6 | 00010 | 00101 | T1=false | 1/1 | 1/1 | 12/17 |
| 7 | 000101 | 001011 | T1=false | 1/1 | 1/1 | 13/18 |
| 8 | 0001011 | 0010111 | T1=false | 1/1 | 1/1 | 14/19 |

### Opponent payoff and cooperation

Cells show own payoff per round and own cooperation percentage, aggregated across the five scored matches for that opponent. All comparators use identical encounters.

**train**

| Opponent | Selected | Seed | TFT | Grim | Ordinary WSLS |
| --- | --- | --- | --- | --- | --- |
| always_cooperate | 3.0000 (100.0%) | 5.0000 (0.0%) | 3.0000 (100.0%) | 3.0000 (100.0%) | 3.0000 (100.0%) |
| always_defect | 0.9958 (0.4%) | 1.0000 (0.0%) | 0.9958 (0.4%) | 0.9958 (0.4%) | 0.4992 (50.1%) |
| random | 2.2217 (48.9%) | 2.9492 (0.0%) | 2.2217 (48.9%) | 2.9365 (0.8%) | 2.2073 (50.0%) |
| tit_for_tat | 3.0000 (100.0%) | 1.0169 (0.0%) | 3.0000 (100.0%) | 3.0000 (100.0%) | 3.0000 (100.0%) |
| grim | 3.0000 (100.0%) | 1.0169 (0.0%) | 3.0000 (100.0%) | 3.0000 (100.0%) | 3.0000 (100.0%) |
| win_stay_lose_shift | 3.0000 (100.0%) | 3.0034 (0.0%) | 3.0000 (100.0%) | 3.0000 (100.0%) | 3.0000 (100.0%) |

**holdout**

| Opponent | Selected | Seed | TFT | Grim | Ordinary WSLS |
| --- | --- | --- | --- | --- | --- |
| alternator | 2.5000 (50.4%) | 3.0094 (0.0%) | 2.5000 (50.4%) | 2.9918 (1.2%) | 2.2529 (50.4%) |
| suspicious_tit_for_tat | 2.4882 (50.2%) | 1.0000 (0.0%) | 2.4882 (50.2%) | 1.0176 (0.6%) | 1.9953 (33.6%) |
| tit_for_two_tats | 3.0000 (100.0%) | 1.0471 (0.0%) | 3.0000 (100.0%) | 3.0000 (100.0%) | 3.0000 (100.0%) |
| hard_tit_for_tat | 3.0000 (100.0%) | 1.0235 (0.0%) | 3.0000 (100.0%) | 3.0000 (100.0%) | 3.0000 (100.0%) |
| random_20 | 1.5494 (20.6%) | 1.8000 (0.0%) | 1.5494 (20.6%) | 1.7918 (0.7%) | 1.1718 (51.5%) |
| random_80 | 2.7282 (78.4%) | 4.1294 (0.0%) | 2.7282 (78.4%) | 4.0976 (1.9%) | 3.2459 (49.6%) |

## Complete selected source: A202

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else 1 if len(opponent_history) >= 4 and opponent_history[-4:-2] == opponent_history[-2:] and opponent_history[-1] != opponent_history[-2] else 1 if len(opponent_history) >= 6 and opponent_history[-6:-3] == opponent_history[-3:] and sum(opponent_history[-3:]) > 0 and sum(opponent_history[-3:]) < 3 else 1 if len(opponent_history) >= 8 and opponent_history[-8:-4] == opponent_history[-4:] and sum(opponent_history[-4:]) > 0 and sum(opponent_history[-4:]) < 4 else 1 if len(opponent_history) >= 10 and opponent_history[-10:-5] == opponent_history[-5:] and sum(opponent_history[-5:]) > 0 and sum(opponent_history[-5:]) < 5 else 1 if len(opponent_history) >= 12 and opponent_history[-12:-6] == opponent_history[-6:] and sum(opponent_history[-6:]) > 0 and sum(opponent_history[-6:]) < 6 else opponent_history[-1]
# EVOLVE-BLOCK-END
```

Source SHA-256: `4da8a4169fe411c2f6ae83273be421f74757d9992acf8a340423b8e4a4832393`.

Trace test key: **T1** = `len(opponent_history) == 0`; **T2** = `len(opponent_history) >= 4 and opponent_history[-4:-2] == opponent_history[-2:] and (opponent_history[-1] != opponent_history[-2])`; **T3** = `len(opponent_history) >= 6 and opponent_history[-6:-3] == opponent_history[-3:] and (sum(opponent_history[-3:]) > 0) and (sum(opponent_history[-3:]) < 3)`; **T4** = `len(opponent_history) >= 8 and opponent_history[-8:-4] == opponent_history[-4:] and (sum(opponent_history[-4:]) > 0) and (sum(opponent_history[-4:]) < 4)`; **T5** = `len(opponent_history) >= 10 and opponent_history[-10:-5] == opponent_history[-5:] and (sum(opponent_history[-5:]) > 0) and (sum(opponent_history[-5:]) < 5)`; **T6** = `len(opponent_history) >= 12 and opponent_history[-12:-6] == opponent_history[-6:] and (sum(opponent_history[-6:]) > 0) and (sum(opponent_history[-6:]) < 6)`.

### Scored encounter trace: train / always_defect / seed 11

First 8 rounds of the actual 174-round evaluated encounter; full-match candidate payoff 173. C=0, D=1. Tests are listed in actual interpreter execution order; true/false identifies the executed branch. The replay's full totals are asserted equal to the unchanged evaluator.

| Round | Own history | Opponent history | Executed tests | Actions own/other | Payoff own/other | Cumulative own/other |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | empty | empty | T1=true | 0/1 | 0/5 | 0/5 |
| 2 | 0 | 1 | T1=false; T2=false; T3=false; T4=false; T5=false; T6=false | 1/1 | 1/1 | 1/6 |
| 3 | 01 | 11 | T1=false; T2=false; T3=false; T4=false; T5=false; T6=false | 1/1 | 1/1 | 2/7 |
| 4 | 011 | 111 | T1=false; T2=false; T3=false; T4=false; T5=false; T6=false | 1/1 | 1/1 | 3/8 |
| 5 | 0111 | 1111 | T1=false; T2=false; T3=false; T4=false; T5=false; T6=false | 1/1 | 1/1 | 4/9 |
| 6 | 01111 | 11111 | T1=false; T2=false; T3=false; T4=false; T5=false; T6=false | 1/1 | 1/1 | 5/10 |
| 7 | 011111 | 111111 | T1=false; T2=false; T3=false; T4=false; T5=false; T6=false | 1/1 | 1/1 | 6/11 |
| 8 | 0111111 | 1111111 | T1=false; T2=false; T3=false; T4=false; T5=false; T6=false | 1/1 | 1/1 | 7/12 |

### Scored encounter trace: train / random / seed 11

First 8 rounds of the actual 174-round evaluated encounter; full-match candidate payoff 433. C=0, D=1. Tests are listed in actual interpreter execution order; true/false identifies the executed branch. The replay's full totals are asserted equal to the unchanged evaluator.

| Round | Own history | Opponent history | Executed tests | Actions own/other | Payoff own/other | Cumulative own/other |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | empty | empty | T1=true | 0/0 | 3/3 | 3/3 |
| 2 | 0 | 0 | T1=false; T2=false; T3=false; T4=false; T5=false; T6=false | 0/0 | 3/3 | 6/6 |
| 3 | 00 | 00 | T1=false; T2=false; T3=false; T4=false; T5=false; T6=false | 0/1 | 0/5 | 6/11 |
| 4 | 000 | 001 | T1=false; T2=false; T3=false; T4=false; T5=false; T6=false | 1/0 | 5/0 | 11/11 |
| 5 | 0001 | 0010 | T1=false; T2=false; T3=false; T4=false; T5=false; T6=false | 0/1 | 0/5 | 11/16 |
| 6 | 00010 | 00101 | T1=false; T2=true | 1/1 | 1/1 | 12/17 |
| 7 | 000101 | 001011 | T1=false; T2=false; T3=false; T4=false; T5=false; T6=false | 1/1 | 1/1 | 13/18 |
| 8 | 0001011 | 0010111 | T1=false; T2=false; T3=false; T4=false; T5=false; T6=false | 1/1 | 1/1 | 14/19 |

### Opponent payoff and cooperation

Cells show own payoff per round and own cooperation percentage, aggregated across the five scored matches for that opponent. All comparators use identical encounters.

**train**

| Opponent | Selected | Seed | TFT | Grim | Ordinary WSLS |
| --- | --- | --- | --- | --- | --- |
| always_cooperate | 3.0000 (100.0%) | 5.0000 (0.0%) | 3.0000 (100.0%) | 3.0000 (100.0%) | 3.0000 (100.0%) |
| always_defect | 0.9958 (0.4%) | 1.0000 (0.0%) | 0.9958 (0.4%) | 0.9958 (0.4%) | 0.4992 (50.1%) |
| random | 2.4298 (35.1%) | 2.9492 (0.0%) | 2.2217 (48.9%) | 2.9365 (0.8%) | 2.2073 (50.0%) |
| tit_for_tat | 3.0000 (100.0%) | 1.0169 (0.0%) | 3.0000 (100.0%) | 3.0000 (100.0%) | 3.0000 (100.0%) |
| grim | 3.0000 (100.0%) | 1.0169 (0.0%) | 3.0000 (100.0%) | 3.0000 (100.0%) | 3.0000 (100.0%) |
| win_stay_lose_shift | 3.0000 (100.0%) | 3.0034 (0.0%) | 3.0000 (100.0%) | 3.0000 (100.0%) | 3.0000 (100.0%) |

**holdout**

| Opponent | Selected | Seed | TFT | Grim | Ordinary WSLS |
| --- | --- | --- | --- | --- | --- |
| alternator | 2.9859 (1.8%) | 3.0094 (0.0%) | 2.5000 (50.4%) | 2.9918 (1.2%) | 2.2529 (50.4%) |
| suspicious_tit_for_tat | 1.0353 (1.2%) | 1.0000 (0.0%) | 2.4882 (50.2%) | 1.0176 (0.6%) | 1.9953 (33.6%) |
| tit_for_two_tats | 3.0000 (100.0%) | 1.0471 (0.0%) | 3.0000 (100.0%) | 3.0000 (100.0%) | 3.0000 (100.0%) |
| hard_tit_for_tat | 3.0000 (100.0%) | 1.0235 (0.0%) | 3.0000 (100.0%) | 3.0000 (100.0%) | 3.0000 (100.0%) |
| random_20 | 1.6153 (15.1%) | 1.8000 (0.0%) | 1.5494 (20.6%) | 1.7918 (0.7%) | 1.1718 (51.5%) |
| random_80 | 2.9682 (64.8%) | 4.1294 (0.0%) | 2.7282 (78.4%) | 4.0976 (1.9%) | 3.2459 (49.6%) |
