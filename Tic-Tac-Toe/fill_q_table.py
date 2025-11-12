"""This code uses dynamic programming to create and fill a q-table with possible moves and Q-scores for each possible state of tic-tac-toe."""
import list_possible_states
possible_states = list_possible_states.return_states()
winning_states = list_possible_states.return_winning()
q_table = []
for state in possible_states:
    
    q_table.append([state, move, q])