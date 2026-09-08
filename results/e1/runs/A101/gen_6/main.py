# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    if len(opponent_history) == 0:
        return 1
    elif len(opponent_history) == 1:
        return 0
    elif opponent_history[1] == 0:
        return 1
    else:
        return opponent_history[-1]
# EVOLVE-BLOCK-END
