import os
import re
import csv
import json
import pickle

dict_city_by_country = pickle.load(open('../bin/dict_city_by_country.bin', 'rb'))

dict_unlocode_code = {}
# 导入 CLLI 代码信息
for i in range(1, 4):
    with open(f'../UNLOCODE_{i}.csv', newline='', encoding='latin1') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            if row[-2] == '': continue
            country_code = row[1].lower()
            city_name = row[3].lower()

            if country_code in dict_city_by_country and \
                    city_name in dict_city_by_country[country_code]:
                city_info = dict_city_by_country[country_code][city_name]
                dict_unlocode_code[country_code+row[2].lower()] = city_info
pickle.dump(dict_unlocode_code, open('../bin/dict_unlocode_code.bin', 'wb'))
