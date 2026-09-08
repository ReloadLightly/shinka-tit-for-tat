# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    if len(opponent_history) < 3:
        return 0 if len(opponent_history) else 1
    return opponent_history[-1]
# EVOLVE-BLOCK-END
