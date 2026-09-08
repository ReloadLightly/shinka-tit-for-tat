# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else (0 if opponent_history[-1] == 1 else (1 if (len(opponent_history) % 31 == 0 and opponent_history.count(1) == 0) or (own_history.count(1) > 0 and opponent_history.count(1) == 0) else 0))
# EVOLVE-BLOCK-END
