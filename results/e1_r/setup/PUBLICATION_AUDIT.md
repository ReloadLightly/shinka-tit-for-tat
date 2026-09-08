# E1-R publication audit — 2026-09-08

At continuation, GitHub main was still the pre-call freeze at
`b6647198e07df4eba7f23b0507dda0ea3d6e322a`. Local evidence already recorded the
stopped execution: `execution_started=true`, `closed=true`, `stopped=true`,
20 external invocations, A101 exit 0 and B101 exit 2. Inspection of host processes
found no E1-R launcher, backend or mutation session. The last native response
records “Connection failed: error sending request” and `turn.failed`, with no
program. No execution was launched, resumed or reset during publication work.
The underlying transport cause remains unresolved.

The existing scientific audit and raw execution artifacts were preserved.
An independent call to the offline `audit()` function reproduced the complete
archived audit after excluding only the new analysis timestamp. All candidates
were interpreted through `policy.py`. Recomputed usage and native context
extractions were captured in memory and compared against the preserved records,
without rewriting them. The source proofs and supplemental traces reproduced
exactly. Both SQLite integrity checks returned `ok`. All frozen operational and
scientific source hashes, protocol/catalog hashes and previous ledgers match.
The E1-R ledger hash was unchanged before and after verification.

The report renderer now includes every archived selected-policy trace, including
A101's scored holdout encounter with alternator. This is presentation of existing
post-search evidence; it adds no experimental condition or proposal.

- [Independent verification results](publication_verification.json) and
  [console](publication_verification_console.txt); the exact verifier is retained
  as [verify_publication.py](verify_publication.py), with a repository-relative root.
- [Final unittest suite](tests_publication.txt): 52 tests passed in 17.439 seconds.
- [E1-R zero-call preflight](preflight_publication.json) and
  [pilot zero-call preflight](pilot_preflight_publication.txt): passed.
- Credential-pattern scan: 4,981 files scanned, zero matches; report local links
  resolve. Pattern checks supplement inspection of prompts, native context,
  logs, usage and publication scope; they are not a universal secret detector.

A second scan of the 501 staged files found zero credential-pattern matches
and confirmed that index contents matched the reviewed working files. Only
E1-R evidence, analysis and documentation were staged. Authored code/report
whitespace checks passed. A whole-evidence whitespace check reports native
log padding and generated SVG whitespace; those raw bytes are preserved.
SQLite sidecars are retained consistently with E1; both WAL files are empty.

The first final-suite attempt reproduced the documented outer-sandbox async
stall while copying the local mock seed. Only this turn's stalled unittest
process (host PID 1355622) was terminated. Its
[console is preserved](tests_publication_sandbox_stall.txt); the leftover mock
fixture was moved to `/tmp/e1r_publication_sandbox_fixture`. The suite then passed
with normal local process access. These were zero-external-call tests, unrelated
to the live invocation-20 transport failure, and consumed no experiment slots.

Publication contains the stopped run and its report. The three-call diagnostic
in FOLLOWUP.md remains a proposal requiring new authorization; none was run.
