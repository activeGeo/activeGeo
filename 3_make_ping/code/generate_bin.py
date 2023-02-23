import os
import pickle
import geopy.distance

ok_server_dict = pickle.load(open('../src/ok_server_dict.bin', 'rb'))
ok_client_dict = pickle.load(open('../src/raw_client_dict.bin', 'rb'))

serverclient_rtt_dict = {k:{} for k in ok_server_dict}
server_ips = [x[0:-4] for x in os.listdir('./result')]
for server_ip in server_ips:
    with open(f'./result/{server_ip}.txt', 'r') as srcfile:
        for row in srcfile:
            info = row.strip().split('\t')
            if info[0] not in ok_client_dict: continue

            rtts = eval(info[1])
            rtt  = min(rtts[:-1]) if len(rtts) > 1 else rtts[0]
            serverclient_rtt_dict[server_ip][info[0]] = rtt

pickle.dump(serverclient_rtt_dict, open('../pickle_bin/serverclient_rtt_dict.bin', 'wb'))

clientserver_rtt_dict = {k:{} for k in ok_client_dict}
for server_ip in serverclient_rtt_dict:
    for client_ip in serverclient_rtt_dict[server_ip]:
        info = serverclient_rtt_dict[server_ip][client_ip]
        clientserver_rtt_dict[client_ip][server_ip] = info

pickle.dump(clientserver_rtt_dict, open('../pickle_bin/clientserver_rtt_dict.bin', 'wb'))
