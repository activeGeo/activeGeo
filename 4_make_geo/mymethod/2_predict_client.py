import os
import pickle

TYPE = 'test01'
BIN_DIR = os.path.expanduser(f'~/ipgeo/pickle_bin/{TYPE}')

print('Loading pickle ...')
ok_server_dict = pickle.load(open(f'{BIN_DIR}/ok_server_dict.bin', 'rb'))
ok_client_dict = pickle.load(open(f'{BIN_DIR}/ok_client_dict.bin', 'rb'))
ok_train_set = pickle.load(open(f'{BIN_DIR}/ok_train_set.bin', 'rb'))
ok_test_set = pickle.load(open(f'{BIN_DIR}/ok_test_set.bin', 'rb'))
client_region_dict = pickle.load(open(f'{BIN_DIR}/client_region_dict.bin', 'rb'))

xgb_rtt_dict = pickle.load(open(f'{BIN_DIR}/xgb_rtt_dict.bin', 'rb'))
print('Loading OK ...')


# 预测区域
from sklearn.ensemble import RandomForestClassifier

# 制作数据
def make_data_1(client_set, input_list, output_list):
    for client_ip in client_set:
        output_list.append(client_region_dict[client_ip].index(1))

        now_input = []    
        for server_ip in ok_server_dict:
            now_input.append(xgb_rtt_dict[client_ip][server_ip])
        input_list.append(now_input)

train_data  = []
train_label = []
make_data_1(ok_train_set, train_data, train_label)

test_data  = []
test_label = []
make_data_1(ok_test_set, test_data, test_label)

rfc = RandomForestClassifier(n_estimators=300, n_jobs=30)
rfc = rfc.fit(train_data, train_label)
predict_region = rfc.predict(test_data)

pickle.dump(rfc, open(f'{BIN_DIR}/RF1.bin', 'wb'))



# 预测坐标
from sklearn.ensemble import RandomForestRegressor

# 制作数据
def make_data_2(client_set, input_list, output_list):
    for client_ip in client_set:
        output_list.append(ok_client_dict[client_ip]['coordinate'])

        now_input = []    
        now_input.extend(client_region_dict[client_ip])
        for server_ip in ok_server_dict:
            now_input.append(xgb_rtt_dict[client_ip][server_ip])
        input_list.append(now_input)

train_data  = []
train_label = []
make_data_2(ok_train_set, train_data, train_label)

test_data  = []
test_label = []
make_data_2(ok_test_set, test_data, test_label)

rfc = RandomForestRegressor(n_estimators=300, n_jobs=30)
rfc = rfc.fit(train_data, train_label)
predict_coor = rfc.predict(test_data)[0]

pickle.dump(rfc, open(f'{BIN_DIR}/RF2.bin', 'wb'))
