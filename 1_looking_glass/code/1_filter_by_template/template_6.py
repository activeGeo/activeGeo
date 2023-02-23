# 使用了模板 'freshmeat' 的网页, 但是网页信息中没有 'freshmeat' 字样

import os
import re
import sys
import pickle
from bs4 import BeautifulSoup, Comment

LG_DIR = '../../'
WEBPAGES_DIR = f'{LG_DIR}/data/webpages/'
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

keyword = 'looking.house'
def check_one_soup(soup):
    try:
        footer = soup.footer
        if footer and keyword.upper() in footer.get_text():
            return True
    except:
        return 'BAD'
    return 'BAD'

# 删去待选 websites 中使用 looking.house 模板的网站
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

list_good_routers = list()

# 下面的代码是对 Looking.house 网站直接进行分析
import requests
LG_HOUSE_URL = 'https://looking.house'
LG_HOUSE_HOME_URL = LG_HOUSE_URL + '/points.php'
req = requests.get(LG_HOUSE_HOME_URL, timeout=20)
soup = BeautifulSoup(req.text, "lxml")
container_list = soup.find_all('div', 'panel panel-info')

for container in container_list:
    table_tbody = container.table.tbody

    rows = table_tbody.find_all('tr')
    for row in rows:
        cols     = row.find_all('td')
        point_id = cols[0].a.get('href').split('=')[1]
        ip_info  = cols[0].get_text(separator='\n').split()
        position = cols[1].find('button').get_text().split(',')
        country  = position[0].strip()
        city     = position[-1].strip()

        v4 = ip_info[0]
        v6 = ip_info[1] if len(ip_info) > 1 else 'None'

        one_result = {
            'website': LG_HOUSE_URL,
            'geohint': (city, point_id, ''),
            'ipv4hint': v4,
            'ipv6hint': v6,
        }
        list_good_routers.append(one_result)
pickle.dump(list_good_routers, open(f'{DST_FILES_DIR}/list_good_routers.bin', 'wb'))

for one_result in list_good_routers:
    print(one_result)
