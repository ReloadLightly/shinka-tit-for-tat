# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if not opponent_history else opponent_history[-1]
# EVOLVE-BLOCK-END
