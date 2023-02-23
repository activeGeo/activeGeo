# 从城市定位到经纬度, 通过 Geonames 数据进行融合

import csv
import json
import ast
import glob
import pickle

BIN_DIR = '../pickle_bin'
SRC_DIR = '../src'

def format_name(name):
    return name.replace('-','').replace(' ','').lower()

set_country_name = pickle.load(open(f'{BIN_DIR}/set_country_name.bin', 'rb'))
set_country_code = pickle.load(open(f'{BIN_DIR}/set_country_code.bin', 'rb'))


# 对于那些首都和国家名重合的地区, 不能把它们列入黑名单
set_one_city_country = set()
with open(f'{SRC_DIR}/country_info.txt', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter='\t')
    for row in spamreader:
        if row[0][0] == '#':
            continue
        country_name = format_name(row[4])
        captial_name = format_name(row[5])
        if country_name == captial_name:
            set_one_city_country.add(country_name)

# 删除一些容易歧义的名字(如 uk, qc)
set_blacklist_words = set()
for blacklist_file in glob.glob(f'{SRC_DIR}/blacklists/*'):
    with open(blacklist_file, 'r') as srcfile:
        for row in srcfile:
            set_blacklist_words.add(row.strip().lower())

# 国家名、国家代码也应该不能当称城市名
set_blacklist_words.update(set_country_name)
set_blacklist_words.update(set_country_code)
set_blacklist_words = set_blacklist_words - set_one_city_country
        
# 保存到 pickle 中
pickle.dump(set_blacklist_words, open(f'{BIN_DIR}/set_blackwords.bin', 'wb'))
