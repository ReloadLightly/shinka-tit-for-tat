# E2 — transfer of already generated strategies

## Question and result

Which strategies generated in E1 and E1-R retain their payoff advantages on fresh encounters, and which decision rules explain them? This is a zero-model-call, post-search analysis of fixed programs. Historical winners remain fixed.

Status: **complete**. Coverage: **86,400/86,400 successful matches** across 72 entries (35 generated ASTs, five named references including the seed, and 32 memory-one comparators). Frozen CLOCK_BOOTTIME elapsed **2497.819 seconds**, within the frozen 2,700-second allowance. Status counts: `{'ok': 86400}`. Experimental model/proposal/judge/embedding calls: **zero**.

Main execution began 2026-09-08T18:23:54.458856+00:00 and closed 2026-09-08T19:07:59.213527+00:00.

Clock qualification: those UTC timestamps span **2,644.755 seconds (44.08 minutes)**, 146.936 seconds longer than the frozen elapsed clock. Across 86,402 clock observations the boot identity is unchanged and the execution-ordered boottime values are monotonic; 76 adjacent observations show UTC/boottime discrepancies above 0.1 seconds. The host clock-adjustment cause is unestablished, so the two measures are not interchangeable estimates of precise physical wall time. Both recorded spans are below 45 minutes. Original accounting and timestamps are untouched; [runtime_clock_audit.json](runtime_clock_audit.json) preserves the discrepancy and verification recomputes it.

| Policy / first origin | Original train | Fresh train | Δ TFT | Δ grim | Original development | Fresh development | Δ TFT | Δ grim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E1-R A101:4 | 2.655386 | 2.660859 | +0.121902 | +0.000000 | 2.649804 | 2.655990 | +0.106837 | +0.000000 |
| E1 A202:5 | 2.570925 | 2.575313 | +0.036356 | -0.085546 | 2.434118 | 2.440402 | -0.108751 | -0.215588 |
| initial | 2.331077 | 2.334698 | -0.204259 | -0.326161 | 2.001569 | 2.003754 | -0.545399 | -0.652236 |
| always_cooperate | 2.243655 | 2.247356 | -0.291601 | -0.413503 | 2.239412 | 2.245521 | -0.303632 | -0.410469 |
| tit_for_tat | 2.536238 | 2.538957 | +0.000000 | -0.121902 | 2.544314 | 2.549153 | +0.000000 | -0.106837 |
| grim | 2.655386 | 2.660859 | +0.121902 | +0.000000 | 2.649804 | 2.655990 | +0.106837 | +0.000000 |
| win_stay_lose_shift | 2.451072 | 2.454183 | -0.084774 | -0.206676 | 2.444314 | 2.450268 | -0.098885 | -0.205722 |

E1-R A101’s selected grim retains its TFT advantage on fresh training (+0.121902) and fresh development encounters (+0.106837). E1 A202’s selected period detector retains a training advantage over TFT (+0.036356) but remains below grim (-0.085546). Its development disadvantage persists: -0.108751 vs TFT and -0.215588 vs grim. Fresh encounters do not rescue its original transfer weakness.

## Setup and provenance

The untouched world is a simultaneous iterated Prisoner’s Dilemma: actions 0=C and 1=D, candidate payoffs CC=3, CD=0, DC=5, DD=1. Each match length is geometric with stopping probability 0.00346. environment.horizon(seed) samples the endpoint independently; policies see only the two histories. There is no endpoint disclosure, fixed truncation, action noise, self-play addition, or cooperation reward. Generated policies are interpreted by unchanged policy.py, never imported or executed as arbitrary Python.

| Panel | Opponents | Seeds | Matches/policy | Rounds/policy |
| --- | --- | --- | --- | --- |
| Original training | Always C; always D; fair random; TFT; grim; WSLS | 100001–100100 | 600 | 178734 |
| Original development holdout | Alternator; suspicious TFT; TFT for two tats; hard TFT; random p(C)=0.2; random p(C)=0.8 | 200001–200100 | 600 | 164100 |

Opponent rules are unchanged: always-C/D are constant; random policies draw independent cooperation with probabilities 0.5, 0.2 or 0.8. TFT starts C and copies the opponent’s last action. Grim starts C and defects permanently after any opponent D. Ordinary WSLS starts C, repeats its own action after payoff 3 or 5, and switches after 0 or 1. Alternator starts C and alternates. Suspicious TFT starts D then copies the last action. TFT for two tats starts with two cooperations and defects only after two consecutive opponent defections. Hard TFT starts C and defects if either of the last two available opponent actions was D. Both decisions use histories before the current round.

Each opponent receives all 100 seeds and equal aggregate weight because it shares horizons with the other opponents in its panel. Score is total own payoff divided by total rounds, not the mean of match means. The fresh ranges are disjoint from historical training seeds 11,23,47,89,131 and holdout seeds 211,307,401,503,601. Random streams retain the original train/holdout label and SHA-256 derivation from split/opponent/seed. All policies face identical manifests. Differences are computed separately on each complete panel and opponent. No panels are pooled into an objective. These public development opponents are not a new confirmatory population.

The 40 E1 and 18 E1-R original live-valid occurrences were checked against canonical source bytes, live correctness and metrics, and archived database membership in the preserved audits. AST deduplication retains all 58 origins and source hashes, including programs from incomplete E1 A303 and E1-R B101. Three rejected sources and two originally unevaluated generated sources are excluded without repair; all missing, blocked and unattempted slots are listed in the catalogue. Sources in incomplete runs do not acquire historical primary outcomes merely by being evaluated in E2.

The freeze was committed and remotely verified before evaluation at `6adb42eb2e924a8b54c843d89cdcd28cb2412100`. Recovery found a clean repository and no E2 process, freeze, checkpoint or result locally or on GitHub at fd19af5; the milestone was unstarted in available evidence. No prior E2 runtime could be observed; no running experiment was terminated. The new runtime ledger was created once. Full protocol: [PROTOCOL.md](protocol/PROTOCOL.md); exact source and input hashes: [freeze.json](protocol/freeze.json).

## All generated strategies and ranks

All six ASTs above TFT on original training remain above it on fresh training: two grim implementations and four period-detector variants (period ranges 2, 2–3, 2–4 and 2–6). None exceeds grim. The leading twelve training ranks are unchanged; seven lower-ranked ASTs move. The 32-round periodic-defection variant drops from rank 28 to 32. No AST changes which side of TFT it occupies on training.

On development, only three generated ASTs exceed TFT: the two grim implementations and E1 A101 slot 9. The latter cooperates for two rounds and then copies the opponent’s previous action. Its fresh score is 2.630670 (+0.081517 vs TFT), rank 3 of 35. Against suspicious TFT the two initial cooperations restore mutual cooperation instead of TFT’s alternation: +0.493784 per opponent round. Small losses against the two random opponents slightly reduce that gain; other development opponents tie TFT. This is a new exploratory E2 development observation: that source had no archived original development score and was not the historical winner. Its training score remains slightly below TFT.

| Policy / first origin | Original train | Fresh train | Δ TFT | Δ grim | Original development | Fresh development | Δ TFT | Δ grim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E1-R A101:4 | 2.655386 | 2.660859 | +0.121902 | +0.000000 | 2.649804 | 2.655990 | +0.106837 | +0.000000 |
| E1 A202:5 | 2.570925 | 2.575313 | +0.036356 | -0.085546 | 2.434118 | 2.440402 | -0.108751 | -0.215588 |
| E1 A202:4 | 2.568951 | 2.571749 | +0.032792 | -0.089110 | Unavailable | 2.421871 | -0.127282 | -0.234119 |
| E1 A101:8 | 2.474055 | 2.476138 | -0.062820 | -0.184721 | Unavailable | 2.385765 | -0.163388 | -0.270225 |
| E1 A101:9 | 2.535110 | 2.538001 | -0.000957 | -0.122859 | Unavailable | 2.630670 | +0.081517 | -0.025320 |
| E1 B202:5 | 2.052171 | 2.039517 | -0.499441 | -0.621342 | Unavailable | 2.051731 | -0.497422 | -0.604260 |
| E1 B202:7 | 2.046954 | 2.047859 | -0.491099 | -0.613000 | Unavailable | 1.898062 | -0.651091 | -0.757928 |
| E1-R A101:3 | 2.003384 | 2.005712 | -0.533245 | -0.655147 | Unavailable | 2.000810 | -0.548342 | -0.655180 |
| E1 A202:10 | 2.120981 | 2.122495 | -0.416462 | -0.538364 | Unavailable | 2.470293 | -0.078860 | -0.185698 |
| E1-R B101:6 | 2.432459 | 2.436615 | -0.102342 | -0.224244 | Unavailable | 2.211578 | -0.337575 | -0.444412 |
| E1 B202:4 | 2.046954 | 2.047859 | -0.491099 | -0.613000 | Unavailable | 1.898062 | -0.651091 | -0.757928 |
| E1 A101:6 | 2.319515 | 2.345978 | -0.192980 | -0.314881 | Unavailable | 2.089183 | -0.459970 | -0.566807 |
| E1 B202:1 | 2.099690 | 2.098745 | -0.440213 | -0.562115 | Unavailable | 2.241578 | -0.307575 | -0.414412 |
| E1-R A101:7 | 2.087563 | 2.088853 | -0.450105 | -0.572006 | Unavailable | 2.242108 | -0.307044 | -0.413882 |
| E1 A202:2 | 2.550761 | 2.554114 | +0.015157 | -0.106745 | Unavailable | 2.398020 | -0.151133 | -0.257971 |
| E1-R B101:7 | 2.536238 | 2.538957 | +0.000000 | -0.121902 | Unavailable | 2.549153 | +0.000000 | -0.106837 |
| E1-R B101:4 | 2.474055 | 2.476138 | -0.062820 | -0.184721 | Unavailable | 2.385765 | -0.163388 | -0.270225 |
| E1-R B101:3 | 2.369007 | 2.371989 | -0.166969 | -0.288871 | Unavailable | 1.898239 | -0.650914 | -0.757751 |
| E1 A202:3 | 2.561619 | 2.566412 | +0.027454 | -0.094448 | Unavailable | 2.410963 | -0.138190 | -0.245027 |
| E1 A202:6 | 2.330936 | 2.334715 | -0.204242 | -0.326144 | Unavailable | 2.004899 | -0.544254 | -0.651091 |
| E1-R B101:2 | 2.655386 | 2.660859 | +0.121902 | +0.000000 | Unavailable | 2.655990 | +0.106837 | +0.000000 |
| E1-R A101:5 | 2.289481 | 2.291573 | -0.247384 | -0.369286 | Unavailable | 1.901091 | -0.648062 | -0.754899 |
| E1 A303:2 | 2.051043 | 2.050617 | -0.488340 | -0.610242 | Unavailable | 1.900445 | -0.648708 | -0.755545 |
| E1-R A101:2 | 2.037366 | 2.039612 | -0.499345 | -0.621247 | Unavailable | 2.301444 | -0.247709 | -0.354546 |
| E1 A101:7 | 2.536238 | 2.538957 | +0.000000 | -0.121902 | Unavailable | 2.549153 | +0.000000 | -0.106837 |
| E1 A101:1 | 2.536238 | 2.538957 | +0.000000 | -0.121902 | 2.544314 | 2.549153 | +0.000000 | -0.106837 |
| E1 A101:10 | 1.958263 | 1.947923 | -0.591035 | -0.712937 | Unavailable | 2.196399 | -0.352754 | -0.459592 |
| E1 A101:3 | 2.459250 | 2.460517 | -0.078441 | -0.200342 | Unavailable | 2.233077 | -0.316076 | -0.422913 |
| E1 A303:3 | 2.451072 | 2.454183 | -0.084774 | -0.206676 | Unavailable | 2.450268 | -0.098885 | -0.205722 |
| E1 A101:2 | 2.095601 | 2.096949 | -0.442009 | -0.563911 | Unavailable | 2.278184 | -0.270969 | -0.377806 |
| E1 B202:9 | 2.456007 | 2.458268 | -0.080690 | -0.202592 | Unavailable | 2.223376 | -0.325777 | -0.432614 |
| E1 A101:4 | 2.451072 | 2.454183 | -0.084774 | -0.206676 | Unavailable | 2.450268 | -0.098885 | -0.205722 |
| E1 B101:10 | 1.897208 | 1.897546 | -0.641411 | -0.763313 | Unavailable | 1.838190 | -0.710963 | -0.817800 |
| E1-R B101:1 | 2.536238 | 2.538957 | +0.000000 | -0.121902 | Unavailable | 2.549153 | +0.000000 | -0.106837 |
| E1 B101:2 | 2.536238 | 2.538957 | +0.000000 | -0.121902 | 2.544314 | 2.549153 | +0.000000 | -0.106837 |

The accompanying [CATALOGUE.md](CATALOGUE.md) contains every original source/origin, decision-rule descriptions, original and fresh ranks, per-opponent scores/cooperation/differences, exclusions and all comparator results. Five ASTs, representing 25 original occurrences, implement exact TFT by direct source logic; two ASTs implement grim, two implement ordinary WSLS, and two implement TFT for two tats. These source-based identifications are distinct from finite encounter equality. E1 B202 slot 5 instead adds defections at positive history lengths divisible by 32 (rounds 33, 65, …) and remains a distinct periodic variant despite its historical finite-probe false positive. summary.json also retains complete integer totals and rank populations. Training ranks compare the 35 ASTs. A fresh rank is unavailable if any member of its ranking population lacks a complete score. Original development ranks use only ASTs with an archived score; fresh ranks compare all 35 and additionally the same historical-availability subset. These are exploratory screening ranks, not evolutionary replicates or reselections.

| AST / first origin | Original train rank | Fresh train rank | Original development rank | Fresh development rank | Fresh development rank within original available subset |
| --- | --- | --- | --- | --- | --- |
| `ast_88f3a4f11dba1800` / E1-R A101:4 | 1 | 1 | 1 | 1 | 1 |
| `ast_57dad27c89beb4e1` / E1 A202:5 | 3 | 3 | 4 | 12 | 4 |

Among all 32 memory-one comparators, `00111` ranks first on both panels (2.660859 training / 2.655990 development), matching grim on its reachable histories. TFT `00101` ranks second on training and third on development. Development runner-up `01001` scores 2.564491. The complete comparator table and family ranks are in the catalogue and summary. This is exhaustive only within the fixed five-bit memory-one class, not a global optimality proof.

## Focal mechanism: E1-R A101 selected slot 4, grim

Complete original source:
```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 or opponent_history.count(1) == 0 else 1
# EVOLVE-BLOCK-END
```

The first condition cooperates when the history is empty or contains no defection. Once an opponent 1 is recorded, its count never returns to zero, so the policy defects forever. This establishes grim behavior by source logic on legal histories; equality with the reference in scored encounters is an additional finite check. Its own-history argument is unused. TFT instead copies the latest opponent action and can resume cooperation.

| Panel | Own payoff | Rounds | Cooperations | Cooperation rate |
| --- | --- | --- | --- | --- |
| train | 475586 | 178734 | 119460 | 0.668368 |
| holdout | 435848 | 164100 | 55682 | 0.339317 |

| Panel | Opponent | Own payoff / rounds | Payoff/round | Cooperation | Δ TFT | Δ grim |
| --- | --- | --- | --- | --- | --- | --- |
| train | always_cooperate | 89367/29789 | 3.000000 | 1.000000 | +0.000000 | +0.000000 |
| train | always_defect | 29689/29789 | 0.996643 | 0.003357 | +0.000000 | +0.000000 |
| train | grim | 89367/29789 | 3.000000 | 1.000000 | +0.000000 | +0.000000 |
| train | random | 88429/29789 | 2.968512 | 0.006848 | +0.731411 | +0.000000 |
| train | tit_for_tat | 89367/29789 | 3.000000 | 1.000000 | +0.000000 | +0.000000 |
| train | win_stay_lose_shift | 89367/29789 | 3.000000 | 1.000000 | +0.000000 | +0.000000 |
| holdout | alternator | 81855/27350 | 2.992870 | 0.007276 | +0.495430 | +0.000000 |
| holdout | hard_tit_for_tat | 82050/27350 | 3.000000 | 1.000000 | +0.000000 | +0.000000 |
| holdout | random_20 | 48853/27350 | 1.786216 | 0.004461 | +0.235868 | +0.000000 |
| holdout | random_80 | 113394/27350 | 4.146033 | 0.020512 | +1.394150 | +0.000000 |
| holdout | suspicious_tit_for_tat | 27646/27350 | 1.010823 | 0.003656 | -1.484424 | +0.000000 |
| holdout | tit_for_two_tats | 82050/27350 | 3.000000 | 1.000000 | +0.000000 | +0.000000 |

The training advantage over TFT comes entirely from fair random: permanent retaliation extracts more when random later cooperates. Against training always-C, TFT, grim and WSLS both preserve mutual cooperation; against always-D both cooperate once and then defect. On development, grim exploits alternator and random opponents but loses heavily to suspicious TFT. Suspicious TFT defects first and then copies: TFT enters alternating exploitation, whereas grim’s permanent retaliation settles into mutual defection after the opening. This tradeoff persists on fresh seeds.

## Focal mechanism: E1 A202 selected slot 5, period detection

Complete original source:
```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else 1 if len(opponent_history) >= 4 and opponent_history[-4:-2] == opponent_history[-2:] and opponent_history[-1] != opponent_history[-2] else 1 if len(opponent_history) >= 6 and opponent_history[-6:-3] == opponent_history[-3:] and sum(opponent_history[-3:]) > 0 and sum(opponent_history[-3:]) < 3 else 1 if len(opponent_history) >= 8 and opponent_history[-8:-4] == opponent_history[-4:] and sum(opponent_history[-4:]) > 0 and sum(opponent_history[-4:]) < 4 else 1 if len(opponent_history) >= 10 and opponent_history[-10:-5] == opponent_history[-5:] and sum(opponent_history[-5:]) > 0 and sum(opponent_history[-5:]) < 5 else 1 if len(opponent_history) >= 12 and opponent_history[-12:-6] == opponent_history[-6:] and sum(opponent_history[-6:]) > 0 and sum(opponent_history[-6:]) < 6 else opponent_history[-1]
# EVOLVE-BLOCK-END
```

Read the conditional expression left to right. With n previous observations: E returns C when n=0; P2 returns D if n≥4 and the last two two-action blocks match with alternating actions; P3, P4, P5 and P6 return D if n≥2k and the last two k-action blocks match and contain both actions. The first true branch wins. If none applies, L copies the last opponent action. The rule detects only a repeated recent suffix, not an enduring periodic opponent, and does not remember a detection as persistent state. Its own-history argument is unused. All-C/all-D repeated suffixes are excluded by the mixed-action checks.

| Panel | Own payoff | Rounds | Cooperations | Cooperation rate |
| --- | --- | --- | --- | --- |
| train | 460296 | 178734 | 129693 | 0.725620 |
| holdout | 400470 | 164100 | 76842 | 0.468263 |

| Panel | Opponent | Own payoff / rounds | Payoff/round | Cooperation | Δ TFT | Δ grim |
| --- | --- | --- | --- | --- | --- | --- |
| train | always_cooperate | 89367/29789 | 3.000000 | 1.000000 | +0.000000 | +0.000000 |
| train | always_defect | 29689/29789 | 0.996643 | 0.003357 | +0.000000 | +0.000000 |
| train | grim | 89367/29789 | 3.000000 | 1.000000 | +0.000000 | +0.000000 |
| train | random | 73139/29789 | 2.455235 | 0.350364 | +0.218134 | -0.513277 |
| train | tit_for_tat | 89367/29789 | 3.000000 | 1.000000 | +0.000000 | +0.000000 |
| train | win_stay_lose_shift | 89367/29789 | 3.000000 | 1.000000 | +0.000000 | +0.000000 |
| holdout | alternator | 81756/27350 | 2.989250 | 0.010896 | +0.491810 | -0.003620 |
| holdout | hard_tit_for_tat | 82050/27350 | 3.000000 | 1.000000 | +0.000000 | +0.000000 |
| holdout | random_20 | 44592/27350 | 1.630420 | 0.134113 | +0.080073 | -0.155795 |
| holdout | random_80 | 82079/27350 | 3.001060 | 0.657294 | +0.249177 | -1.144973 |
| holdout | suspicious_tit_for_tat | 27943/27350 | 1.021682 | 0.007276 | -1.473565 | +0.010859 |
| holdout | tit_for_two_tats | 82050/27350 | 3.000000 | 1.000000 | +0.000000 | +0.000000 |

Against fair random, accidental repeated suffixes create extra defections and improve payoff by 0.218134 per opponent round over TFT; this alone supplies the panel advantage of 0.036356. Against alternator, the P2 branch exploits recurring cooperation (+0.491810 vs TFT). Development random_20 and random_80 gains are +0.080073 and +0.249177. The sole negative development component is suspicious TFT (−1.473565): starting from C/D alternation, the detector defects on round 5 where TFT would cooperate, then the responsive opponent copies defection and they settle into DD. Hard TFT and TFT for two tats stay at mutual cooperation. Thus the period detector’s development loss is concentrated in one interaction, rather than uniform across the panel. Neither focal policy exceeds grim on fresh training. These opponent differences have equal one-sixth panel weights.

## Short traces from scored E2 encounters

These six encounters and their first 16 rounds were predeclared. Every trace replays the entire scored encounter through environment.play and checks all totals against its durable main record; no second evaluation record is added. traces.json retains full branch tests, histories and outcomes. In the tables C=0, D=1; E is the initial branch, G the grim condition, P2–P6 the mixed suffix tests, and L the final copy branch.

### E1-R A101:4 — train/random/100001

Full scored match: 90 rounds, own payoff 265, payoff/round 2.944444.

| Round | Branch tests in order | Own | Opponent | Payoff | Cumulative |
| --- | --- | --- | --- | --- | --- |
| 1 | G true → C | C | D | 0 | 0 |
| 2 | G false → D | D | D | 1 | 1 |
| 3 | G false → D | D | C | 5 | 6 |
| 4 | G false → D | D | D | 1 | 7 |
| 5 | G false → D | D | D | 1 | 8 |
| 6 | G false → D | D | D | 1 | 9 |
| 7 | G false → D | D | D | 1 | 10 |
| 8 | G false → D | D | D | 1 | 11 |
| 9 | G false → D | D | D | 1 | 12 |
| 10 | G false → D | D | D | 1 | 13 |
| 11 | G false → D | D | C | 5 | 18 |
| 12 | G false → D | D | C | 5 | 23 |
| 13 | G false → D | D | D | 1 | 24 |
| 14 | G false → D | D | D | 1 | 25 |
| 15 | G false → D | D | C | 5 | 30 |
| 16 | G false → D | D | C | 5 | 35 |

Exact reproduction, from repository root (prints verified JSON and does not change the scored record):

```bash
python3 analyze_e2.py --trace ast_88f3a4f11dba1800 --split train --opponent random --seed 100001 --rounds 16
```

### E1-R A101:4 — holdout/alternator/200001

Full scored match: 505 rounds, own payoff 1514, payoff/round 2.998020.

| Round | Branch tests in order | Own | Opponent | Payoff | Cumulative |
| --- | --- | --- | --- | --- | --- |
| 1 | G true → C | C | C | 3 | 3 |
| 2 | G true → C | C | D | 0 | 3 |
| 3 | G false → D | D | C | 5 | 8 |
| 4 | G false → D | D | D | 1 | 9 |
| 5 | G false → D | D | C | 5 | 14 |
| 6 | G false → D | D | D | 1 | 15 |
| 7 | G false → D | D | C | 5 | 20 |
| 8 | G false → D | D | D | 1 | 21 |
| 9 | G false → D | D | C | 5 | 26 |
| 10 | G false → D | D | D | 1 | 27 |
| 11 | G false → D | D | C | 5 | 32 |
| 12 | G false → D | D | D | 1 | 33 |
| 13 | G false → D | D | C | 5 | 38 |
| 14 | G false → D | D | D | 1 | 39 |
| 15 | G false → D | D | C | 5 | 44 |
| 16 | G false → D | D | D | 1 | 45 |

Exact reproduction, from repository root (prints verified JSON and does not change the scored record):

```bash
python3 analyze_e2.py --trace ast_88f3a4f11dba1800 --split holdout --opponent alternator --seed 200001 --rounds 16
```

### E1-R A101:4 — holdout/suspicious_tit_for_tat/200001

Full scored match: 505 rounds, own payoff 508, payoff/round 1.005941.

| Round | Branch tests in order | Own | Opponent | Payoff | Cumulative |
| --- | --- | --- | --- | --- | --- |
| 1 | G true → C | C | D | 0 | 0 |
| 2 | G false → D | D | C | 5 | 5 |
| 3 | G false → D | D | D | 1 | 6 |
| 4 | G false → D | D | D | 1 | 7 |
| 5 | G false → D | D | D | 1 | 8 |
| 6 | G false → D | D | D | 1 | 9 |
| 7 | G false → D | D | D | 1 | 10 |
| 8 | G false → D | D | D | 1 | 11 |
| 9 | G false → D | D | D | 1 | 12 |
| 10 | G false → D | D | D | 1 | 13 |
| 11 | G false → D | D | D | 1 | 14 |
| 12 | G false → D | D | D | 1 | 15 |
| 13 | G false → D | D | D | 1 | 16 |
| 14 | G false → D | D | D | 1 | 17 |
| 15 | G false → D | D | D | 1 | 18 |
| 16 | G false → D | D | D | 1 | 19 |

Exact reproduction, from repository root (prints verified JSON and does not change the scored record):

```bash
python3 analyze_e2.py --trace ast_88f3a4f11dba1800 --split holdout --opponent suspicious_tit_for_tat --seed 200001 --rounds 16
```

### E1 A202:5 — train/random/100001

Full scored match: 90 rounds, own payoff 231, payoff/round 2.566667.

| Round | Branch tests in order | Own | Opponent | Payoff | Cumulative |
| --- | --- | --- | --- | --- | --- |
| 1 | E T | C | D | 0 | 0 |
| 2 | E F, P2 F, P3 F, P4 F, P5 F, P6 F → L | D | D | 1 | 1 |
| 3 | E F, P2 F, P3 F, P4 F, P5 F, P6 F → L | D | C | 5 | 6 |
| 4 | E F, P2 F, P3 F, P4 F, P5 F, P6 F → L | C | D | 0 | 6 |
| 5 | E F, P2 F, P3 F, P4 F, P5 F, P6 F → L | D | D | 1 | 7 |
| 6 | E F, P2 F, P3 F, P4 F, P5 F, P6 F → L | D | D | 1 | 8 |
| 7 | E F, P2 F, P3 F, P4 F, P5 F, P6 F → L | D | D | 1 | 9 |
| 8 | E F, P2 F, P3 F, P4 F, P5 F, P6 F → L | D | D | 1 | 10 |
| 9 | E F, P2 F, P3 F, P4 F, P5 F, P6 F → L | D | D | 1 | 11 |
| 10 | E F, P2 F, P3 F, P4 F, P5 F, P6 F → L | D | D | 1 | 12 |
| 11 | E F, P2 F, P3 F, P4 F, P5 F, P6 F → L | D | C | 5 | 17 |
| 12 | E F, P2 F, P3 F, P4 F, P5 F, P6 F → L | C | C | 3 | 20 |
| 13 | E F, P2 F, P3 F, P4 F, P5 F, P6 F → L | C | D | 0 | 20 |
| 14 | E F, P2 F, P3 F, P4 F, P5 F, P6 F → L | D | D | 1 | 21 |
| 15 | E F, P2 F, P3 F, P4 F, P5 F, P6 F → L | D | C | 5 | 26 |
| 16 | E F, P2 F, P3 F, P4 F, P5 F, P6 F → L | C | C | 3 | 29 |

Exact reproduction, from repository root (prints verified JSON and does not change the scored record):

```bash
python3 analyze_e2.py --trace ast_57dad27c89beb4e1 --split train --opponent random --seed 100001 --rounds 16
```

### E1 A202:5 — holdout/alternator/200001

Full scored match: 505 rounds, own payoff 1513, payoff/round 2.996040.

| Round | Branch tests in order | Own | Opponent | Payoff | Cumulative |
| --- | --- | --- | --- | --- | --- |
| 1 | E T | C | C | 3 | 3 |
| 2 | E F, P2 F, P3 F, P4 F, P5 F, P6 F → L | C | D | 0 | 3 |
| 3 | E F, P2 F, P3 F, P4 F, P5 F, P6 F → L | D | C | 5 | 8 |
| 4 | E F, P2 F, P3 F, P4 F, P5 F, P6 F → L | C | D | 0 | 8 |
| 5 | E F, P2 T | D | C | 5 | 13 |
| 6 | E F, P2 T | D | D | 1 | 14 |
| 7 | E F, P2 T | D | C | 5 | 19 |
| 8 | E F, P2 T | D | D | 1 | 20 |
| 9 | E F, P2 T | D | C | 5 | 25 |
| 10 | E F, P2 T | D | D | 1 | 26 |
| 11 | E F, P2 T | D | C | 5 | 31 |
| 12 | E F, P2 T | D | D | 1 | 32 |
| 13 | E F, P2 T | D | C | 5 | 37 |
| 14 | E F, P2 T | D | D | 1 | 38 |
| 15 | E F, P2 T | D | C | 5 | 43 |
| 16 | E F, P2 T | D | D | 1 | 44 |

Exact reproduction, from repository root (prints verified JSON and does not change the scored record):

```bash
python3 analyze_e2.py --trace ast_57dad27c89beb4e1 --split holdout --opponent alternator --seed 200001 --rounds 16
```

### E1 A202:5 — holdout/suspicious_tit_for_tat/200001

Full scored match: 505 rounds, own payoff 511, payoff/round 1.011881.

| Round | Branch tests in order | Own | Opponent | Payoff | Cumulative |
| --- | --- | --- | --- | --- | --- |
| 1 | E T | C | D | 0 | 0 |
| 2 | E F, P2 F, P3 F, P4 F, P5 F, P6 F → L | D | C | 5 | 5 |
| 3 | E F, P2 F, P3 F, P4 F, P5 F, P6 F → L | C | D | 0 | 5 |
| 4 | E F, P2 F, P3 F, P4 F, P5 F, P6 F → L | D | C | 5 | 10 |
| 5 | E F, P2 T | D | D | 1 | 11 |
| 6 | E F, P2 T | D | D | 1 | 12 |
| 7 | E F, P2 F, P3 F, P4 F, P5 F, P6 F → L | D | D | 1 | 13 |
| 8 | E F, P2 F, P3 F, P4 F, P5 F, P6 F → L | D | D | 1 | 14 |
| 9 | E F, P2 F, P3 F, P4 F, P5 F, P6 F → L | D | D | 1 | 15 |
| 10 | E F, P2 F, P3 F, P4 F, P5 F, P6 F → L | D | D | 1 | 16 |
| 11 | E F, P2 F, P3 F, P4 F, P5 F, P6 F → L | D | D | 1 | 17 |
| 12 | E F, P2 F, P3 F, P4 F, P5 F, P6 F → L | D | D | 1 | 18 |
| 13 | E F, P2 F, P3 F, P4 F, P5 F, P6 F → L | D | D | 1 | 19 |
| 14 | E F, P2 F, P3 F, P4 F, P5 F, P6 F → L | D | D | 1 | 20 |
| 15 | E F, P2 F, P3 F, P4 F, P5 F, P6 F → L | D | D | 1 | 21 |
| 16 | E F, P2 F, P3 F, P4 F, P5 F, P6 F → L | D | D | 1 | 22 |

Exact reproduction, from repository root (prints verified JSON and does not change the scored record):

```bash
python3 analyze_e2.py --trace ast_57dad27c89beb4e1 --split holdout --opponent suspicious_tit_for_tat --seed 200001 --rounds 16
```

## Execution, coverage, failures and reproducibility

Main evaluation used one bounded worker at a time, at most 300 seconds per policy, under a cumulative 45-minute CLOCK_BOOTTIME deadline. Every start and result was fsynced; no match was retried. Completion accounting is [completion.json](completion.json), start/deadline is [runtime.json](runtime.json), and worker launches, exits and logs are retained in workers/ and execution.jsonl. All 600 scheduled encounters in a panel must succeed for that panel to have a complete score. A policy failure would retain its exact pre-decision counterexample; infrastructure/unknown and absent matches remain explicit and suppress complete aggregates. [failures.json](failures.json) contains all observed failures.

Eight focused pre-freeze unittest checks passed. Fourteen full historical policy/panel records (420 matches) replayed exactly before fresh evaluation. The zero-call preflight validated the seed score without a model or subscription-quota/connectivity call; system Python did not include optional Shinka, which E2 does not require. The full dependency-enabled suite first reproduced the previously documented sandbox stall while copying a mocked E1 seed. Only that test process was stopped after diagnosis, its log and fixture were preserved, and the suite was rerun with normal local process access. A first host rerun failed the unchanged child-death timing test; its isolated rerun and the next full suite passed. An analysis merge bug was caught and fixed by a new test before export. All failure logs remain preserved. These were local verification failures, separate from main E2 evaluation. The final test and independent export/trace verification outcomes are recorded in [setup/VERIFICATION.md](setup/VERIFICATION.md).

Machine evidence: [inventory](protocol/inventory.json), [encounters](protocol/encounters.json), [configuration](protocol/config.json), [summary](summary.json), [per-match results](per_match.jsonl), [trace records](traces.json), [catalogue](CATALOGUE.md), [commands](COMMANDS.md). matches/*.jsonl are the original append-only event checkpoints; per_match.jsonl expands all scheduled cells and is checked against those records without reevaluating the main panel.

```bash
# Read-only verification of archived E2 artifacts
python3 analyze_e2.py --verify
# Focused frozen implementation tests
python3 -m unittest discover -s tests -p test_e2.py -v
# Full local suite, with pinned optional dependency
.venv/bin/python -m unittest discover -s tests -v
# Default zero-call preflight
python3 run_evo.py --preflight
```

Exact preparation, pre-freeze checks, freeze/push, main execution and export commands are in COMMANDS.md. run_e2.py refuses closed execution, existing freezes and changed frozen inputs. Analysis output creation refuses overwrites. A fresh scientific replication needs a separate output protocol, not a reset of this ledger.

## Limitations and one bounded follow-up

This is descriptive transfer to fresh stochastic encounters with the same panels and stopping distribution. It supports no claim about other opponent populations, noisy actions, arbitrary horizons, universal optimality or knowledge-free invention. More encounter seeds are not independent evolutionary replicates. AST counts are syntactic counts, and equal scored behavior is not a universal equivalence proof. The public development panel has already informed analysis. E1 and E1-R remain closed and incomplete as designed; E2 does not complete their missing A/B outcomes or support a search-method effect. Historical selections and original files are preserved.

One proposed follow-up, **not executed**: freeze a separate zero-call robustness protocol for these same two focal sources, TFT and E1 A101 slot 9, against the six training opponents on 20 new seeds, comparing ordinary play with one forced opponent-action error at round 10 when the independently sampled match reaches it (no horizon extension). That is 4 × 6 × 20 × 2 = 960 matches, a 10-minute cumulative cap, no evolution or reselection. Report matched payoff loss and whether mutual cooperation recovers. Grim’s permanent response and the observed suspicious-TFT loss, together with the two-initial-cooperation variant’s recovery from suspicious TFT, motivate testing response to a single disruption; current noiseless scores cannot answer it.
