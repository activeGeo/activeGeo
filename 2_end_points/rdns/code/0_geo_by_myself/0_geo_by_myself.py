# 通过对 RDNS Hostname 匹配完整城市名获取地理信息

import queue
import os
import ast
import sys
import pickle
import concurrent.futures
from publicsuffix2 import get_tld

RDNS_PROJ_DIR = '../../'
RDNS_FILES = RDNS_PROJ_DIR + '/src/rapid7_data/data-{}.txt'
RDNS_FILES_NUM = len(os.listdir(RDNS_PROJ_DIR + '/src/rapid7_data'))

GEOINFO_DIR = os.path.expanduser('../../../../0_location_hint/pickle_bin')
set_country_code = pickle.load(open(f'{GEOINFO_DIR}/set_country_code.bin', 'rb'))
dict_geohint_by_country = pickle.load(open(f'{GEOINFO_DIR}/dict_geohint_by_country.bin', 'rb'))

DST_DIR = './result/'
os.system(f'mkdir -p {DST_DIR}/dict_prefix_info')

def check_one_file(idx):
    print(f"RUNNING {idx} ...")
    dict_prefix_info = {}
    with open(RDNS_FILES.format(idx), 'r') as srcfile:
        for row in srcfile:
            one_json = ast.literal_eval(row.strip())
            now_ip = one_json['name']
            hostname = one_json['value'].lower()

            hostname_split = hostname.split('.')

            # 后缀必须是国家代码
            suffix = hostname_split[-1].lower()
            if suffix == 'uk': suffix = 'gb'
            if suffix not in set_country_code: continue

            # 找到 hostname 公开后缀的位置
            # for example: a.b.edu.cn, we need 'a.b'
            # pos = len([a,b,edu,cn]) - len([edu,cn])
            pos = len(hostname_split) - len(get_tld(hostname).split('.'))

            split_names = set()
            # 对于 '-' 字符, 有两种选择, 一个是删掉, 一个是替换为 '.'
            for i in range(0, pos):
                split_names.add(hostname_split[i].replace('-', ''))
                split_names.update(hostname_split[i].split('-'))

                # 将 Hostname 分割后与对应国家城市集进行比对
                for split_name in split_names:
                    if split_name in dict_geohint_by_country[suffix]:
                        prefix = now_ip[0:now_ip.rfind('.')]
                        match_word = split_name
                        result = dict_geohint_by_country[suffix][match_word]

                        # 是否已经有该前缀信息
                        if prefix not in dict_prefix_info:
                            dict_prefix_info[prefix] = {}

                        # 该前缀是否有 match_word, 记录信息
                        if match_word not in dict_prefix_info[prefix]:
                            dict_prefix_info[prefix][match_word] = {
                                'hostname': hostname,
                                'result': result,
                                'num': 0
                            }

                        # 更新该前缀中 match_word 信息
                        dict_prefix_info[prefix][match_word]['num'] += 1
    pickle.dump(dict_prefix_info, open(f'{DST_DIR}/dict_prefix_info/{idx}.bin', 'wb'))
    print(f"------- {idx} is OK ---------")
    return

TASK_NUM = 30
with concurrent.futures.ProcessPoolExecutor(max_workers=TASK_NUM) as executor:
    futures = [executor.submit(check_one_file, idx) for idx in range(RDNS_FILES_NUM)]
    for future in concurrent.futures.as_completed(futures):
        future.result()
