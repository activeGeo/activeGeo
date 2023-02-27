import os
import pickle

BIN_DIR = os.path.expanduser(f'../pickle_bin')

dict_client_info = pickle.load(open(f'{BIN_DIR}/dict_client_info.bin', 'rb'))
ok_train_list = pickle.load(open(f'{BIN_DIR}/ok_train_list.bin', 'rb'))
ok_test_list  = pickle.load(open(f'{BIN_DIR}/ok_test_list.bin', 'rb'))

dict_countrycode_info = pickle.load(open(f'{BIN_DIR}/dict_countrycode_info.bin', 'rb'))

for country_code in dict_countrycode_info:
    dict_countrycode_info[country_code]['none'] = 'World'

print('Generating region information ...')

for r_type in ['none', 'rir', 'continent', 'subregion']:

    region_set = set()
    for client_ip in (ok_train_list + ok_test_list):
        country_code = dict_client_info[client_ip]['country_code'].lower()
        region_name = dict_countrycode_info[country_code][r_type]
        region_set.add(region_name)

    region_idx_dict = dict()
    for i, region_name in enumerate(region_set):
        region_idx_dict[region_name] = i

    pickle.dump(region_idx_dict, open(f'{BIN_DIR}/dict_region_idx_{r_type}.bin', 'wb'))


    client_region_dict = dict()
    for client_ip in (ok_train_list + ok_test_list):
        country_code = dict_client_info[client_ip]['country_code'].lower()
        region_name = dict_countrycode_info[country_code][r_type]

        client_region_dict[client_ip] = [ 0 for i in region_idx_dict ]
        client_region_dict[client_ip][region_idx_dict[region_name]] = 1

    pickle.dump(client_region_dict, open(f'{BIN_DIR}/dict_client_region_{r_type}.bin', 'wb'))
    print(f'Success: generating region information BY {r_type}')
