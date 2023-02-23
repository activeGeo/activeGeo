# client 的 region info

import os
import pickle
from collections import defaultdict

TYPE = 'test01'

BIN_DIR = os.path.expanduser(f'~/ipgeo/pickle_bin/{TYPE}')
GEOINFO_DIR = os.path.expanduser(f'~/geoinfo/bin')

print('Loading pickle ...')

ok_server_dict    = pickle.load(open(f'{BIN_DIR}/ok_server_dict.bin', 'rb'))
ok_client_dict    = pickle.load(open(f'{BIN_DIR}/ok_client_dict.bin', 'rb'))
ok_train_set = pickle.load(open(f'{BIN_DIR}/ok_train_set.bin', 'rb'))
ok_test_set  = pickle.load(open(f'{BIN_DIR}/ok_test_set.bin', 'rb'))

dict_country_region = pickle.load(open(f'{GEOINFO_DIR}/dict_country_region.bin', 'rb'))
print('Success: loading pickle')
print()
print('Generating region information ...')

# dict_country_class = dict_country_rir
country_class_dict = dict_country_region

region_set = set()
for client_ip in (ok_train_set | ok_test_set):
    country_code = ok_client_dict[client_ip]['country_code'].lower()
    region_name = country_class_dict[country_code]
    region_set.add(region_name)

region_idx_dict = dict()
for i, region_name in enumerate(region_set):
    region_idx_dict[region_name] = i

pickle.dump(region_idx_dict, open(f'{BIN_DIR}/region_idx_dict.bin', 'wb'))


client_region_dict = dict()
for client_ip in (ok_train_set | ok_test_set):
    country_code = ok_client_dict[client_ip]['country_code'].lower()
    region_name = country_class_dict[country_code]

    client_region_dict[client_ip] = [ 0 for i in region_idx_dict ]
    client_region_dict[client_ip][region_idx_dict[region_name]] = 1

pickle.dump(client_region_dict, open(f'{BIN_DIR}/client_region_dict.bin', 'wb'))
print('Success: generating region information')
