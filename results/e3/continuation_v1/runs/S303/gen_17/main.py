# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 1 if len(opponent_history) == 8 and opponent_history.count(1) == 0 else (1 if len(opponent_history) > 8 and opponent_history.count(1) == 0 else 0)
# EVOLVE-BLOCK-END
