# client 的 region info

import os
import pickle
from collections import defaultdict

BIN_DIR = os.path.expanduser(f'../pickle_bin')

print('Loading pickle ...')

dict_client_info = pickle.load(open(f'{BIN_DIR}/dict_client_info.bin', 'rb'))
ok_train_list = pickle.load(open(f'{BIN_DIR}/ok_train_list.bin', 'rb'))
ok_test_list  = pickle.load(open(f'{BIN_DIR}/ok_test_list.bin', 'rb'))

dict_countrycode_info = pickle.load(open(f'{BIN_DIR}/dict_countrycode_info.bin', 'rb'))

print('Success: loading pickle')
print()
print('Generating region information ...')

# dict_country_class = dict_country_rir
country_class_dict = dict_country_region

region_set = set()
for client_ip in (ok_train_list + ok_test_list):
    country_code = dict_client_info[client_ip]['country_code'].lower()
    region_name = country_class_dict[country_code]
    region_set.add(region_name)

region_idx_dict = dict()
for i, region_name in enumerate(region_set):
    region_idx_dict[region_name] = i

pickle.dump(region_idx_dict, open(f'{BIN_DIR}/region_idx_dict.bin', 'wb'))


client_region_dict = dict()
for client_ip in (ok_train_list + ok_test_list):
    country_code = dict_client_info[client_ip]['country_code'].lower()
    region_name = country_class_dict[country_code]

    client_region_dict[client_ip] = [ 0 for i in region_idx_dict ]
    client_region_dict[client_ip][region_idx_dict[region_name]] = 1

pickle.dump(client_region_dict, open(f'{BIN_DIR}/client_region_dict.bin', 'wb'))
print('Success: generating region information')
