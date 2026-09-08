# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) < 4 else 1 if opponent_history.count(1) == 0 and len(opponent_history) % 9 == 0 else 0 if opponent_history[-1] == 0 else 0 if own_history[-1] == 1 and opponent_history[-2] == 1 else 1
# EVOLVE-BLOCK-END
