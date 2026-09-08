# E3 — live continuation beyond an evolved grim policy

Question: starting from the previously generated grim policy, can ShinkaEvolve
generate a higher-original-training-payoff policy whose advantage survives fresh
encounters? This is continuation from evolved code, not discovery from the
always-defect seed or an uninformed prior. No independent-generation condition
is included; three searches are exploratory and cannot establish an advantage
over that method. E1, E1-R and E2 remain separate preserved experiments.

Seed: copy the exact bytes of `results/e1_r/runs/A101/gen_4/main.py`, SHA-256
`fc938dea6c869791ffb3d7fbbb03f95b21ea86152fb3414345a9d107323d56a1`, to
`results/e3/protocol/seed.py`. Keep `initial.py` untouched. Initial training
payoff is 2.655386350817823. Each run initializes its own archive with this seed
alone. No newly generated program or feedback crosses between runs.

Serial runs S101, S202, S303 use local Python/NumPy seeds 101, 202, 303. Each gets
20 proposal opportunities; the separate ledger has a hard total of 60 external
invocations. Reserve durably before external launch. Invalid sources, duplicate
sources, failed launches and any live smoke consume slots without replacement.
There is no live smoke: the first call is a real S101 proposal. Local seeds do
not make remote outputs deterministic. Fresh Codex exec sessions receive only
the unchanged task, native proposal-format instructions, sampled parent and
top-k inspiration code, and original-training feedback.

Use pinned Shinka 0.0.7 commit `9912af12d423504b8d580f4179fd15f5f88b8c50`.
Keep native parent selection, accumulated programs, archive and prompt sampling,
full rewrite parsing, and training feedback. Retain E1-R's reduced configuration:
one island, archive size 16, fitness-only archive criterion, weighted native
parent sampling, zero random archive inspirations, one top-k inspiration,
no migration/dynamic islands, full rewrite format FULL_SYS_FORMATS[0], one
attempt/resample/patch, one model, no dynamic model selection, embeddings, novelty
judge, meta recommendations or prompt evolution. Native parent sampling retains
its existing child-count weighting; this is not an added fitness reward. Serial
quiescent boundaries drain the preceding evaluation and archive side effects
before native sampling of the next proposal. Do not claim every paper mechanism.

Model: `gpt-5.6-terra`, low reasoning effort, through subscription-authenticated
Codex 0.153.4 and Headless 0.6.1. Verify local model/effort availability and quota.
No API keys, paid API, purchased-credit continuation, auxiliary models, judge or
embedding calls, automatic model substitution, or GitHub Actions. Existing
request/stream retry counts remain zero. API-list-price estimates are not
subscription charges. Count invocations, completed model turns, available native
response/token records, and runtimes separately; absent usage is unavailable.

Re-establish the E1-R supported native retrieval controls with six localhost-only
forced calls before proposals. Disable shell/files/images, apps/plugins/MCP,
skills/memory, agents, project documents, environment context and web retrieval;
the advertised code-mode entrypoints have no enabled host. Verify the restricted
model catalog, retaining model identity/instructions while disabling apply_patch
registration. Fresh mutation sessions cannot retrieve repository/evaluator/
opponent/reference code, identities, reports, recognition, development results
or outside experiment material. The supplied E3 seed is the intentional earlier
code exception. This tested tool boundary is not an OS confidentiality container
or a claim of knowledge-free invention.

The fixed simultaneous IPD is unchanged: 0=C, 1=D; payoffs CC=3, CD=0, DC=5,
DD=1. Policies observe only both pre-round histories. No action noise, extra
state, seed, horizon, opponent identity or current opposing action is available.
Independent geometric stopping probability 0.00346 has no fixed cutoff. Keep
the interpreter, proposal limits (16,000 bytes, 400 AST nodes), allowed syntax,
original six training opponents and seeds 11,23,47,89,131. Score total own payoff
/ total rounds; invalid policies score -1. No TFT/cooperation/novelty reward,
new opponent, manual repair, or hand-written hybrid. Candidate sources are
interpreted by policy.py, never imported or exec'd.

## Failure accounting and faithful continuation

Failed invocations consume their slot and have no measured policy fitness.
Preserve raw sanitized output. A failure is automatically recoverable only when
the evidence explicitly contains `Connection failed: error sending request`
and has no quota/authentication indicator. All other transport errors/timeouts
remain ambiguous. Quota/auth, lost information controls, source/configuration
mismatch or ambiguous checkpoint integrity pause the same experiment.

On a recoverable send failure, stop further launches, drain actual native work,
save the full SQLite database (including programs, archive, ancestry, child
counts and attempt records), native generation and accounting state, Python and
NumPy RNG states, runtime DB metadata, invocation ledger and configuration hash.
Check no surviving workers. Perform one bounded read-only model/quota check;
only a successful check permits the next unused opportunity. At most two such
automatic recoveries are allowed over all E3. A third failure pauses. Reserve
each recovery check durably; do not repeat a consumed slot or a failed check.
An explicit resume uses the same database and verified checkpoint, not the best
policy alone. A ledger with an ambiguous reserved invocation cannot resume.

Fresh runtime objects reopen the unchanged database; after setup restore all
saved search/accounting fields and RNGs before native sampling. SQLite metadata
rows are compared by their keys; program/archive row ordering is retained.
The selected configuration uses Python/NumPy RNG for sampling and never needs
SQLite random fallback while its valid archive exists. Quiescent checkpoints
contain no active proposal, evaluation, database retry or archive-side-effect
task. Checkpoint mismatches pause; never reconstruct missing history by guessing.
Failed missing-program slots count only toward opportunity completion; no fake
Program row, score or archive member is created. Preserve each checkpoint.

Retain Codex/Headless/native-provider/evaluator bounds 180/210/240/60 seconds and
the E1-R bounded 350-second drain. Each 20-slot run has a cumulative 9,000-second
outer child-runtime bound across segments. The bound allows metadata and drain
overhead; its clock and recorded UTC are distinct observations. A killed or
unclean process cannot silently reset its allowance. Check workers before resume.

A run completes when all 20 invocations have terminal outcomes and its archive
is safely finalized, even if its final proposal failed. A recoverable failure
still requires its availability check before proceeding to the next run. Report
completed, paused and unstarted statuses, measured/valid counts and failures.
Do not expose post-search evaluation while any future mutation could resume.

## Fixed selection and fresh transfer

Within each run select highest admissible original-training payoff including
the seed, breaking exact ties by earliest slot. Keep the seed absent improvement.
Freeze all three selections before any recognition or transfer evaluation.
The pre-call encounter manifest uses unchanged training opponents with seeds
300001–300100 and unchanged development opponents with seeds 400001–400100.
Verify disjointness from original seeds and E2's 100001–100100/200001–200100.
Retain horizon and SHA-256 train/holdout/opponent/seed match RNG derivation.

Evaluate S101/S202/S303 selections, seed/grim and reference TFT on identical
encounters: 600 matches per policy per panel, 6,000 total. Panels stay separate.
Use serial 300-second workers per policy/panel; preserve failures without retries.
Primary descriptive outcome is each selected development payoff minus seed
development payoff. Also report original-training gain, fresh-training gain,
valid rate, AST duplicates within each run including seed, best trajectories,
source behavior and per-opponent results. Classify no training improvement,
training gain failing transfer, or positive gain retained on both fresh panels.
Never reselect after transfer. Public development types are not an untouched
confirmatory opponent population. No pooling with interrupted experiments.

The report preserves every prompt/source/result/failure/context/archive/usage/
checkpoint/command without credentials; gives complete selected original code,
an actual evolutionary sequence or stagnation, scored encounter traces and
exact replay commands, limitations and one bounded unexecuted follow-up. Changed
text, changed behavior, familiar strategy recovery and novel-strategy claims are
distinct. Finite probe equality is not a universal-equivalence proof. No further
experiment or E2 evaluation-only follow-up is part of E3.
