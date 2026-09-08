# E1 implementation and checks

The reviewed pilot checkout and `origin/main` both pointed to
`fe5e130a4b2f3428b4b2bc482bd0378214672ea4` before edits; the worktree was clean.
The existing pilot report, SQLite audit, completed five-slot ledger, and fixed
scientific source files were read and preserved. E1's protocol and executable
boundary were committed as `e0ca3f3` before any external proposal invocation.

Shinka's pinned `examples/sine_approx_headless` example and native provider were inspected
during setup alongside `core/async_runner.py`, `core/sampler.py`, database
sampling, and the installed Headless wrapper. The provider renders system,
history, and user sections, calls Headless, and passes text to the native full
rewrite parser. Headless passes the prompt file to fresh `codex exec` through
stdin. Its default Codex command grants broad read-only file access and enables
search; these defaults alone are insufficient for E1.

The new `e1_backend.py` is a boundary around the native command, not a policy
generator. It keeps the fixed subscription-only provider used in the pilot,
removes inherited API-key/endpoint and supervisor context variables, forces
ChatGPT authentication, and reads existing credentials in place. No global
credential or permission configuration is edited. Codex 0.153.4 / Headless
0.6.1 and model availability are recorded in `subscription_before.json` and
the frozen protocol. The subscription request/stream retry settings are zero.

Effective information controls were tested against a localhost-only HTTP
fixture with the installed Codex binary. These local fixture sessions are
not external proposal invocations and received no Authorization header. The
fixture supplies deliberately forced model-side calls; no real model is queried.
Shell execution, file mutation, MCP read, agent spawning, and file-image read
all returned unsupported-tool errors. The remaining `functions.exec` entrypoint
returned a disabled code-mode-host error. The canary outside the working
directory remained unchanged and its contents never appeared in requests.
The actual request advertises only inert `functions.exec` and `functions.wait`,
with no nested tool registrations. Search is disabled, and no search tool is
advertised. The code-mode-host startup warning is expected: plain text proposals
remain possible while attempted code-mode execution fails closed.

Several obvious controls were insufficient when tested in isolation:
`features.multi_agent=false` did not remove all collaboration tools;
`agents.enabled=false` did. Disabling shell tools did not remove apply-patch
registration. Supported `model_catalog_json` preserves the selected model's
metadata except `apply_patch_tool_type=null`, which removes that registration.
`catalog_control.json` records this single metadata change and original hashes.
The final checks use exactly the shared `restricted_settings` implementation.
The native base instructions remain in the model catalog; no opponent or
recognition information is in that catalog. This establishes a tested native
tool boundary, not an OS filesystem container or an absence of prior knowledge.

Relevant supported controls were checked against the official
[Codex configuration reference](https://developers.openai.com/codex/config-reference/)
and effective local request/dispatch behavior. The installed Shinka provider is
from the [pinned upstream source](https://github.com/SakanaAI/ShinkaEvolve/tree/9912af12d423504b8d580f4179fd15f5f88b8c50).
`restriction_checks_verified.json` is the decisive recorded test, including
requests, commands, attempted calls, and refusals. The earlier local check is
also retained. An automatic approval review timed out once for the repeated
localhost check; its one permitted retry was approved. This consumed no model call.

Condition A preserves Shinka's weighted parent selection (lambda 10), elite
selection ratio 0.3, one island, fitness archive of size 16, and one top-k
inspiration (zero archive inspirations). The exact effective configuration is
saved per run. Condition B changes only the parent/context sampler to always
return a copy of the original seed plus empty inspirations; Shinka's native
parser, evaluator scheduling, and result storage remain the common harness.
Database storage in B does not feed later prompts. A fixed native full-rewrite
format removes irrelevant format variation between fresh independent prompts.
The backend checks every B prompt and every first A prompt byte-for-byte against
the frozen initial prompt before an external launch. There is no session resume.

The initial local harness checks exposed a test-fixture path mismatch, an
adapter method signature mismatch, and an assertion expecting a more specific
interpreter error string. These were fixed before the protocol freeze and
before model calls. The final 31-test suite passed, including two mocked
opportunities in each condition, fresh initial/B prompt equality, and a rejected
tuple fixture with no replacement. The unchanged interpreter's rejection is
`Unsupported syntax or more than 400 AST nodes`; the post-search audit additionally
lists unsupported node types. The first sandboxed mock harness was interrupted
after it stalled; a bounded run outside that outer sandbox completed the checks.
All test logs remain evidence of setup, not evolutionary results.

The analysis script refuses holdout/recognition without frozen terminal entries
for all six planned runs. After the stop, those entries were four completed
selections, A303's partial best-so-far and a seed-only placeholder for unstarted
B303. The two unfinished entries receive no primary holdout result. This
terminal handling does not complete the predeclared three-pair design.
Additional local tests check that gate, terminal status handling and round-level branch
tracing through the unchanged interpreter. Trace replay uses the actual scored
match RNG and checks full totals against `environment.play`; no candidate is
ever imported or exec'd. Neither analysis nor report rendering makes model calls.

E1 stopped at 44 external proposals. The final audit found two evaluator losses
caused by the pinned scheduler measuring its evaluation limit from proposal
start (B101 slot 3, A303 slot 4). A303 slot 5's subscription metadata check then
timed out before another external launch. Setting `should_stop` did stop all
launches, but did not satisfy the runner's separate `finalization_complete` wait.
The supervisor interrupted only that stopped child, preserving its finally-block
summary and letting the parent close the ledger. The as-executed source freeze
remains unchanged; the ledger was never reopened.

`failure_reproductions.json` demonstrates the timer bug with mocked processes
and a concrete metadata-reader buffering vulnerability with a local fake server.
It does not prove that buffering was the exact cause of the live timeout.
The first diagnostic timer fixture used an incomplete mock specification; that
local-only test failure and corrected successful run are both preserved.
The final suite passed 36 tests, including failure reproductions. These tests
record and explain known defects; passing them does not mean the live harness
defects have already been repaired.
