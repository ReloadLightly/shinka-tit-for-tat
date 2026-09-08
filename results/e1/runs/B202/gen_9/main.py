# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 1 if len(opponent_history) == 0 or opponent_history.count(1) == 0 else (0 if opponent_history[-1] == 1 and opponent_history.count(1) == 1 else opponent_history[-1])
# EVOLVE-BLOCK-END
