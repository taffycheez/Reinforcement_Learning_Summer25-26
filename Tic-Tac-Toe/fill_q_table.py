"""This code uses dynamic programming to create and fill a q-table with possible moves and Q-scores for each possible state of tic-tac-toe."""
import time

start_time = time.perf_counter()

import list_possible_states
# Retrieving list of possible gameplay and won states from the previous code.
possible_states, terminal_states = list_possible_states.return_states()

# Categorising terminal states into crosses won (1), naughts won (-1), and drawn (0).
for i, state in enumerate(terminal_states):
    naughts, crosses = state
    if any((crosses & w) == w for w in list_possible_states.winning_positions):
        terminal_states[i] = (state, 1)
    elif any((naughts & w) == w for w in list_possible_states.winning_positions):
        terminal_states[i] = (state, -1)
    else:
        terminal_states[i] = (state, 0)

# 65.3% of terminal states are won by x, 33.0% by o, and 1.7% are drawn. 

q_table = []
for naughts, crosses in possible_states:
    n_0 = naughts.bit_count()
    n_x = crosses.bit_count()
    if n_0 == n_x: # Crosses' turn
        for n in range(9):
            for t in terminal_states:
                if (naughts, crosses + 2**n) == t[0]: # Adding 2^n changes the nth digit (starting at 0, going from the right) to a 1
                    q_table.append([(naughts, crosses), n, t[1]])
    else: # Naughts' turn
        for n in range(9):
            for t in terminal_states:
                if (naughts, crosses + 2**n) == t[0]:
                    q_table.append([(naughts, crosses), n, t[1]])

end_time = time.perf_counter()

print(end_time - start_time)

print(q_table)

