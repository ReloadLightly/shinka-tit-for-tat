# E1-R command record

All commands run in `/home/roland/actir/shinka-tit-for-tat`.

```bash
git status --short
git log -3 --oneline
git fetch origin
git ls-remote origin refs/heads/main
codex --version
headless --version
.venv/bin/python -m unittest discover -s tests -p test_e1r.py -v
.venv/bin/python check_e1r_restrictions.py --output results/e1_r/setup/restriction_checks_verified.json
.venv/bin/python e1r_status.py --output results/e1_r/setup/subscription_check_initial.json
.venv/bin/python rehearse_e1r.py
# Outer sandbox thread/async stall; stopped only the local mock child:
kill -TERM 1310550
.venv/bin/python rehearse_e1r.py --root results/e1_r/setup/rehearsal_verified
# Local relative-path fixture defect, fixed without model calls:
.venv/bin/python rehearse_e1r.py --root results/e1_r/setup/rehearsal_final
.venv/bin/python rehearse_e1r.py --root results/e1_r/setup/rehearsal_frozen
.venv/bin/python -m unittest discover -s tests -v > results/e1_r/setup/tests_frozen.txt 2>&1
.venv/bin/python run_e1r.py --preflight > results/e1_r/setup/preflight.json
.venv/bin/python run_evo.py --preflight > results/e1_r/setup/pilot_preflight.txt
```

The async native rehearsals and full tests used normal local process access after
reproducing the outer supervising sandbox issue; no mutation boundary was relaxed.
Codex restriction tests used only localhost, no auth headers and no external model.
Live and publication commands will be appended as executed.

```bash
.venv/bin/python rehearse_e1r.py --root results/e1_r/setup/rehearsal_release > results/e1_r/setup/rehearsal_release_console.txt 2>&1
```
This last rehearsal includes suppression of native database-write retries;
previous successful rehearsal records remain separate and labeled local mocks.

```bash
.venv/bin/python diagnose_e1r_stop.py > results/e1_r/setup/legacy_stop_console.txt 2>&1
.venv/bin/python -m unittest discover -s tests -v > results/e1_r/setup/tests_release.txt 2>&1
.venv/bin/python run_e1r.py --freeze > results/e1_r/setup/freeze_console.txt 2>&1
```

## Live execution and post-stop analysis

```bash
git add .gitignore README.md PROJECT_STATUS.md audit_e1r.py check_e1r_restrictions.py diagnose_e1r_stop.py e1r_backend.py e1r_io.py e1r_process.py e1r_runtime.py e1r_status.py rehearse_e1r.py render_e1r.py run_e1r.py tests/test_e1r.py results/e1_r
git commit -m "Freeze E1-R protocol after execution repairs and zero-call rehearsals"
git push origin main
git ls-remote origin refs/heads/main
.venv/bin/python run_e1r.py --execute > results/e1_r/setup/live_console.txt 2>&1
# One execution only; returned 2 after invocation 20 transport failure.
# No manual signal and no restart. The parent closed the ledger and froze selections.
.venv/bin/python audit_e1r.py --usage-only > results/e1_r/setup/usage_check_early.txt 2>&1
.venv/bin/python audit_e1r.py > results/e1_r/setup/audit_console.txt 2>&1
.venv/bin/python e1r_status.py --output results/e1_r/setup/subscription_after.json
.venv/bin/python diagnose_e1r.py
MPLCONFIGDIR=/tmp/e1r_matplotlib .venv/bin/python render_e1r.py
.venv/bin/python write_e1r_report.py
.venv/bin/python -m unittest discover -s tests -v > results/e1_r/setup/tests_post_stop.txt 2>&1
```

The pre-call protocol commit was `b6647198e07df4eba7f23b0507dda0ea3d6e322a`,
verified on GitHub. Only reporting/analysis files and documentation changed
after that freeze; operational frozen sources and all scientific files remain
unchanged. The post-stop metadata command makes zero model turns and does not
reopen or consume the experimental ledger. A targeted read-only query of native
warning/error logs for the failed thread found no additional diagnostic rows;
its sanitized record is native_failure_log.json. The standalone diagnosis and
rendering scripts reproduce source proofs, exact scored traces and report tables.

## Continuation and publication verification

The continuation found the local ledger already closed at 20 invocations, while
remote main remained at the pre-call commit. Host process inspection confirmed
no live E1-R execution. No launcher was invoked during this continuation.

```bash
git status --short
git log -5 --oneline
git ls-remote origin refs/heads/main
ps -eo pid,ppid,etime,args
.venv/bin/python -m unittest discover -s tests -v > results/e1_r/setup/tests_publication.txt 2>&1
# Documented sandbox async stall in local mocked run; stop only this test process:
kill -TERM 1355622
mv results/e1_r/setup/tests_publication.txt results/e1_r/setup/tests_publication_sandbox_stall.txt
# Normal local process access, zero external proposals:
.venv/bin/python -m unittest discover -s tests -v > results/e1_r/setup/tests_publication.txt 2>&1
.venv/bin/python run_e1r.py --preflight > results/e1_r/setup/preflight_publication.json
.venv/bin/python run_evo.py --preflight > results/e1_r/setup/pilot_preflight_publication.txt
.venv/bin/python /tmp/verify_e1r_publication.py > results/e1_r/setup/publication_verification_console.txt 2>&1
MPLCONFIGDIR=/tmp/e1r_matplotlib .venv/bin/python render_e1r.py
.venv/bin/python write_e1r_report.py
git diff --check
```

The temporary verifier is preserved as `setup/verify_publication.py` with only
its root resolution changed to repository-relative. It recomputes the audit
without writing it, captures usage/source-diagnosis outputs in memory, and
compares them to preserved evidence. The failed local mock fixture was moved
to `/tmp/e1r_publication_sandbox_fixture`; its console remains in this commit.
GitHub commands used network-enabled execution after sandbox DNS resolution
failed. This did not change the frozen mutation controls.

Publication sequence:

```bash
git add README.md PROJECT_STATUS.md render_e1r.py diagnose_e1r.py write_e1r_report.py results/e1_r
git commit -m "Report stopped E1-R execution with audited sources, traces, and usage"
git push origin main
git ls-remote origin refs/heads/main
```

Final remote verification also uses a fresh shallow clone of GitHub main,
checks its commit against the published local commit, and compares every
published changed file byte for byte, including ledger, report and run evidence.
The clone and verification receipt are local `/tmp` artifacts, outside the
experimental evidence directory. No proposal calls are involved.
