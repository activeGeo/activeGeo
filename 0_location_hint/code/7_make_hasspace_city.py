# 从城市定位到经纬度, 通过 Geonames 数据进行融合

import csv
import json
import ast
import glob
import pickle

BIN_DIR = '../pickle_bin'
SRC_DIR = '../src'

dict_city_by_name = pickle.load(open(f'{BIN_DIR}/dict_city_by_name.bin', 'rb'))

# 导入城市信息
CITY_FILE = f'{SRC_DIR}/cities1000.txt'
POPULATION_THRESHOLD = 200000

dict_hasspace_city = dict()
with open(CITY_FILE, newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter='\t')
    for row in spamreader:
        if int(row[14]) < POPULATION_THRESHOLD: continue

        set_name = set()
        # append city_name, ascii_name, alter_name
        if row[1] != '': set_name.add(row[1].lower())
        if row[2] != '': set_name.add(row[2].lower())
        if row[3] != '': set_name.update([x.lower() for x in row[3].split(',')])

        for name in set_name:
            if ' ' in name and name.isascii():
                good_name = name.replace('-', '').replace(' ', '')
                if good_name in dict_city_by_name:
                    dict_hasspace_city[name] = dict_city_by_name[good_name]

dict_hasspace_city['los angles'] = dict_hasspace_city['los angeles']
print(len(dict_hasspace_city))
pickle.dump(dict_hasspace_city, open(f'{BIN_DIR}/dict_hasspace_city.bin', 'wb'))
