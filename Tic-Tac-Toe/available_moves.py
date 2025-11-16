import time

start = time.perf_counter()

import list_possible_states
# Retrieving list of possible gameplay and won states from the previous code.
possible_states, terminal_states = list_possible_states.return_states() 

for depth in range(0,9):
    for naughts, crosses in possible_states[depth]:
        free_positions = format(naughts ^ crosses, '09b')
        available_moves = [8-i for i, bit in enumerate(free_positions) if bit == '0']

end = time.perf_counter()

print(end - start)