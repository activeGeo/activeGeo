import os
import pickle
import geopy.distance

# Parameters
SRC_DIR = '../'
DATA_DIR = './result'
DST_DIR = '../pickle_bin'
TASK_NUM = 30 * 2

ok_server_dict = pickle.load(open(f'{SRC_DIR}/ok_server_dict.bin', 'rb'))
ok_client_dict = pickle.load(open(f'{SRC_DIR}/ok_client_dict.bin', 'rb'))

dict_serverclient_rtt = {k:{} for k in ok_server_dict}
server_ips = [x[0:-4] for x in os.listdir(DATA_DIR)]
for server_ip in server_ips:
    with open(f'{DATA_DIR}/{server_ip}.txt', 'r') as srcfile:
        for row in srcfile:
            info = row.strip().split('\t')
            if info[0] not in ok_client_dict: continue

            rtts = eval(info[1])
            rtt  = min(rtts[:-1]) if len(rtts) > 1 else rtts[0]
            dict_serverclient_rtt[server_ip][info[0]] = rtt

pickle.dump(dict_serverclient_rtt, open(f'{DST_DIR}/dict_serverclient_rtt.bin', 'wb'))

dict_clientserver_rtt = {k:{} for k in ok_client_dict}
for server_ip in dict_serverclient_rtt:
    for client_ip in dict_serverclient_rtt[server_ip]:
        info = dict_serverclient_rtt[server_ip][client_ip]
        dict_clientserver_rtt[client_ip][server_ip] = info

pickle.dump(dict_clientserver_rtt, open(f'{DST_DIR}/dict_clientserver_rtt.bin', 'wb'))
