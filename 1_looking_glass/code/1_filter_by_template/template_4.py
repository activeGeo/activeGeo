# 筛选使用了模板 LookingGlass 的网页
import os
import re
import sys
import pickle
from bs4 import BeautifulSoup
 
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
    node_items = soup.body.find('select', {'id': 'routers'}).find_all('option')
    result = []
    for x in node_items:
        result.append((x.get('value'), x.get_text()))
    return result

keyword = 'Looking Glass'
def check_one_soup(soup):
    try:
        footer_bar = soup.body.find('div', {'class': 'footer_bar'})
        if footer_bar and keyword in footer_bar.get_text():
            return get_items_from_webpage(soup)
        return 'BAD'
    except:
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
            elif result == 'TBD':
                TBD_WEBSITES_FILE.writelines(website + '\n')
            else:
                for one_router in result:
                    one_result = {
                        'website': website,
                        'geohint': ('', one_router[0], one_router[1]),
                        'ipv4hint': '',
                        'ipv6hint': '',
                    }
                    list_good_routers.append(one_result)
pickle.dump(list_good_routers, open(f'{DST_FILES_DIR}/list_good_routers.bin', 'wb'))

for one_result in list_good_routers:
    print(one_result)
