"""Fixed IPD world. Candidate has histories only; all decisions are simultaneous."""
import hashlib
import math
import random

PAYOFFS = {(0, 0): 3, (0, 1): 0, (1, 0): 5, (1, 1): 1}
STOP_PROBABILITY = 0.00346
TRAIN_OPPONENTS = ('always_cooperate', 'always_defect', 'random', 'tit_for_tat', 'grim', 'win_stay_lose_shift')
HOLDOUT_OPPONENTS = ('alternator', 'suspicious_tit_for_tat', 'tit_for_two_tats', 'hard_tit_for_tat', 'random_20', 'random_80')
TRAIN_SEEDS = (11, 23, 47, 89, 131)
HOLDOUT_SEEDS = (211, 307, 401, 503, 601)


def reference(name, own, other, rng):
    if name == 'always_cooperate': return 0
    if name == 'always_defect': return 1
    if name == 'random': return int(rng.random() >= 0.5)
    if name == 'random_20': return int(rng.random() >= 0.2)
    if name == 'random_80': return int(rng.random() >= 0.8)
    if name == 'tit_for_tat': return other[-1] if other else 0
    if name == 'grim': return int(1 in other)
    if name == 'win_stay_lose_shift':
        if not own:
            return 0
        return own[-1] if PAYOFFS[(own[-1], other[-1])] in (3, 5) else 1 - own[-1]
    if name == 'alternator': return len(own) % 2
    if name == 'suspicious_tit_for_tat': return other[-1] if other else 1
    if name == 'tit_for_two_tats': return int(len(other) >= 2 and other[-2:] == (1, 1))
    if name == 'hard_tit_for_tat': return int(1 in other[-2:])
    raise ValueError('Unknown reference policy: ' + name)


def reference_policy(name):
    if name.startswith('random'):
        raise ValueError('Stochastic reference needs match-specific RNG')
    return lambda own, other: reference(name, own, other, None)


def horizon(seed):
    # Geometric support 1,2,..., no deterministic cutoff. Drawn independently of play.
    u = random.Random(seed).random()
    return 1 + int(math.log1p(-u) / math.log1p(-STOP_PROBABILITY))


def play(candidate, opponent_name, turns, seed):
    if type(turns) is not int or turns < 1:
        raise ValueError('Positive integer turns required')
    rng = random.Random(seed)
    own, other = (), ()
    score = opponent_score = cooperations = 0
    for _ in range(turns):
        action = candidate(own, other)
        opponent_action = reference(opponent_name, other, own, rng)
        if type(action) is not int or action not in (0, 1):
            raise ValueError('Candidate returned invalid action')
        score += PAYOFFS[(action, opponent_action)]
        opponent_score += PAYOFFS[(opponent_action, action)]
        cooperations += action == 0
        own += (action,)
        other += (opponent_action,)
    return {'total_payoff': score, 'opponent_total_payoff': opponent_score, 'turns': turns,
            'cooperations': cooperations, 'mean_payoff': score / turns,
            'opponent_mean_payoff': opponent_score / turns}


def evaluate_policy(candidate, split='train'):
    if split not in ('train', 'holdout'):
        raise ValueError('split must be train or holdout')
    names, seeds = (TRAIN_OPPONENTS, TRAIN_SEEDS) if split == 'train' else (HOLDOUT_OPPONENTS, HOLDOUT_SEEDS)
    totals = {'total_payoff': 0, 'opponent_total_payoff': 0, 'turns': 0, 'cooperations': 0}
    rows = []
    for name in names:
        for seed in seeds:
            match_seed = int.from_bytes(hashlib.sha256(f'{split}/{name}/{seed}'.encode()).digest()[:8], 'big')
            result = play(candidate, name, horizon(seed), match_seed)
            rows.append({'opponent': name, 'seed': seed, **result})
            for key in totals:
                totals[key] += result[key]
    return {**totals, 'mean_payoff': totals['total_payoff'] / totals['turns'],
            'cooperation_rate': totals['cooperations'] / totals['turns'],
            'matches': len(rows), 'rows': rows}
