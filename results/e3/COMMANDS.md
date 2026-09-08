# E3 exact commands

From `/home/roland/actir/shinka-tit-for-tat`:

```bash
source .venv/bin/activate
python run_evo.py --preflight
python run_e3.py --preflight
python -m unittest discover -s tests -v
# The following preparation/live commands are single-use and refuse overwrite:
python prepare_e3.py
git add .gitignore run_e3.py e3_backend.py e3_state.py prepare_e3.py rehearse_e3.py analyze_e3.py tests/test_e3.py results/e3
git commit -m "Freeze E3 continuation search and faithful recovery protocol"
git push origin main
git ls-remote origin refs/heads/main
python run_e3.py --execute
# Only after all three selections are frozen:
python analyze_e3.py --transfer
```

`python run_e3.py --resume` is only for an interrupted launcher with a verified
quiescent checkpoint and an unlatched ledger. It preserves the same experiment
and unused opportunities; paused ambiguous/quota/control failures fail closed.
Automatic classified send-error recoveries occur inside `--execute` and are
limited to two total. Never reset the ledger or rerun a consumed slot.

Zero-call scored trace replay after completion:

```bash
python analyze_e3.py --trace S101 --split train --opponent random --seed 300001
python analyze_e3.py --trace S202 --split holdout --opponent suspicious_tit_for_tat --seed 400001
python analyze_e3.py --trace S303 --split holdout --opponent random_80 --seed 400001
```

The report supplies the actually featured encounters and explains their complete
selected original sources. Policies are always loaded through policy.py.
