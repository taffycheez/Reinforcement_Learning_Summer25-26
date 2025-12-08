"""This code uses dynamic programming to create and fill a q-table with possible moves and Q-scores for each possible state of tic-tac-toe, and for an optimal 
opponent."""

import time

start_time = time.perf_counter()

def create_q_table(): 
    import list_possible_states
    # Retrieving list of possible gameplay and won states from the previous code.
    possible_states, state_value_dict = list_possible_states.return_states() 

    q_table = state_value_dict.copy()

    for depth in range(8, -1, -1): # initialise to states one move away from filling the board; increment down to 0 (starting state)
        for state in possible_states[depth]:
            if state not in state_value_dict: # nonterminal state
                naughts, crosses = state
                # naughts OR crosses has 0 wherever there are two 0s in a position (free position) and 1 wherever a position is full
                # 1 << i has the ith digit, starting at 0, being a 1 (since 1 is just 0b1, 1 << 3 for example is 0b1000) 
                # so comparing these two results using the & operator (which gives 1 iff both values are 1) gives a number which has 1
                # if the position is occupied and 0 if it is not; so we take those values of i for which the result is 0
                available_moves = [i for i in range(9) if not (naughts | crosses) & (1 << i)]

                moves_and_qs = [] # to keep track of the move which leads to the optimal outcome

                if depth % 2 == 0: # crosses' turn
                    for n in available_moves: # going through possible moves
                        next_state = (naughts, crosses + 2**n) # adding 2^n changes the nth position (starting from 0, going right to left) to a 1, if it is 0
                        if next_state in state_value_dict:
                            q = state_value_dict[next_state]
                            moves_and_qs.append((n, q))
                    best_q = max(q for n, q in moves_and_qs)
                
                else: # naughts' turn
                    for n in available_moves:
                        next_state = (naughts + 2**n, crosses)
                        if next_state in state_value_dict:
                            q = state_value_dict[next_state]
                            moves_and_qs.append((n, q))
                    best_q = min(q for n, q in moves_and_qs)
                
                q_table[(naughts, crosses)] = moves_and_qs # updating q-table
                state_value_dict[state] = best_q # this is q-value if the player moves optimally. it will be used in future iterations
    
    return q_table

q_table = create_q_table()

len_q = 0

x_win = 0
o_win = 0
draw = 0

for move_q_list in q_table.values():
    if isinstance(move_q_list, int):
        if move_q_list == 1:
            x_win += 1
        else:
            draw += 1 
        len_q += 1
        continue
    for move, q in move_q_list:
        if q == 1:
            x_win += 1
        elif q == -1:
            o_win += 1
        else:
            draw += 1
    len_q += len(move_q_list)

end_time = time.perf_counter()



