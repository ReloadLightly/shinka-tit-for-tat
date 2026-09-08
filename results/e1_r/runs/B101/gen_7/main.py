# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if not opponent_history else (1 if opponent_history[-1] == 1 else 0)
# EVOLVE-BLOCK-END
