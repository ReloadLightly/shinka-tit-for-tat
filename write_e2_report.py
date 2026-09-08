#!/usr/bin/env python3
"""Render E2 evidence. No evaluation or external calls."""
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from e2_common import E2, ROOT, read

RULES = {
'88f3': 'Grim: cooperate until the opponent has defected, then defect permanently.',
'57da': 'Copy the last opponent action, except defect on detected mixed periodic suffixes of periods 2–6.',
'053d': 'Copy the last opponent action, except defect on mixed periodic suffixes of periods 2–4.',
'0728': 'Cooperate initially and defect only after two consecutive opponent defections (TFT for two tats).',
'0765': 'Cooperate on the first two rounds, then copy the last opponent action.',
'0a7f': 'TFT with an additional defection whenever positive history length is divisible by 32.',
'1084': 'Cooperate first, exploit an opponent with no defection yet, otherwise copy its last action.',
'2d4e': 'Defect for four rounds; cooperate thereafter only if the opponent has never defected.',
'5efd': 'Period 2–4 detection plus priority conciliatory branches after own defection and an exploitation branch after six all-cooperate observations.',
'6562': 'Start by defecting; cooperate only when the opponent last defected and either there is only one observation or its preceding action was cooperation.',
'6a4a': 'Cooperate first; defect while the opponent has never defected; thereafter copy its last action.',
'7aba': 'Play D then C; thereafter defect forever if the opponent cooperated in round 2, else copy its latest action.',
'7afd': 'Cooperate after opponent defection; against a never-defecting opponent begin exploitation at history length 31 and continue while it stays cooperative.',
'7b58': 'Cooperate for 12 rounds; then defect if the opponent never defected, or if own last defection met cooperation; otherwise cooperate.',
'7cfa': 'TFT except defect on a repeated alternating suffix (period 2).',
'7dfe': 'Exact TFT by binary last-action branches.',
'8372': 'Cooperate initially and defect only after two consecutive opponent defections (TFT for two tats).',
'8f21': 'Open D,C, sometimes another C after opponent C,D; otherwise exploit never-defectors and copy the latest action after any defection.',
'90ec': 'TFT except defect on mixed periodic suffixes of periods 2–3.',
'93a7': 'Period 2–6 detector with a round-2 defection and repeated defection after exploiting cooperation.',
'9c7f': 'Grim by the count of opponent defections.',
'a331': 'Open C,C,C,D,C; conditionally defect on round 6; then exploit never-defectors and otherwise copy the last action.',
'a5b3': 'Cooperate first; exploit after three all-cooperate observations; forgive a single retaliatory defection when both players have defected exactly once; otherwise TFT.',
'aaac': 'Open D,C,C, then TFT.',
'ab54': 'Start C; stay if the last actions match and switch otherwise. For binary actions this returns the opponent’s last action: exact TFT, not ordinary WSLS.',
'abc6': 'Exact TFT: cooperate first and then copy the opponent’s last action.',
'b643': 'TFT for two tats with a defection every 20 rounds while the opponent has never defected.',
'ba64': 'TFT with exploitation after 12 cooperative observations and forgiveness of the first opponent retaliation when both just defected.',
'bfd1': 'Ordinary WSLS: repeat own action after opponent cooperation, switch after opponent defection.',
'c578': 'Defect after three opponent defections; otherwise use a WSLS-like response to defection and probe after four mutual cooperations.',
'c709': 'Defect first and against never-defectors; forgive the first observed opponent defection; otherwise copy its last action.',
'd803': 'Ordinary WSLS: start C, then cooperate after matching actions and defect after mismatching actions.',
'de86': 'Start D; then cooperate if either of the last two available opponent actions was C, otherwise defect.',
'f6ea': 'Exact TFT using the history truth value for the initial branch.',
'f740': 'Exact TFT with an explicit initial if statement.',
}


def fmt(x):
    return 'Unavailable' if x is None else f'{x:.6f}'


def signed(x):
    return 'Unavailable' if x is None else f'{x:+.6f}'


def table(headers, rows):
    return '\n'.join(['| ' + ' | '.join(headers) + ' |', '| ' + ' | '.join(['---'] * len(headers)) + ' |'] +
                     ['| ' + ' | '.join(map(str, r)) + ' |' for r in rows]) + '\n'


def label(spec):
    if spec['kind'] != 'generated':
        return spec['id']
    o = spec['origins'][0]
    return f"{o['experiment'].upper().replace('_', '-')} {o['run']}:{o['slot']}"


def write_new(path, text):
    with path.open('x') as out:
        out.write(text)


def main():
    inv = read(E2 / 'protocol/inventory.json')
    summary = read(E2 / 'summary.json')
    data = summary['policies']
    traces = read(E2 / 'traces.json')
    runtime, completion = read(E2 / 'runtime.json'), read(E2 / 'completion.json')
    specs = inv['policies']
    execution_status = 'complete' if summary['coverage'].get('ok', 0) == summary['planned_matches'] else 'partial'
    generated = [s for s in specs if s['kind'] == 'generated']
    grim, period = specs[:2]
    started_utc = datetime.fromtimestamp(runtime['unix_seconds'], timezone.utc).isoformat()
    ended_utc = datetime.fromtimestamp(completion['clock']['unix_seconds'], timezone.utc).isoformat()
    def panel(pid, split):
        return data[pid]['panels'][split]
    def ptable(entries):
        return table(['Policy / first origin', 'Original train', 'Fresh train', 'Δ TFT', 'Δ grim',
                      'Original development', 'Fresh development', 'Δ TFT', 'Δ grim'], [
            [label(s)] + [v for split in ('train', 'holdout') for v in (
                fmt(panel(s['id'], split)['original_mean_payoff']), fmt(panel(s['id'], split)['mean_payoff']),
                signed(panel(s['id'], split)['difference_from_tit_for_tat']), signed(panel(s['id'], split)['difference_from_grim']))]
            for s in entries])
    def opponent_table(pid):
        totals = table(['Panel', 'Own payoff', 'Rounds', 'Cooperations', 'Cooperation rate'], [
            [split, panel(pid, split)['total_payoff'], panel(pid, split)['turns'], panel(pid, split)['cooperations'],
             fmt(panel(pid, split)['cooperation_rate'])] for split in ('train', 'holdout')])
        return totals + '\n' + table(['Panel', 'Opponent', 'Own payoff / rounds', 'Payoff/round', 'Cooperation', 'Δ TFT', 'Δ grim'], [
            [split, name, f"{s['total_payoff']}/{s['turns']}", fmt(s['mean_payoff']), fmt(s['cooperation_rate']),
             signed(s['difference_from_tit_for_tat']), signed(s['difference_from_grim'])]
            for split in ('train', 'holdout') for name, s in panel(pid, split)['per_opponent'].items()])
    def rank_table(entries):
        return table(['AST / first origin', 'Original train rank', 'Fresh train rank', 'Original development rank',
                      'Fresh development rank', 'Fresh development rank within original available subset'], [
            [f"`{s['id']}` / {label(s)}", str(panel(s['id'], 'train')['original_rank']), str(panel(s['id'], 'train')['fresh_rank']),
             str(panel(s['id'], 'holdout')['original_rank']), str(panel(s['id'], 'holdout')['fresh_rank']),
             str(panel(s['id'], 'holdout')['fresh_rank_original_available_subset'])] for s in entries])

    catalogue = ['# E2 candidate and provenance catalogue\n',
        'All 58 live-valid occurrences map to 35 parsed ASTs. Every source hash and original status is retained in '
        '[the frozen inventory](protocol/inventory.json). No generated source was repaired. Different ASTs need not '
        'mean different behavior. Rule descriptions below follow the preserved source; they are not fitness labels. '
        'All ranks use competition ties. E2 rankings do not alter historical selections.\n',
        '## All generated policies: scores\n', ptable(generated),
        '## Original and exploratory fresh ranks\n',
        f"Training ranks use 35 generated ASTs; original development ranks use {panel(grim['id'], 'holdout')['original_rank_population_count']} ASTs with an archived development score; fresh ranks use all 35. "
        'None means unavailable, never zero. A shared AST may have an available score from another complete origin; '
        'the incomplete origin itself remains historically unavailable. The last column compares the same available subset.\n',
        rank_table(generated)]
    for spec in generated:
        pid = spec['id']
        catalogue += [f'## {pid} — {label(spec)}\n', RULES[pid[4:8]] + '\n',
            table(['Experiment', 'Condition', 'Run', 'Slot', 'Run status', 'Original status', 'Historical selected/provisional', 'Source SHA-256', 'Source'], [
                [o['experiment'], o['condition'], o['run'], o['slot'], o['run_status'], o['original_status'],
                 o['historical_selected'], f"`{o['source_sha256']}`", f"[original](../../{o['source']})"] for o in spec['origins']]),
            'Complete unchanged representative source (all byte variants are linked above):\n',
            '```python\n' + (ROOT / spec['source']).read_text().rstrip() + '\n```\n', opponent_table(pid)]
    catalogue += ['## Exclusions: every originally ineligible or absent slot\n',
        table(['Experiment', 'Run', 'Slot', 'Run status', 'Original status', 'Source / reason'], [
            [e['experiment'], e['run'], e['slot'], e['run_status'], e['original_status'],
             (f"[source](../../{e['source']}) — " if e['source'] else '') + str(e['reason'])] for e in inv['exclusions']]),
        '62 excluded slots include 3 rejected sources, 2 generated but originally unevaluated sources, 1 failed invocation '
        'without a source, 1 blocked-before-launch slot and 55 unattempted slots. Invalid or missing sources are not silently '
        'repaired or counted as live-valid. This inventory is of 120 planned slots, not 120 actual invocations.\n',
        '## Named references and all 32 memory-one policies\n', ptable([s for s in specs if s['kind'] != 'generated']),
        table(['Comparator', 'Training cooperation rate', 'Development cooperation rate'], [
            [spec['id'], fmt(panel(spec['id'], 'train')['cooperation_rate']), fmt(panel(spec['id'], 'holdout')['cooperation_rate'])]
            for spec in specs if spec['kind'] != 'generated']),
        'Memory-one bit order: initial action, after CC, CD, DC, DD (own action first). The 32 existing comparator '
        'functions come from baseline.memory_one. The original seed is the always-defect comparator. Full per-opponent '
        'statistics and family ranks for every comparator are in summary.json; every encounter is in per_match.jsonl.\n']
    write_new(E2 / 'CATALOGUE.md', '\n'.join(catalogue))

    report = ['# E2 — transfer of already generated strategies\n',
        '## Question and result\n',
        'Which strategies generated in E1 and E1-R retain their payoff advantages on fresh encounters, and which decision '
        'rules explain them? This is a zero-model-call, post-search analysis of fixed programs. Historical winners remain fixed.\n',
        f"Status: **{execution_status}**. Coverage: **{summary['coverage'].get('ok', 0):,}/{summary['planned_matches']:,} successful matches** across 72 entries "
        '(35 generated ASTs, five named references including the seed, and 32 memory-one comparators). '
        f"Frozen CLOCK_BOOTTIME elapsed **{completion['elapsed_seconds']:.3f} seconds**, within the frozen 2,700-second allowance. "
        f"Status counts: `{summary['coverage']}`. Experimental model/proposal/judge/embedding calls: **zero**.\n",
        f'Main execution began {started_utc} and closed {ended_utc}.\n',
        'Clock qualification: those UTC timestamps span **2,644.755 seconds (44.08 minutes)**, 146.936 seconds longer than the frozen elapsed clock. Across 86,402 clock observations the boot identity is unchanged and the execution-ordered boottime values are monotonic; 76 adjacent observations show UTC/boottime discrepancies above 0.1 seconds. The host clock-adjustment cause is unestablished, so the two measures are not interchangeable estimates of precise physical wall time. Both recorded spans are below 45 minutes. Original accounting and timestamps are untouched; [runtime_clock_audit.json](runtime_clock_audit.json) preserves the discrepancy and verification recomputes it.\n',
        ptable(specs[:7]),
        f"E1-R A101’s selected grim retains its TFT advantage on fresh training ({signed(panel(grim['id'], 'train')['difference_from_tit_for_tat'])}) "
        f"and fresh development encounters ({signed(panel(grim['id'], 'holdout')['difference_from_tit_for_tat'])}). "
        f"E1 A202’s selected period detector retains a training advantage over TFT ({signed(panel(period['id'], 'train')['difference_from_tit_for_tat'])}) "
        f"but remains below grim ({signed(panel(period['id'], 'train')['difference_from_grim'])}). Its development disadvantage persists: "
        f"{signed(panel(period['id'], 'holdout')['difference_from_tit_for_tat'])} vs TFT and "
        f"{signed(panel(period['id'], 'holdout')['difference_from_grim'])} vs grim. Fresh encounters do not rescue its original transfer weakness.\n",
        '## Setup and provenance\n',
        'The untouched world is a simultaneous iterated Prisoner’s Dilemma: actions 0=C and 1=D, candidate payoffs '
        'CC=3, CD=0, DC=5, DD=1. Each match length is geometric with stopping probability 0.00346. '
        'environment.horizon(seed) samples the endpoint independently; policies see only the two histories. '
        'There is no endpoint disclosure, fixed truncation, action noise, self-play addition, or cooperation reward. '
        'Generated policies are interpreted by unchanged policy.py, never imported or executed as arbitrary Python.\n',
        table(['Panel', 'Opponents', 'Seeds', 'Matches/policy', 'Rounds/policy'], [
            ['Original training', 'Always C; always D; fair random; TFT; grim; WSLS', '100001–100100', 600, panel('grim', 'train')['turns']],
            ['Original development holdout', 'Alternator; suspicious TFT; TFT for two tats; hard TFT; random p(C)=0.2; random p(C)=0.8', '200001–200100', 600, panel('grim', 'holdout')['turns']]]),
        'Opponent rules are unchanged: always-C/D are constant; random policies draw independent cooperation with probabilities 0.5, 0.2 or 0.8. TFT starts C and copies the opponent’s last action. Grim starts C and defects permanently after any opponent D. Ordinary WSLS starts C, repeats its own action after payoff 3 or 5, and switches after 0 or 1. Alternator starts C and alternates. Suspicious TFT starts D then copies the last action. TFT for two tats starts with two cooperations and defects only after two consecutive opponent defections. Hard TFT starts C and defects if either of the last two available opponent actions was D. Both decisions use histories before the current round.\n',
        'Each opponent receives all 100 seeds and equal aggregate weight because it shares horizons with the other opponents '
        'in its panel. Score is total own payoff divided by total rounds, not the mean of match means. '
        'The fresh ranges are disjoint from historical training seeds 11,23,47,89,131 and holdout seeds 211,307,401,503,601. '
        'Random streams retain the original train/holdout label and SHA-256 derivation from split/opponent/seed. '
        'All policies face identical manifests. Differences are computed separately on each complete panel and opponent. '
        'No panels are pooled into an objective. These public development opponents are not a new confirmatory population.\n',
        'The 40 E1 and 18 E1-R original live-valid occurrences were checked against canonical source bytes, live correctness '
        'and metrics, and archived database membership in the preserved audits. AST deduplication retains all 58 origins and '
        'source hashes, including programs from incomplete E1 A303 and E1-R B101. '
        'Three rejected sources and two originally unevaluated generated sources are excluded without repair; all missing, '
        'blocked and unattempted slots are listed in the catalogue. Sources in incomplete runs do not acquire historical primary '
        'outcomes merely by being evaluated in E2.\n',
        f"The freeze was committed and remotely verified before evaluation at `{runtime['freeze_commit']}`. "
        'Recovery found a clean repository and no E2 process, freeze, checkpoint or result locally or on GitHub at fd19af5; '
        'the milestone was unstarted in available evidence. No prior E2 runtime could be observed; no running experiment was terminated. '
        'The new runtime ledger was created once. Full protocol: [PROTOCOL.md](protocol/PROTOCOL.md); '
        'exact source and input hashes: [freeze.json](protocol/freeze.json).\n',
        '## All generated strategies and ranks\n',
        'All six ASTs above TFT on original training remain above it on fresh training: two grim implementations and four period-detector variants (period ranges 2, 2–3, 2–4 and 2–6). None exceeds grim. The leading twelve training ranks are unchanged; seven lower-ranked ASTs move. The 32-round periodic-defection variant drops from rank 28 to 32. No AST changes which side of TFT it occupies on training.\n',
        'On development, only three generated ASTs exceed TFT: the two grim implementations and E1 A101 slot 9. The latter cooperates for two rounds and then copies the opponent’s previous action. Its fresh score is 2.630670 (+0.081517 vs TFT), rank 3 of 35. Against suspicious TFT the two initial cooperations restore mutual cooperation instead of TFT’s alternation: +0.493784 per opponent round. Small losses against the two random opponents slightly reduce that gain; other development opponents tie TFT. This is a new exploratory E2 development observation: that source had no archived original development score and was not the historical winner. Its training score remains slightly below TFT.\n',
        ptable(generated),
        'The accompanying [CATALOGUE.md](CATALOGUE.md) contains every original source/origin, decision-rule descriptions, '
        'original and fresh ranks, per-opponent scores/cooperation/differences, exclusions and all comparator results. '
        'Five ASTs, representing 25 original occurrences, implement exact TFT by direct source logic; two ASTs implement grim, two implement ordinary WSLS, and two implement TFT for two tats. These source-based identifications are distinct from finite encounter equality. E1 B202 slot 5 instead adds defections at positive history lengths divisible by 32 (rounds 33, 65, …) and remains a distinct periodic variant despite its historical finite-probe false positive. '
        'summary.json also retains complete integer totals and rank populations. Training ranks compare the 35 ASTs. '
        'A fresh rank is unavailable if any member of its ranking population lacks a complete score. Original development ranks use only ASTs with an archived score; fresh ranks compare all 35 and additionally '
        'the same historical-availability subset. These are exploratory screening ranks, not evolutionary replicates or reselections.\n',
        rank_table([grim, period]),
        'Among all 32 memory-one comparators, `00111` ranks first on both panels (2.660859 training / 2.655990 development), matching grim on its reachable histories. TFT `00101` ranks second on training and third on development. Development runner-up `01001` scores 2.564491. The complete comparator table and family ranks are in the catalogue and summary. This is exhaustive only within the fixed five-bit memory-one class, not a global optimality proof.\n',
        '## Focal mechanism: E1-R A101 selected slot 4, grim\n',
        'Complete original source:\n```python\n' + (ROOT / grim['source']).read_text().rstrip() + '\n```\n',
        'The first condition cooperates when the history is empty or contains no defection. Once an opponent 1 is recorded, '
        'its count never returns to zero, so the policy defects forever. This establishes grim behavior by source logic '
        'on legal histories; equality with the reference in scored encounters is an additional finite check. '
        'Its own-history argument is unused. TFT instead copies the latest opponent action and can resume cooperation.\n',
        opponent_table(grim['id']),
        'The training advantage over TFT comes entirely from fair random: permanent retaliation extracts more when random '
        'later cooperates. Against training always-C, TFT, grim and WSLS both preserve mutual cooperation; against always-D '
        'both cooperate once and then defect. On development, grim exploits alternator and random opponents but loses heavily '
        'to suspicious TFT. Suspicious TFT defects first and then copies: TFT enters alternating exploitation, whereas grim’s '
        'permanent retaliation settles into mutual defection after the opening. This tradeoff persists on fresh seeds.\n',
        '## Focal mechanism: E1 A202 selected slot 5, period detection\n',
        'Complete original source:\n```python\n' + (ROOT / period['source']).read_text().rstrip() + '\n```\n',
        'Read the conditional expression left to right. With n previous observations: E returns C when n=0; '
        'P2 returns D if n≥4 and the last two two-action blocks match with alternating actions; '
        'P3, P4, P5 and P6 return D if n≥2k and the last two k-action blocks match and contain both actions. '
        'The first true branch wins. If none applies, L copies the last opponent action. '
        'The rule detects only a repeated recent suffix, not an enduring periodic opponent, and does not remember a detection '
        'as persistent state. Its own-history argument is unused. All-C/all-D repeated suffixes are excluded by the mixed-action checks.\n',
        opponent_table(period['id']),
        'Against fair random, accidental repeated suffixes create extra defections and improve payoff by 0.218134 per opponent round over TFT; this alone supplies the panel advantage of 0.036356. '
        'Against alternator, the P2 branch exploits recurring cooperation (+0.491810 vs TFT). Development random_20 and random_80 gains are +0.080073 and +0.249177. '
        'The sole negative development component is suspicious TFT (−1.473565): starting from C/D alternation, the detector defects on round 5 where TFT would cooperate, then the responsive opponent copies defection and they settle into DD. '
        'Hard TFT and TFT for two tats stay at mutual cooperation. Thus the period detector’s development loss is concentrated in one interaction, rather than uniform across the panel. '
        'Neither focal policy exceeds grim on fresh training. These opponent differences have equal one-sixth panel weights.\n',
        '## Short traces from scored E2 encounters\n',
        'These six encounters and their first 16 rounds were predeclared. Every trace replays the entire scored encounter '
        'through environment.play and checks all totals against its durable main record; no second evaluation record is added. '
        'traces.json retains full branch tests, histories and outcomes. In the tables C=0, D=1; '
        'E is the initial branch, G the grim condition, P2–P6 the mixed suffix tests, and L the final copy branch.\n']
    for t in traces:
        spec = next(s for s in specs if s['id'] == t['policy_id'])
        e = t['encounter']
        report += [f"### {label(spec)} — {e['split']}/{e['opponent']}/{e['seed']}\n",
            f"Full scored match: {e['turns']} rounds, own payoff {t['full_match']['total_payoff']}, "
            f"payoff/round {t['full_match']['mean_payoff']:.6f}.\n"]
        rows = []
        for r in t['rows']:
            if spec['id'] == grim['id']:
                branch = 'G true → C' if r['branch_tests'][0]['result'] else 'G false → D'
            else:
                names = ['E', 'P2', 'P3', 'P4', 'P5', 'P6']
                branch = ', '.join(names[i] + (' T' if x['result'] else ' F') for i, x in enumerate(r['branch_tests']))
                if not any(x['result'] for x in r['branch_tests']): branch += ' → L'
            rows.append([r['round'], branch, 'CD'[r['action']], 'CD'[r['opponent_action']], r['payoff'], r['cumulative_payoff']])
        report += [table(['Round', 'Branch tests in order', 'Own', 'Opponent', 'Payoff', 'Cumulative'], rows),
            'Exact reproduction, from repository root (prints verified JSON and does not change the scored record):\n',
            f"```bash\npython3 analyze_e2.py --trace {t['policy_id']} --split {e['split']} --opponent {e['opponent']} --seed {e['seed']} --rounds 16\n```\n"]
    report += ['## Execution, coverage, failures and reproducibility\n',
        f"Main evaluation used one bounded worker at a time, at most 300 seconds per policy, under a cumulative 45-minute "
        'CLOCK_BOOTTIME deadline. Every start and result was fsynced; no match was retried. '
        f"Completion accounting is [completion.json](completion.json), start/deadline is [runtime.json](runtime.json), "
        'and worker launches, exits and logs are retained in workers/ and execution.jsonl. '
        'All 600 scheduled encounters in a panel must succeed for that panel to have a complete score. '
        'A policy failure would retain its exact pre-decision counterexample; infrastructure/unknown and absent matches '
        'remain explicit and suppress complete aggregates. [failures.json](failures.json) contains all observed failures.\n',
        'Eight focused pre-freeze unittest checks passed. Fourteen full historical policy/panel records (420 matches) '
        'replayed exactly before fresh evaluation. The zero-call preflight validated the seed score without a model or '
        'subscription-quota/connectivity call; system Python did not include optional Shinka, which E2 does not require. '
        'The full dependency-enabled suite first reproduced the previously documented sandbox stall while copying a mocked '
        'E1 seed. Only that test process was stopped after diagnosis, its log and fixture were preserved, and the suite was '
        'rerun with normal local process access. A first host rerun failed the unchanged child-death timing test; its isolated rerun and the next full suite passed. An analysis merge bug was caught and fixed by a new test before export. All failure logs remain preserved. These were local verification failures, separate from main E2 evaluation. '
        'The final test and independent export/trace verification outcomes are recorded in [setup/VERIFICATION.md](setup/VERIFICATION.md).\n',
        'Machine evidence: [inventory](protocol/inventory.json), [encounters](protocol/encounters.json), '
        '[configuration](protocol/config.json), [summary](summary.json), [per-match results](per_match.jsonl), '
        '[trace records](traces.json), [catalogue](CATALOGUE.md), [commands](COMMANDS.md). '
        'matches/*.jsonl are the original append-only event checkpoints; per_match.jsonl expands all scheduled cells '
        'and is checked against those records without reevaluating the main panel.\n',
        '```bash\n# Read-only verification of archived E2 artifacts\npython3 analyze_e2.py --verify\n'
        '# Focused frozen implementation tests\npython3 -m unittest discover -s tests -p test_e2.py -v\n'
        '# Full local suite, with pinned optional dependency\n.venv/bin/python -m unittest discover -s tests -v\n'
        '# Default zero-call preflight\npython3 run_evo.py --preflight\n```\n',
        'Exact preparation, pre-freeze checks, freeze/push, main execution and export commands are in COMMANDS.md. '
        'run_e2.py refuses closed execution, existing freezes and changed frozen inputs. Analysis output creation refuses '
        'overwrites. A fresh scientific replication needs a separate output protocol, not a reset of this ledger.\n',
        '## Limitations and one bounded follow-up\n',
        'This is descriptive transfer to fresh stochastic encounters with the same panels and stopping distribution. '
        'It supports no claim about other opponent populations, noisy actions, arbitrary horizons, universal optimality '
        'or knowledge-free invention. More encounter seeds are not independent evolutionary replicates. AST counts are '
        'syntactic counts, and equal scored behavior is not a universal equivalence proof. The public development panel '
        'has already informed analysis. E1 and E1-R remain closed and incomplete as designed; E2 does not complete their '
        'missing A/B outcomes or support a search-method effect. Historical selections and original files are preserved.\n',
        'One proposed follow-up, **not executed**: freeze a separate zero-call robustness protocol for these same two focal '
        'sources, TFT and E1 A101 slot 9, against the six training opponents on 20 new seeds, comparing ordinary play with one forced '
        'opponent-action error at round 10 when the independently sampled match reaches it (no horizon extension). '
        'That is 4 × 6 × 20 × 2 = 960 matches, a 10-minute cumulative cap, no evolution or reselection. '
        'Report matched payoff loss and whether mutual cooperation recovers. Grim’s permanent response and the observed '
        'suspicious-TFT loss, together with the two-initial-cooperation variant’s recovery from suspicious TFT, motivate testing response to a single disruption; current noiseless scores cannot answer it.\n']
    write_new(E2 / 'E2_REPORT.md', '\n'.join(report))
    print('Wrote E2_REPORT.md and CATALOGUE.md')


if __name__ == '__main__':
    main()
