"""This file implements a function that, q-table with bitboard representations of ."""

def bitboard_to_visual(bitboard):
    visual = list('_' for i in range(9)) # creating 'empty' list
    naughts, crosses = bitboard
    naughts, crosses = format(naughts, '09b'), format(crosses,'09b') # e.g. the binary number 0b011010000 becomes the string '011010000'
    for index, digit in enumerate(naughts):
        if digit == '1': # if naughts occupy this position
            visual[index] = 'o'
    for index, digit in enumerate(crosses):
        if digit == '1': # if crosses occupy this position
            visual[index] = 'x' 
    return ''.join(visual) # joining list to create a string and returning

# retrieving possible states and their values from the previous function
import q_table_optimal_opponent
q_table = q_table_optimal_opponent.create_q_table()
# counter variables
terminal = 0 
x_wins = 0
o_wins = 0
draws = 0
with open("q_table.txt", "w") as file:
    file.write("A move is represented by a number, which is the index (going from right to left, starting at 0) of the position to be occupied.\n")
    file.write("For example, Move: 0 indicates that the player occupied the bottom right square.\n")
    for state, move_q_list in q_table.items():
        file.write(f"[{bitboard_to_visual(state)}] ")
        if isinstance(move_q_list, int):
            file.write(f"Terminal q-value: {move_q_list};\n")
            terminal += 1
        else:
            for move, q in move_q_list:
                file.write(f"Move: {move}, Q-value: {q}; ")
                if q == 1:
                    x_wins += 1
                if q == -1:
                    o_wins += 1
                if q == 0:
                    draws += 1
            file.write("\n")
    # summary
    file.write(f"{x_wins} moves led to crosses winning\n")
    file.write(f"{o_wins} moves led to naughts winning\n")
    file.write(f"{draws} moves led to a draw\n")
    file.write(f"{terminal} states were terminal and {x_wins + o_wins + draws} were gameplay states\n")
    file.write(f"There were a total of {terminal + x_wins + o_wins + draws} states")

import q_table_random_opponent
q_table = q_table_random_opponent.create_q_table()
# counter variables
terminal = 0 
x_wins = 0
o_wins = 0
draws = 0
with open("random_q_table.txt", "w") as file:
    file.write("A move is represented by a number, which is the index (going from right to left, starting at 0) of the position to be occupied.\n")
    file.write("For example, Move: 0 indicates that the player occupied the bottom right square.\n")
    for state, move_q_list in q_table.items():
        file.write(f"[{bitboard_to_visual(state)}] ")
        if isinstance(move_q_list, int):
            file.write(f"Terminal q-value: {move_q_list};\n")
            terminal += 1
        else:
            for move, q in move_q_list:
                file.write(f"Move: {move}, Q-value: {q:.2f}; ")
                if q >= 0.5:
                    x_wins += 1
                if q <= -0.5:
                    o_wins += 1
                else:
                    draws += 1
            file.write("\n")
    # summary
    file.write(f"{x_wins} moves were closer to crosses winning\n")
    file.write(f"{o_wins} moves were closer to naughts winning\n")
    file.write(f"{draws} moves were closer to a draw than to either side winning\n")
    file.write(f"{terminal} states were terminal and {x_wins + o_wins + draws} were gameplay states\n")
    file.write(f"There were a total of {terminal + x_wins + o_wins + draws} states")