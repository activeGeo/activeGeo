# 爬去 pictimo 网站的信息, 正确结果储存在 ./data/2_pictimo_good.csv

from bs4 import BeautifulSoup, Comment
import re
import requests
  
homepage = 'https://www.pictimo.com'
country_url = homepage + '/' + 'country'

# 首先通过主页得到国家列表
req = requests.get(country_url, timeout=10)
soup = BeautifulSoup(req.text, "html.parser")

wrong_result = open('../data/2_pictimo_wrong.csv', 'w')
good_result = open('../data/2_pictimo_good.csv', 'w')

# 检测是否是 v4, 要求输入是字符串
def is_ipv4(ip):
    m = re.match(r"^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$", ip)
    return bool(m) and all(map(lambda n: 0 <= int(n) <= 255, m.groups()))

# 发现网站中表示国家的 div 都用这个名字, 不保证以后都是这样
country_list = soup.find_all('div', { 'class': 'col-md-3 col-sm-3 col-xs-3' })
for country in country_list:
    country_name = (country['onclick']).split('\'')[1]
    # 得到这个国家的页面
    this_url = homepage + '/' + country_name
    country_name = country_name.split('/')[-1]
    print( f'country: {this_url}' )

    # 请求该页面, 找到所有摄像头对应的网页
    req = requests.get(this_url, timeout=10)
    soup = BeautifulSoup(req.text, "html.parser")

    div_1 = soup.find_all('div', { 'class': 'row templatemorow' })
    list_links = []
    for tmp_div in div_1:
        list_links.extend(tmp_div.find_all('a'))

    webcam_num = int(len(list_links) / 2)
    for idx in range(0, webcam_num, 2):
        ip_src   = list_links[idx*2+0]['data-pop']
        city_src = list_links[idx*2+1]['href']

        try:
            ip = ip_src.split('/')[2].split(':')[0]
        except:
            print(ip_src)
            continue
        city = city_src.split('/')[2]


        new_line = ip + ',' + city + ',' + country_name + '\n'
        print(new_line)
        
        if is_ipv4(ip):
            good_result.writelines(new_line)
        else:
            wrong_result.writelines(new_line)

# 因为网页属于下拉响应, 所以直接通过 request 请求只能得到一部分
# 通过分析网络流得出该网站的 API
url = 'https://www.pictimo.com/get_infinitescroll_cams.php?page=country&countryID='
for i in range(0, 250):
    print(i)
    this_url = url + str(i)
    req = requests.get(this_url, timeout=10)

    for one_json in eval(req.text):
        print(one_json)
        try:
            ip_src = one_json['imgLocation']
            city = one_json['City'].split(',')[0].lower()
            country = one_json['Country'].lower()

            ip = ip_src.split('/')[2].split(':')[0]

            new_line = ip + ',' + city + ',' + country + '\n'
            print(new_line)
            if is_ipv4(ip):
                good_result.writelines(new_line)
            else:
                print('WRONG')
                wrong_result.writelines(new_line)
        except:
            print('WRONG')
            wrong_result.writelines(one_json)
