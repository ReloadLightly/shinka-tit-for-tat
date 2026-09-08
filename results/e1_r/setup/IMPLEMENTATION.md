# E1-R execution adapters, version 1

E1 and the pilot sources, outputs and ledgers remain unchanged. E1-R has separate
`run_e1r.py`, `e1r_backend.py`, `e1r_status.py`, `e1r_runtime.py`, `e1r_io.py`,
`e1r_process.py` and `results/e1_r/`. Model, task, prompt format, original seed,
interpreter, evaluator, panels, fitness and recognition are unchanged.

The installed Shinka 0.0.7 at commit 9912af12d423504b8d580f4179fd15f5f88b8c50
is not edited. `e1r_runtime.py` version 1 hash-checks its async runner and
scheduler. It installs two per-run interface adapters. The original async loop,
parent selection, proposal generation, parser, job finalization and database
remain upstream code. Reproduce by installing requirements-shinka.txt and
running the committed E1-R launcher; no unrecorded site-packages patch is needed.

1. `e1r_status.py` uses binary unbuffered pipes, an explicit bytes buffer and
   `os.read`. Complete queued lines are consumed before polling again. Every
   loop checks a monotonic deadline, including notification floods; partial
   UTF-8 is decoded only once a full JSON line exists. EOF, partial EOF, malformed
   JSON, oversized data, timeout and RPC errors fail closed. Four metadata RPCs
   each have 30 seconds, followed by bounded process cleanup. Diagnostics keep
   method names, counts, elapsed time and outcome, never arbitrary error payloads.
   Notifications are counted; mismatched response IDs cannot satisfy a request.
   There is no metadata retry loop.
2. The scheduler sees a shallow job copy whose timeout `start_time` is the
   actual `evaluation_started_at`. The original job retains proposal timestamps
   for usage analysis. Existing 60-second timeout/kill logic is used unchanged.
   Tests reproduce a wrongful kill with 82 seconds of proposal time, verify
   fresh evaluation survives, and verify a real 61-second evaluation is killed.
3. A stop-aware finalization event races normal upstream finalization with
   `should_stop`. A durable backend latch prevents launches immediately. Existing
   proposals have up to 250 seconds to save their bounded results, then are
   cancelled; outstanding evaluations are drained with their own 60-second
   limit through the native finalizer. The complete drain has a 350-second
   bound. The native finally block closes the DB/scheduler. The serial parent
   saves the child exit, closes the ledger and freezes all six terminal statuses
   and selections, with no manual signal or automatic continuation.

The parent retains the 2,600-second run watchdog. Codex, Headless wrapper and
native provider retain 180/210/240-second bounds. `e1r_process.py` also sets
Linux PR_SET_PDEATHSIG locally: a killed outer wrapper cannot leave its separately
grouped child running. Tests verify both timeout output retention and parent-death
cleanup. No global credential or permission configuration changes.

Ledger writes use atomic replace, file fsync and directory fsync. A separate
execution lock prevents simultaneous experiment launches; the existing exclusive
proposal lock prevents simultaneous mutations. Freeze creates a zero-invocation
ledger. Execution is single-use and requires all frozen code/protocol bytes in
HEAD before the first call. Per-run and total limits, exact slot order and no
replacement are checked before every reservation. The old ledgers' hashes are
verified on every external boundary. Model availability is checked without
substitution at freeze and before each proposal. Failed external launches count;
metadata failures before a proposal do not consume a proposal but stop the study.

Both conditions retain native FULL_SYS_FORMATS[0]. A has upstream parent/archive
selection and training feedback; B overrides only its context sampler to return
the seed and no inspirations. The initial rendered prompt is byte-identical to
E1's. The backend verifies all A initial and every B prompt before launch.
Database finalization retries are also disabled (MAX_DB_RETRY_ATTEMPTS=1); a failed write latches a stop. Retries: one Shinka query attempt / one backoff attempt / one patch attempt /
one resample attempt (meaning no second attempt); Codex request and stream
retries zero. No auxiliary models, embeddings, fallback or spend threshold.

## Native mutation information controls

Installed Codex 0.153.4 / Headless 0.6.1 were verified. The selected model catalog
matches current cached gpt-5.6-terra metadata except apply_patch_tool_type=null,
which removes file-edit tool registration. No model identity/instructions changed.
Supported per-process CLI settings disable web/search, shell, unified execution,
file/image tools, MCP, plugins, apps, skills, memory, agents, project documents,
environment context and other retrieval. Only inert functions.exec/wait remain
advertised; the disabled code-mode host refuses forced dispatch. This expected
startup item-level error does not prevent text generation and is not confused
with fatal error / turn.failed events. The exact commands and forced localhost
requests are preserved in restriction_checks_verified.json. The six checks sent
no authentication, made no external model calls, and could neither retrieve nor
modify the outside-directory canary. Generic native instructions and pretrained
knowledge remain; this is a tested native tool boundary, not an OS container.

## Local verification history

The first focused suite passed 12 tests, later extended to 16. The first full
rehearsal stalled before reading the seed under the supervising filesystem/
network sandbox. A minimal asyncio.to_thread fixture also timed out there.
Only that zero-call child was terminated; its logs remain in setup/rehearsal.
The next rehearsal used a relative --root argument and exposed a mock-entrypoint
path bug. It remains in setup/rehearsal_verified; root is now resolved before use.
The successful six-run and metadata/backend/quota fixtures are in
setup/rehearsal_final. A final rehearsal of the frozen implementation is in
setup/rehearsal_release, following setup/rehearsal_frozen. These are synthetic tests, not scientific proposals.
They use constant-cooperator and invalid-tuple fixtures, never manually supplied
TFT. E1-R's experimental allowance remains separate from every local mock ledger.

`diagnose_e1r_stop.py` additionally runs the unchanged old E1 runner with a
forced local metadata failure. It demonstrably hangs after the stop latch and
is ended by its automatic 25-second fixture timeout. The original failed
transport/timer fixtures are re-recorded in legacy_failure_reproductions.json.
These legacy reproductions are separate from the corrected successful stop tests.
The final required unittest suite passed 52 tests (tests_release.txt).
