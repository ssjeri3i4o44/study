# -*- coding: utf-8 -*-
import numpy as np
import random as rd

from mlxtend.feature_selection import ColumnSelector
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import Imputer
from sklearn import preprocessing
import math
import matplotlib.pyplot as plt
from sklearn import cross_validation,metrics
from sklearn import model_selection
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import MultiTaskLasso
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.neural_network import MLPClassifier
from mlxtend.classifier import StackingClassifier
from sklearn import svm
import xgboost as xgb
from sklearn.ensemble import GradientBoostingClassifier
import time
import random
import pandas as pd
starttime = time.clock()


T21 = pd.read_excel('T21.xls',index_col='样本编号')
nor = pd.read_excel('normal.xls',index_col='中孕实验编号')

T21 = T21[['孕周','预产年龄', '体重','出生日期','采血日期','实验日期','T21','AFP MoM','hCGb MoM']]
nor = nor[['孕周','预产年龄','体重', '出生日期','采血日期','实验日期','T21','AFP MoM','hCGb MoM']]
T21['label'] = 1
nor['label'] = 0
data = pd.concat([T21, nor],axis=0, ignore_index=True)

##时间处理
def timedeal(t):
    try:
        timearray = t.strftime("%Y-%m-%d %H:%M:%S")
        timearray = time.strptime(timearray, "%Y-%m-%d %H:%M:%S")
        tm = int(time.mktime(timearray))
    except:
        return 0
    return tm

for t in ['出生日期','采血日期','实验日期']:
    #data[t] = str(data[t])
    data[t] = data[t].apply(timedeal)

y = data['label']
del data['label']

#缺失值填充
imp = Imputer(missing_values=np.nan , strategy='mean', axis=0)
imp.fit(data)
data = imp.transform(data)

####实验相差时间
emtime1 = data[:,4]
emtime2 = data[:,5]
emptime = emtime2-emtime1
emptime = emptime.transpose()
data = np.c_[data,emptime]

X = preprocessing.normalize(data, norm='l2')#归一化

#def stacking(w):
def fitness(w):
    [para1,para2,para3,para4,para5,para6] = w
    para1 = int(para1)
    para2 = int(para2)
    para3 = int(para3)
    para4 = int(para4)
    #n = int(n)
    clf1 = KNeighborsClassifier(n_neighbors=para1)
    #clf2 = DecisionTreeClassifier(criterion="entropy",max_depth=para2,random_state=para3,class_weight='balanced')
    #clf2 = MLPClassifier(activation='relu',solver='sgd',max_iter=para2)
    clf2 = GaussianNB()
    clf4 = xgb.XGBClassifier(eta= 0.1, max_depth=40, subsample=0.9,colsample_bytree=0.9,n_estimators=500)
    clf3= RandomForestClassifier(n_estimators=para2, criterion="entropy", random_state=para3, max_depth=para4)

    lr = LogisticRegression()
    #lr = svm.SVC(kernel='rbf', gamma=para5, decision_function_shape='ovr')
    sclf = StackingClassifier(classifiers= [clf1,clf2,clf3, clf4],
                              use_probas=True,average_probas=True,
                              meta_classifier=lr, use_features_in_secondary=True)
    predict = model_selection.cross_val_predict(sclf, X, y, cv=5)
    auc = metrics.roc_auc_score(y,predict)
    score = metrics.accuracy_score(y,predict)
    f1 = metrics.f1_score(y,predict)
    print('F1:', f1.mean())
    print('score:',score.mean())
    return auc.mean()

def initialize(m,D,xMin,xMax):    #初始化
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

    # vi = [vi[j] if vi[j] < xMax[j] else xMax[j] for j in range(D)]
    # vi = [vi[j] if vi[j] > xMin[j] else xMin[j] for j in range(D)]
    return vi

def crossover(Xi,vX,D,CR,t,T):       #交叉，得到试验个体
    #ui = [vX[j] if rd.random() < CR else Xi[j] for j in range(D) ]
    #rand_index = random.choice(range(N))
    #y = [z[j] if random.random() < CR or j == rand_index else x[j] for j in range(argn)]
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
    #rand = rd.randint(0,D-1)
    #ui[rand] = vX[rand]
    return ui

def de_main(m,D,F,CR,T):
    #m种群个数，D是维度，T迭代最大次数
    xMin = [1,1,1,1,0.01,0.01]
    xMax = [30,20,20,10,10,10]
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
    plt.ylabel('AUC')
    plt.show()


if __name__ == '__main__':
    de_main(5,6,0.3,0.5,5)
    #ensemble()
    # w=[0.2,0.2,0.2,0.2,0.2]
    # f1 = np.array([[1,1],[1,2],[1,3],[1,4]])
    # f2 = np.array([[2,0],[2,1],[2,2],[2,4]])
    # f3 = np.array([[3, 0], [3, 1], [3, 2], [3, 4]])
    # f4 = np.array([[4, 0], [4, 1], [4, 2], [4, 4]])
    # f5 = np.array([[5, 0], [5, 1], [5, 2], [5, 4]])
    # # for i in range(4):
    # #     fun.append(w[0]*f1[i] + w[1]*f2[i] + w[2]*f3[i] + w[3]*f4[i] + w[4]*f5[i])
    # fun = w[0]*f1 + w[1]*f2 + w[2]*f3 + w[3]*f4 + w[4]*f5
    # print("fun=:",fun)
endtime = time.clock()
print (endtime - starttime)