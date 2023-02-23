import os
import re
import csv
import json
import pickle
import reverse_geocode

BIN_DIR = '../pickle_bin'
SRC_DIR = '../src'

dict_clli_code = {}
# 导入 CLLI 代码信息
with open(f'{SRC_DIR}/clli_first6_1.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter='\t')
    for row in spamreader:
        coor = (float(row[1]), float(row[2]))
        coor_info = reverse_geocode.search((coor,))[0]
        country_code = coor_info['country_code'].lower()
        city_name = coor_info['city'].lower()

        clli_code = row[0].lower()
        dict_clli_code[clli_code] = (coor, country_code, None, city_name, None)

# 有些 CCLI 代码没有在上一个文件中，手动进行了查找，导入该部分信息
with open(f'{SRC_DIR}/clli_first6_2.txt', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    next(spamreader)
    for row in spamreader:
        clli_code = row[0].lower()
        coor = (float(row[3]), float(row[4]))
        dict_clli_code[clli_code] = (coor, row[5].lower(), None, row[1].lower(), None)

pickle.dump(dict_clli_code, open(f'{BIN_DIR}/dict_clli_code.bin', 'wb'))
