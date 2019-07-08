import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
from sklearn import metrics
from sklearn.linear_model import Ridge,LinearRegression
from sklearn.preprocessing import PolynomialFeatures

def WSL(x,y,weights):
    '''
    :param x:
    :param y:
    :param weights:各样本权重
    :return clf:训练模型
            x2:训练特征转为多项式
            coef:多项式系数
            intercept:二次项函数截距
            y_predict:预测结果
    '''
    # 转多项式特征
    ploy2 = PolynomialFeatures(degree=2)
    ploy2.fit(x)
    x2 = ploy2.transform(x)
    # 多项式回归
    clf = LinearRegression()
    clf.fit(x2, y, sample_weight=weights)
    coef= clf.coef_
    intercept = clf.intercept_
    y_predict = clf.predict(x2)
    print('R2：', clf.score(x2, y))
    return clf,x2,coef,intercept,y_predict


# 孕天拟合
def WSL_day(data, day, Conc, day_early, day_later, xlabel, ylabel, title):
    '''
    :param data: 样本
    :param day: 孕天特征
    :param Conc: 指标浓度值特征
    :param day_early:孕天开始天数
    :param day_later:孕天结束天数
    :param xlabel: 横坐标
    :param ylabel:纵坐标
    :param title:图标题
    '''
    plt.style.use('seaborn-whitegrid')
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    print('样本量', len(data))
    data = data[(data[day] > day_early) & (data[day] < day_later)]
    print('符合孕天内样本量', len(data))

    weights = data[day].value_counts().sort_index()
    y_fit = data.groupby(data[day])[Conc].median()
    x_fit = y_fit.index
    x = x_fit.values.reshape(-1, 1)
    y = y_fit.values.reshape(-1, 1)
    clf,x2,coef,intercept,y_predict = WSL(x, y, weights)

    # 中位数曲线
    plt.figure(figsize=(12, 7))
    plt.plot(x_fit, y_fit, '-p', color='g')

    # 拟合曲线
    plt.plot(x, y_predict, color='r')
    ax = plt.axes()
    ax.set(xlabel=xlabel, ylabel=ylabel, title=title)

    print('拟合公式：%f x2 + %f x + %f' % (coef[0][2], coef[0][1], intercept))
    return coef, intercept


# 体重拟合
def WSL_weight(data, weight, day, Conc_day, day_early, day_later, xlabel, ylabel, title):
    '''
    :param data: 样本
    :param weight: 体重特征名
    :param day: 孕天特征名
    :param Conc_day: 孕天矫正过后的浓度值
    :param day_early: 孕天开始天数
    :param day_later: 孕天结束天数
    :param xlabel: 横坐标
    :param ylabel: 纵坐标
    :param title: 图标题
    '''
    print('总样本量', len(data))
    # 去掉缺PLGF的样本
    data = data.dropna(subset=[Conc_day])
    # 去掉缺孕天的样本
    data = data.dropna(subset=[weight])
    data = data[(data[day] > day_early) & (data[day] < day_later)]
    data = data[(data[weight] < 120)]
    print('符合孕天内样本量', len(data))
    data[weight] = data[weight].astype(int)
    weights = data[weight].value_counts().sort_index()
    y_fit = data.groupby(data[weight])[Conc_day].median()
    x_fit = y_fit.index
    x = x_fit.values.reshape(-1, 1)
    y = y_fit.values.reshape(-1, 1)
    clf, x2, coef, intercept, y_predict = WSL(x, y, weights)

    # 中位数曲线
    plt.figure(figsize=(12, 7))
    plt.plot(x_fit, y_fit, '-p', color='g')

    # 拟合曲线
    plt.plot(x, y_predict, color='r')
    ax = plt.axes()
    ax.set(xlabel=xlabel, ylabel=ylabel, title=title)

    print('体重拟合公式：%f x2 + %f x + %f' % (coef[0][2], coef[0][1], intercept))

#孕天样本分布
def counts_day(data,day,Conc,day_early,day_later,xlabel,ylabel,title):
    '''
    :param data: 样本
    :param day: 孕天特征
    :param Conc: 浓度特征
    :param day_early: 孕天开始天数
    :param day_later: 孕天结束天数
    :param xlabel: 横坐标
    :param ylabel: 列坐标
    :param title: 图标题
    '''
    print('总样本量:',len(data))
    data = data.dropna(subset = [Conc])
    data = data.dropna(subset = [day])
    data = data[(data[day]>day_early) & (data[day]<day_later)]
    print('删除缺失浓度和孕天，并且符合孕天内样本量',len(data))
    day = pd.DataFrame(data[day].apply(int).value_counts()).reset_index()
    day.columns=['day','样本量']
    day = day.sort_values(by = 'day')
    plt.figure(figsize = (12,7))
    ax = plt.axes()
    sns.barplot(day['day'], day['样本量'],estimator=sum);
    ax.set(xlabel = xlabel, ylabel = ylabel,title = title);

# 体重样本分布
def counts_weight(data,weight,day,day_early,day_later,xlabel,ylabel,title):
    '''
    :param data: 样本
    :param weight: 体重特征
    :param day: 孕天特征
    :param day_early: 孕天开始天数
    :param day_later: 孕天结束天数
    :param xlabel: 横坐标
    :param ylabel: 纵坐标
    :param title: 图标题
    '''
    print('总的样本量',len(data))
    #去掉缺孕天的样本
    data = data.dropna(subset = [day])
    data = data.dropna(subset = [weight])
    data = data[(data[day]>day_early) & (data[day]<day_later)]
    data = data[(data[weight]<=120)]
    print('符合孕期内删除缺失值的样本量',len(data))
    day_E = pd.DataFrame(data[weight].apply(int).value_counts()).reset_index()
    day_E.columns=['weight','样本量']
    day_E = day_E.sort_values(by = 'weight')
    plt.figure(figsize = (12,7))
    ax = plt.axes()
    sns.barplot(day_E['weight'], day_E['样本量'],estimator=sum);
    ax.set(xlabel = xlabel, ylabel = ylabel,title = title);


