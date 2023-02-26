# 使用 CAIDA 的正则表达式

import queue
import re
import os
import ast
import sys
import pickle
import concurrent.futures

RDNS_PROJ_DIR = '../../'

RDNS_FILES = RDNS_PROJ_DIR + '/src/rapid7_data/data-{}.txt'
RDNS_FILES_NUM = len(os.listdir(RDNS_PROJ_DIR + '/src/rapid7_data'))
GEOHINT_FILE = RDNS_PROJ_DIR + '/src/georule_by_caida.json'

PPV_THRESHOLD = 0.9
DST_DIR = './result/dict_prefix_info'
os.system(f'mkdir -p {DST_DIR}')

# 执行后，dict_domain_info 包含了域名后缀的嵌套信息
# for example, two domains: a.b.c, d.b.c
# we have dict_domain_info[c][b][a], dict_domain_info[c][b][d]
dict_domain_info = {}
with open(GEOHINT_FILE, 'r') as srcfile:
    for (_, row) in enumerate(srcfile):
        one_json = ast.literal_eval(row.strip())

        # 可信值不高的要丢弃
        if float(one_json['score']['ppv']) < PPV_THRESHOLD:
            continue

        # for example, a.b.c --> dict_domain_info[c][b][a] = {'re': xx}
        now_domain_info = dict_domain_info
        for domain_split in reversed(one_json['domain'].split('.')):
            if domain_split not in now_domain_info:
                now_domain_info[domain_split] = {}
            now_domain_info = now_domain_info[domain_split]

        now_domain_info['re'] = one_json['re']
        now_domain_info['score'] = one_json['score']
        now_domain_info['geohints'] = set()
        for geohint in one_json['geohints']:
            now_domain_info['geohints'].add(geohint['code'])
            now_domain_info[geohint['code']] = geohint


def check_one_file(idx):
    print(f"RUNNING {idx} ...")
    dict_prefix_info = {}

    with open(RDNS_FILES.format(idx), 'r') as srcfile:
        for row in srcfile:
            one_json = ast.literal_eval(row.strip())
            now_ip = one_json['name']
            hostname = one_json['value']

            # 在可利用后缀字典中寻找这个 hostname 是否有可以利用的后缀
            now_domain_info = dict_domain_info
            for hostname_split in reversed(hostname.split('.')):
                if hostname_split not in now_domain_info: 
                    break
                now_domain_info = now_domain_info[hostname_split]
            if 're' not in now_domain_info: continue

            regrex_result = re.match(now_domain_info['re'][0], hostname)
            if regrex_result:
                match_word = regrex_result.group(1)
                if match_word in now_domain_info:
                    prefix = now_ip[0:now_ip.rfind('.')]
                    result = now_domain_info[match_word]

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

    pickle.dump(dict_prefix_info, open(f'{DST_DIR}/{idx}.bin', 'wb'))
    print(f"------- {idx} is OK ---------")
    return

TASK_NUM = 30
with concurrent.futures.ProcessPoolExecutor(max_workers=TASK_NUM) as executor:
    dict_prefix_info = {}
    futures = [executor.submit(check_one_file, idx) for idx in range(RDNS_FILES_NUM)]
    for future in concurrent.futures.as_completed(futures):
        future.result()
