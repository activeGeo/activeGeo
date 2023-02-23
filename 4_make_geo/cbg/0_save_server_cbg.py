import pickle
import os
import numpy as np
from CBG import CBG
import concurrent.futures

import sys
SRC_TYPE = sys.argv[1]

DST_PATH = f'./pickle_bin/{SRC_TYPE}'
os.system(f'mkdir -p {DST_PATH}')

RTT_MIN = -1
RTT_MAX = 0

BIN_PATH = os.path.expanduser(f'~/ipgeo/pickle_bin/{SRC_TYPE}')

ok_server_dict = pickle.load(open(f'{BIN_PATH}/ok_server_dict.bin', 'rb'))
serverclient_rtt_dict = pickle.load(open(f'{BIN_PATH}/serverclient_rtt_dict.bin', 'rb'))
serverclient_dis_dict = pickle.load(open(f'{BIN_PATH}/serverclient_dis_dict.bin', 'rb'))

def train_one_server(tuple_parm):
    (server_ip, clients) = tuple_parm
    x = np.array([])
    y = np.array([])

    for client_ip in clients:
        if client_ip not in serverclient_rtt_dict[server_ip]: 
            continue

        rtt = serverclient_rtt_dict[server_ip][client_ip]
        dis = serverclient_dis_dict[server_ip][client_ip]

        if RTT_MIN < rtt < RTT_MAX: continue
        x = np.append(x, dis)
        y = np.append(y, rtt)
    
    obs = np.vstack((x, y))
    return CBG(obs, False)

for idx in range(0, 6):
    print(idx)
    ok_train_set = set(pickle.load(open(f'{BIN_PATH}/ok_train_list_{idx}.bin', 'rb')))

    server_cbg_dict = dict()
    TASK_NUM = 30

    # 训练得到 CBG
    task_server_dict = dict()
    with concurrent.futures.ProcessPoolExecutor(max_workers=TASK_NUM) as executor:
        tasks_list = []
        for server_ip in ok_server_dict:
            one_task = executor.submit(train_one_server, (server_ip, ok_train_set)) 
            tasks_list.append(one_task)
            task_server_dict[one_task] = server_ip

        for one_task in concurrent.futures.as_completed(tasks_list):
            server_ip = task_server_dict[one_task]
            server_cbg_dict[server_ip] = one_task.result()
    pickle.dump(server_cbg_dict, open(f'{DST_PATH}/server_cbg_dict_rtt_{idx}_{RTT_MAX}.bin', 'wb'))
