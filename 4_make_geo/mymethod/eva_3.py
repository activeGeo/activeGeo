import os
import pickle
import math
import geopy.distance
from geo_by_myself import make_predict

def coor_to_nv(coor):
    (lat, lon) = coor
    lat = lat / 180 * math.pi
    lon = lon / 180 * math.pi

    cos_lat = math.cos(lat)
    cos_lon = math.cos(lon)
    sin_lat = math.sin(lat)
    sin_lon = math.sin(lon)
    return [cos_lat*cos_lon, cos_lat*sin_lon, sin_lat]

def nv_to_coor(nvector):
    [n0, n1, n2] = nvector
    return (math.asin(n2) * 180 / math.pi, math.atan2(n1, n0) * 180 / math.pi)

dict_server_info = pickle.load(open('../pickle_bin/dict_server_info.bin', 'rb'))
dict_client_info = pickle.load(open('../pickle_bin/dict_client_info.bin', 'rb'))
ok_train_list = pickle.load(open('../pickle_bin/ok_train_list.bin', 'rb'))
ok_test_list = pickle.load(open('../pickle_bin/ok_test_list.bin', 'rb'))
dict_clientserver_rtt = pickle.load(open('../pickle_bin/dict_rtt_xgb.bin', 'rb'))
dict_client_region = pickle.load(open('../pickle_bin/dict_client_region_subregion.bin', 'rb'))

new_dict_client_info = {}
for client_ip in dict_client_info:
    new_dict_client_info[client_ip] = {}
    coor = dict_client_info[client_ip]['coordinate']
    new_dict_client_info[client_ip]['coordinate'] = coor_to_nv(coor)

stage_2, stage_3 = make_predict(
    dict_server_info,
    dict_client_info,
    ok_train_list,
    ok_test_list,
    dict_clientserver_rtt,
    dict_client_region,
    loss = 'mse'
)

err_dis = 0
for test_ip in ok_test_list:
    good_coor = dict_client_info[test_ip]['coordinate']
    test_coor = stage_3[test_ip]
    err_dis += geopy.distance.geodesic(good_coor, test_coor).km
print(err_dis / len(ok_test_list))

# stage_2, stage_3 = make_predict(
#     dict_server_info,
#     dict_client_info,
#     ok_train_list,
#     ok_test_list,
#     dict_clientserver_rtt,
#     dict_client_region,
#     loss = 'latlon'
# )

# err_dis = 0
# for test_ip in ok_test_list:
#     good_coor = dict_client_info[test_ip]['coordinate']
#     test_coor = stage_3[test_ip]
#     err_dis += geopy.distance.geodesic(good_coor, test_coor).km
# print(err_dis / len(ok_test_list))

stage_2, stage_3 = make_predict(
    dict_server_info,
    new_dict_client_info,
    ok_train_list,
    ok_test_list,
    dict_clientserver_rtt,
    dict_client_region,
    loss = 'nvector'
)

err_dis = 0
for test_ip in ok_test_list:
    good_coor = dict_client_info[test_ip]['coordinate']
    test_coor = stage_3[test_ip]
    print(test_coor)
    # err_dis += geopy.distance.geodesic(good_coor, test_coor).km
# print(err_dis / len(ok_test_list))
