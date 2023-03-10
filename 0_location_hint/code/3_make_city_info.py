# 从城市定位到经纬度, 通过 Geonames 数据进行融合

import csv
import json
import ast
import glob
import pickle

BIN_DIR = '../pickle_bin'
SRC_DIR = '../src'

NAME_MIN_LEN = 4

def format_name(name):
    return name.replace('-','').replace(' ','').lower()

# if ascii, len should > NAME_MIN_LEN, else good
def is_good_name(name):
    not_ascii_name = {x for x in name if ord(x) >= 128}
    if len(not_ascii_name) == 0:
        return len(name) >= NAME_MIN_LEN
    return True
    # else:
    #     return all(u'\u4e00' < c < u'\u9fff' for c in not_ascii_name)


set_blackwords = pickle.load(open(f'{BIN_DIR}/set_blackwords.bin', 'rb'))
set_country_code = pickle.load(open(f'{BIN_DIR}/set_country_code.bin', 'rb'))
dict_admin_by_country = pickle.load(open(f'{BIN_DIR}/dict_admin_by_country.bin', 'rb'))

# 导入城市信息
CITY_FILE = f'{SRC_DIR}/cities1000.txt'
POPULATION_THRESHOLD = 1000

dict_city_by_country = {k:{} for k in set_country_code}
dict_city_by_name = {}

with open(CITY_FILE, newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter='\t')
    for row in spamreader:
        coordinate = (float(row[4]), float(row[5]))
        country_code = row[8].lower()
        population = int(row[14])

        if population < POPULATION_THRESHOLD: continue

        # GB should use admin2 as admin
        admin_code = row[10] if country_code != 'gb' else row[11]
        admin_name = None

        if admin_code.lower() in dict_admin_by_country[country_code]:
            admin_name = dict_admin_by_country[country_code][admin_code.lower()]

        # append city_name, ascii_name, alter_name
        set_name = set()
        if row[1] != '': set_name.add(format_name(row[1]))
        if row[2] != '': set_name.add(format_name(row[2]))
        set_alter_name = set()
        if row[3] != '': 
            set_alter_name.update([format_name(x) for x in row[3].split(',')])

        set_name.update(set_alter_name)
        set_name.difference(set_blackwords)
        set_name = {x for x in set_name if is_good_name(x)}

        for name in set_name:
            this_city_info = (coordinate, country_code, admin_name, name, population)
            # add to country
            if name not in dict_city_by_country[country_code]:
                dict_city_by_country[country_code][name] = this_city_info
            else:
                is_bigger = (population > dict_city_by_country[country_code][name][-1])
                is_alter = (name in set_alter_name)
                if is_bigger and (not is_alter):
                    dict_city_by_country[country_code][name] = this_city_info

            # add to city name
            if name not in dict_city_by_name:
                dict_city_by_name[name] = this_city_info
            else:
                is_bigger = (population > dict_city_by_name[name][-1])
                is_alter = (name in set_alter_name)
                if is_bigger and (not is_alter):
                    dict_city_by_name[name] = this_city_info

# 按照人口排序
# for name in dict_city_by_name:
#     dict_city_by_name[name].sort(key=lambda city_info: city_info[-1], reverse=True)

print('number of good cities: ', len(dict_city_by_name))
# 保存到 pickle 中
pickle.dump(dict_city_by_country, open(f'{BIN_DIR}/dict_city_by_country.bin', 'wb'))
pickle.dump(dict_city_by_name, open(f'{BIN_DIR}/dict_city_by_name.bin', 'wb'))
