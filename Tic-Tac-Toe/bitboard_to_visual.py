"""This file implements a function that, given a bitboard representation of a game of tic-tac-toe, converts it to a visual representation using a matrix
of naughts and crosses."""

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
import list_possible_states
possible_states, state_value_dict = list_possible_states.return_states()
# counter variables
gameplay = 0 
x_wins = 0
o_wins = 0
draws = 0
with open("possible_states.txt", "w") as file:
    for statelist in possible_states.values(): # for list of states at a depth
        for state in statelist: # for state in this list
            val = state_value_dict[state] # retrieve value
            if val == None: # if gameplay state
                gameplay += 1
            elif val == 1: # if x won
                x_wins += 1
            elif val == -1: # if o won
                o_wins += 1
            else: # otherwise must be draw
                draws += 1
            file.write(f"{bitboard_to_visual(state)},\n") # append state to file
    # summary
    file.write(f"Crosses won {x_wins} times\n")
    file.write(f"Naughts won {o_wins} times\n")
    file.write(f"{draws} states were drawn\n")
    file.write(f"The remaining {gameplay} states were non-terminal, i.e. gameplay states\n")
    file.write(f"There were a total of {gameplay + x_wins + o_wins + draws} states")
