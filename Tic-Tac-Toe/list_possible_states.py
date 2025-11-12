"""This code creates a list all posittive valid states of tic-tac-toe as binary bitboard tuples."""
import time

start_time = time.perf_counter()

winning_positions = [0b000000111, # row 0
                  0b000111000, # row 1
                  0b111000000, # row 2
                  0b100100100, # column 0
                  0b010010010, # column 1
                  0b001001001, # column 2
                  0b100010001, # diagonal \
                  0b001010100 # diagonal /
]

def valid_state(naughts, crosses):
    """Checks whether the given tic-tac-toe bitboard represents a valid state of the game."""
    # Each square must be occupied by only one piece
    # So naughts AND crosses must return 0
    if naughts & crosses != 0:
        return 0
    # Number of crosses = number of naughts (or number of naughts + 1)
    # So if no_naughts > no_crosses or no_crosses > no_naughts + 1, invalid state
    n_0 = naughts.bit_count()
    n_x = crosses.bit_count()
    if (n_0 > n_x) or (n_x > n_0 + 1):
        return 0
    # Count number of 'wins' (filled rows, columns, or diagonals) for naughts and for crosses
    x_wins = any((crosses & winning_pos) == winning_pos for winning_pos in winning_positions)
    o_wins = any((naughts & winning_pos) == winning_pos for winning_pos in winning_positions)
    # For a valid crosses win, number of crosses should = no. naughts + 1 
    if x_wins and n_x != n_0 + 1:
        return 0
    # If naughts won, no. of naughts should = no. of crosses
    if o_wins and n_0 != n_x:
        return 0
    # Remaining wins must be valid
    if x_wins or o_wins:
        return 2  
    # Cannot be a win so must be a valid game state
    return 1

def return_states():
    """Returns all possible valid winning and gameplay states of tic-tac-toe."""
    gameplay_states = []
    winning_states = []
    # The greatest number that a naughts position can correspond to is 480 (111100000)
    # For a crosses position this is 496 (111110000)
    for naughts in range(0, 481):
        for crosses in range(0,497):
            result = valid_state(naughts, crosses)
            if result == 1:
                gameplay_states.append((naughts, crosses))
            elif result == 2:
                winning_states.append((naughts, crosses))
    return (gameplay_states, winning_states)

gameplay_states, winning_states = return_states()
print(len(gameplay_states))
print(len(winning_states))

end_time = time.perf_counter()

print(end_time - start_time)

# 4536 valid non-winning states 
# 5478 valid states including winning states
# So 942 winning states



