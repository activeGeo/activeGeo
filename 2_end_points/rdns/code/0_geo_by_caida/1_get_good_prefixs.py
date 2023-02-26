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
set_country_code = pickle.load(open(f'{GEOINFO_BIN_DIR}/set_country_code.bin', 'rb'))
set_blackwords = pickle.load(open(f'{GEOINFO_BIN_DIR}/set_blackwords.bin', 'rb'))
dict_clli_code = pickle.load(open(f'{GEOINFO_BIN_DIR}/dict_clli_code.bin', 'rb'))

DICT_PREFIX_INFO_DIR = './result/dict_prefix_info'
DICT_PREFIX_INFO_NUM = len(os.listdir(DICT_PREFIX_INFO_DIR))

def format_name(name):
    return name.replace('-','').replace(' ','').lower()

NUM_THRESHOLD = 100
LEN_THRESHOLD = 4
def check_one_file(idx):
    dict_one_file = dict()

    dict_prefix_info = pickle.load(open(DICT_PREFIX_INFO_DIR + f'/{idx}.bin', 'rb'))
    for prefix in dict_prefix_info:
        # 对于一个 /24 子网，要求只能有一个关键词
        if len(dict_prefix_info[prefix]) == 1:
            match_word = next(iter(dict_prefix_info[prefix]))
            one_result = dict()

            # REQUIREMENT
            # 1. 子网中可以抽取该关键词数量大于数量阈值
            # 2. 抽取的关键词不能在黑名单中
            # 3. 抽取的关键词长度要大于长度阈值 (IATA 除外)
            # 4. 如果后缀名是国家代码, 要求抽取的城市在该国家中

            # REQ 2
            if match_word in set_blackwords: continue

            match_result = dict_prefix_info[prefix][match_word]['result']
            # REQ 1
            if dict_prefix_info[prefix][match_word]['num'] < NUM_THRESHOLD: 
                continue
            # REQ 3
            if len(match_word) < LEN_THRESHOLD and match_result['type'] != 'iata': 
                continue

            if match_result['type'] == 'clli':
                if match_result['code'] not in dict_clli_code: continue

                position = dict_clli_code[match_result['code']]
                one_result['city'] = position[3]
                one_result['coordiante'] = position[0]
                one_result['country_code'] = position[1]
            # 进入该分支，match_result 已经有了坐标
            else:
                one_result['coordinate'] = (float(match_result['lat']), float(match_result['lng']))
                one_result['country_code'] = format_name(match_result['location']['cc'])

                # 如果没有 place (城市名), 只给了坐标, 需要去查一下城市名称
                if 'place' not in match_result['location']:
                    position = reverse_geocode.search((one_result['coordinate'],))[0]
                    one_result['city'] = format_name(position['city'])
                else:
                    one_result['city'] = format_name(match_result['location']['place'])

            hostname = dict_prefix_info[prefix][match_word]['hostname']
            # REQ 4
            if hostname.split('.')[-1] in set_country_code:
                if hostname.split('.')[-1] != one_result['country_code']:
                    continue

            one_result['hostname'] = dict_prefix_info[prefix][match_word]['hostname']
            one_result['ipnum'] = dict_prefix_info[prefix][match_word]['num']
            one_result['match_word'] = match_word
            one_result['match_type'] = match_result['type']
            dict_one_file[prefix] = one_result
    return dict_one_file

TASK_NUM = 30
with concurrent.futures.ProcessPoolExecutor(max_workers=TASK_NUM) as executor:
    dict_good_prefixs = dict()
    futures = [executor.submit(check_one_file, idx) for idx in range(DICT_PREFIX_INFO_NUM)]
    for future in concurrent.futures.as_completed(futures):
        dict_good_prefixs.update(future.result())

    pickle.dump(dict_good_prefixs, open(f'{DICT_PREFIX_INFO_DIR}/../dict_good_prefixs.bin', 'wb'))
    print(len(dict_good_prefixs))
