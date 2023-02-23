import os
import random
import pickle
from collections import defaultdict

SRC_DIR = os.path.expanduser(f'../3_make_ping/pickle_bin/')
DST_DIR = os.path.expanduser(f'./pickle_bin')

os.system(f'ln -sf {SRC_DIR}/ok_server_dict.bin {DST_DIR}/ok_server_dict.bin')
os.system(f'ln -sf {SRC_DIR}/raw_client_dict.bin {DST_DIR}/raw_client_dict.bin')
os.system(f'ln -sf {SRC_DIR}/serverclient_rtt_dict.bin {DST_DIR}/serverclient_rtt_dict.bin')
os.system(f'ln -sf {SRC_DIR}/clientserver_rtt_dict.bin {DST_DIR}/clientserver_rtt_dict.bin')

ok_client_dict = pickle.load(open(f'{DST_DIR}/raw_client_dict.bin', 'rb'))
TRAIN_NUM = int(len(ok_client_dict) * 0.8)

ok_train_set = set(random.sample([*ok_client_dict], TRAIN_NUM))
ok_test_set  = ok_client_dict.keys() - ok_train_set

print('length of train:', len(ok_train_set))
print('length of test:', len(ok_test_set))

pickle.dump(ok_train_set, open(f'{DST_DIR}/ok_train_set.bin', 'wb'))
pickle.dump(ok_test_set, open(f'{DST_DIR}/ok_test_set.bin', 'wb'))


ok_server_dict = pickle.load(open(f'{DST_DIR}/ok_server_dict.bin', 'rb'))
ok_client_dict = pickle.load(open(f'{DST_DIR}/ok_client_dict.bin', 'rb'))

serverclient_rtt_dict = pickle.load(open(f'{DST_DIR}/serverclient_rtt_dict.bin', 'rb'))
clientserver_rtt_dict = pickle.load(open(f'{DST_DIR}/clientserver_rtt_dict.bin', 'rb'))

print('Save RTT Now ...')

# 按照 NAN 填充
import math

now_rtt_dict = {k:{} for k in ok_client_dict}
for client_ip in ok_client_dict:
    now_rtt_dict[client_ip].update(clientserver_rtt_dict[client_ip])
    
    bad_server_set = ok_server_dict.keys() - clientserver_rtt_dict[client_ip].keys()
    for server_ip in bad_server_set:
        now_rtt_dict[client_ip][server_ip] = math.nan            
pickle.dump(now_rtt_dict, open(f'{DST_DIR}/nan_rtt_dict.bin', 'wb'))

print('Imputing with nan')


# 按照 MEAN 填充
import statistics

server_mean_dict = {}
for server_ip in ok_server_dict: 
    server_mean_dict[server_ip] = statistics.mean(serverclient_rtt_dict[server_ip].values())

client_mean_dict = {}
for client_ip in ok_client_dict:
    client_mean_dict[client_ip] = statistics.mean(clientserver_rtt_dict[client_ip].values())

now_rtt_dict = {k:{} for k in ok_client_dict}    
for client_ip in ok_client_dict:
    now_rtt_dict[client_ip].update(clientserver_rtt_dict[client_ip])
    
    bad_server_set = ok_server_dict.keys() - clientserver_rtt_dict[client_ip].keys()
    for server_ip in bad_server_set:
        now_rtt_dict[client_ip][server_ip] = (server_mean_dict[server_ip] + client_mean_dict[client_ip]) / 2            
pickle.dump(now_rtt_dict, open(f'{DST_DIR}/mean_rtt_dict.bin', 'wb'))

print('Imputing with mean')


# 按照 MEAN 填充
import statistics

server_median_dict = {}
for server_ip in ok_server_dict: 
    server_median_dict[server_ip] = statistics.median(serverclient_rtt_dict[server_ip].values())

client_median_dict = {}
for client_ip in ok_client_dict:
    client_median_dict[client_ip] = statistics.median(clientserver_rtt_dict[client_ip].values())

now_rtt_dict = {k:{} for k in ok_client_dict}    
for client_ip in ok_client_dict:
    now_rtt_dict[client_ip].update(clientserver_rtt_dict[client_ip])
    
    bad_server_set = ok_server_dict.keys() - clientserver_rtt_dict[client_ip].keys()
    for server_ip in bad_server_set:
        now_rtt_dict[client_ip][server_ip] = (server_median_dict[server_ip] + client_median_dict[client_ip]) / 2            
pickle.dump(now_rtt_dict, open(f'{DST_DIR}/median_rtt_dict.bin', 'wb'))

print('Imputing with median')
