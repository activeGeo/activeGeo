import queue
import os
import ast
import sys
import json
import pickle
import threading
import concurrent.futures
from collections import defaultdict

ITDK_DIR = '../../src/itdk_data'
ITDK_FILE = ITDK_DIR + '/data-{}.txt'
ITDK_FILE_NUM = len(os.listdir(ITDK_DIR))

DST_DIR = '../../pickle_bin'

dict_name_binpath = {
    'caida': '../0_geo_by_caida/result/',
    'myself': '../0_geo_by_myself/result/',
}

def format_name(name):
    return name.replace('-','').replace(' ','').lower()

list_dict_good_prefixs = []
for name in dict_name_binpath:
    binpath = dict_name_binpath[name] + '/dict_good_prefixs.bin'
    dict_good_prefixs = pickle.load(open(binpath, 'rb'))
    list_dict_good_prefixs.append(dict_good_prefixs)

set_bad_prefixs = set()
for i in range(len(list_dict_good_prefixs)):
    for j in range(i+1, len(list_dict_good_prefixs)):
        dict_good_prefixs_1 = list_dict_good_prefixs[i]
        dict_good_prefixs_2 = list_dict_good_prefixs[j]

        set_both_keys = dict_good_prefixs_1.keys() & dict_good_prefixs_2.keys()
        for prefix in set_both_keys:
            city_1 = (dict_good_prefixs_1[prefix]['city'])
            city_2 = (dict_good_prefixs_2[prefix]['city'])
            if city_1 != city_2:
                set_bad_prefixs.add(prefix)


for prefix_idx, name in enumerate(dict_name_binpath):
    dict_good_prefixs = list_dict_good_prefixs[prefix_idx]

    def search_in_one(idx):
        dict_good_ips = {}
        print(f'RUNNING {idx}')
        with open(ITDK_FILE.format(idx), 'r') as srcfile:
            for row in srcfile:
                if row[0] == '#': continue
                ip_list = row.split(':')[1].split()

                for ip in ip_list:
                    prefix = '.'.join(ip.split('.')[0:3])
                    if prefix in set_bad_prefixs: continue
                    if prefix in dict_good_prefixs:
                        dict_good_ips[ip] = {}
                        dict_good_ips[ip].update(dict_good_prefixs[prefix])
                        dict_good_ips[ip]['city'] = format_name(dict_good_ips[ip]['city'])
                        dict_good_ips[ip]['type'] = 'v4'
                        dict_good_ips[ip]['ip'] = ip
        return dict_good_ips

    TASK_NUM = 30
    with concurrent.futures.ProcessPoolExecutor(max_workers=TASK_NUM) as executor:
        dict_good_ips = dict()
        futures = [executor.submit(search_in_one, idx) for idx in range(ITDK_FILE_NUM)]
        for future in concurrent.futures.as_completed(futures):
            dict_good_ips.update(future.result())
        print('TOTAL NUM: ', len(dict_good_ips))

    pickle.dump(dict_good_ips, open(f'{DST_DIR}/rdns_by_{name}.bin', 'wb'))
