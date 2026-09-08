# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    if len(opponent_history) < 4:
        return 0
    elif len(opponent_history) == 4:
        return 1
    elif len(opponent_history) == 5:
        return 1 if opponent_history[4] == 0 else 0
    elif opponent_history[4] == 0:
        return 1
    else:
        return opponent_history[-1]
# EVOLVE-BLOCK-END
