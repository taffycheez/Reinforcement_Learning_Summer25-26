import q_learning
import gameplay_sim
import monte_carlo

def plot_convergence(method):
    result = []
    for i in range(1, 101):
        q_table = method.play_tic_tac_toe(i, 'learning', 'optimal', 5, 0.1)
        result.append(q_table[(1,2)][2])
    return result

def plot_performance(method):
    result = []
    for i in range(1, 1001):
        q_table = method.play_tic_tac_toe(i, 'learning', 'random', 10, 0.01)
        games = gameplay_sim.play_tic_tac_toe(100, q_table, 'random')
        outcome = 0
        for game in games:
            if game[-1] == 1:
                outcome += 1
        result.append(outcome/100)
    return result


mc = plot_performance(monte_carlo)

import matplotlib.pyplot as plt
import numpy as np
#q, mc = np.array(q), np.array(mc)
mc = np.array(mc)

x = np.array(range(1000))

fig, ax = plt.subplots()
#ax.plot(x, q, label = 'q')
ax.plot(x, mc, label = 'mc')
ax.grid()
ax.legend()
plt.show()