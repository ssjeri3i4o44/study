from DE import *
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import lightgbm as lgb

# 训练数据

trainset = pd.read_excel('breast.xlsx')
X = pd.read_excel('breast.xlsx')
y = X[0]
del X[0]


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=1)
train_data = lgb.Dataset(X_train, label = y_train)
valid_data = lgb.Dataset(X_test,label=y_test)

'''
def params(p):
    [p1, p2, p3, p4, p5, p6, p7] = p
    lgb_params = {
        'boosting_type': 'gbdt',
        'objective': 'multiclass',# xentlambda
        'num_class':3,
        'metric': 'multi_error',
        #'silent': 0,
        'learning_rate': p1,
        'is_unbalance': 'true',  # because training data is unbalance (replaced with scale_pos_weight)
        'num_leaves': np.int(p2),  # we should let it be smaller than 2^(max_depth)
        'max_depth': -1,  # -1 means no limit
        'min_child_samples': np.int(p3),  # Minimum number of data need in a child(min_data_in_leaf)
        'max_bin': np.int(p4),  # Number of bucketed bin for feature values
        'subsample': 1,  # Subsample ratio of the training instance.
        'subsample_freq': 1,  # frequence of subsample, <=0 means no enable
        'colsample_bytree': 1,  # Subsample ratio of columns when constructing each tree.
        'min_child_weight': 0,  # Minimum sum of instance weight(hessian) needed in a child(leaf)
        #'scale_pos_weight':100,
        'subsample_for_bin': np.int(p5),  # Number of samples for constructing bin
        'min_split_gain': 0,  # lambda_l1, lambda_l2 and min_gain_to_split to regularization
        'reg_alpha': p6,  # L1 regularization term on weights
        'reg_lambda': p7,  # L2 regularization term on weights
        'nthread': -1,
        'verbose': 0,
        'save_binary':True,#数据集保存为二进制文件，下次读数据时速度会变快
    }
    return lgb_params

'''
#params_key = [np.int(num_leaves),'num_leaves','min_child_samples','max_bin','subsample_for_bin','reg_alpha','reg_lambda']
params = {
    'boosting_type': 'gbdt',
    'objective': 'multiclass',  # xentlambda
    'num_class': 3,
    'metric': 'multi_error',
    # 'silent': 0,
    'learning_rate': 0.1,
    'is_unbalance': 'true',  # because training data is unbalance (replaced with scale_pos_weight)
    'num_leaves': np.int(3),  # we should let it be smaller than 2^(max_depth)
    'max_depth': -1,  # -1 means no limit
    'min_child_samples': np.int(3),  # Minimum number of data need in a child(min_data_in_leaf)
    'max_bin': np.int(100),  # Number of bucketed bin for feature values
    'subsample': 1,  # Subsample ratio of the training instance.
    'subsample_freq': 1,  # frequence of subsample, <=0 means no enable
    'colsample_bytree': 1,  # Subsample ratio of columns when constructing each tree.
    'min_child_weight': 0,  # Minimum sum of instance weight(hessian) needed in a child(leaf)
    # 'scale_pos_weight':100,
    'subsample_for_bin': np.int(100),  # Number of samples for constructing bin
    'min_split_gain': 0,  # lambda_l1, lambda_l2 and min_gain_to_split to regularization
    'reg_alpha': 0.1,  # L1 regularization term on weights
    'reg_lambda': 0.1,  # L2 regularization term on weights
    'nthread': -1,
    'verbose': 1,
    'save_binary': True,  # 数据集保存为二进制文件，下次读数据时速度会变快
}
params_update = {'learning_rate': 2,
                 'num_leaves': np.int(3),
                 'min_child_samples': np.int(3),
                 'max_bin': np.int(100),
                 'subsample_for_bin': np.int(100),
                 'reg_alpha': 0.1,
                 'reg_lambda': 0.1,
}
params_int_update = ['num_leaves','min_child_samples','max_bin','subsample_for_bin']
xMin = [0,1,1,1,1,0,0]
xMax = [1,100,100,1000,1000,1,1]
m = 5
D = 7
F = 0.3
CR = 0.5
T = 30

bestX,bestfitness,= de_main(m, D, F, CR, T,xMin,xMax,lgb,train_data,valid_data,X_test,y_test,params,params_update,params_int_update)



