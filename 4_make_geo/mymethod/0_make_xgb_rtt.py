import os
import pickle
import xgboost as xgb

BIN_DIR = os.path.expanduser(f'../pickle_bin')

dict_server_info = pickle.load(open(f'{BIN_DIR}/dict_server_info.bin', 'rb'))

ok_train_list = pickle.load(open(f'{BIN_DIR}/ok_train_list.bin', 'rb'))
ok_test_list  = pickle.load(open(f'{BIN_DIR}/ok_test_list.bin', 'rb'))

dict_nan_rtt = pickle.load(open(f'{BIN_DIR}/dict_nan_rtt.bin', 'rb'))


import numpy as np
import pandas as pd

# 训练数据
train_rtt = []
for client_ip in ok_train_list:
    now_input = []
    for server_ip in dict_server_info:
        now_input.append(dict_nan_rtt[client_ip][server_ip])
    train_rtt.append(now_input)
train_rtt = pd.DataFrame(train_rtt)

# 测试数据
test_rtt = []
for client_ip in ok_test_list:
    now_input = []
    for server_ip in dict_server_info:
        now_input.append(dict_nan_rtt[client_ip][server_ip])
    test_rtt.append(now_input)
test_rtt = pd.DataFrame(test_rtt)


from sklearn.multioutput import MultiOutputRegressor
from sklearn.metrics.pairwise import haversine_distances

# 训练模型的参数
params = {}
# params['booster'] = 'gbtree'
# params['eta'] = 0.1
params['objective'] = 'reg:squarederror'
# params['gamma'] = 0.1
# params['max_depth'] = 7 # default
# params['subsample'] = 0.7
# params['min_child_weight'] = 3
# params['nthread'] = 60
# params['tree_method'] = 'hist'
params['n_estimators'] = 500
params['eval_metric'] = haversine_distances


print('Begining training xgb models')

XGB_MODELS = []

for i in range(train_rtt.shape[1]):
    print(i)
    column_data = train_rtt.iloc[:, i]   # 某个需要填充的列，索引为i
    other_data = train_rtt.drop(i, axis=1)

    ytrain = column_data[column_data.notnull()]  # 被选中填充的特征矩阵 T 中的非空值
    Xtrain = other_data.loc[ytrain.index]  # 新特征矩阵上，被选出来要填充的特征的非空值对应的记录

    xgb_model = xgb.XGBRegressor(**params).fit(Xtrain, ytrain)
    XGB_MODELS.append(xgb_model)

pickle.dump(XGB_MODELS, open(f'{BIN_DIR}/XGB_MODELS.bin', 'wb'))
print('Success: training xgb models')


# 开始进行预测
xgb_rtt_dict = {}

# 首先是训练数据
for i in range(0, train_rtt.shape[1]):
    column_data = train_rtt.iloc[:, i]   # 需要填充的列
    other_data = train_rtt.drop(i, axis=1)

    ytest  = column_data[column_data.isnull()]  # 被选中填充的特征矩阵T中的空值
    Xtest = other_data.loc[ytest.index]   # 空值对应的记录 
    ypredict = XGB_MODELS[i].predict(Xtest)

    train_rtt.iloc[ytest.index, i] = ypredict

for i, client_ip in enumerate(ok_train_list):
    if not i % 5000: print(i)
    xgb_rtt_dict[client_ip] = {}
    for j, server_ip in enumerate(dict_server_info):
        xgb_rtt_dict[client_ip][server_ip] = train_rtt.loc[i, j]


# 然后测试数据
for i in range(0, test_rtt.shape[1]):
    column_data = test_rtt.iloc[:, i]   # 需要填充的列
    other_data = test_rtt.drop(i, axis=1)

    ytest  = column_data[column_data.isnull()]  # 被选中填充的特征矩阵T中的空值
    Xtest = other_data.loc[ytest.index]   # 空值对应的记录 
    ypredict = XGB_MODELS[i].predict(Xtest)

    test_rtt.iloc[ytest.index, i] = ypredict

for i, client_ip in enumerate(ok_test_list):
    if not i % 5000: print(i)
    xgb_rtt_dict[client_ip] = {}
    for j, server_ip in enumerate(dict_server_info):
        xgb_rtt_dict[client_ip][server_ip] = test_rtt.loc[i, j]

pickle.dump(xgb_rtt_dict, open(f'{BIN_DIR}/xgb_rtt_dict.bin', 'wb'))
