# --- IMPORT DEPENDENCIES ------------------------------------------------------+

from __future__ import division
import random
import pandas as pd

from sklearn.svm import SVC
from sklearn import metrics
from sklearn import model_selection
import matplotlib.pyplot as plt


# --- COST FUNCTION ------------------------------------------------------------+

# function we are attempting to optimize (maximum )

def fitness(w):
    [para1, para2, para3, para4,para5] = w
    para2 = int(para2)
    para5 = int(para5)
    clf = SVC(C=para1, kernel='rbf', degree=para2, gamma=para3,shrinking=True,
        probability=False, tol=para4, cache_size=200, class_weight='balanced',
        verbose=False, max_iter=para5, decision_function_shape='ovr',
        random_state=None)
    predict = model_selection.cross_val_predict(clf, X, y, cv=5)
    auc = metrics.roc_auc_score(y,predict)
    return auc

def graph(xx, yy):
    plt.figure(1)
    plt.plot(xx, yy, marker='+')
    plt.title('PSO')
    plt.xlabel('Number of iterations')
    plt.ylabel('AUC')
    plt.show()

# --- MAIN ---------------------------------------------------------------------+

class Particle:
    def __init__(self, x0):
        self.position_i = []  # particle position
        self.velocity_i = []  # particle velocity
        self.pos_best_i = []  # best position individual
        self.best_i = 0  # best individual
        self.fit_i =0  # individual

        for i in range(0, num_dimensions):
            self.velocity_i.append(random.uniform(-1, 1))
            self.position_i.append(x0[i])

    # evaluate current fitness
    def evaluate(self, costFunc):
        self.fit_i = costFunc(self.position_i)
        # check to see if the current position is an individual best
        if self.fit_i > self.best_i:
            self.pos_best_i = self.position_i.copy()
            self.best_i = self.fit_i

    # update new particle velocity
    def update_velocity(self, pos_best_g):
        w = 1 # constant inertia weight (how much to weigh the previous velocity)
        c1 = 0.1 # cognative constant
        c2 = 2 # social constant

        for i in range(0, num_dimensions):
            r1 = random.random()
            r2 = random.random()

            vel_cognitive = c1 * r1 * (self.pos_best_i[i] - self.position_i[i])
            vel_social = c2 * r2 * (pos_best_g[i] - self.position_i[i])
            self.velocity_i[i] = w * self.velocity_i[i] + vel_cognitive + vel_social

    # update the particle position based off new velocity updates
    def update_position(self, bounds):
        for i in range(0, num_dimensions):
            self.position_i[i] = self.position_i[i] + self.velocity_i[i]

            # adjust maximum position if necessary
            if self.position_i[i] > bounds[i][1]:
                self.position_i[i] = bounds[i][1]

            # adjust minimum position if neseccary
            if self.position_i[i] < bounds[i][0]:
                self.position_i[i] = bounds[i][0]


class PSO():
    def __init__(self, costFunc, x0, bounds, num_particles, maxiter, verbose=False):
        global num_dimensions
        num_dimensions = len(x0)
        best_g = 0  # best for group
        pos_best_g = []  # best position for group
        # establish the swarm
        swarm = []
        for i in range(0, num_particles):
            swarm.append(Particle(x0))

        # begin optimization loop
        i = 0
        best = []
        while i < maxiter:
            if verbose: print(f'iter: {i:>4d}, best solution: {best_g:10.6f}')
            # cycle through particles in swarm and evaluate fitness
            for j in range(0, num_particles):
                swarm[j].evaluate(costFunc)
                # determine if current particle is the best (globally)
                if swarm[j].fit_i > best_g or best_g == 1:
                    pos_best_g = list(swarm[j].position_i)
                    best_g = float(swarm[j].fit_i)
            best.append(best_g)

            # cycle through swarm and update velocities and position
            for j in range(0, num_particles):
                swarm[j].update_velocity(pos_best_g)
                swarm[j].update_position(bounds)
            i += 1
        # print final results
        xx = range(0, maxiter, 1)
        graph(xx, best)
        print('\nFINAL SOLUTION:')
        print(f'   > {pos_best_g}')
        print(f'   > {best_g}\n')

if __name__ == '__main__':
    X = pd.read_excel('breast.xlsx')
    y = X[0]
    del X[0]
    initial = [100,100,1,1,149]  # initial starting location [x1,x2...]
    bounds = [(0.01, 100), (0.000001, 100),(0.000001,1),(0.000001,1),(1,249)]  # input bounds [(x1_min,x1_max),(x2_min,x2_max)...]
    PSO(fitness, initial, bounds, num_particles=10, maxiter=100, verbose=True)

