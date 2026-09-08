# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    if len(opponent_history) == 0:
        return 0
    if opponent_history.count(1) == 0:
        return 0 if len(opponent_history) < 3 else 1
    if opponent_history.count(1) == 1 and own_history.count(1) == 1 and opponent_history[-1] == 1:
        return 0
    return opponent_history[-1]
# EVOLVE-BLOCK-END
