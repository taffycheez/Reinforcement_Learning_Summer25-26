"""This file implements a function that, given a bitboard representation of a game of tic-tac-toe, converts it to a visual representation using a matrix
of naughts and crosses."""

def bitboard_to_visual(bitboard):
    visual = list('_' for _ in range(9))
    naughts, crosses = bitboard
    naughts, crosses = format(naughts, '09b'), format(crosses,'09b')
    for index, digit in enumerate(naughts):
        if digit == '1':
            visual[index] = 'o'
    for index, digit in enumerate(crosses):
        if digit == '1':
            visual[index] = 'x'
    for i, char in enumerate(visual):
       if i == 2 or i == 5:
          print(f"{char} ")
       else:
           print(f"{char} ", end="")

bitboard_to_visual((0b010100001,0b100011000))