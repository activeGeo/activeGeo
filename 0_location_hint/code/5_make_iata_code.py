import os
import re
import csv
import json
import ast
import glob
import pickle

BIN_DIR = '../pickle_bin'
SRC_DIR = '../src'

def format_name(name):
    return name.replace('-', '').replace(' ', '').lower()

dict_city_by_name = pickle.load(open(f'{BIN_DIR}/dict_city_by_name.bin', 'rb'))
set_blackwords = pickle.load(open(f'{BIN_DIR}/set_blackwords.bin', 'rb'))

dict_iata_code = {}
airport_code_str = r'<div class="airport-info-table">([\s\S]+?)</div>'
airport_location_str = r'<p class="subheader">([\s\S]+?)</p>'
iata_code_str = r'IATA Code([\s\S]+?)</span>'
for path, dir_list, file_list in os.walk(f'{SRC_DIR}/pages_offline'):
    for filename in file_list:
        contents = open(os.path.join(path, filename), 'r').read()
        # 先找到可能包含代码信息和地址信息的字符串
        codes_list = re.findall(airport_code_str, contents)
        locations_list = re.findall(airport_location_str, contents)
        # 去除那些假的字符串, 即要求必须是 cityname, country (country_code) 形式
        locations_list = [x for x in locations_list if ',' in x and '(' in x]

        for codes, locations in zip(codes_list, locations_list):
            # 寻找括号中的内容
            country_code = locations[locations.find('(')+1: locations.find(')')].lower()
            # 寻找城市名
            cityname = format_name(locations.strip().split(',')[0])
            # 寻找 IATA 代码, 如果为空 该部分为 <span "">
            iata_code = re.findall(iata_code_str, codes)[-1][-3:].lower()

            if iata_code[-1] != '>' and cityname in dict_city_by_name:
                city_info = dict_city_by_name[cityname]
                if country_code == city_info[1] and iata_code not in set_blackwords:
                    dict_iata_code[iata_code] = city_info

# 保存到 pickle 中
pickle.dump(dict_iata_code, open(f'{BIN_DIR}/dict_iata_code.bin', 'wb'))
