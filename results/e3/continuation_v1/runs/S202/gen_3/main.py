# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if opponent_history.count(1) < 2 else 1
# EVOLVE-BLOCK-END
