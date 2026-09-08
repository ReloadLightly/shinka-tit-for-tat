# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    if len(opponent_history) == 0:
        return 0
    elif len(opponent_history) == 1:
        return 1
    elif opponent_history[0] == 0 and opponent_history[1] == 0:
        return 0 if opponent_history.count(1) == 1 else 1
    else:
        return 1
# EVOLVE-BLOCK-END
