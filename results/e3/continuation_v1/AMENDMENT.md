# E3 continuation amendment v1

This explicitly authorized amendment continues the experiment frozen at
3288b90e625daf0f02e684eb32d791c4f3f261a1, using evidence reviewed at
7b5e8b40a2ac040b09c5c3247244a5844ab3e72b. It supplies no new experiment or budget.
The [original protocol](../protocol/PROTOCOL.md), ledger, failure logs and checkpoint
snapshots are immutable; reconciliation.json links their hashes and timestamp.

S101 opportunity 1 is consumed as local_prelaunch_failure: three local attempts,
zero external launches, no generated policy and no fitness. This accounting record
was made at reconciliation time. It does not claim a reservation existed earlier.
Opportunity 1 is never rerun and the retries are not generations 2 and 3.

There remain 59 external proposal launches: S101 opportunities 2–20 (19),
S202 1–20 (20), S303 1–20 (20). Each assigned opportunity is durable before the
wrapper, independent of the external-invocation reservation. A local launch failure,
failed external call, invalid source or duplicate consumes its opportunity.
No replacements, smoke calls, retry/resampling calls or new 60-call allowance.
Historical plus future external invocations cannot exceed the original 60 cap.
Completion requires 20 terminal opportunities per run and a safely finalized archive,
not 20 external calls for S101. Unequal available model opportunities are reported.

The full terminal S101 database and configuration, all ancestry and child counts,
attempt records, DB runtime fields and Python/NumPy RNG states are retained.
The derived checkpoint changes only the explicit opportunity accounting (0 to 1);
next_generation_to_submit remains 2 and every native saved counter remains intact.
The count of completed opportunities is subsequently updated from durable outcomes
by the existing native completion adapter; no fake Program row or fitness is added.
Cumulative runtime starts with the actual previous 67.56626177899307 seconds.
The reconciliation is idempotent and refuses conflicting original or newer state.

All scientific settings, seed, training panels, selection rule, model gpt-5.6-terra
at low effort, subscription authentication, pinned Shinka/native context sampling,
serial order, timeout bounds, two classified-send-failure recoveries and original
6,000-match transfer manifest remain unchanged. Fresh mutation sessions retain the
verified native restrictions and receive no supervisory, recognition or transfer
context. Original source mismatches are explicitly covered by new continuation
hashes, without changing the original freeze. Tests use synthetic local fixtures
only and never create scientific candidates or authorize external proposals.

The legacy fixture repair gives interpreter startup a separate bounded readiness
handshake before the original timed behavior. Production timeouts are unchanged;
UTF-8, buffered output, deadline, and process cleanup assertions remain active.
The original failed test logs remain in ../setup.

Implementation, reconciliation, readiness evidence and source hashes are committed,
pushed and remotely verified before the first external continuation proposal.
All three training-only selections must be frozen before recognition or transfer.
No further experiment is executed by this amendment.
