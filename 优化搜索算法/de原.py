# -*- coding: utf-8 -*-
import numpy as np
import random as rd
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']
import pandas as pd
from sklearn import model_selection
####导入数据
import xlrd
import numpy as np
#from sklearn import cross_validation

cost_function = np.random.randint(0,100,(5,5))
#定义适应函数
def fitness(w):
    ''''
    [para1, para2, para3, para4,para5] = w
    para2 = int(para2)
    para5 = int(para5)
    clf = SVC(C=para1, kernel='rbf', degree=para2, gamma=para3,shrinking=True,
        probability=False, tol=para4, cache_size=200, class_weight='balanced',
        verbose=False, max_iter=para5, decision_function_shape='ovr',
        random_state=None)
    predict = model_selection.cross_val_predict(clf, X, y, cv=5)
    auc = metrics.roc_auc_score(y,predict)
    '''
    [x1,x2,x3,x4,x5] = w
    for x in w:
        x = int(x)
    auc = cost_function[int(x1), int(x2)] + cost_function[int(x2), int(x3)] + cost_function[int(x3), int(x4)] + cost_function[int(x4), int(x5)]
    return auc

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

def de_main(m,D,F,CR,T):
    #m种群个数，D是维度，T迭代最大次数
    xMin = [0,0,0,0,0]
    xMax = [5,5,5,5,5]
    X = initialize(m,D,xMin,xMax)     #初始化
    print("X of start：",X)
    t = 0
    bestX = X[0]
    bestfitness = fitness(X[0])
    best = []
    while t < T:
        for i in range(m-1):
            vX = mutation(X,m,D,i,F,xMin,xMax,bestX,t,T)      #变异
            uX = crossover(X[i],vX,D,CR,t,T)        #交叉
            fit_uX = fitness(uX)
            fit_Xi = fitness(X[i])
            if fit_uX >= fit_Xi :     #选择，取适应度值大的
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
        print(t,"=========================================")
    print("X of end:",X)
    xx = range(0,T,1)
    graph(xx, best)
    print('bestX is : ', bestX)
    print('AUC is : ', fitness(bestX))
    print('bestfitness is :', bestfitness)
    return bestX,bestfitness


def graph(xx,yy):
    plt.figure(1)
    plt.plot(xx,yy,marker='+')
    plt.xlabel('Number of iterations')
    plt.ylabel('auc')
    plt.title('DE')
    plt.show()

de_main(5,5,0.7,0.7,5)
