#!/usr/bin/env python3
"""Read-only completed E3 verification and exact replay of saved scored traces."""
import json
from e3_state import E3, ROOT, read, sha, database_digest, validate_accounting, verify_freeze
from run_e3 import configure_imports, training_records
from run_e1r import select
from e3_backend import ORDER
from e2_common import aggregate


def verify():
    configure_imports()
    verify_freeze()
    ledger = read(E3/'ledger.json')
    validate_accounting(ledger)
    assert ledger['closed'] and all(ledger['runs'][r]['status']=='completed' for r in ORDER)
    assert len(ledger['opportunities'])==60 and len(ledger['invocations'])<=59
    frozen=read(E3/'training_selections_frozen.json')
    assert frozen['ledger_sha256']==sha(E3/'ledger.json')
    for run_id in ORDER:
        assert frozen['selections'][run_id]==select(training_records(run_id))
        folder=E3/'runs'/run_id
        pointer=read(folder/'checkpoint.json'); snapshot=E3/pointer['path']
        assert sha(snapshot/'state.json')==pointer['sha256']
        saved=read(snapshot/'state.json')
        assert saved['consumed']==20 and saved['runner']['next_generation_to_submit']==21
        assert saved['runner']['completed_generations']==21 and saved['drained']
        assert sha(snapshot/'programs.sqlite')==saved['database_sha256']
        assert sha(snapshot/'ledger.json')==saved['ledger_sha256']
        assert sha(folder/'configuration.json')==saved['configuration_sha256']
        assert database_digest(folder/'programs.sqlite')==database_digest(snapshot/'programs.sqlite')==saved['database_digest']
        assert saved['invocations']==ledger['invocations'][:len(saved['invocations'])]
        assert saved['opportunities']==ledger['opportunities'][:len(saved['opportunities'])]
    execution=read(E3/'transfer/execution.json')
    assert len(execution['workers'])==10 and all(w['returncode']==0 for w in execution['workers'])
    manifest=read(E3/'protocol/encounters.json')
    summary=read(E3/'transfer/summary.json')
    matches=0
    for name in (*ORDER,'seed','TFT'):
        for split in ('train','holdout'):
            rows=[json.loads(s) for s in (E3/'transfer'/f'{name}_{split}.jsonl').read_text().splitlines()]
            expected=[r for r in manifest if r['split']==split]
            assert len(rows)==len(expected)==600
            assert [{k:r[k] for k in expected[0]} for r in rows]==expected
            assert all(r['policy']==name and r['status']=='ok' for r in rows)
            value=aggregate(rows)
            value['opponents']={op:aggregate([r for r in rows if r['opponent']==op],expected=100) for op in sorted({r['opponent'] for r in rows})}
            assert summary[name][split]==value
            matches+=len(rows)
    from analyze_e3 import trace
    traces=read(E3/'traces.json')
    for saved in traces:
        e=saved['encounter']
        assert trace(saved['policy'],e['split'],e['opponent'],e['seed'],len(saved['steps']))==saved
    usage=read(E3/'usage_summary.json')
    assert usage['external_invocations']==len(ledger['invocations'])
    assert usage['unique_native_threads']==len(ledger['invocations'])
    assert all(r['tool_calls_observed']==0 for r in usage['runs'].values())
    result={'passed':True,'external_proposal_invocations_in_verification':0,'historical_external_invocations':len(ledger['invocations']),
        'completed_searches':3,'verified_fresh_matches':matches,'exact_scored_trace_replays':len(traces),
        'selected_minus_seed':{r:{split:summary[r][split]['mean_payoff']-summary['seed'][split]['mean_payoff']
                                      for split in ('train','holdout')} for r in ORDER}}
    print(json.dumps(result,indent=2))
    return result


if __name__=='__main__':
    verify()
