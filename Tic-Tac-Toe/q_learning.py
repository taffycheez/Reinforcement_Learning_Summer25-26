import random
import math

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

# retrieving list of possible states
import list_possible_states
POSSIBLE_STATES, TERMINAL_STATES = list_possible_states.return_states() 
# POSSIBLE_STATES is a dictionary mapping a depth (no. of moves that have occured) to a list of states
# the states are tuples of binary numbers
# for example at depth 0 there is just (0,0); at depth 1 there is (0, 1), (0, 2), etc

# TERMINAL_STATES is a dictionary mapping a terminal state to its outcome (1 for crosses won, -1 for naughts won, 0 for draw)

# creating a dictionary of possible moves at each game state
MOVES_AT_STATE = {}
for statelist in POSSIBLE_STATES.values():
    for state in statelist:
        if state not in TERMINAL_STATES: # nonterminal state
            naughts, crosses = state
            moves = [i for i in range(9) if not (naughts | crosses) & (1 << i)]
            MOVES_AT_STATE[state] = moves

# retrieving optimal q-table
# this is a dictionary mapping a state to a list of tuples
# each tuple is a move and a q-value representing the eventual outcome given optimal play on both sides
import q_table_optimal_opponent
q_table_optimal = q_table_optimal_opponent.create_q_table()

# initialising resultant q-table
# decided to use a dictionary mapping state to a dictionary
# the 'inner' dictionary maps a move to an outcome
q_table = {}
for state, moves in MOVES_AT_STATE.items():
    q_table[state] = {move: 0 for move in moves}

# outermost function
def play_tic_tac_toe(games, x_strategy, o_strategy, tau, alpha):
    """Function which plays the given number of games using the given strategy (random or optimal) for both agent and opponent."""
    gamecount = 0 # initialise game counter
    while gamecount < games:
        # initialise the game state
        gamestate = (0, 0)
        while gamestate not in TERMINAL_STATES: # continsue playing until a terminal state is achieved
            old = gamestate # save the old gamestate
            gamestate, move, r = make_a_turn(gamestate, x_strategy, o_strategy, tau) # make a move
            
            if gamestate in TERMINAL_STATES: # if game has ended, reward is what was returned from make_a_turn
                reward = r
            else: # otherwise, reward is the best possible outcome from the next resulting state
                # (it should be r + max q_table[gamestate].values() but since r is 0 for non-terminal states i left it out)
                if o_strategy == 'optimal':
                    reward = min(q for m, q in q_table_optimal[gamestate])
                else:
                    reward = max(q_table[gamestate].values())
            q_table[old][move] = (1-alpha) * q_table[old][move] + alpha * reward
            
            if gamestate not in TERMINAL_STATES:
                gamestate, _, _  = make_a_turn(gamestate, x_strategy, o_strategy, tau)
            # print(bitboard_to_visual(old), bitboard_to_visual(gamestate), r, q_table[old][move])
        # update game counter
        gamecount += 1
    # return q-table
    return q_table

# 2nd layer of function
def make_a_turn(state, x_strategy, o_strategy, tau):
    """"""
    naughts, crosses = state
    # decide whose turn it is
    n_0 = naughts.bit_count()
    n_x = crosses.bit_count()
    if n_0 == n_x: # crosses' turn
        a = choose_action(state, x_strategy, tau)
        new_state = (naughts, crosses + 2**a)
    else: # naughts' turn
        a = choose_action(state, o_strategy, tau)
        new_state = (naughts + 2**a, crosses)
    if new_state in TERMINAL_STATES:
        r = TERMINAL_STATES[new_state]
    else:
        r = 0
    # return the new state s', move a, and immediate reward r
    return new_state, a, r

# 3rd layer of function
def choose_action(state, strategy, tau):    
    """"""
    # do this to figure out whose turn it is
    naughts, crosses = state
    n_0 = naughts.bit_count()
    n_x = crosses.bit_count()
    # random strategy chooses with equal probabilities so Pr(a) = 1/N_a 
    if strategy == 'random':
        move = random.choice(MOVES_AT_STATE[state])
    # optimal strategy has Pr(a) = 1 for argmax Q[s,]
    if strategy == 'optimal':
        if n_0 == n_x: # crosses' turn
            # this returns the move with the max q-value (best outcome for crosses)
            move = max(q_table_optimal[state], key=lambda x: x[1])[0]
        else: # naughts' turn
            # this returns the move with the min q-value (best outcome for naughts)
            move = min(q_table_optimal[state], key=lambda x: x[1])[0]
    # if it is the agent
    if strategy == 'learning':
        # Boltzmann function
        weights = []
        # precomputing sum for speed
        weight_denominator = sum([math.exp(q_table[state][a]/tau) for a in MOVES_AT_STATE[state]])
        for a in MOVES_AT_STATE[state]:
            weight = math.exp(q_table[state][a]/tau) / weight_denominator
            weights.append(weight)
        move = random.choices(MOVES_AT_STATE[state], weights = weights, k = 1)[0] # choose a with Pr(a)
    return move

table = play_tic_tac_toe(10000, 'learning', 'random', 5, 0.1)

print(table[(0,0)])

# for state, d in table.items():
#     for m, q in d.items():
#         if q != 0:
#             print(bitboard_to_visual(state), m, q)
