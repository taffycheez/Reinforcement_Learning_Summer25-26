"""Code to simulate tic-tac-toe gameplay for:
- random opponent against random agent
- random opponent against optimal agent 
- optimal opponent against optimal agent
- optimal opponent against random agent"""

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

def make_a_turn(state, x_strategy, o_strategy, tau):
    """"""
    # decide whose turn it is

    # choose the action 

    # return the new state s'

def choose_action(state, x_strategy, o_strategy, tau):
    """"""
    # random strategy chooses with equal probabilities so Pr(a) = 1/N_a 

    # optimal strategy has Pr(a) = 1 for argmax Q[s,]

    # Bolzmann function

    # choose a with Pr(a)

def play_tic_tac_toe(games, x_strategy, o_strategy, tau):
    """Function which plays the given number of games using the given strategy (random or optimal) for both agent and opponent."""
    gamecount = 0 # initialise game counter
    while gamecount < games:
        # initialise the game state
        gamestate = (0, 0)
        depth = 0
        while depth < 9 or gamestate not in TERMINAL_STATES: # continue playing until board is filled or a terminal state is achieved
            make_a_turn(gamestate)

        # update game counter
        gamecount += 1

        # return list of states, actions, resulting states, and immediate rewards [s, a, s', r]
