# E3 preparation evidence

Recovery found local main and GitHub both at
9564d2125d5b818e24df1aa2b958938dc2f843f6, a clean tree, no E3 artifacts and no
host-visible E1/E1-R/E2/E3 mutation or evaluator worker. All earlier code and
evidence remain unchanged. This milestone does not execute E2's proposed follow-up.

E3 reuses E1-R's native restrictions, byte-buffered metadata reader, bounded
subprocess/parent-death controls, evaluator timing correction, stop-aware drain
and fsynced JSON replacement. New files implement only E3 accounting, full
checkpoint/resume, serial launch and fixed transfer. The installed upstream
package is unchanged. Versioned source hashes are checked before every call.

The genuine loop runs at most one proposal and evaluation concurrently; the E3
boundary waits for both plus native database/archive side effects to finish
before the next parent sampling. Checkpoints back up the entire SQLite database,
including ordered program/archive rows and attempt records, all active search
counters/costs and DB runtime metadata, both local RNG states, ledger and config.
Only quiescent checkpoints are admissible. Native missing-program failure slots
count toward opportunity completion separately from persisted program counts;
they do not gain a fictitious fitness or program row. Each consumed slot remains
visible in the ledger, attempt evidence and generation opportunity record.

Reopening a SQLite database rewrites some metadata rows with INSERT OR REPLACE,
changing their rowid order while preserving keyed values. The first exact-state
test exposed this; its failure is retained in tests_e3_initial.txt and the first
full-suite log. The fix compares metadata_store by its key. Program/archive row
ordering remains significant and preserved. The native context recovery test
checks the same parent and inspirations, complete program records and subsequent
Python/NumPy RNG state after reopening.

Local restriction tests initially failed to bind localhost in the supervising
sandbox. Re-running outside it passed all six forced tool calls with no auth
header and no canary read/write. catalog_comparison.json confirms the installed
requested model metadata is identical except the intentional apply_patch tool
registration disable. Model/low effort/ChatGPT Pro were independently checked
through read-only metadata, with 11% account-wide usage and credit balance
90.6853810000 before proposals.

The first native mock rehearsal repeated the documented sandbox thread stall
before initial source reading; it ended at its 240-second automatic test bound.
The host rehearsal and release rehearsal completed normal, middle failure,
final failure and first-slot failure cases. The first/middle cases reopen the
same actual database/checkpoint and continue at the next slot to 20, without
replacement. Each fixture uses only local constant-action/invalid-tuple outputs,
not an external model or hand-written experimental candidate. Mock ledgers and
sources are separately marked local_mock_only; none counts toward E3's 60.

Focused unittest checks cover all 60 ordered reservations, duplicate rejection,
failed launch persistence, narrow failure classification, two recovery checks
maximum, analysis gating, RNG roundtrip and native context recovery. The original
zero-call preflight validates unchanged initial.py independently of the E3 seed.

Protocol and source freeze is committed before any live invocation. A read-only
GitHub SHA check is recorded before execution. Runtime and final publication
evidence are added after the freeze without modifying its scientific code.
