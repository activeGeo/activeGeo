import os
import re
import pickle
import random
import requests
import concurrent.futures
from functools import partial

# Parameters
SRC_DIR = '../src'
DST_DIR = './result'
TASK_NUM = 30 * 2

dict_server_info = pickle.load(open(f'{SRC_DIR}/dict_server_info.bin', 'rb'))
dict_client_info = pickle.load(open(f'{SRC_DIR}/dict_client_info.bin', 'rb'))
print('client: ', len(dict_client_info))

os.system(f'mkdir -p {DST_DIR}')

requests_get = partial(requests.get, timeout=10, verify=False)
requests_post = partial(requests.post, timeout=10, verify=False)

def make_ping_str(website):
    if '.php' in website.split('/')[-1]:
        website = website[:website.rfind('/')]
    if '?lang=' in website:
        website = website[:website.rfind('?lang=')]
    if website[-1] != '/':
        website = website + '/'
    return website

def test_api_0(website, client_ip='8.8.8.8', items=None):
    try:
        ping_str = make_ping_str(website) 
        ping_str += 'ajax.php?cmd=ping&host={}'
        req = requests_get(ping_str.format(client_ip))
        return req.text
    except Exception as e:
        pass
    return ''

def test_api_1(website, client_ip='8.8.8.8', items=None):
    try:
        ping_str = make_ping_str(website)
        ping_str += '?query=ping&protocol=IPv4&addr={}&router='
        ping_str += items[1].replace(' ', '+')
        req = requests_get(ping_str.format(client_ip))
        return req.text
    except Exception as e:
        pass
    return ''

def test_api_2(website, client_ip='8.8.8.8', items=None):
    try:
        ping_str = make_ping_str(website)
        ping_str += '?command=ping&protocol=ipv4&query={}&router='
        ping_str += items[1].replace(' ', '+')
        req = requests_get(ping_str.format(client_ip), timeout=10)
        return req.text
    except Exception as e:
        pass
    return ''

def test_api_3(website, client_ip='8.8.8.8', items=None):
    try:
        ping_str = make_ping_str(website)
        ping_json = {
            'query': 'ping',
            'protocol': 'IPv4',
            'addr': client_ip,
            'router': items[1].replace(' ', '+'),
        }
        req = requests_post(ping_str, data=ping_json)
        return req.text
    except Exception as e:
        pass
    return ''

def test_api_4(website, client_ip='8.8.8.8', items=None):
    try:
        ping_str = make_ping_str(website)
        ping_str += 'action.php?mode=looking_glass&action=ping'
        ping_json = {
            'id': items[1],
            'domain': client_ip,
        }
        req = requests_post(ping_str, data=ping_json)
        return req.text
    except Exception as e:
        pass
    return ''

def test_api_5(website, client_ip='8.8.8.8', items=None):
    try:
        ping_str = make_ping_str(website)
        ping_str += 'execute.php'
        ping_json = {
            'routers': items[1].replace(' ', '+'),
            'query': 'ping',
            'parameter': client_ip,
            'dontlook': '',
        }
        req = requests_post(ping_str, data=ping_json)
        return req.text
    except Exception as e:
        pass
    return ''

api_func_list = [
    test_api_0, 
    test_api_1, 
    test_api_2, 
    test_api_3,
    test_api_4,
    test_api_5,
]

pairs = []
for server_ip in dict_server_info:
    for client_ip in dict_client_info:
        pairs.append((server_ip, client_ip))
random.shuffle(pairs)
print(f'Number of pairs: {len(pairs)}')

TIME_REGREX = r'min(.?/)avg.?/max.*?=(.+?)ms'
def request_one_pair(one_pair):
    server_ip, client_ip = one_pair

    server_info = dict_server_info[server_ip]
    api_type  = dict_server_info[server_ip]['api_type']

    req = None
    try:
        make_api_func = api_func_list[api_type]
        raw_text = make_api_func(server_info['website'], client_ip, server_info['geohint'])
        [split_word, time_word] = re.findall(TIME_REGREX, raw_text)[0]
        result = [float(x.strip()) for x in time_word.split(split_word)]
        return result if len(result) else None
    except:
        return None

executor = concurrent.futures.ThreadPoolExecutor(max_workers=TASK_NUM)

tasks_parm = {}
for one_pair in pairs:
    one_task = executor.submit(request_one_pair, one_pair)
    tasks_parm[one_task] = one_pair

for one_task in concurrent.futures.as_completed(tasks_parm.keys()):
    one_pair = tasks_parm[one_task]
    with open(f'{DST_DIR}/{one_pair[0]}.txt', 'a') as srcfile:
        rtt_list = one_task.result()
        if rtt_list:
            srcfile.writelines(one_pair[1] + '\t' + str(rtt_list) + '\n')
