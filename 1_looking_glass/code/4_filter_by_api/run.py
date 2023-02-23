import os
import re
import pickle
import requests
from functools import partial

FORMER_RESULT_DIR = '../3_filter_by_geoinfo/result'

# 1. use api to geolocate successfully
# 2. cannot use api
DST_FILES_DIR = f'./result/'
os.system(f'mkdir -p {DST_FILES_DIR}')

requests_get = partial(requests.get, timeout=10, verify=False)
requests_post = partial(requests.post, timeout=10, verify=False)

list_good_routers = []
list_bad_routers = []

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

list_test_api = [
    test_api_0, 
    test_api_1, 
    test_api_2, 
    test_api_3,
    test_api_4,
    test_api_5,
]

TIME_REGREX = r'min(.?/)avg.?/max.*?=(.+?)ms'
input_list = pickle.load(open(f'{FORMER_RESULT_DIR}/list_good_routers.bin', 'rb'))

for idx, one_router in enumerate(input_list):
    print(idx)
    print(one_router)
    for jdx, test_api in enumerate(list_test_api):
        print('--> ', jdx)

        if 'looking.house' in one_router['website'] and jdx != 4:
            continue

        if '' != one_router['geohint'][0] and 0 == jdx:
            continue

        raw_text = test_api(one_router['website'], items=one_router['geohint'])
        try:
            [split_word, time_word] = re.findall(TIME_REGREX, raw_text)[0]
            result = [float(x.strip()) for x in time_word.split(split_word)]
            if len(result):
                one_router['api_type'] = jdx
                print(f'FIND! the api type of {idx} is {jdx}')
                break
        except Exception as e:
            pass
    if 'api_type' in one_router:
        list_good_routers.append(one_router)
    else:
        list_bad_routers.append(one_router)

print('dst: ', len(list_good_routers))
pickle.dump(list_good_routers, open(f'{DST_FILES_DIR}/list_good_routers.bin', 'wb'))
pickle.dump(list_bad_routers, open(f'{DST_FILES_DIR}/list_bad_routers.bin', 'wb'))
