"""This code creates a list all posittive valid states of tic-tac-toe as binary bitboard tuples."""

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
    # Determine whether there are any 'wins' (filled rows, columns, or diagonals) for naughts and for crosses
    x_wins = any((crosses & winning_pos) == winning_pos for winning_pos in winning_positions)
    o_wins = any((naughts & winning_pos) == winning_pos for winning_pos in winning_positions)
    # For a valid crosses win, number of crosses should = no. naughts + 1 
    if x_wins and n_x != n_0 + 1:
        return 0
    # If naughts won, no. of naughts should = no. of crosses
    if o_wins and n_0 != n_x:
        return 0
    # Remaining wins (and draws) must be valid
    if x_wins:
        return (1, n_0 + n_x) # x won
    if o_wins:
        return (-1, n_0 + n_x) # o won
    if n_0 + n_x == 9:
        return (0, n_0 + n_x) # draw
    # Cannot be a win so must be a valid game state. Return None to signify this as well as the depth of the game (no. of moves that have happened)
    return (None, n_0 + n_x)

def return_states():
    """Returns all possible valid winning and gameplay states of tic-tac-toe."""
    possible_states = {} # dict mapping depth/no. of moves to list of states as tuples of binary numbers
    state_value_dict = {} # dictionary mapping state to value (-1 for naughts wins, 1 for crosses wins, 0 for draw)
    # The greatest number that a naughts position can correspond to is 480 (111100000)
    # For a crosses position this is 496 (111110000)
    for naughts in range(0, 481):
        for crosses in range(0,497):
            result = valid_state(naughts, crosses)
            if result == 0:
                continue
            if result[0] == None:
                possible_states.setdefault(result[1], []).append((naughts, crosses))
            else:
                possible_states.setdefault(result[1], []).append((naughts, crosses))
                state_value_dict[(naughts, crosses)] = result[0]
    return possible_states, state_value_dict

possible_states, state_value_dict = return_states()

# 4536 valid non-winning states 
# 5478 valid states including winning states
# So 942 winning states
# 16 drawn states (?)

# Using basic counter variables we can determine that 65.3% of terminal states are won by x, 33.0% by o, and 1.7% are drawn.



