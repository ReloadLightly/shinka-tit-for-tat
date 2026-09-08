# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 1 if len(opponent_history) == 0 else (0 if opponent_history[-1] == 0 or (len(opponent_history) > 1 and opponent_history[-2] == 0) else 1)
# EVOLVE-BLOCK-END
