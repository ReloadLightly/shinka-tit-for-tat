# E3 continuation v1 commands

Run from `/home/roland/actir/shinka-tit-for-tat` with the existing `.venv` and
subscription login. No install, key authentication, model substitution or new
experiment is part of these commands.

```bash
export PATH="$PWD/.venv/bin:$PATH"
python reconcile_e3.py
python -m unittest discover -s tests -p test_e1r.py -v
python -m unittest discover -s tests -p 'test_e3*.py' -v
python check_e3_boundary.py --output results/e3/continuation_v1/setup/boundary
python -m unittest discover -s tests -v
python run_e3.py --preflight
python run_evo.py --preflight
python reconcile_e3.py --freeze
# Commit and remotely verify the exact continuation freeze before proposals.
git add .gitignore analyze_e3.py e3_backend.py e3_state.py run_e3.py tests/test_e1r.py tests/test_e3.py tests/test_e3_continuation.py reconcile_e3.py check_e3_boundary.py results/e3/continuation_v1
git commit -m "Freeze reconciled E3 continuation with 59 remaining external opportunities"
git push origin main
git ls-remote origin refs/heads/main
python run_e3.py --resume
# Only after all three completed runs and frozen training selections:
python analyze_e3.py --transfer
```

The boundary fixture refuses to overwrite its output; use a new path for a local
replay. It uses a disposable committed checkout, restored full native checkpoint,
installed Shinka and Headless, fake final executable, and no external proposals.
Restriction checks reuse `check_e1r_restrictions.check` with E3's `restricted_settings`
and catalog, with all endpoints localhost and no authentication headers.
Read-only subscription metadata: `python e1r_status.py --output <new-path.json>`.
Original commands and failure logs remain in `../COMMANDS.md` and `../setup`.

## Terminal execution and publication

Continuation freeze: `58e9733ff0a177cb48a4c7bdfacc3e11e7ee1713`, verified on
remote main before the first proposal. `run_e3.py --resume` exited 0 after all
three runs; `analyze_e3.py --transfer` exited 0 after all 6,000 matches. The search
ledger is closed. Running either execution command again refuses the closed
ledger or existing transfer directory; they are historical commands, not a request
to spend further calls or overwrite evidence.

```bash
# Audit regeneration (no model call; recognition requires the completed-search gate):
.venv/bin/python audit_e3.py
# Exact existing scored trace; use the frozen manifest's full opponent identifier:
.venv/bin/python analyze_e3.py --trace S101 --split holdout --opponent suspicious_tit_for_tat --seed 400001 --rounds 16
# Read-only terminal-state, selection, 6,000-record and six-trace verification:
PATH="$PWD/.venv/bin:$PATH" .venv/bin/python verify_e3.py
# Regenerate the self-contained report from existing terminal evidence:
.venv/bin/python write_e3_report.py
```

The first trace command used the nonexistent shorthand `suspicious_tft` and
failed at lookup; the subsequent verifier found the trace file absent. Those
reporting errors are preserved under setup. Correcting the command changed no
policy, encounter or score. Final verification passes. The original 75-test
suite was not rerun unchanged after live search: frozen production files remained
identical, and final work used the direct artifact and scored-trace verifier.
