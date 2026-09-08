# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) < 2 else opponent_history[-1]
# EVOLVE-BLOCK-END
