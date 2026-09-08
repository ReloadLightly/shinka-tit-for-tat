# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else 0 if len(opponent_history) < 3 and opponent_history[-1] == 0 else 1 if len(opponent_history) < 3 else 1 - own_history[-1] if len(opponent_history) > 4 and opponent_history[-1] == own_history[-2] and opponent_history[-2] == own_history[-3] and opponent_history[-3] == own_history[-4] else 0 if len(opponent_history) == 4 and opponent_history.count(0) == 4 and own_history[-1] == 1 else 1 if len(opponent_history) > 2 and opponent_history.count(0) == len(opponent_history) else 0 if opponent_history[-1] == 0 else 1
# EVOLVE-BLOCK-END
