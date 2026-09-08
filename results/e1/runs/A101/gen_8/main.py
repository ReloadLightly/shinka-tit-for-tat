# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) < 2 else (1 if opponent_history[-1] == 1 and opponent_history[-2] == 1 else 0)
# EVOLVE-BLOCK-END
