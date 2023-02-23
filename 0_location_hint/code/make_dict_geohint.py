import csv
import json
import ast
import pickle

BIN_DIR = '../pickle_bin'
SRC_DIR = '../src'

def format_name(name):
    return name.replace('-','').replace(' ','').lower()

dict_city_by_country = pickle.load(open(f'{BIN_DIR}/dict_city_by_country.bin', 'rb'))

dict_geohint_by_country = {}
for country_code in dict_city_by_country:
    dict_geohint_by_country[country_code] = {}
    for name in dict_city_by_country[country_code]:
        city_info = dict_city_by_country[country_code][name]
        dict_geohint_by_country[country_code][name] = city_info
        dict_geohint_by_country[country_code][name+city_info[1]] = city_info
        if city_info[2]:
            dict_geohint_by_country[country_code][name+city_info[2]] = city_info

# 保存到 pickle 中
pickle.dump(dict_geohint_by_country, open(f'{BIN_DIR}/dict_geohint_by_country.bin', 'wb'))
