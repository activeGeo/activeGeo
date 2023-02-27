import os
import pickle
import geopy.distance

BIN_DIR = os.path.expanduser(f'../pickle_bin')

dict_server_info = pickle.load(open(f'{BIN_DIR}/dict_server_info.bin', 'rb'))
dict_client_info = pickle.load(open(f'{BIN_DIR}/dict_client_info.bin', 'rb'))


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
