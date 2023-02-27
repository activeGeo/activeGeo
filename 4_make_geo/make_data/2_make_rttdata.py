import os
import pickle
import numpy as np
import pandas as pd
import xgboost as xgb


BIN_DIR = os.path.expanduser(f'../pickle_bin')

dict_server_info = pickle.load(open(f'{BIN_DIR}/dict_server_info.bin', 'rb'))
dict_client_info = pickle.load(open(f'{BIN_DIR}/dict_client_info.bin', 'rb'))
dict_serverclient_rtt = pickle.load(open(f'{BIN_DIR}/dict_serverclient_rtt.bin', 'rb'))
dict_clientserver_rtt = pickle.load(open(f'{BIN_DIR}/dict_clientserver_rtt.bin', 'rb'))
ok_train_list = pickle.load(open(f'{BIN_DIR}/ok_train_list.bin', 'rb'))
ok_test_list  = pickle.load(open(f'{BIN_DIR}/ok_test_list.bin', 'rb'))

USING_CPU_NUM = 32


'''
3. Make RTT data
'''
# 按照 NAN 填充
import math
print('Imputing with nan ...')

now_rtt_dict = {k:{} for k in dict_client_info}
for client_ip in dict_client_info:
    now_rtt_dict[client_ip].update(dict_clientserver_rtt[client_ip])
    
    bad_server_set = dict_server_info.keys() - dict_clientserver_rtt[client_ip].keys()
    for server_ip in bad_server_set:
        now_rtt_dict[client_ip][server_ip] = math.nan            
pickle.dump(now_rtt_dict, open(f'{BIN_DIR}/dict_rtt_nan.bin', 'wb'))

# 按照 MEAN 填充
import statistics
print('Imputing with mean ...')

server_mean_dict = {}
for server_ip in dict_server_info: 
    server_mean_dict[server_ip] = statistics.mean(dict_serverclient_rtt[server_ip].values())

client_mean_dict = {}
for client_ip in dict_client_info:
    client_mean_dict[client_ip] = statistics.mean(dict_clientserver_rtt[client_ip].values())

now_rtt_dict = {k:{} for k in dict_client_info}    
for client_ip in dict_client_info:
    now_rtt_dict[client_ip].update(dict_clientserver_rtt[client_ip])
    
    bad_server_set = dict_server_info.keys() - dict_clientserver_rtt[client_ip].keys()
    for server_ip in bad_server_set:
        now_rtt_dict[client_ip][server_ip] = (server_mean_dict[server_ip] + client_mean_dict[client_ip]) / 2            
pickle.dump(now_rtt_dict, open(f'{BIN_DIR}/dict_rtt_mean.bin', 'wb'))



# 按照 MEDIAN 填充
import statistics
print('Imputing with median ...')

server_median_dict = {}
for server_ip in dict_server_info: 
    server_median_dict[server_ip] = statistics.median(dict_serverclient_rtt[server_ip].values())

client_median_dict = {}
for client_ip in dict_client_info:
    client_median_dict[client_ip] = statistics.median(dict_clientserver_rtt[client_ip].values())

now_rtt_dict = {k:{} for k in dict_client_info}    
for client_ip in dict_client_info:
    now_rtt_dict[client_ip].update(dict_clientserver_rtt[client_ip])
    
    bad_server_set = dict_server_info.keys() - dict_clientserver_rtt[client_ip].keys()
    for server_ip in bad_server_set:
        now_rtt_dict[client_ip][server_ip] = (server_median_dict[server_ip] + client_median_dict[client_ip]) / 2            
pickle.dump(now_rtt_dict, open(f'{BIN_DIR}/dict_rtt_median.bin', 'wb'))


# Using XGB to predict
dict_nan_rtt = pickle.load(open(f'{BIN_DIR}/dict_rtt_nan.bin', 'rb'))

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


# 训练模型的参数
params = {}
params['objective'] = 'reg:squarederror'
params['n_estimators'] = 500


print('Begining training xgb models')

XGB_MODELS = []

for i in range(train_rtt.shape[1]):
    print(i)
    column_data = train_rtt.iloc[:, i]   # 某个需要填充的列，索引为i
    other_data = train_rtt.drop(i, axis=1)

    ytrain = column_data[column_data.notnull()]  # 被选中填充的特征矩阵 T 中的非空值
    Xtrain = other_data.loc[ytrain.index]  # 新特征矩阵上，被选出来要填充的特征的非空值对应的记录

    xgb_model = xgb.XGBRegressor(**params, n_jobs=USING_CPU_NUM).fit(Xtrain, ytrain)
    XGB_MODELS.append(xgb_model)

pickle.dump(XGB_MODELS, open(f'{BIN_DIR}/XGB_MODELS.bin', 'wb'))
print('Success: training xgb models')


# 开始进行预测
dict_xgb_rtt = {}

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
    dict_xgb_rtt[client_ip] = {}
    for j, server_ip in enumerate(dict_server_info):
        dict_xgb_rtt[client_ip][server_ip] = train_rtt.loc[i, j]


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
    dict_xgb_rtt[client_ip] = {}
    for j, server_ip in enumerate(dict_server_info):
        dict_xgb_rtt[client_ip][server_ip] = test_rtt.loc[i, j]

pickle.dump(dict_xgb_rtt, open(f'{BIN_DIR}/dict_rtt_xgb.bin', 'wb'))
