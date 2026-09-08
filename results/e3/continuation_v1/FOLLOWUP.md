# One proposed follow-up — not executed

Run a separate **zero-model-call, 960-match, 10-minute** robustness study comparing
the exact grim seed with the unselected S101/5 source, whose one-defection
forgiveness branch loses only 0.001833 on original training. This asks whether
its branch can recover cooperation after an isolated error, and against which
opponents; it assumes no recovery result in advance.

Freeze both source hashes and a new manifest before evaluation. Use the unchanged
six training opponent types and geometric stopping rule, with new seeds
500001–500020. For each policy/opponent/seed pair, compare ordinary play with one
forced flip of the opponent's round-10 action, only if the independently sampled
match reaches that round. Both histories record the flipped action. This gives
2 policies × 6 opponents × 20 seeds × 2 conditions = 960 matches. Record own-payoff
difference and whether/when mutual cooperation resumes. Use serial workers,
retain failures without replacements, and stop at 10 minutes.

This would be a new perturbation protocol, not part of E3. No evolution,
reselection, new opponent, model call or claim based on unevaluated outcomes.
It has not been executed. E2's earlier proposed comparison remains historical.
