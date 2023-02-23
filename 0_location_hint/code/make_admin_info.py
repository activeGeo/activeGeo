# 从城市定位到经纬度, 通过 Geonames 数据进行融合

import csv
import json
import ast
import glob
import pickle

BIN_DIR = '../pickle_bin'
SRC_DIR = '../src'

set_country_code = pickle.load(open(f'{BIN_DIR}/set_country_code.bin', 'rb'))

def format_name(name):
    return name.replace('-','').replace(' ','').lower()

# 导入州代码信息
dict_admin_by_country = {k:{} for k in set_country_code}
with open(f'{SRC_DIR}/admin1CodeASCII.txt', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter='\t')
    for row in spamreader:
        country_code = row[0].split('.')[0].lower()
        admin_code = row[0].split('.')[1].lower()
        admin_name = format_name(row[1])

        dict_admin_by_country[country_code][admin_code] = admin_name

# 英国的 admin Code 使用 admin2Code
dict_admin_by_country['gb'] = {}
with open(f'{SRC_DIR}/admin2CodeUK.txt', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter='\t')
    for row in spamreader:
        admin_code = row[0].split('.')[2].lower()
        admin_name = format_name(row[1])

        if len(admin_code) == 2:
            dict_admin_by_country['gb'][admin_code] = admin_name

# 保存到 pickle 中
pickle.dump(dict_admin_by_country, open(f'{BIN_DIR}/dict_admin_by_country.bin', 'wb'))
