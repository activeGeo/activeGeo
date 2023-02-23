import os
import time
import pickle
import requests
from functools import partial

 
LG_DIR = '../../'
FORMER_RESULT_DIR = '../4_filter_by_api/result'

MACHINE_IP = '198.13.38.108'

# 1. use api to geolocate successfully
# 2. cannot use api
DST_FILES_DIR = f'{LG_DIR}/pickle_bin/'
os.system(f'mkdir -p {DST_FILES_DIR}')

requests_get = partial(requests.get, timeout=15, verify=False)
requests_post = partial(requests.post, timeout=15, verify=False)

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
        time_str_list = [ s for s in req.text.split() if 'time' in s ]
        return req.text
    except:
        pass
    return ''

def test_api_2(website, client_ip='8.8.8.8', items=None):
    try:
        ping_str = make_ping_str(website)
        ping_str += '?command=ping&protocol=ipv4&query={}&router='
        ping_str += items[1].replace(' ', '+')
        req = requests_get(ping_str.format(client_ip), timeout=10)
        return req.text
    except:
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
    except:
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
    except:
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

input_list = pickle.load(open(f'{FORMER_RESULT_DIR}/list_good_routers.bin', 'rb'))
RECORD_FILE = open('./send.txt', 'w')
print('src: ', len(input_list))
for idx, one_router in enumerate(input_list):
    print(idx)
    time.sleep(7)
    begin_time = str(time.time())
    test_api = list_test_api[one_router['api_type']]
    test_api(one_router['website'], client_ip=MACHINE_IP, items=one_router['geohint'])
    end_time = str(time.time())
    RECORD_FILE.writelines('\t'.join([begin_time, end_time, str(idx)]) + '\n')
