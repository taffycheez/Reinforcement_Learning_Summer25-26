import random
import math

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
q_table_optimal = q_table_optimal_opponent.create_q_table()

# initialising resultant q-table
q_table = {}
for state, moves in MOVES_AT_STATE:
    q_table[state] = [(move, 0) for move in moves]

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
    # return the new state s'
    return new_state

def choose_action(state, strategy, tau):
    """"""
    # random strategy chooses with equal probabilities so Pr(a) = 1/N_a 
    if strategy == 'random':
        move = random.choice(MOVES_AT_STATE[state])
    # optimal strategy has Pr(a) = 1 for argmax Q[s,]
    if strategy == 'optimal':
        move = max(q_table_optimal[state], key=lambda x: x[1])[0]
    # if it is the agent
    if strategy == 'learning':
        # Boltzmann function
        weights = []
        weight_denominator = sum([math.exp(q_table[a]/tau) for a in MOVES_AT_STATE[state]])
        for a in MOVES_AT_STATE[state]:
            weight = math.exp(q_table[[state]]/tau) / weight_denominator
            weights.append(weight)
        move = random.choices(MOVES_AT_STATE[state], weights = weights, k = 1)[0] # choose a with Pr(a)
    return move

def play_tic_tac_toe(games, x_strategy, o_strategy, tau, alpha):
    """Function which plays the given number of games using the given strategy (random or optimal) for both agent and opponent."""
    gamecount = 0 # initialise game counter
    while gamecount < games:
        # initialise the game state
        gamestate = (0, 0)
        depth = 0
        while depth < 9 and gamestate not in TERMINAL_STATES: # continue playing until board is filled or a terminal state is achieved
            gamestate = make_a_turn(gamestate, x_strategy, o_strategy, tau)

        # update game counter
        gamecount += 1

    # return list of states, actions, resulting states, and immediate rewards [s, a, s', r]
    return q_table