import os
import random
import pickle
from collections import defaultdict

SRC_DIR = os.path.expanduser(f'./src/')
DST_DIR = os.path.expanduser(f'./pickle_bin')

dict_server_info = pickle.load(open(f'{SRC_DIR}/dict_server_info.bin', 'rb'))
dict_client_info = pickle.load(open(f'{SRC_DIR}/dict_client_info.bin', 'rb'))
serverclient_rtt_dict = pickle.load(open(f'{SRC_DIR}/serverclient_rtt_dict.bin', 'rb'))
clientserver_rtt_dict = pickle.load(open(f'{SRC_DIR}/clientserver_rtt_dict.bin', 'rb'))


'''
1. Make coordinate dictionary
'''
dict_server_coor = {}
for server_ip in dict_server_info:
    print(dict_server_info[server_ip])
    dict_server_coor[server_ip] = dict_server_info[server_ip]['coordinate']

dict_client_coor = {}
for client_ip in dict_client_info:
    dict_client_coor[client_ip] = dict_client_info[client_ip]['coordinate']

pickle.dump(dict_server_coor, open(f'{DST_DIR}/dict_server_coor.bin', 'wb'))
pickle.dump(dict_client_coor, open(f'{DST_DIR}/dict_client_coor.bin', 'wb'))

'''
2. Make Train and Test
'''
TRAIN_NUM = int(len(dict_client_info) * 0.8)

ok_train_set = set(random.sample([*dict_client_info], TRAIN_NUM))
ok_test_set  = dict_client_info.keys() - ok_train_set

print('length of train:', len(ok_train_set))
print('length of test:', len(ok_test_set))

pickle.dump(ok_train_set, open(f'{DST_DIR}/ok_train_set.bin', 'wb'))
pickle.dump(ok_test_set, open(f'{DST_DIR}/ok_test_set.bin', 'wb'))


'''
3. Make RTT data
'''
# 按照 NAN 填充
import math
print('Imputing with nan ...')

now_rtt_dict = {k:{} for k in dict_client_info}
for client_ip in dict_client_info:
    now_rtt_dict[client_ip].update(clientserver_rtt_dict[client_ip])
    
    bad_server_set = dict_server_info.keys() - clientserver_rtt_dict[client_ip].keys()
    for server_ip in bad_server_set:
        now_rtt_dict[client_ip][server_ip] = math.nan            
pickle.dump(now_rtt_dict, open(f'{DST_DIR}/nan_rtt_dict.bin', 'wb'))

# 按照 MEAN 填充
import statistics
print('Imputing with mean ...')

server_mean_dict = {}
for server_ip in dict_server_info: 
    server_mean_dict[server_ip] = statistics.mean(serverclient_rtt_dict[server_ip].values())

client_mean_dict = {}
for client_ip in dict_client_info:
    client_mean_dict[client_ip] = statistics.mean(clientserver_rtt_dict[client_ip].values())

now_rtt_dict = {k:{} for k in dict_client_info}    
for client_ip in dict_client_info:
    now_rtt_dict[client_ip].update(clientserver_rtt_dict[client_ip])
    
    bad_server_set = dict_server_info.keys() - clientserver_rtt_dict[client_ip].keys()
    for server_ip in bad_server_set:
        now_rtt_dict[client_ip][server_ip] = (server_mean_dict[server_ip] + client_mean_dict[client_ip]) / 2            
pickle.dump(now_rtt_dict, open(f'{DST_DIR}/mean_rtt_dict.bin', 'wb'))



# 按照 MEDIAN 填充
import statistics
print('Imputing with median ...')

server_median_dict = {}
for server_ip in dict_server_info: 
    server_median_dict[server_ip] = statistics.median(serverclient_rtt_dict[server_ip].values())

client_median_dict = {}
for client_ip in dict_client_info:
    client_median_dict[client_ip] = statistics.median(clientserver_rtt_dict[client_ip].values())

now_rtt_dict = {k:{} for k in dict_client_info}    
for client_ip in dict_client_info:
    now_rtt_dict[client_ip].update(clientserver_rtt_dict[client_ip])
    
    bad_server_set = dict_server_info.keys() - clientserver_rtt_dict[client_ip].keys()
    for server_ip in bad_server_set:
        now_rtt_dict[client_ip][server_ip] = (server_median_dict[server_ip] + client_median_dict[client_ip]) / 2            
pickle.dump(now_rtt_dict, open(f'{DST_DIR}/median_rtt_dict.bin', 'wb'))

