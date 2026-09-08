# System Instructions

Improve the Python function policy(own_history, opponent_history) to maximize its own average payoff in a repeated two-action simultaneous game. Each argument is the tuple of that player's previous actions in this match; both are empty initially. Return the integer 0 or 1, never a Boolean. The payoff to you is 3 for (0,0), 0 for (0,1), 5 for (1,0), and 1 for (1,1). The second entry is the other player's action. The other player has the transposed payoff table. A match independently ends after each round with probability 0.00346. You cannot see the ending time, opponent identity, seed, or current opponent action. There is no execution noise. Fitness is your total payoff divided by total rounds across a fixed heterogeneous opponent panel with several independently seeded matches. Each opponent receives the same set of match lengths. Only average payoff is returned as feedback.

Edit only the EVOLVE-BLOCK. The candidate is a deliberately small executable Python subset interpreted by the evaluator. Keep exactly one unannotated function with the specified signature. Its body may contain if/elif/else and return, with no assignments. Expressions may contain integer constants, histories, indexing and slices, len(history), sum(history), min(history), max(history), history.count(0) or history.count(1), integer +, -, %, comparisons, not/and/or, and conditional expressions. No imports, extra functions, loops, comprehensions, globals, random numbers, external calls, files, or state outside the two histories. Handle empty history and do not call min/max on an empty sequence. At most 16000 source bytes and 400 AST nodes. This subset allows dependence on the entire past, not just the previous round. Maximize payoff; no other criterion contributes to fitness.

Use only this task, the supplied programs, and training feedback. Do not read local files or search for additional experiment information. Return the requested proposal as text.

Rewrite the program to improve its performance on the specified metrics.
Provide the complete new program code.
You MUST respond using a short summary name, description and the full code:

<NAME>
A shortened name summarizing the code you are proposing. Lowercase, no spaces, underscores allowed.
</NAME>

<DESCRIPTION>
A description and argumentation process of the code you are proposing.
</DESCRIPTION>

<CODE>
```{language}
# The new rewritten program here.
```
</CODE>

* Keep the markers "EVOLVE-BLOCK-START" and "EVOLVE-BLOCK-END" in the code. Do not change the code outside of these markers.
* Make sure your rewritten program maintains the same inputs and outputs as the original program, but with improved internal implementation.
* Make sure the file still runs after your changes.
* Use the <NAME>, <DESCRIPTION>, and <CODE> delimiters to structure your response. It will be parsed afterwards.

# Previous Messages

[]

# User Request

Here are the performance metrics of a set of previously implemented programs:

# Prior programs

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 1
# EVOLVE-BLOCK-END

```

Performance metrics:
Combined score to maximize: 2.33
mean_payoff: 2.33


# Current program

Here is the current program we are trying to improve (you will need to propose a new program with the same inputs and outputs as the original program, but with improved internal implementation):

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0
# EVOLVE-BLOCK-END

```

Here are the performance metrics of the program:

Combined score to maximize: 2.24
mean_payoff: 2.24


# Task

Rewrite the program to improve its performance on the specified metrics.
Provide the complete new program code.

IMPORTANT: Make sure your rewritten program maintains the same inputs and outputs as the original program, but with improved internal implementation.
