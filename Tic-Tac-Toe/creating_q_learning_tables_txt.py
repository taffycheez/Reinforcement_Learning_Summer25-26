import q_learning

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

q_table_vs_random = q_learning.play_tic_tac_toe(1000, 'learning', 'random', 100, 0.5)
q_table_vs_optimal = q_learning.play_tic_tac_toe(10000, 'learning', 'optimal', 100, 0.5)
q_table_both_learning = q_learning.play_tic_tac_toe(1000, 'learning', 'learning', 100, 0.5)

with open("q_learning_table_vs_random.txt", "w") as file:
    file.write("A move is represented by a number, which is the index (going from right to left, starting at 0) of the position to be occupied.\n")
    file.write("For example, Move: 0 indicates that the player occupied the bottom right square.\n")
    for state, move_q_dict in q_table_vs_random.items():
        file.write(f"[{bitboard_to_visual(state)}] ")
        for move, q in move_q_dict.items():
            file.write(f"Move: {move}, q-value: {q}; ")
        file.write("\n")

with open("q_learning_table_vs_optimal.txt", "w") as file:
    file.write("A move is represented by a number, which is the index (going from right to left, starting at 0) of the position to be occupied.\n")
    file.write("For example, Move: 0 indicates that the player occupied the bottom right square.\n")
    for state, move_q_dict in q_table_vs_optimal.items():
        file.write(f"[{bitboard_to_visual(state)}] ")
        for move, q in move_q_dict.items():
            file.write(f"Move: {move}, q-value: {q}; ")
        file.write("\n")

with open("q_learning_table_both_learning.txt", "w") as file:
    file.write("A move is represented by a number, which is the index (going from right to left, starting at 0) of the position to be occupied.\n")
    file.write("For example, Move: 0 indicates that the player occupied the bottom right square.\n")
    for state, move_q_dict in q_table_both_learning.items():
        file.write(f"[{bitboard_to_visual(state)}] ")
        for move, q in move_q_dict.items():
            file.write(f"Move: {move}, q-value: {q}; ")
        file.write("\n")