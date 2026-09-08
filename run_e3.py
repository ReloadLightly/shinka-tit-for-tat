#!/usr/bin/env python3
"""E3 continuation search. Default is zero-call preflight; live mode is explicit."""
import argparse
from dataclasses import asdict
import fcntl
import hashlib
import json
import os
from pathlib import Path
import random
import shlex
import shutil
import signal
import subprocess
import sys
import tempfile
import threading
import time

from e3_backend import E3, MODEL, ORDER, ROOT, utc, verify_freeze
from e3_state import checkpoint, verify_checkpoint, restore, read, sha, surviving_workers
from e1r_io import write_json
from e1r_runtime import install, verify_upstream
from e1r_status import read_status, require_subscription_capacity
from evaluate import evaluate_file
from run_evo import dependency_status
from run_e1r import ENV_CONTROLS, configure_imports, task, select

RUN_SECONDS = 9000


def ledger():
    return read(E3 / 'ledger.json')


def initial_prompt():
    from shinka.core.sampler import PromptSampler
    from shinka.database import Program
    from shinka.llm.providers.headless import _render_prompt
    with tempfile.TemporaryDirectory() as tmp:
        metrics, correct = evaluate_file(E3 / 'protocol/seed.py', tmp)
    seed = Program(id='initial', code=(E3 / 'protocol/seed.py').read_text(), generation=0,
        correct=correct['correct'], combined_score=metrics['combined_score'],
        public_metrics=metrics['public'], private_metrics=metrics['private'], text_feedback='')
    sampler = PromptSampler(task_sys_msg=task(), patch_types=['full'], patch_type_probs=[1.0], use_text_feedback=True)
    system, user, _ = sampler.sample(seed, [], [])
    return _render_prompt(msg=user, system_msg=system, msg_history=[])


def progress(run_id, slot, stage, valid=None, score=None, best=None):
    print(f'[E3] run={run_id} slot={slot}/20 stage={stage} valid={valid} '
          f'training={score} current_best={best} invocations={len(ledger()["invocations"])}/60', flush=True)


def training_records(run_id):
    rows = []
    for slot in range(21):
        folder = E3 / 'runs' / run_id / f'gen_{slot}'
        source = folder / 'main.py'
        if not source.exists():
            continue
        correct = read(folder / 'results/correct.json') if (folder / 'results/correct.json').exists() else {'correct': False, 'error': 'No measured fitness'}
        metrics = read(folder / 'results/metrics.json') if (folder / 'results/metrics.json').exists() else {}
        rows.append({'slot': slot, 'source': str(source.relative_to(ROOT)), 'sha256': sha(source),
                     'correct': correct['correct'], 'error': correct.get('error'), 'training': metrics.get('combined_score')})
    return rows


def preflight():
    configure_imports()
    assert dependency_status()['pinned_commit_matches']
    verify_upstream()
    assert sha(E3 / 'protocol/seed.py') == 'fc938dea6c869791ffb3d7fbbb03f95b21ea86152fb3414345a9d107323d56a1'
    return {'external_proposal_invocations': 0, 'seed_sha256': sha(E3 / 'protocol/seed.py'),
            'initial_prompt_sha256': hashlib.sha256(initial_prompt().encode()).hexdigest(),
            'dependency': dependency_status(), 'model': MODEL, 'reasoning_effort': 'low'}


def verify_committed():
    verify_freeze()
    commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
    frozen = read(E3 / 'protocol/freeze.json')
    names = list(frozen['source_sha256']) + ['results/e3/' + n for n in frozen['artifact_sha256']] + ['results/e3/protocol/freeze.json']
    for name in names:
        if subprocess.check_output(['git', 'show', f'{commit}:{name}']) != (ROOT / name).read_bytes():
            raise RuntimeError('Uncommitted freeze: ' + name)
    return commit


def freeze_selections():
    state = ledger()
    if not state.get('closed') or any(state['runs'][r]['status'] != 'completed' for r in ORDER):
        raise RuntimeError('All three searches must finish before selection/analysis gate')
    target = E3 / 'training_selections_frozen.json'
    if target.exists():
        raise RuntimeError('Selections already frozen')
    write_json(target, {'frozen_utc': utc(), 'ledger_sha256': sha(E3 / 'ledger.json'),
                       'selections': {r: select(training_records(r)) for r in ORDER}})


def recovery_check(run_id):
    state = ledger()
    saved = verify_checkpoint(E3, run_id)
    workers = surviving_workers(E3, exclude=(os.getpid(),))
    if workers:
        raise RuntimeError('Surviving E3 workers: ' + str(workers))
    if state.get('failure_class') != 'transient_send' or len(state.get('recoveries', [])) >= 2:
        return False
    record = {'run_id': run_id, 'after_slot': saved['consumed'], 'started_utc': utc(),
              'checkpoint': read(E3 / 'runs' / run_id / 'checkpoint.json'), 'workers': workers,
              'status': 'checking'}
    state.setdefault('recoveries', []).append(record)
    write_json(E3 / 'ledger.json', state)  # Reserve the one bounded check too.
    try:
        status = read_status()
        require_subscription_capacity(status)
        if not any(m['model'] == MODEL and any(e['reasoningEffort'] == 'low' for e in m['supportedReasoningEfforts']) for m in status['models']):
            raise RuntimeError('Model/effort unavailable')
        record.update(status='passed', subscription=status, finished_utc=utc())
        state.update(stopped=False, stop_reason=None, failure_class=None)
    except BaseException as exc:
        record.update(status='failed', error=type(exc).__name__, finished_utc=utc())
        state.update(stopped=True, failure_class='availability_check_failed')
    write_json(E3 / 'ledger.json', state)
    return not state['stopped']


def execute(resume=False):
    with (E3 / 'execution.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        commit = verify_committed()
        state = ledger()
        if state.get('closed') or (state['execution_started'] and not resume):
            raise RuntimeError('Existing experiment: explicit faithful resume required')
        if surviving_workers(E3, exclude=(os.getpid(),)):
            raise RuntimeError('Surviving E3 workers')
        if state.get('stopped'):
            raise RuntimeError('Paused failure requires review; no automatic retry on launcher restart')
        for item in state['runs'].values():
            if item.get('open_segment'):
                opened = item['open_segment']
                if opened['boot_id'] != Path('/proc/sys/kernel/random/boot_id').read_text().strip():
                    raise RuntimeError('Interrupted runtime clock cannot be reconciled across host reboot')
                item['runtime_seconds'] = item.get('runtime_seconds', 0) + time.monotonic() - opened['monotonic']
                item.pop('open_segment')
        state.update(execution_started=True, protocol_commit=state.get('protocol_commit', commit))
        write_json(E3 / 'ledger.json', state)
        for run_id in ORDER:
            while ledger()['runs'][run_id]['status'] != 'completed':
                state = ledger()
                folder = E3 / 'runs' / run_id
                folder.mkdir(parents=True, exist_ok=True)
                used_time = state['runs'][run_id].get('runtime_seconds', 0)
                remaining = RUN_SECONDS - used_time
                if remaining <= 0:
                    state.update(stopped=True, failure_class='run_timeout', stop_reason='Cumulative run bound reached')
                    write_json(E3 / 'ledger.json', state)
                    return 2
                state['runs'][run_id]['status'] = 'running'
                state['runs'][run_id]['open_segment'] = {'monotonic': time.monotonic(),
                    'boot_id': Path('/proc/sys/kernel/random/boot_id').read_text().strip(), 'utc': utc()}
                write_json(E3 / 'ledger.json', state)
                start = time.monotonic()
                with (folder / 'console.log').open('a') as log:
                    child = subprocess.Popen([sys.executable, str(ROOT / 'run_e3.py'), '--run', run_id],
                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, start_new_session=True)
                    timer = threading.Timer(remaining, lambda: os.killpg(child.pid, signal.SIGKILL) if child.poll() is None else None)
                    timer.start()
                    try:
                        for line in child.stdout:
                            log.write(line)
                            log.flush()
                            if '[E3]' in line:
                                print(line.strip(), flush=True)
                        rc = child.wait()
                    finally:
                        timer.cancel()
                state = ledger()
                state['runs'][run_id].update(returncode=rc, runtime_seconds=used_time + time.monotonic()-start,
                                              status='paused', finished_utc=utc())
                state['runs'][run_id].pop('open_segment', None)
                write_json(E3 / 'ledger.json', state)
                try:
                    saved = verify_checkpoint(E3, run_id)
                    if surviving_workers(E3, exclude=(os.getpid(),)):
                        raise RuntimeError('Surviving E3 workers')
                except Exception as exc:
                    state.update(stopped=True, failure_class='checkpoint_integrity', stop_reason=str(exc))
                    write_json(E3 / 'ledger.json', state)
                    return 2
                if state.get('stopped'):
                    if not recovery_check(run_id):
                        return 2
                    state = ledger()
                elif rc:
                    state.update(stopped=True, failure_class='ambiguous', stop_reason=f'Run exit {rc}')
                    write_json(E3 / 'ledger.json', state)
                    return 2
                if saved['consumed'] == 20:
                    state['runs'][run_id]['status'] = 'completed'
                    write_json(E3 / 'ledger.json', state)
                    break
                if not state.get('recoveries'):
                    raise RuntimeError('Unexpected incomplete run')
        state = ledger()
        assert len(state['invocations']) == 60
        state.update(closed=True, completed_utc=utc())
        write_json(E3 / 'ledger.json', state)
        freeze_selections()
        return 0


def run_one(run_id):
    verify_freeze()
    configure_imports()
    from shinka.core import EvolutionConfig, ShinkaEvolveRunner
    from shinka.database import DatabaseConfig, Program
    from shinka.launch import LocalJobConfig
    import numpy as np
    random.seed(int(run_id[1:]))
    np.random.seed(int(run_id[1:]))
    folder = E3 / "runs" / run_id
    saved = verify_checkpoint(E3, run_id) if (folder / "checkpoint.json").exists() else None
    if (folder / "gen_0").exists() and saved is None:
        raise RuntimeError("Existing run lacks faithful checkpoint")
    folder.mkdir(parents=True, exist_ok=True)
    shim_dir = E3 / "bin"
    shim_dir.mkdir(exist_ok=True)
    shim = shim_dir / "codex"
    if not shim.exists():
        shim.symlink_to(ROOT / "e3_backend.py")
    os.environ.update(E3_REAL_CODEX=shutil.which("codex"), E3_REAL_HEADLESS=shutil.which("headless"),
                      E3_RUN_ID=run_id, PATH=str(shim_dir) + os.pathsep + os.environ["PATH"],
                      SHINKA_HEADLESS_COMMAND=shlex.join([sys.executable, str(ROOT / "e3_backend.py")]))
    work = Path(tempfile.mkdtemp(prefix="e3_mutation_"))
    evo = EvolutionConfig(task_sys_msg=task(), init_program_path=str(E3 / "protocol/seed.py"),
        results_dir=str(folder), num_generations=21, job_type="local", language="python",
        patch_types=["full"], patch_type_probs=[1.0], max_patch_resamples=1, max_patch_attempts=1,
        llm_models=[f"headless/codex@{MODEL}?effort=low"], llm_dynamic_selection=None,
        llm_kwargs={"headless_work_dir": str(work)}, embedding_model=None,
        meta_rec_interval=None, meta_llm_models=None, novelty_llm_models=None,
        max_novelty_attempts=1, evolve_prompts=False, prompt_evolution_interval=None,
        use_text_feedback=True, enable_wandb_logging=False, enable_controlled_oversubscription=False,
        max_api_costs=None)
    db = DatabaseConfig(num_islands=1, archive_size=16, archive_selection_strategy="fitness",
        archive_criteria={"combined_score": 1.0}, num_archive_inspirations=0,
        num_top_k_inspirations=1, migration_rate=0.0, enable_dynamic_islands=False)
    job = LocalJobConfig(eval_program_path=str(ROOT / "evaluate.py"), python_executable=sys.executable, time="00:01:00")
    if saved is None:
        write_json(folder / "configuration.json", {"run_id": run_id, "evolution": asdict(evo),
                                                "database": asdict(db), "job": asdict(job), "started_utc": utc()})

    class E3Runner(ShinkaEvolveRunner):
        async def _setup_async(self):
            await super()._setup_async()
            if saved:
                restore(self, saved)

        async def _setup_initial_program(self, code):
            if saved:
                # Native last_iteration=0 resume would otherwise duplicate the seed.
                return
            return await super()._setup_initial_program(code)

        async def _count_completed_generations_from_db(self):
            count = await super()._count_completed_generations_from_db()
            present = set(await self.async_db.get_persisted_generation_ids_async())
            records = [r for r in ledger()['invocations'] if r['run_id'] == run_id]
            # Accounting only: no fabricated Program row or policy fitness.
            return count + sum(r['slot'] not in present and r['status'] != 'reserved'
                               for r in records if (folder / f"gen_{r['slot']}" / 'opportunity.json').exists()
                               and read(folder / f"gen_{r['slot']}" / 'opportunity.json')['no_program'])

        async def _start_proposals(self, num_proposals):
            # Serial quiescent boundary: all preceding evaluation and archive
            # side effects must be committed before native context sampling.
            await self._cleanup_completed_proposal_tasks()
            if (self.active_proposal_tasks or self.running_jobs or self._get_completed_job_work_count()
                or self._has_background_side_effect_work()):
                return
            if ledger().get('stopped'):
                self.should_stop.set()
                return
            checkpoint(self, E3, run_id, 'boundary')
            return await super()._start_proposals(min(num_proposals, 1))

        async def _generate_proposal_async(self, generation, task_id):
            try:
                return await super()._generate_proposal_async(generation, task_id)
            finally:
                records = [r for r in ledger()['invocations'] if r['run_id'] == run_id and r['slot'] == generation]
                if records and records[0]['status'] != 'reserved':
                    no_program = not any(j.generation == generation for j in self.running_jobs)
                    write_json(folder / f'gen_{generation}' / 'opportunity.json', {**records[0], 'no_program': no_program})
                    await self._update_completed_generations()
                else:
                    state = ledger()
                    state.update(stopped=True, failure_class='ambiguous', stop_reason='No terminal invocation for assigned generation')
                    write_json(E3 / 'ledger.json', state)
                    self.should_stop.set()

        async def _cleanup_async(self):
            # The E1-R finalization event drains calls and evaluations first.
            await self._wait_for_completed_job_batches()
            await self._wait_for_background_side_effects()
            await self._cleanup_completed_proposal_tasks()
            await self._update_completed_generations()
            checkpoint(self, E3, run_id, 'terminal')
            return await super()._cleanup_async()

        async def _run_patch_async(self, parent_program, archive_programs, top_k_programs, generation, meta_recs=None, **kwargs):
            if ledger().get("stopped"):
                raise RuntimeError("Stopped experiment: no further proposals")
            os.environ["E3_SLOT"] = str(generation)
            target = folder / f"gen_{generation}"
            target.mkdir(exist_ok=True)
            write_json(target / "supplied_context.json", {"parent": parent_program.to_dict(),
                "archive_inspirations": [p.to_dict() for p in archive_programs],
                "top_k_inspirations": [p.to_dict() for p in top_k_programs]})
            progress(run_id, generation, "proposal", best=select(training_records(run_id))["training"])
            try:
                return await super()._run_patch_async(parent_program, archive_programs, top_k_programs, generation, meta_recs, **kwargs)
            except BaseException as exc:
                state = ledger()
                state.update(stopped=True, stop_reason=state.get("stop_reason") or f"Proposal infrastructure: {type(exc).__name__}")
                write_json(E3 / "ledger.json", state)
                raise
            finally:
                if ledger().get("stopped"):
                    self.should_stop.set()

        async def _process_single_job_safely(self, job):
            result = await super()._process_single_job_safely(job)
            if job.db_retry_count:
                state = ledger()
                state.update(stopped=True, stop_reason="Database finalization failed; no retry")
                write_json(E3 / "ledger.json", state)
                self.should_stop.set()
            rows = training_records(run_id)
            newest = rows[-1]
            progress(run_id, newest["slot"], "evaluated", newest["correct"], newest["training"], select(rows)["training"])
            return result

    runner = E3Runner(evo_config=evo, db_config=db, job_config=job,
                     max_evaluation_jobs=1, max_proposal_jobs=1, max_db_workers=1, verbose=True)
    runner.MAX_DB_RETRY_ATTEMPTS = 1
    install(runner, lambda record: write_json(folder / "terminal_finalization.json", record))
    start = time.monotonic()
    segment = len(list((folder / "segments").glob("*.json"))) if (folder / "segments").exists() else 0
    (folder / "segments").mkdir(exist_ok=True)
    try:
        runner.run()
    finally:
        if (work / "headless_prompts").exists():
            shutil.copytree(work / "headless_prompts", folder / "headless_prompts", dirs_exist_ok=True)
        records = training_records(run_id)
        summary = {"run_id": run_id, "records": records, "training_selected": select(records) if records else None,
                   "runtime_seconds": time.monotonic() - start, "finished_utc": utc(),
                   "shinka_completed_generations": runner.completed_generations,
                   "headless_list_price_estimate_not_charge": runner.total_api_cost}
        write_json(folder / "segments" / f"{segment:02d}.json", summary)
        write_json(folder / "training_summary.json", summary)
    return 2 if ledger().get("stopped") else 0



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--preflight', action='store_true')
    group.add_argument('--execute', action='store_true')
    group.add_argument('--resume', action='store_true')
    group.add_argument('--run', choices=ORDER)
    args = parser.parse_args()
    if args.execute or args.resume:
        raise SystemExit(execute(resume=args.resume))
    elif args.run:
        raise SystemExit(run_one(args.run))
    else:
        print(json.dumps(preflight(), indent=2))
