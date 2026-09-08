## What the generated policies do

The 59 generated sources contain **20 parsed ASTs, 18 valid**. Within-run AST
duplicates, including comparison to each seed, total 37 (S101 14, S202 11,
S303 12); global AST deduplication is a different count (39 repeated occurrences).
All generated candidates received an evaluation. There are 62 native program
rows including the three seeds, and 48 final archive members (16 per run).

**27 generated occurrences implement familiar TFT**, in three source forms.
The direct `opponent_history[-1]` form and its equivalent Boolean conditional
cooperate initially and copy the opponent thereafter. S303/18 has a redundant
own-history expression: if the previous actions agree, returning own equals
returning opponent; if they differ, `1-own` equals opponent for binary actions.
All 27 pass the frozen 1,640 probes. These source arguments establish TFT for
these particular programs on equal-length binary histories, independently of
finite-probe agreement. **15 occurrences implement familiar grim**, in two source
forms. The seed and both generated grim forms cooperate precisely while the
opponent's defection count is zero; that count cannot decrease, so retaliation
is permanent. These are recovered implementations of known strategies, not
novel discoveries.

The table groups every remaining source by its actual decision rule. Full code,
all duplicate origins and per-opportunity branch expressions are in the complete
source catalogue. C means cooperation and D defection; round numbers start at 1.

| Source occurrence(s) | Actual behavior | Original training |
| --- | --- | ---: |
| S101/2 | Grim with an exception: cooperate when there have been exactly two opponent defections and the last opponent action was C. At three total defections, retaliation is permanent. | 2.654258 |
| S101/4; S202/3,12 | Cooperate until the opponent's second **total** defection, then defect forever. This differs from counting consecutive defections. | 2.651720 |
| S101/5 | Grim with an exception after exactly one opponent defection when its latest action is C; a second total defection removes forgiveness. | 2.653553 |
| S202/1 | Open C,D. Thereafter, only opponents whose first two actions were C,C can receive cooperation, and only while their total defection count is exactly one. All other cases defect. | 2.330936 |
| S202/6 | Grim, but cooperate whenever history length modulo 50 is 0 or 1: rounds 1–2, 51–52, 101–102, etc. | 2.640299 |
| S202/15 | Grim, with cooperation restored whenever the opponent's last two actions were both C. | 2.596588 |
| S202/17 | Grim, with cooperation restored whenever the opponent's last three actions were all C. | 2.625917 |
| S202/18 | Cooperate only through round 6 while the opponent has never defected; defect from round 7 onward, or earlier after any defection. | 2.336717 |
| S303/2,13 | Familiar tit-for-two-tats: cooperate initially; defect exactly after two consecutive opponent defections. | 2.474055 |
| S303/4 | From its own reachable histories, cooperate through round 8, then defect against a never-defecting opponent; once the opponent defects, cooperate permanently. Its redundant own-action branch differs on some unreachable input histories. | 2.084743 |
| S303/9 | Open C; normally copy the opponent. Override with D after an entirely cooperative history of length divisible by 83; override with C after mutual D. This is a periodic-defection/forgiveness hybrid, not exact TFT. | 2.067541 |
| S303/17 | Cooperate through round 8; thereafter defect only if the opponent has never defected. Cooperate permanently after its first defection. Same reachable behavior as S303/4 by the preceding branch argument, despite a different AST. | 2.084743 |
| S101/19 | Rejected: a tuple literal `(1, 1, 1)` in a history comparison is outside the interpreter grammar. 62 AST nodes, below the size limit; no repaired version was evaluated. | −1 (invalid) |
| S202/20 | Rejected: a tuple literal `(0, 0, 0)` is outside the interpreter grammar. 53 AST nodes, below the size limit; no repaired version was evaluated. | −1 (invalid) |

The ten other valid variant occurrences combine delayed retaliation, limited
forgiveness or history-length triggers. Changed code and behavior are established;
worldwide novelty is not. Their measured training scores all fall below grim.
Only the three selected sources and fixed references received fresh transfer:
there is no fresh-development claim for an unselected variant.

## Actual evolutionary changes and stagnation

The incumbent trajectory is flat in all three runs: 2.655386350817823 from seed
to completion. Native parent selection still explored lower-scoring programs.
For example, S202/2 (TFT, 2.536238) → S202/3 (second-total-defection trigger,
2.651720) → S202/4 (grim, 2.655386) improves the sampled parent's score twice.
However, the exact grim seed was supplied as top-k inspiration in both steps.
This is recovery of an already available incumbent, not a new best or new
strategy. Likewise S101/7 returns from S101/2's limited-forgiveness variant to
the original grim source, with seed slot 0 supplied as inspiration. The full
parent/inspiration record supports these concrete relationships; no hidden
model reasoning is inferred.

The closest new variant was S101/2, **−0.001128** below the seed on original
training. The 27 TFT occurrences scored 2.536238, **−0.119148** below the seed.
Selection retained slot 0 in every run under the frozen earliest-tie rule.
The result is **no training improvement**, followed by zero selected-minus-seed
transfer differences. It does not establish global optimality of grim, prove
that a larger or differently configured search cannot improve it, or show that
all unselected variants would transfer poorly.

Three exploratory searches with 19/20/20 available model opportunities cannot
repair the unfinished independent-generation comparison. Public development
opponent types, fixed training samples, deterministic noiseless play, restricted
program syntax, small budgets and the LLM's prior knowledge limit the claim.
Native retrieval restrictions isolate the supplied mutation information; they
are not an OS confidentiality container or a knowledge-free starting point.
