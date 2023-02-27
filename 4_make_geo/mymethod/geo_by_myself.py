import os
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor

# import argparse
# parser = argparse.ArgumentParser(description='Geo by our three-phase method')
# parser.add_argument('--dict_server_info', help='path of dict_server_info.bin')
# parser.add_argument('--dict_client_info', help='path of dict_client_info.bin')
# parser.add_argument('--ok_train_list', help='path of ok_train_list.bin')
# parser.add_argument('--ok_test_list', help='path of ok_test_list.bin')
# parser.add_argument('--dict_rtt_info', help='path of the rtt dictionary')
# parser.add_argument('--dict_client_region', help='path of client region dictionary')
# args = parser.parse_args()

def make_predict(
    dict_server_info,
    dict_client_info,
    ok_train_list,
    ok_test_list,
    dict_clientserver_rtt,
    dict_client_region,
    N_JOBS = 30,
    loss = 'mse',
):
    # 制作数据
    def make_data_1(clients):
        input_list, output_list = [], []
        for client_ip in clients:
            output_list.append(dict_client_region[client_ip].index(1))

            now_input = []    
            for server_ip in dict_server_info:
                now_input.append(dict_clientserver_rtt[client_ip][server_ip])
            input_list.append(now_input)
        return (input_list, output_list)

    def make_data_2(clients):
        input_list, output_list = [], []
        for client_ip in clients:
            output_list.append(dict_client_info[client_ip]['coordinate'])

            now_input = []    
            now_input.extend(dict_client_region[client_ip])
            for server_ip in dict_server_info:
                now_input.append(dict_clientserver_rtt[client_ip][server_ip])
            input_list.append(now_input)
        return (input_list, output_list)

    (train_data, train_label) = make_data_1(ok_train_list)
    (test_data, test_label) = make_data_1(ok_test_list)

    rfc = RandomForestClassifier(n_estimators=300, n_jobs=N_JOBS)
    rfc = rfc.fit(train_data, train_label)
    predict_region = rfc.predict(test_data)

    dict_predict_region = {}
    for ip_idx, test_ip in enumerate(ok_test_list):
        one_region = [0 for x in range(len(dict_client_region[test_ip]))]
        one_region[predict_region[ip_idx].item()] = 1
        dict_predict_region[test_ip] = one_region
    # pickle.dump(rfc, open(f'{DST_DIR}/RF1.bin', 'wb'))

    (train_data, train_label) = make_data_2(ok_train_list)
    (test_data, test_label) = make_data_2(ok_test_list)

    rfc = RandomForestRegressor(n_estimators=300, n_jobs=N_JOBS, criterion=loss)
    rfc = rfc.fit(train_data, train_label)
    predict_coor = rfc.predict(test_data)
    dict_predict_coor = {}
    for ip_idx, test_ip in enumerate(ok_test_list):
        dict_predict_coor[test_ip] = predict_coor[ip_idx].tolist()

    # pickle.dump(rfc, open(f'{DST_DIR}/RF2.bin', 'wb'))
    # pickle.dump(predict_coor, open(f'{DST_DIR}/predict_coor.bin', 'wb'))
    return (dict_predict_region, dict_predict_coor)
