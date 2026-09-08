# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    if len(opponent_history) < 3:
        return 0
    if opponent_history.count(1) == 0:
        return 1
    if opponent_history[-3:] == (1, 1, 1):
        return 1
    return 0
# EVOLVE-BLOCK-END
