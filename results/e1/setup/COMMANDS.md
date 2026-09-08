# E1 commands and evidence

Run from `/home/roland/actir/shinka-tit-for-tat`. The repository was inspected
with `git status --short`, `git fetch origin`, `git rev-parse HEAD origin/main`,
and GitHub PR/issue reads before editing. Both Git refs matched reviewed pilot
commit `fe5e130a4b2f3428b4b2bc482bd0378214672ea4` and the worktree was clean.

The decisive local setup commands were:

```bash
.venv/bin/python check_e1_restrictions.py --output results/e1/setup/restriction_checks_verified.json
timeout 180 .venv/bin/python -m unittest discover -s tests -v > results/e1/setup/tests_final.txt 2>&1
.venv/bin/python run_e1.py --preflight > results/e1/setup/preflight.json
.venv/bin/python run_e1.py --freeze > results/e1/setup/freeze_console.txt 2>&1
git add .gitignore e1_backend.py run_e1.py check_e1_restrictions.py tests/test_e1.py results/e1
git commit -m 'Freeze E1 protocol and test restricted subscription search harness'
```

The restriction checks are localhost fixtures with zero external proposals.
The suite passed 31 tests, including two mocked Shinka opportunities per condition.
Preflight made zero calls. Freeze performed read-only account/model/quota checks,
recorded the setup explanation, and created the immutable configuration before
any external proposal. The freeze commit is `e0ca3f3`.

The single authorized live execution command was:

```bash
.venv/bin/python run_e1.py --execute > results/e1/setup/live_console.txt 2>&1
```

It runs the six ordered child commands `.venv/bin/python run_e1.py --run RUN_ID`
with ten proposal opportunities each. The default command remains zero-call;
an existing E1 ledger forbids rerunning or resetting the allowance. Native
Headless and Codex command arguments for every external launch are in the ledger.
Progress is saved both in `live_console.txt` and each run's `console.log`.

During execution, the following accounting-only command checked fresh native
contexts, explicit model/effort, available per-response usage and tool calls.
It does not evaluate holdout or perform recognition:

```bash
.venv/bin/python audit_e1.py --usage-only
python3 -m unittest discover -s tests -p test_e1_analysis.py -v > results/e1/setup/tests_analysis.txt 2>&1
```

The two analysis tests use a local constant-action fixture on a training encounter
and a missing-selection gate; they do not diagnose E1 proposals before the freeze.
The final post-selection analysis/report and verification commands are recorded
in the main E1 report after execution.

Execution stopped at 44 external invocations; the exact targeted cleanup command
was `kill -INT 1271638` after verifying that PID was the stopped A303 child and
that no proposal was running. The parent returned exit status 2 and closed the
ledger. No runner was restarted.

Post-stop commands included:

```bash
.venv/bin/python subscription_status.py --output results/e1/setup/subscription_after.json
.venv/bin/python audit_e1.py --freeze-terminal
.venv/bin/python audit_e1.py > results/e1/setup/audit_console.txt 2>&1
.venv/bin/python diagnose_e1_failures.py > results/e1/setup/failure_reproductions_verified_console.txt 2>&1
MPLCONFIGDIR=/tmp/e1_matplotlib .venv/bin/python render_e1.py
.venv/bin/python write_e1_report.py
timeout 180 .venv/bin/python -m unittest discover -s tests -v > results/e1/setup/tests_post_stop.txt 2>&1
.venv/bin/python run_e1.py --preflight > results/e1/setup/preflight_post_stop.json
.venv/bin/python run_evo.py --preflight > results/e1/setup/pilot_preflight_post_stop.json
```

The final suite passed 36 tests. Both preflights made zero proposal calls.
Post-stop analysis found paired holdout differences 0, −0.11019607843137269,
and unavailable. Incomplete runs were not assigned zero performance. Local
failure reproductions succeeded without model calls; they do not fix or resume
the frozen experiment. Credential-pattern checks covered text and SQLite content;
fixed scientific files, frozen source hashes and the pilot ledger were unchanged.

Publication commands for the preserved partial milestone:

```bash
git fetch origin
git add README.md PROJECT_STATUS.md audit_e1.py diagnose_e1_failures.py render_e1.py write_e1_report.py tests/test_e1_analysis.py tests/test_e1_failures.py results/e1
git commit -m 'Record stopped E1 comparison, diagnostics, and complete partial report'
git push origin main
git rev-parse HEAD
git ls-remote origin refs/heads/main
```

The final response reports the remote-verified commit. The committed evidence
cannot contain its own final commit hash. No GitHub Actions workflow was used.
