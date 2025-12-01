import time

start = time.perf_counter()

import list_possible_states
# Retrieving list of possible gameplay and won states from the previous code.
possible_states, terminal_states = list_possible_states.return_states() 

for depth in range(0,9):
    for naughts, crosses in possible_states[depth]:
        available_moves = [i for i in range(9) if not (naughts | crosses) & (1 << i)]

end = time.perf_counter()

print(end - start)