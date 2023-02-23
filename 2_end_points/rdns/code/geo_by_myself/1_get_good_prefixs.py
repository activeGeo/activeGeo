import queue
import re
import os
import ast
import sys
import csv
import pickle
import reverse_geocode
import concurrent.futures

GEOINFO_BIN_DIR = os.path.expanduser('../../../../0_location_hint/pickle_bin')
set_blackwords = pickle.load(open(f'{GEOINFO_BIN_DIR}/set_blackwords.bin', 'rb'))
dict_geohint_by_country = pickle.load(open(f'{GEOINFO_BIN_DIR}/dict_geohint_by_country.bin', 'rb'))
dict_city_by_country = pickle.load(open(f'{GEOINFO_BIN_DIR}/dict_city_by_country.bin', 'rb'))

DICT_PREFIX_INFO_BIN = './result/dict_prefix_info/{}.bin'
DICT_PREFIX_INFO_NUM = len(os.listdir('./result/dict_prefix_info'))

def format_name(name):
    return name.replace('-','').replace(' ','').lower()

NUM_THRESHOLD = 100
LEN_THRESHOLD = 4
def check_one_file(idx):
    dict_one_file = dict()

    dict_prefix_info = pickle.load(open(DICT_PREFIX_INFO_BIN.format(idx), 'rb'))
    for prefix in dict_prefix_info:
        for match_word in dict_prefix_info[prefix]:
            match_result = dict_prefix_info[prefix][match_word]['result']
            country_code = match_result[1]
            match_result = dict_geohint_by_country[country_code][match_word]
            dict_prefix_info[prefix][match_word]['result'] = match_result

    for prefix in dict_prefix_info:
        # 对于一个 /24 子网，要求只能有一个关键词
        if len(dict_prefix_info[prefix]) == 1:
            match_word = next(iter(dict_prefix_info[prefix]))
            one_result = dict()

            # REQUIREMENT
            # 1. 子网中可以抽取该关键词数量大于数量阈值
            # 2. 抽取的关键词不能在黑名单中
            # 3. 抽取的关键词长度要大于长度阈值
            if dict_prefix_info[prefix][match_word]['num'] < NUM_THRESHOLD: continue
            if match_word in set_blackwords: continue
            if len(match_word) < LEN_THRESHOLD: continue

            match_result = dict_prefix_info[prefix][match_word]['result']

            one_result['city'] = match_result[3]
            one_result['coordiante'] = match_result[0]
            one_result['country_code'] = match_result[1]
            one_result['hostname'] = dict_prefix_info[prefix][match_word]['hostname']
            one_result['ipnum'] = dict_prefix_info[prefix][match_word]['num']
            one_result['match_word'] = match_word
            dict_one_file[prefix] = one_result
    return dict_one_file

TASK_NUM = 30
with concurrent.futures.ProcessPoolExecutor(max_workers=TASK_NUM) as executor:
    dict_good_prefixs = {}
    futures = [executor.submit(check_one_file, idx) for idx in range(DICT_PREFIX_INFO_NUM)]
    for future in concurrent.futures.as_completed(futures):
        dict_good_prefixs.update(future.result())

    pickle.dump(dict_good_prefixs, open('./result/dict_good_prefixs.bin', 'wb'))
    print(len(dict_good_prefixs))
