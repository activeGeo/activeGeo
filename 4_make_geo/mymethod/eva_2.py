import os
import pickle
import geopy.distance
from geo_by_myself import make_predict

dict_server_info = pickle.load(open('../pickle_bin/dict_server_info.bin', 'rb'))
dict_client_info = pickle.load(open('../pickle_bin/dict_client_info.bin', 'rb'))
ok_train_list = pickle.load(open('../pickle_bin/ok_train_list.bin', 'rb'))
ok_test_list = pickle.load(open('../pickle_bin/ok_test_list.bin', 'rb'))
dict_clientserver_rtt = pickle.load(open('../pickle_bin/dict_rtt_xgb.bin', 'rb'))

for r_type in ['none', 'rir', 'continent', 'subregion']:
    print(r_type)
    dict_client_region = pickle.load(open(f'../pickle_bin/dict_client_region_{r_type}.bin', 'rb'))
    stage_2, stage_3 = make_predict(
        dict_server_info,
        dict_client_info,
        ok_train_list,
        ok_test_list,
        dict_clientserver_rtt,
        dict_client_region,
    )
    err_num = 0
    for test_ip in ok_test_list:
        if dict_client_region[test_ip] != stage_2[test_ip]:
            err_num += 1
    print(err_num)

    err_dis = 0
    for test_ip in ok_test_list:
        good_coor = dict_client_info[test_ip]['coordinate']
        test_coor = stage_3[test_ip]
        err_dis += geopy.distance.geodesic(good_coor, test_coor).km
    print(err_dis / len(ok_test_list))
