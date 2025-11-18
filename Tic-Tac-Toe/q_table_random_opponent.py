"""This code uses dynamic programming to create and fill a q-table with possible moves and Q-scores for each possible state of tic-tac-toe, 
and for a random opponent."""

# for random opponent need to average over moves_and_qs list instead of taking max. 

import list_possible_states
# Retrieving list of possible gameplay and won states from the previous code.
possible_states = list_possible_states.return_states() 

q_table = {}
higher_states = {}
higher_states[9] = possible_states[9] 

depth = 8 # initialise to states one move away from filling the board
while depth >= 0:   
    nonterminal_states = [state for state, q in possible_states[depth] if q is None]
    for state, q in possible_states[depth]:
        if q is None: # if nonterminal state
            naughts, crosses = state
            # naughts XOR crosses has 0 wherever there are two 0s in a position (free position) and 1 wherever a position is full
            free_positions = format(naughts ^ crosses, '09b')
            # so available moves are wherever a digit of the above result is 0
            available_moves = [8-i for i, bit in enumerate(free_positions) if bit == '0']
            if depth % 2 == 0: # crosses' turn
                moves_and_qs = []
                for n in available_moves:
                    for state, q in higher_states[depth + 1]: # can only lead to a state of depth one higher
                        if (naughts, crosses + 2**n) == state:
                            moves_and_qs.append((n,q))
                            break # each state-move combo can only lead to one resulting state
                    if q == 1: # if win for crosses
                        break
                q_table[(naughts, crosses)] = moves_and_qs
                max_q = max(q for n, q in moves_and_qs)
                higher_states.setdefault(depth, []).append(((naughts, crosses), max_q))
            else: # naughts' turn
                moves_and_qs = []
                for n in available_moves:
                    for state, q in higher_states[depth + 1]:
                        if (naughts + 2**n, crosses) == state:
                            moves_and_qs.append((n,q))
                            break
                    if q == -1: # if win for naughts
                        break
                q_table[(naughts, crosses)] = moves_and_qs
                min_q = min(q for n, q in moves_and_qs)
                higher_states.setdefault(depth, []).append(((naughts, crosses), min_q))
        else: # terminal state
            higher_states.setdefault(depth, []).append((state, q))
    depth -= 1