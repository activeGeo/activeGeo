import os
import random
import pickle
import geopy.distance
from collections import defaultdict

BIN_DIR = os.path.expanduser(f'./pickle_bin')

dict_server_info = pickle.load(open(f'{BIN_DIR}/dict_server_info.bin', 'rb'))
dict_client_info = pickle.load(open(f'{BIN_DIR}/dict_client_info.bin', 'rb'))
dict_serverclient_rtt = pickle.load(open(f'{BIN_DIR}/dict_serverclient_rtt.bin', 'rb'))
dict_clientserver_rtt = pickle.load(open(f'{BIN_DIR}/dict_clientserver_rtt.bin', 'rb'))


'''
1. Make distance dictionary
'''
print('Making distance dictionary ...')
dict_serverclient_dis = {}
for server_ip in dict_server_info:
    dict_serverclient_dis[server_ip] = {}
    server_coor = dict_server_info[server_ip]['coordinate']
    print(f'Running {server_ip}')
    for client_ip in dict_client_info:
        client_coor = dict_client_info[client_ip]['coordinate']
        dis = geopy.distance.geodesic(server_coor, client_coor).km
        dict_serverclient_dis[server_ip][client_ip] = dis
pickle.dump(dict_serverclient_dis, open(f'{BIN_DIR}/dict_serverclient_dis.bin', 'wb'))
print('Success: Make distance dictionary.')


# '''
# 2. Make Train and Test
# '''
# TRAIN_NUM = int(len(dict_client_info) * 0.8)

# ok_train_set = set(random.sample([*dict_client_info], TRAIN_NUM))
# ok_test_set  = dict_client_info.keys() - ok_train_set

# print('length of train:', len(ok_train_set))
# print('length of test:', len(ok_test_set))

# pickle.dump(ok_train_set, open(f'{DST_DIR}/ok_train_set.bin', 'wb'))
# pickle.dump(ok_test_set, open(f'{DST_DIR}/ok_test_set.bin', 'wb'))


# '''
# 3. Make RTT data
# '''
# # 按照 NAN 填充
# import math
# print('Imputing with nan ...')

# now_rtt_dict = {k:{} for k in dict_client_info}
# for client_ip in dict_client_info:
#     now_rtt_dict[client_ip].update(dict_clientserver_rtt[client_ip])
    
#     bad_server_set = dict_server_info.keys() - dict_clientserver_rtt[client_ip].keys()
#     for server_ip in bad_server_set:
#         now_rtt_dict[client_ip][server_ip] = math.nan            
# pickle.dump(now_rtt_dict, open(f'{DST_DIR}/dict_nan_rtt.bin', 'wb'))

# # 按照 MEAN 填充
# import statistics
# print('Imputing with mean ...')

# server_mean_dict = {}
# for server_ip in dict_server_info: 
#     server_mean_dict[server_ip] = statistics.mean(dict_serverclient_rtt[server_ip].values())

# client_mean_dict = {}
# for client_ip in dict_client_info:
#     client_mean_dict[client_ip] = statistics.mean(dict_clientserver_rtt[client_ip].values())

# now_rtt_dict = {k:{} for k in dict_client_info}    
# for client_ip in dict_client_info:
#     now_rtt_dict[client_ip].update(dict_clientserver_rtt[client_ip])
    
#     bad_server_set = dict_server_info.keys() - dict_clientserver_rtt[client_ip].keys()
#     for server_ip in bad_server_set:
#         now_rtt_dict[client_ip][server_ip] = (server_mean_dict[server_ip] + client_mean_dict[client_ip]) / 2            
# pickle.dump(now_rtt_dict, open(f'{DST_DIR}/dict_mean_rtt.bin', 'wb'))



# # 按照 MEDIAN 填充
# import statistics
# print('Imputing with median ...')

# server_median_dict = {}
# for server_ip in dict_server_info: 
#     server_median_dict[server_ip] = statistics.median(dict_serverclient_rtt[server_ip].values())

# client_median_dict = {}
# for client_ip in dict_client_info:
#     client_median_dict[client_ip] = statistics.median(dict_clientserver_rtt[client_ip].values())

# now_rtt_dict = {k:{} for k in dict_client_info}    
# for client_ip in dict_client_info:
#     now_rtt_dict[client_ip].update(dict_clientserver_rtt[client_ip])
    
#     bad_server_set = dict_server_info.keys() - dict_clientserver_rtt[client_ip].keys()
#     for server_ip in bad_server_set:
#         now_rtt_dict[client_ip][server_ip] = (server_median_dict[server_ip] + client_median_dict[client_ip]) / 2            
# pickle.dump(now_rtt_dict, open(f'{DST_DIR}/dict_median_rtt.bin', 'wb'))

