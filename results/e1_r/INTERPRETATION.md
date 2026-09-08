**The planned comparison remains unanswered: E1-R has no completed A/B pair.**
A101 completed ten opportunities; B101 consumed ten slots but its last Codex
invocation failed before supplying a policy. B202, A202, A303 and B303 never
started. Under the pre-call completion rule, B101 is incomplete even though its
budget was consumed. All three paired A-minus-B primary differences are
**unavailable**. With n=0 available pairs, the paired mean, median, range and
sample SD are undefined. Missing outcomes are not zero.

The repairs worked in this run: no generated policy lost its evaluator result,
and the terminal stop finalized automatically. The new failure was Codex's
**“Connection failed: error sending request”**, at B101 opportunity 10. The guard
latched the stop after that single failed launch; no retry, resampling,
replacement or restart occurred. The closed ledger retains **40 unused
invocations that cannot be reused**. This partial E1-R evidence is reported
separately from the earlier 44/60 E1 experiment.

**Exact TFT appeared, but was not training-selected.** Seven admissible sources
implement it: A101 slots **6 and 10**, B101 slots **1, 5, 7, 8 and 9**. They pass
all 1,640 frozen probes. Their source establishes a stronger result: each returns
integer C on empty history and exactly the opponent's last binary action
otherwise, with no other dependency. B101 slot 7 spells the latter as “1 if the
last action is 1, else 0,” which is identical on legal binary histories.
[Source diagnoses](source_diagnoses.json) record the three expression forms and
argument; the finite probes alone would not prove equivalence.

A101's selected slot **4** is **grim trigger**, with training payoff
**2.655386350818** and measured development-holdout payoff
**2.649803921569**. B101 independently generated a source-equivalent grim rule
at slot **2**, with the same measured training score, and retains it as its
provisional selection. No B101 primary holdout result was computed. Thus this
observed high-training-payoff behavior did not require accumulated feedback to
appear; the incomplete experiment cannot estimate whether evolution improves
expected selected-policy holdout payoff.

### What the selected programs do

Both original sources are reproduced completely below. A101 tests whether the
opponent history is empty **or** contains no defection. It cooperates in that
case and defects otherwise. Empty history already contains no defection, so
that first check is redundant. B101's shorter expression defects whenever the
count of opponent defections is nonzero, otherwise cooperates. Neither uses its
own history. On every finite legal binary history they implement the same rule:
**cooperate until the first opponent defection, then defect permanently**.
This is source-established grim equivalence, not a name-based classification.
They differ from TFT after an earlier defection followed by cooperation: grim
continues D, while TFT returns C.

The payoff explains the selection. Against the five deterministic training
opponents, grim and TFT earn identical averages. Against fair random, grim
earns **2.936548** per round versus TFT's **2.221658**. That single-opponent
increase of **0.714890**, divided by six equally weighted opponents, accounts
for the entire **0.119148** aggregate training gain. No resemblance, cooperation
or simplicity criterion was used.

On A101's scored holdout, grim gains against alternator (**+0.491765**), random
20% cooperation (**+0.242353**) and random 80% cooperation (**+1.369412**) relative
to TFT. It loses heavily against suspicious TFT (**−1.470588**); TFT-for-two-tats
and hard TFT are unchanged. The net aggregate difference is **+0.105490**.
These are fixed-encounter measurements, not claims of universal superiority.
The selected rule equals the existing hand-written grim reference; it is not a
newly established global optimum over the full-history search space.

The actual scored seed-211 encounter with suspicious TFT starts **C/D**, then
**D/C**, then **D/D forever**. The candidate receives 0, 5, then 1 per round.
The opponent initially defects, copies the candidate's first C on round 2,
then copies its permanent D. Against alternator, the candidate plays C in the
first two rounds and D thereafter. These branches explain the sustained
holdout loss and gain. Short scored traces and opponent totals appear below;
[additional exact traces](interpretation_traces.json) retain the branch tests
and full-match totals.

### Generated sources, validity and actual search progress

There were **19 generated sources**, all evaluated: **18 live-valid and archived**,
plus **one interpreter rejection**. A101 slot 1 has **48 AST nodes**, within the
400-node cap, but uses the forbidden tuple literal `(1, 1, 1)`. Its generic
“unsupported syntax or more than 400 AST nodes” message is specifically a tuple
rejection here. It received the fixed −1 validity sentinel and was not repaired.
B101 slot 10 produced no policy and has no evaluator result, database program
row or archive entry. Its native `llm_output_invalid` failure label reflects
missing response content downstream of the transport error; it is not evidence
of invalid generated Python.

Each started run has nine valid proposals out of ten consumed opportunities
(**90%**). Among generated files alone, the rates are 9/10 for A101 and 9/9 for
B101. There are **five AST duplicates**, three in A101 and two in B101; they
consume slots and overlap validity counts. Including the two original seed
rows, Shinka stores **21 program rows and 20 archive members**. No generated
policy is merely an unevaluated file. The four unstarted runs have no native
seed evaluation or archive; their frozen seed identities are placeholders.

A101 reached its best training score at slot 4. Slots 8 and 9 repeat that exact
grim source, and its remaining proposals do not improve the best. Native Shinka
records slot 9 as its best pointer; the frozen earliest-tie rule selects slot 4.
B101 reached its provisional best at slot 2, without receiving its slot-1 output
or score in the second session. All A initial and all ten B prompts equal the
frozen initial prompt byte for byte. Twenty fresh native sessions were recorded;
no tool call was observed, including in the failed session.

The parent-to-child example below is A101 slot 6 → slot 8: TFT → grim, a training
increase of 0.119148. **Grim slot 4 was already supplied as the top-k inspiration**,
and the child exactly repeats it. This is a real native search step but not a
new best or a novel discovery at slot 8. The record shows what information was
available; it does not reveal or establish the model's internal reasoning.

### The terminal failure and resource accounting

Invocation 20 was durably reserved at 14:33:32.732 UTC on 2026-09-08. Codex exited
with code 1 after **13.471 seconds**, emitting a connection error and
`turn.failed`. It recorded no completed Codex turn or native response-usage
record; unreported remote processing cannot be inferred from those absences.
Headless returned the same error. There was no generated code and downstream
evaluation was not submitted. The expected “Code Mode unavailable” startup
warning also appears in successful sessions; it was not the fatal error.

The stop-aware drain completed in **0.051 seconds**, with no evaluator running
and no proposal cancellation needed. The child exited with status 2, the parent
closed the ledger at its recorded return, and all six identities/statuses were
frozen at **14:33:54.708 UTC**. This required **no manual interruption**.
The exact low-level cause of the connection failure is unresolved: preserved
logs identify a send/connection failure, not a proven DNS, TLS, quota or service
cause. The targeted native warning/error log query yielded no extra diagnosis.

The post-stop read-only subscription check succeeded. Rounded account-wide
usage was **6% before and 6% after**; the credit balance remained
**90.6853810000**. There is no evidence of quota exhaustion or purchased-credit
continuation. Rounding and concurrent supervisor use prevent attributing that
account-wide percentage to E1-R alone. The two Shinka run runtimes total
**925.373 seconds**; Codex subprocess runtimes total **698.031 seconds**.
The combined Headless API-list-price estimate is **$0.3417076**, not a subscription
charge. Available usage comprises **20 external invocations, 19 completed Codex
turn events and 19 native model-response records**, distinct accounting units.
