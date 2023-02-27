import os
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor

# def coor_to_nv(coor):
#     (lat, lon) = coor
#     lat = lat / 180 * math.pi
#     lon = lon / 180 * math.pi

#     cos_lat = math.cos(lat)
#     cos_lon = math.cos(lon)
#     sin_lat = math.sin(lat)
#     sin_lon = math.sin(lon)
#     return [cos_lat*cos_lon, cos_lat*sin_lon, sin_lat]

# def nv_to_coor(nvector):
#     [n0, n1, n2] = nvector
#     return (math.asin(n2) * 180 / math.pi, math.atan2(n1, n0) * 180 / math.pi)

# # 制作数据
# def make_data_1(clients):
#     input_list, output_list = [], []
#     for client_ip in clients:
#         client_coor = dict_client_info[client_ip]['coordinate']
#         output_list.append(coor_to_nv(client_coor))

#         now_input = []    
#         now_input.extend(dict_client_region[client_ip])
#         for server_ip in dict_server_info:
#             now_input.append(dict_clientserver_rtt[client_ip][server_ip])
#         input_list.append(now_input)
#     return (input_list, output_list)

# (train_data, train_label) = make_data_1(ok_train_list)
# (test_data, test_label) = make_data_1(ok_test_list)

# rfc = RandomForestRegressor(n_estimators=300, n_jobs=N_JOBS, criterion='nvector2')
# rfc = rfc.fit(train_data, train_label)
# predict_coor = rfc.predict(test_data)
# dict_predict_coor = {}
# for ip_idx, test_ip in enumerate(ok_test_list):
#     dict_predict_coor[test_ip] = predict_coor[ip_idx].tolist()


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

(train_data, train_label) = make_data_2(ok_train_list)
(test_data, test_label) = make_data_2(ok_test_list)

rfc = RandomForestRegressor(n_estimators=300, n_jobs=N_JOBS, criterion='latlon')
rfc = rfc.fit(train_data, train_label)
predict_coor = rfc.predict(test_data)
dict_predict_coor = {}
for ip_idx, test_ip in enumerate(ok_test_list):
    dict_predict_coor[test_ip] = predict_coor[ip_idx].tolist()
