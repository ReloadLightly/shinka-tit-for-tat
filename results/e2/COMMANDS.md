# E2 command record

All commands run from `/home/roland/actir/shinka-tit-for-tat`. Experimental model calls: zero. No evolution, model/usage diagnostics, subscription quota checks, transport repair, or paid API was run.

## Recovery before implementation

```bash
cat AGENTS.md README.md PROJECT_STATUS.md SCIENTIFIC_REPOSITORY_STANDARD.md
git status --short
git status --ignored --short
git log -8 --oneline
git remote -v
git worktree list
git branch -vv
git ls-remote origin HEAD refs/heads/main
ps -eo pid,ppid,lstart,etime,pcpu,args
```

Initial sandbox process visibility was restricted to the tool's namespace and GitHub DNS was unavailable. Host-visible read-only inspection established no E2 process and GitHub main/HEAD at fd19af5dd0f168f14b82dd5e2f5b1e68b210fe33. One clean local worktree, no E2 files/checkpoints/freeze/runtime records. Thus unstarted in available evidence. Unrecorded prior activity cannot be reconstructed; nothing suggested an interrupted scored evaluation. No previous Codex, WSL, or unrelated process was stopped. A subsequent full ref audit found no stash, no alternate remote branch and no E2 paths in the two retained Codex snapshot trees (`4a047a028fd8071a0834704d0f4bd365a66de73f` and `49191d50557120c02d2cff5b4c5c9f3ac537c51b`).

## Tests, preparation and pre-evaluation freeze

```bash
python3 -m unittest discover -s tests -p test_e2.py -v > results/e2/setup/tests_before_freeze.txt 2>&1
python3 run_e2.py --prepare
python3 run_e2.py --replay-history
python3 run_evo.py --preflight > results/e2/setup/zero_call_preflight.json
git diff --check
git add e2_common.py run_e2.py tests/test_e2.py results/e2/protocol results/e2/historical_replay.json results/e2/setup
git commit -m 'Freeze zero-call E2 strategy-transfer protocol and encounters'
git push origin main
git ls-remote origin refs/heads/main
```

Remote freeze verified at `6adb42eb2e924a8b54c843d89cdcd28cb2412100` before main evaluation. Preparation, historical replay and existing artifact creation refuse overwrites. The zero-call pilot preflight ran local login/version checks only; no model catalog, subscription quota or connectivity diagnostic was called. E2 uses stdlib Python and does not require installed Shinka. Fourteen archived historical panels (420 matches) replayed exactly.

## Single main evaluation

```bash
python3 run_e2.py --execute > results/e2/execution.log 2>&1
```

One invocation of the controller, no recovery restart, no policy/match retries. It launches one bounded local worker per policy; all commands are `python3 run_e2.py --worker POLICY_ID` under the controller's inherited exclusive lock, per-policy marker, alarm and global deadline. Worker logs are in `workers/`; durable raw events are in `matches/`. Do not invoke workers directly. `runtime.json` records the immutable first start and freeze commit; `completion.json` closes execution and makes later `--execute` refuse. To audit current evidence, use read-only analysis commands below instead of attempting a repeat evaluation.

## Verification and retained local test failures

```bash
.venv/bin/python -m unittest discover -s tests -v > results/e2/setup/tests_full.txt 2>&1
PYTHONPATH=tests .venv/bin/python -m unittest test_e1r.ProcessTests.test_nested_child_dies_when_guard_dies -v > results/e2/setup/test_child_cleanup_retry.txt 2>&1
python3 -m unittest discover -s tests -p test_e2_analysis.py -v > results/e2/setup/tests_analysis.txt 2>&1
```

The first full-suite attempt stalled at the previously documented sandbox mock-seed-copy step. Its host PID 1421944 was checked against the exact unittest command before SIGTERM. Only this session's test process was stopped. Its log was renamed to `setup/tests_full_sandbox_stall.txt` and the mock fixture moved to `setup/e1_unit_ovrxu4tt/`. No E2 worker was stopped. The test suite was then run with normal local process access.

The first host run had one failure in the unchanged `test_nested_child_dies_when_guard_dies` check, which waits two seconds for child death. Its log is `setup/tests_full_first_host_failure.txt`. The isolated test passed in 0.101 s; a complete host rerun passed all 60 then-discovered tests in 56.388 s. The failure's precise timing/system cause is unestablished; no historical implementation was changed.

Two subsequent analysis tests cover missing/unknown cells, duplicate-record rejection and tied/missing ranks. The first caught a duplicate `turns` keyword while merging encounter metadata and results; `analyze_e2.py` was fixed before any export. Both tests then passed. A third check subsequently confirmed that incomplete ranking populations cannot acquire fresh ranks; all three final analysis checks passed (`setup/tests_analysis_final.txt`). The failure log is retained as `setup/tests_analysis_first_failure.txt`. No frozen evaluator/adapter/runner or main match record changed.

## Post-execution export, report and independent verification

```bash
python3 analyze_e2.py --export
python3 write_e2_report.py
python3 analyze_e2.py --verify > results/e2/setup/analysis_verification.txt
python3 -m unittest discover -s tests -p test_e2.py -v > results/e2/setup/tests_frozen_final.txt 2>&1
```

All output creation refuses overwrites. `--verify` is read-only except ordinary Python bytecode caching and replays only the six featured traces as verification, not another main panel. Complete exact trace commands are printed in E2_REPORT.md; for example:

```bash
python3 analyze_e2.py --trace ast_88f3a4f11dba1800 --split train --opponent random --seed 100001 --rounds 16
python3 analyze_e2.py --trace ast_57dad27c89beb4e1 --split holdout --opponent suspicious_tit_for_tat --seed 200001 --rounds 16
```

Publication stages only E2 implementation/analysis/tests/evidence and README/PROJECT_STATUS. Credentials, books, environments, historical ledgers and unrelated changes are excluded. Final commit/push and independent remote SHA verification are recorded by Git history and the session completion response; this file intentionally does not claim a self-referential final commit hash.

## Final review additions

```bash
python3 analyze_e2.py --verify > results/e2/setup/analysis_verification_release.txt
python3 -m unittest discover -s tests -p 'test_e2*.py' -v > results/e2/setup/tests_e2_release.txt 2>&1
git diff --check
```

Final review identified the UTC/boottime discrepancy. `runtime_clock_audit.json` was derived from the original 86,402 clock observations and is reproducible by `analyze_e2.clock_audit()` and `--verify`. Reporting now states both elapsed measures and the unestablished host-clock cause. Raw accounting was not modified. Report/catalogue presentation was rerendered after review; subsequent checks compare renderer output in memory without overwriting files. The final analysis tests also keep the original seed within the five named-reference ranking family.

Publication commands:

```bash
git add .gitignore README.md PROJECT_STATUS.md analyze_e2.py write_e2_report.py tests/test_e2_analysis.py results/e2
git commit -m 'Report complete zero-call E2 transfer results and verified traces'
git push origin main
git rev-parse HEAD
git ls-remote origin refs/heads/main
```
