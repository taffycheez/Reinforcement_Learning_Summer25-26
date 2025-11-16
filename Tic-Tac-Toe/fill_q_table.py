"""This code uses dynamic programming to create and fill a q-table with possible moves and Q-scores for each possible state of tic-tac-toe, and for an optimal 
opponent."""

import time

start_time = time.perf_counter()

import list_possible_states
# Retrieving list of possible gameplay and won states from the previous code.
possible_states, terminal_states = list_possible_states.return_states() 

q_table = {}
higher_states = {}

for depth, value in terminal_states.items():
    higher_states[depth] = value

depth = 8 # initialise to states one move away from filling the board
while depth >= 0:
    for naughts, crosses in possible_states[depth]:
        # naughts XOR crosses has 0 wherever there are two 0s in a position (free position) and 1 wherever a position is full
        free_positions = format(naughts ^ crosses, '09b')
        # so available moves are wherever a digit of the above result is 0
        available_moves = [8-i for i, bit in enumerate(free_positions) if bit == '0']
        if depth % 2 == 0: # crosses' turn
            for n in available_moves:
                for state, q in higher_states[depth + 1]: # can only lead to a state of depth one higher
                    if (naughts, crosses + 2**n) == state:
                        q_table.setdefault((naughts, crosses), []).append((n, q))
                        higher_states.setdefault(depth, []).append(((naughts, crosses), q))
                        break
        else: # naughts' turn
            for n in available_moves:
                for state, q in higher_states[depth + 1]:
                    if (naughts + 2**n, crosses) == state:
                        q_table.setdefault((naughts, crosses), []).append((n, q))
                        higher_states.setdefault(depth, []).append(((naughts, crosses), q))
                        break
    depth -= 1

# make this more efficient? 
# calculate runtime (how many combinations it has to go through) and think how to reduce

# then do for random opponent :) 

print(len(q_table))

end_time = time.perf_counter()

print(end_time - start_time)

