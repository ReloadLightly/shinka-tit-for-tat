# First subscription integration pilot

Authorized scope: one ShinkaEvolve search, at most five external Codex proposal
invocations including smoke calls. No smoke call was made. Read-only account,
model-list, version, quota, and CLI-help checks start no model turn.

The original experiment protocol is unchanged: original defection seed, fixed
payoffs, training/holdout panels, geometric termination, and interpreted policy
execution. Fitness and the sole archive criterion are training `combined_score`.
Native Shinka performs parent sampling, prompt construction, full-code patching,
evaluation scheduling, and archive updates. No manual mutation is supplied.

Provider: Shinka commit `9912af12d423504b8d580f4179fd15f5f88b8c50`, native
`headless/codex@gpt-5.6-terra?effort=low`, installed Headless 0.6.1 and Codex
0.153.4. The model is explicitly listed by the authenticated app-server, which
reports ChatGPT Pro. Upstream example and provider hashes are in
`provider_inspection.json`. The dependency versions are saved in the live run.

Local `subscription_guard.py` wraps the supported `SHINKA_HEADLESS_COMMAND`
boundary and puts a Codex recording shim on the child PATH. It does not replace
Shinka's search or native provider response parsing. The shim forces ChatGPT
authentication, ignores user config for this invocation, strips API credentials
and endpoint overrides from the environment, removes Headless's `--search`, and
sets web search disabled plus request/stream retry counts to zero. Global
credentials and configuration files are not edited. The existing login is used
in place, without credential copies in the repository.

The initial launch in `results/pilot_001` failed before a model turn: Codex
0.153.4 rejected retry overrides under reserved provider ID `openai`. The CLI
`--help` check had validated argument syntax but had not loaded configuration.
That failure consumes invocation 1 conservatively. Four later Shinka proposal
slots were blocked locally by the stop latch and made no external invocation.
All failure rows and prompts are retained. The corrected configuration uses
local provider ID `shinka_subscription`, name `OpenAI`,
`requires_openai_auth=true`, and explicit base URL
`https://chatgpt.com/backend-api/codex`, with WebSockets disabled and zero
request/stream retries. This still uses native Codex's existing ChatGPT login;
it is not the usage-billed OpenAI API. `codex debug models --bundled` actually
loaded the corrected config and returned valid catalog JSON without model calls.
The explicit one-time repair command retains invocation 1 and permits only the
four remaining slots, recorded under `results/pilot_001_repaired`. No experiment
condition, model, seed program, panel, or fitness was changed during repair.

The durable first-milestone ledger reserves a slot before each Codex process is
started. A reservation can conservatively overcount a failed OS process launch.
The lock forbids concurrent launches. The launcher refuses a fresh ledger if
this milestone's usage directory already exists. Codex has a 180-second process
group timeout, Headless 210 seconds, native provider 240 seconds, and the outer
launcher 1,500 seconds. Shinka patch attempts, resamples, novelty attempts, and
LLM attempts are each one (no repeat). Embeddings, novelty model calls, meta
calls, prompt evolution, provider fallback, and cost-based scheduling are off.
Native Headless does not honor Shinka `max_tokens`; no token cap is claimed.

Quota is read before every proposal. Unknown quota, account mismatch, exhausted
quota, or at least 90% window usage refuses a launch. Backend errors latch a
stop; no credit purchase, reset, or continuation endpoint is called. The
account has existing credits, so balances are recorded before and after to
check for credit consumption. Headless pricing estimates (or missing prices)
and Shinka's dollar field are not billing evidence.

## Information boundary

This is an **unblinded integration pilot**. Native read-only Codex can read files
outside its working directory. Headless additionally enables web search by
default; this run disables that search. No Docker or bwrap executable was
available during inspection. The separate temporary working directory,
`project_doc_max_bytes=0`, and instruction to use only the supplied prompt do
not establish filesystem confidentiality. Explicit prompts contain only the
task, programs, training feedback, and native patch-format instructions;
recognition and holdout analysis happen afterward. A mutation could still
read public/local experiment information with file tools. We will inspect
traces, but absence of an observed read does not establish enforced blinding.

The supervisor knows the repository and target. LLM prior knowledge also makes
this operational generation/rediscovery, not knowledge-free invention. Finite
behavioral probe agreement is not a universal equivalence proof.

## Provenance and usage interpretation

Preserve native prompts, raw Codex JSON events, Headless output/usage, failed
attempts, canonical `gen_N/main.py` files, feedback, and the SQLite database.
Offline diagnosis is separate from live database membership. `best/` copies are
not additional generated candidates. Codex `turn.completed` events count agent
turns, not the internal model requests which may occur during one invocation.
Inspect native transcript usage when available and label unavailable counts.

Official authentication/configuration references inspected:
[Codex authentication](https://learn.chatgpt.com/docs/auth),
[Codex configuration](https://learn.chatgpt.com/docs/config-file/config-reference).
