# 爬去 insecam 网站的信息, 正确结果储存在 ./data/2_insecam_good.csv

from bs4 import BeautifulSoup, Comment
import re
import requests
import math

# 检测是否是 v4, 要求输入是字符串
def is_ipv4(ip):
    m = re.match(r"^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$", ip)
    return bool(m) and all(map(lambda n: 0 <= int(n) <= 255, m.groups()))
  
insecam_good = open('./2_insecam_good.csv', 'w')
insecam_wrong = open('./2_insecam_wrong.csv', 'w')

headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
}
# 通过该 API 可以请求国家和对应的个数
jsoncountry_url = 'http://www.insecam.org/en/jsoncountries/'
req = requests.get(jsoncountry_url, timeout=10, headers=headers)
print(req.text)

list_country = []

for k, v in eval(req.text).get('countries').items():
    list_country.append((k, v['count']))

# 遍历各个国家 
homepage = 'http://www.insecam.org/en/bycountry'
for one_country in list_country:
    print(one_country)
    iso_code = one_country[0]
    page_max = math.ceil(one_country[1] / 6)

    for i in range(1, page_max+2):
        this_url = f'{homepage}/{iso_code}/?page={i}'

        req = requests.get(this_url, timeout=10, headers=headers)
        soup = BeautifulSoup(req.text, "html.parser")

        cam_list = soup.find_all('a', { 'class': 'thumbnail-item__wrap' })

        for cam in cam_list:
            link = cam.find('img')['src']
            ip = link.split('/')[2].split(':')[0]
            name = cam.find('p').get_text()
            if is_ipv4(ip):
                insecam_good.writelines(ip + ',' + name + '\n')
            else:
                insecam_wrong.writelines(this_url + '\t' + str(cam) + '\n')
            print(ip, name, link)

