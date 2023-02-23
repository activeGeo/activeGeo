# 爬取 LookingGlass 内容

import os
import requests

LG_DIR = '../../'

WEBSITES_FILE = f'{LG_DIR}/src/websites.txt'
WEBPAGES_DIR = f'{LG_DIR}/webpages'

os.system(f'mkdir -p {WEBPAGES_DIR}')

with open(WEBSITES_FILE, 'r') as srcfile:
    for row in srcfile:
        try:
            website = row.strip()
            filename = website.replace('/', '_').replace(':', '.')
            req = requests.get(website, timeout=10)
            with open(f'{WEBPAGES_DIR}/{filename}.txt', 'w') as dst_file:
                dst_file.writelines(req.text)
            print('OK', website)
        except Exception as e:
            print(e)
