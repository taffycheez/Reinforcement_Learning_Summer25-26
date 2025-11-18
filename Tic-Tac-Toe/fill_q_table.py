"""This code uses dynamic programming to create and fill a q-table with possible moves and Q-scores for each possible state of tic-tac-toe, and for an optimal 
opponent."""

import time

start_time = time.perf_counter()

import list_possible_states
# Retrieving list of possible gameplay and won states from the previous code.
possible_states = list_possible_states.return_states() 

q_table = {}
higher_states = {}
higher_states[9] = possible_states[9].copy()
value_at_depth = {}
value_at_depth[9] = {state: val for state, val in higher_states[9]}

for depth in range(8, -1, -1): # initialise to states one move away from filling the board; increment down to 0 (starting state)
    next_value = value_at_depth[depth + 1]

    higher_states[depth] = []
    value_at_depth[depth] = {}

    for state, q in possible_states[depth]:
        if q is not None:
            higher_states[depth].append((state, q))
            value_at_depth[depth][state] = q
            continue
        # nonterminal state
        naughts, crosses = state
        # naughts XOR crosses has 0 wherever there are two 0s in a position (free position) and 1 wherever a position is full
        free_positions = format(naughts ^ crosses, '09b')
        # so available moves are wherever a digit of the above result is 0
        available_moves = [8-i for i, bit in enumerate(free_positions) if bit == '0']

        moves_and_qs = []
        
        if depth % 2 == 0: # crosses' turn               
            for n in available_moves:
                next_state = (naughts, crosses + 2**n)
                if next_state in next_value:
                    q = next_value[next_state]
                    moves_and_qs.append((n,q))
                if q == 1: # if win for crosses
                    break
            
            best_q = max(q for n, q in moves_and_qs)
        else: # naughts' turn
            for n in available_moves:
                for state, q in higher_states[depth + 1]:
                    if (naughts + 2**n, crosses) == state:
                        moves_and_qs.append((n,q))
                        break
                if q == -1: # if win for naughts
                    break
            best_q = min(q for n, q in moves_and_qs)
        q_table[(naughts, crosses)] = moves_and_qs
        higher_states[depth].append(((naughts, crosses), best_q))
        value_at_depth[depth][(naughts, crosses)] = best_q

len_q = 0

x_win = 0
o_win = 0
draw = 0

for k, v in q_table.items():
    for n, q in v:
        if q == 1:
            x_win += 1
        elif q == -1:
            o_win += 1
        else:
            draw += 1
    len_q += len(v)
print(len_q)
print(x_win, o_win, draw)

print(q_table[(0,0)])
end_time = time.perf_counter()

print(end_time - start_time)

