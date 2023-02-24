# 从城市定位到经纬度, 通过 Geonames 数据进行融合

import csv
import json
import ast
import glob
import fiona
import pickle

BIN_DIR = '../pickle_bin'
SRC_DIR = '../src'

def format_name(name):
    return name.replace('-','').replace(' ','').lower()

# 导入国家代码信息
set_country_code = set()
set_country_name = set()

dict_countryname_code = {}
with open(f'{SRC_DIR}/country_code.txt', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter='\t')
    for row in spamreader:
        country_name = format_name(row[1])
        set_country_code.add(row[0].lower())
        set_country_name.add(country_name)
        dict_countryname_code[country_name] = row[0].lower()


dict_countrycode_info = {k:{} for k in set_country_code}

# RIR INFO
with open(f'{SRC_DIR}/country_rir.txt', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter='\t')
    for row in spamreader:
        code = row[1].strip().lower()
        if code not in dict_countrycode_info: continue

        rir_info = row[-1].strip().lower()
        dict_countrycode_info[code]['rir'] = rir_info


# REGION INFO
with open(f'{SRC_DIR}/country_region.json') as srcfile:
    rows = json.load(srcfile)
    for row in rows:
        code = row['alpha-2'].lower()
        if code not in dict_countrycode_info: continue

        continent_info = row['region'].lower()
        subregion_info = row['sub-region'].lower()
        dict_countrycode_info[code]['continent'] = continent_info
        dict_countrycode_info[code]['subregion'] = subregion_info

# 保存到 pickle 中
pickle.dump(set_country_code, open(f'{BIN_DIR}/set_country_code.bin', 'wb'))
pickle.dump(set_country_name, open(f'{BIN_DIR}/set_country_name.bin', 'wb'))
pickle.dump(dict_countryname_code, open(f'{BIN_DIR}/dict_countryname_code.bin', 'wb'))
pickle.dump(dict_countrycode_info, open(f'{BIN_DIR}/dict_countrycode_info.bin', 'wb'))
