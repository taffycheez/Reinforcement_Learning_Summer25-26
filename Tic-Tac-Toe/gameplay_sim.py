"""Code to simulate tic-tac-toe gameplay for:
- random opponent against random agent
- random opponent against optimal agent 
- optimal opponent against optimal agent
- optimal opponent against random agent"""

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

import random 
import q_learning
q_table_vs_optimal = q_learning.play_tic_tac_toe(10000, 'learning', 'optimal', 5, 0.01)
q_table_vs_random = q_learning.play_tic_tac_toe(10000, 'learning', 'random', 5, 0.01)
# retrieving list of possible states
import list_possible_states
POSSIBLE_STATES, TERMINAL_STATES = list_possible_states.return_states() 

# creating a dictionary of possible moves at each game state
MOVES_AT_STATE = {}
for statelist in POSSIBLE_STATES.values():
    for state in statelist:
        if state not in TERMINAL_STATES: # nonterminal state
            naughts, crosses = state
            moves = [i for i in range(9) if not (naughts | crosses) & (1 << i)]
            MOVES_AT_STATE[state] = moves

# retrieving q-table
import q_table_optimal_opponent
q_table = q_table_optimal_opponent.create_q_table()

def make_a_turn(state, x_strategy, o_strategy):
    """"""
    naughts, crosses = state
    # decide whose turn it is
    n_0 = naughts.bit_count()
    n_x = crosses.bit_count()
    if n_0 == n_x: # crosses' turn
        a = choose_action(state, x_strategy)
        new_state = (naughts, crosses + 2**a)
    else: # naughts' turn
        a = choose_action(state, o_strategy)
        new_state = (naughts + 2**a, crosses)

    # return the new state s'
    return new_state

def choose_action(state, strategy):
    """"""
    # random strategy chooses with equal probabilities so Pr(a) = 1/N_a 
    if strategy == 'random':
        move = random.choice(q_table[state])[0]
    # optimal strategy chooses the value of a which maximises q
    if strategy == 'optimal':
        move = max(q_table[state], key=lambda x: x[1])[0]
    if strategy == 'learned_against_optimal':
        move = max(q_table_vs_optimal[state], key=lambda x: q_table_vs_optimal[state][x])
    if strategy == 'learned_against_random':
        move = max(q_table_vs_random[state], key=lambda x: q_table_vs_optimal[state][x])
    return move

def play_tic_tac_toe(games, x_strategy, o_strategy):
    """Function which plays the given number of games using the given strategy (random or optimal) for both agent and opponent."""
    gamecount = 0 # initialise game counter
    gamelist = [] # initialise game list which will contain a list of states and an integer result
    while gamecount < games:
        # initialise the game state
        gamestate = (0, 0)
        moves = []
        depth = 0
        while (depth < 9) and (gamestate not in TERMINAL_STATES): # continue playing until board is filled or a terminal state is achieved
            gamestate = make_a_turn(gamestate, x_strategy, o_strategy)
            moves.append(gamestate)
            depth += 1
        # record result of game
        moves.append(q_table[gamestate])
        gamelist.append(moves)
        # update game counter
        gamecount += 1

    # return list of states, actions, resulting states, and immediate rewards [s, a, s', r]
    return gamelist

gamelist = play_tic_tac_toe(100, 'learned_against_optimal', 'optimal')
x_wins = 0
o_wins = 0
draws = 0
for game in gamelist:
    if game[-1] == 1:
        x_wins += 1
    elif game[-1] == -1:
        o_wins += 1
    else:
        draws += 1
print(x_wins, o_wins, draws)