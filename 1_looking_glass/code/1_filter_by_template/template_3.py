# 使用了模板 'freshmeat' 的网页

import os
import re
import sys
import pickle
from bs4 import BeautifulSoup, Comment

LG_DIR = '../../'
WEBPAGES_DIR = f'{LG_DIR}/webpages/'
SRC_WEBSITES_FILE = sys.argv[1]
IDX = sys.argv[2]

# 1. using this template and get information sucessfully
# 2. using this template but fail to get information
# 3. not using this template
DST_FILES_DIR = f'./result/template_{IDX}'
os.system(f'mkdir -p {DST_FILES_DIR}')

TBD_WEBSITES_FILE = open(f'{DST_FILES_DIR}/tbd_websites.txt', 'w')
BAD_WEBSITES_FILE = open(f'{DST_FILES_DIR}/bad_websites.txt', 'w')
  
def get_items_from_webpage(soup):
    def get_nodes_info(node_label, nodes_list):
        node_details = node_label.find_all('option')
        for node_detail in node_details:
            node_value = node_detail.get('value')
            node_description = node_detail.get_text().strip()
            nodes_list.append((node_value, node_description))

    node_items = soup.body.form.table.find('select', {'name': 'router'})
    node_labels = node_items.find_all('optgroup')

    result = {}
    if node_labels:
        for node_label in node_labels:
            label_name = node_label.get('label')
            result[label_name] = []
            get_nodes_info(node_label, result[label_name])
    else:
        result['default'] = []
        get_nodes_info(node_items, result['default'])
    return result

def check_one_soup(soup):
    comments = soup.find_all(string=lambda text: isinstance(text, Comment))
    for comment in comments:
        if 'freshmeat' in comment:
            return get_items_from_webpage(soup)
    return 'BAD'

list_good_routers = list()
with open(SRC_WEBSITES_FILE, encoding='utf-8') as srcfile:
    for idx, row in enumerate(srcfile):
        print(idx)
        website = row.strip()
        filename = website.replace('/', '_').replace(':', '.')
        filepath = f'{WEBPAGES_DIR}/{filename}.txt'

        if not os.path.exists(filepath):
            continue

        with open(filepath, 'r') as srcfile:
            result = check_one_soup(BeautifulSoup(srcfile.read(), "lxml"))
            if result == 'BAD':
                BAD_WEBSITES_FILE.writelines(website + '\n')
            else:
                for label, routers in result.items():
                    for one_router in routers:
                        one_result = {
                            'website': website,
                            'geohint': (label, one_router[0], one_router[1]),
                            'ipv4hint': '',
                            'ipv6hint': '',
                        }
                        list_good_routers.append(one_result)
pickle.dump(list_good_routers, open(f'{DST_FILES_DIR}/list_good_routers.bin', 'wb'))
for one_router in list_good_routers:
    print(one_router)
