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
    n_0 = naughts.bit_count()
    n_x = crosses.bit_count()
    if naughts & crosses != 0:
        return False
    # Number of crosses = number of naughts (or number of naughts + 1)
    # So if no_naughts > no_crosses or no_crosses > no_naughts + 1, invalid state
    if (n_0 > n_x) or (n_x > n_0 + 1):
        return False
    # Valid non-final position cannot have a row, column, or diagonal filled by one symbol
    # So naughts/crosses AND any winning state cannot return the winning state
    # I.e. naughts/crosses cannot have a winning position filled
    for winning_position in winning_positions:
        if ((naughts & winning_position == winning_position) and (n_0 != n_x)) or ((crosses & winning_position == winning_position) and (n_x != n_0 + 1)):
            return False
    return True

def return_states():
    """Returns all possible valid states of tic-tac-toe."""
    possible_states = []
    # The greatest number that a naughts position can correspond to is 480 (111100000)
    # For a crosses position this is 496 (111110000)
    for naughts in range(0, 481):
        for crosses in range(0,497):
            if valid_state(naughts, crosses):
                possible_states.append((naughts, crosses))
    return possible_states

end_time = time.perf_counter()

print(end_time - start_time)

# 4536 valid non-winning states 
# 5478 valid states including winning states



