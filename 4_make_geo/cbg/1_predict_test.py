import os
import sys
sys.path.append(os.path.expanduser('~'))
from utils.get_wgs84_circle import get_wgs84_circle
import ast
import math
import pickle
import json
import glob
import random
import pyproj
import csv
import geopy.distance
from CBG import CBG
from shapely.geometry import Point, box as Box
import concurrent.futures

# 整个世界
MAX_LAT = 90
MAX_LON = 180
WorldRect = Box(-179.9, -60, 179.9, 85)

RTT_MIN = -1
RTT_MAX = 0

PING_TYPE = sys.argv[1]
print('Loading pickle ...')
BIN_PATH = os.path.expanduser(f'~/ipgeo/pickle_bin/{PING_TYPE}/')
clientserver_rtt_dict = pickle.load(open(f'{BIN_PATH}/clientserver_rtt_dict.bin', 'rb'))
ok_server_dict = pickle.load(open(f'{BIN_PATH}/ok_server_dict.bin', 'rb'))

DST_PATH = os.path.expanduser(f'./pickle_bin/{PING_TYPE}')
for idx in range(3, 6):
    print(idx)
    ok_test_list = pickle.load(open(f'{BIN_PATH}/ok_test_list_{idx}.bin', 'rb'))
    server_cbg_dict = pickle.load(open(f'{DST_PATH}/server_cbg_dict_rtt_{idx}_{RTT_MAX}.bin', 'rb'))
    print('Loading pickle OK ...')
    print('=============================================')

    def predict(client_ip):
        print(f'Predicting {client_ip} ...')
        intersect_poly = WorldRect

        ''' 遍历探测点, 进行预测 '''
        for server_ip in clientserver_rtt_dict[client_ip]:
            point = Point(ok_server_dict[server_ip]['coordinate'])
            ''' 预测半径 '''
            now_cbg = server_cbg_dict[server_ip]

            rtt     = clientserver_rtt_dict[client_ip][server_ip]
            if RTT_MIN < rtt < RTT_MAX: continue

            radius  = now_cbg.predict(rtt)
            if radius > 19975: continue
            if radius < 0    : continue

            circle = get_wgs84_circle((point.y, point.x), radius * 1000, client_ip)
            try:
                intersect_poly = intersect_poly.intersection(circle)
            except:
                pass

        print(f'OK: {client_ip}')

        # geod = pyproj.Geod(ellps="WGS84")
        # area = abs(geod.geometry_area_perimeter(intersect_poly)[0])
        # return {client_ip: (area, intersect_poly, valid_num, rtt_ok_num, rtt_good_num, except_num)}
        return {client_ip: intersect_poly}

    # 预测
    test_result = dict()
    TASK_NUM = 30
    with concurrent.futures.ProcessPoolExecutor(max_workers=TASK_NUM) as executor:
        futures = [executor.submit(predict, client_ip) for client_ip in ok_test_list]
        for future in concurrent.futures.as_completed(futures):
            test_result.update(future.result())
    pickle.dump(test_result, open(f'{DST_PATH}/test_result_rtt_{idx}_{RTT_MAX}.bin', 'wb'))
