# Post-search trace command correction

The first inline trace command requested `holdout/suspicious_tft/400001`, which
is not an identifier in the frozen manifest. `analyze_e3.trace` raised
`StopIteration` at its encounter lookup (analyze_e3.py:103). No trace file was
written. The subsequent verifier therefore raised FileNotFoundError for
`traces.json`; its raw stderr is preserved as verification_before_traces.stderr.txt.

The command was corrected to the manifest's actual `suspicious_tit_for_tat` name.
No source, policy, encounter, scored result or frozen implementation was changed.
This is a reporting-command error, not a failed experimental match or model call.
