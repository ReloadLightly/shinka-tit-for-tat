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
