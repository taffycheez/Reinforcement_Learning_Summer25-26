"""This code uses dynamic programming to create and fill a q-table with possible moves and Q-scores for each possible state of tic-tac-toe, and for an optimal opponent."""
import time

start_time = time.perf_counter()

import list_possible_states
# Retrieving list of possible gameplay and won states from the previous code.
possible_states, terminal_states = list_possible_states.return_states() 

q_table = {}

depth = 8 # initialise to states one move away from filling the board
while depth >= 0:
    higher_states = q_table.copy()
    for naughts, crosses in possible_states[depth]:
        # naughts XOR crosses has 0 wherever there are two 0s in a position (free position) and 1 wherever a position is full
        free_positions = format(naughts ^ crosses, '09b')
        # so available moves are wherever a digit of the above result is 0
        available_moves = [8-i for i, bit in enumerate(free_positions) if bit == '0']
        if depth % 2 == 0: # crosses' turn
            for n in available_moves:
                found = False # each state-move combination can only correspond to one terminal state
                for state, q in terminal_states.items():
                    if (naughts, crosses + 2**n) == state: # Adding 2^n changes the nth digit (starting at 0, going from the right) from a 0 to a 1
                        q_table.setdefault((naughts, crosses), []).append((n, q))
                        found = True
                        break
                if not found:
                    for state, value in higher_states.items():
                        if (naughts, crosses + 2**n) == state:
                            q_table.setdefault((naughts, crosses), []).append((n, value[0][1]))
                            break

        else: # naughts' turn
            for n in available_moves:
                found = False
                for state, q in terminal_states.items():
                    if (naughts + 2**n, crosses) == state:
                        q_table.setdefault((naughts, crosses), []).append((n, q))
                        found = True
                        break
                # break somehow as a move can only lead to one state?
                if not found:
                    for state, value in higher_states.items():
                        if (naughts + 2**n, crosses) == state:
                            q_table.setdefault((naughts, crosses), []).append((n, value[0][1]))
                            break
    depth -= 1

# make this more efficient? 
# calculate runtime (how many combinations it has to go through) and think how to reduce

# then do for random opponent :) 

print(len(q_table))

end_time = time.perf_counter()

print(end_time - start_time)

