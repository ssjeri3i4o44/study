import numpy as np
import random as rd
import math
import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn import model_selection
from sklearn.model_selection import train_test_split
import pandas as pd


#初始化
def initialize(m,D,xMin,xMax):
    X = np.zeros((m,D))
    for i in range(m):
        for j in range(D):
            X[i,j] = xMin[j] + rd.random()*(xMax[j] - xMin[j])
    return X

def mutation(X,m,D,i,F,xMin,xMax,bestX,t,T):      #对每个Xi变异
    rand = []
    while True:
        rand = rd.sample(range(m),4)
        if i not in rand:
            break
    Fi = F+(t/T)*0.5
    vi = bestX + F*(X[rand[1]] + X[rand[2]] - X[rand[0]] - X[rand[3]])
    #变异后，可能超出上下限，若超出上下限，则随机产生一个向量替代
    for j in range(D):
            if vi[j] >= xMax[j] or vi[j] <= xMin[j]:
                vi[j] = bestX[j]
    return vi

def crossover(Xi,vX,D,CR,t,T):       #交叉，得到试验个体
    ui = []
    flag = True
    CRi = CR+(1-t/T)*0.5
    for j in range(D):
        rand = rd.random()
        if rand < CR:
            flag = False
            #ui[j] = vX[j]
            ui.append(vX[j])
        else:
            #ui[j] = Xi[j]
            ui.append(Xi[j])
    if flag:
        randnum = rd.randint(0,D-1)
        ui[randnum] = vX[randnum]
    return ui

# 定义适应函数
def fitness(params,params_update,lgb,train_data,valid_data,X_test,y_test):
    params.update(params_update)
    clf = lgb.train(params, train_data, num_boost_round=200, valid_sets=valid_data, early_stopping_rounds=100)
    y_prob = clf.predict(X_test, num_iteration=clf.best_iteration)
    y_pred = [list(x).index(max(x)) for x in y_prob]
    metric = metrics.hamming_loss(y_test, y_pred)
    return metric


def de_main(m, D, F, CR, T,xMin,xMax,clf,train_data,valid_data,X_test,y_test,params,params_update,params_int_update):
    #m种群个数，D是维度，T迭代最大次数
    X = initialize(m, D, xMin, xMax)  # 初始化
    print("X of start：", X)
    t = 1
    bestX = X[0]
    for i,key in enumerate(params_update):
        params_update[key] = bestX[i]
    for i in params_int_update:
        print(params_update[i])
        params_update[i]  = np.int(int(params_update[i]))
    bestfitness = fitness(params,params_update,clf,train_data,valid_data,X_test,y_test)
    best = []
    while t < T:
        for i in range(m - 1):
            vX = mutation(X, m, D, i, F, xMin, xMax, bestX, t, T)  # 变异
            uX = crossover(X[i], vX, D, CR, t, T)  # 交叉

            #计算交叉以后fitness值
            for j, key in enumerate(params_update):
                params_update[key] = uX[j]
            for j in params_int_update:
                params_update[j] = np.int(params_update[j])
            fit_uX = fitness(params,params_update,clf,train_data,valid_data,X_test,y_test)

            #计算变异以后fitness值
            for j, key in enumerate(params_update):
                params_update[key] = vX[j]
            for j in params_int_update:
                params_update[j] = int(params_update[j])
            fit_Xi =fitness(params,params_update,clf,train_data,valid_data,X_test,y_test)

            if fit_uX >= fit_Xi:  # 选择，取适应度值大的
                X[i] = uX
                if fit_uX > bestfitness:
                    bestfitness = fit_uX
                    bestX = X[i]
                else:
                    pass
            else:
                if fit_Xi > bestfitness:
                    bestfitness = fit_Xi
                    bestX = X[i]
                else:
                    pass
        best.append(bestfitness)
        t = t + 1
        print(t, "=========================================")
    print("X of end:", X)
    xx = range(0, T, 1)

    print('fitness is : ', fitness(params,params_update,clf,train_data,valid_data,X_test,y_test))
    print('bestfitness is :', bestfitness)
    print('bestX is : ', bestX)
    return bestX, bestfitness





