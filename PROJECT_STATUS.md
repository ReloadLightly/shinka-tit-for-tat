# Project status — 2026-09-08

## Completed milestone

The first real ShinkaEvolve pilot ran through the native Headless/Codex provider
using the existing ChatGPT Pro login. Shinka is pinned to
`9912af12d423504b8d580f4179fd15f5f88b8c50` (0.0.7), with Headless 0.6.1,
Codex 0.153.4, and explicit model `gpt-5.6-terra`, low reasoning effort.

The five-invocation allowance was respected: one Codex configuration failure
before a model turn, followed by four successful proposal sessions after a
manual configuration repair. The failure and four locally blocked Shinka slots
remain in `results/pilot_001`; the repaired real search is in
`results/pilot_001_repaired`. Both share one durable five-slot ledger. There were
four native model-response usage records; invocation counts and internal model
turn counts are separate concepts.

Four generated files were live-evaluated. Three were valid and archived; the
fourth was rejected for a forbidden tuple literal and stored as invalid in the
database. No valid generated policy passed the 1,640 TFT probes. The rejected
source expresses TFT under ordinary Python semantics, by a redundant-branch
source argument, but cannot count as an admissible evolved TFT policy.

The payoff-selected winner is repaired-run generation 1, `guarded_win_stay`:
training **2.5331359278059784**, holdout **2.444313725490196**. Its complete source
is in README.md and `results/PILOT_001.md`. Shinka database membership, best ID,
source hashes, recorded scores, and offline rescoring agree. Selection used
only training payoff, with no target/cooperation bonus. Original `initial.py`,
payoffs, panels, stopping rule, evaluator, interpreter, and task file are unchanged.

The account credit balance stayed 90.6853810000. Subscription usage snapshots
moved from 1% to 2%, an account-wide rounded measure also affected by supervisor
usage. Reported tokens: 50,334 input including 15,872 cached, and 4,783 output
including 3,998 reasoning. The $0.1294944 Headless/Shinka API list-price estimate
is not a charge. No paid API calls, API-key authentication, API fallback,
credit purchase/continuation, or GitHub Actions was used.

The default launcher remains zero-call. Local tests (26) and preflights passed
before live work and after the configuration repair. Native request/stream
retries, resampling, auxiliary models, and embeddings are disabled. Quota checks,
process timeouts, serial execution, and durable invocation accounting bound use.
All source, prompts, native context, usage, feedback, failures, configurations,
and databases are preserved after credential review.

## Evidence and scientific limit

- `results/PILOT_001.md`: complete report, commands, every candidate's diagnosis,
  winner source, rejected source, and next experiment.
- `results/pilot_001_audit.json`: canonical-file rescoring and live SQLite audit.
- `results/subscription_pilot_001_usage/`: durable invocation ledger, raw Codex
  and Headless records, native context/usage, and before/after subscription data.
- `results/pilot_001_setup/`: GitHub/provider inspection, method, tests,
  preflights, configuration repair, and console logs.
- Existing baseline and original preflight evidence remain intact.

This is an **unblinded integration pilot**. The read-only wrapper permits broad
filesystem reads. Web search and automatic project instructions were disabled;
no tool call was observed in successful sessions. Generic native agent/skill
instructions were still injected and are preserved. A separate working
directory and absence of observed reads do not establish enforced information
hiding. No knowledge-free invention, hidden-information discovery, global
optimality, or causal benefit from evolutionary feedback is claimed.

## Next bounded experiment

Establish and locally test an enforced mutation information boundary, then run
one five-invocation blinded replication with the same model, seed program,
interpreter, panels, and payoff-only fitness. Preserve the tuple rejection and
do not relax the evaluator in response. Multiple independent seeds and a
feedback-free control remain later work. No further calls are authorized or
made under this exhausted first-pilot ledger.
