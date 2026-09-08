# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else 1 if len(opponent_history) >= 3 and opponent_history[-3:] == (1, 1, 1) else 0 if own_history[-1] == opponent_history[-1] else 1
# EVOLVE-BLOCK-END
