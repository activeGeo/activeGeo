import os
import pickle
from string import digits

GEOBIN_DIR = '../../../0_location_hint/pickle_bin'
dict_city_by_name = pickle.load(open(f'{GEOBIN_DIR}/dict_city_by_name.bin', 'rb'))
dict_hasspace_city = pickle.load(open(f'{GEOBIN_DIR}/dict_hasspace_city.bin', 'rb'))
dict_iata_code = pickle.load(open(f'{GEOBIN_DIR}/dict_iata_code.bin', 'rb'))

TEMPLATE_RESULT_DIR = '../1_filter_by_template/result'
TEMPLATE_NUM = len(os.listdir(TEMPLATE_RESULT_DIR)) - 1

# 1. geolocate successfully
# 2. cannot ensure the correct of geolocatoin
# 3. cannot geolocate
DST_FILES_DIR = f'./result/'
os.system(f'mkdir -p {DST_FILES_DIR}')

list_good_routers = []
list_bad_routers = []
list_tbd_routers = []

def split_word(name):
    name_split = set()

    # remove digits
    table = str.maketrans('', '', digits)
    name = name.translate(table).lower()

    # check format 'xx, yy'
    if name.count(',') > 0 and '(' not in name:
        # 对于 '-' 字符, 有两种选择, 一个是删掉, 一个是替换为 ','
        new_name = name.replace('-', '')
        name_split.update([x.replace(' ', '') for x in new_name.split(',')])
        new_name = name.replace('-', ',')
        name_split.update([x.replace(' ', '') for x in new_name.split(',')])
    # check format 'xx (AS number)'
    elif '(as' in name:
        pass
    else:
        name = name.replace('(', ' ')
        name = name.replace(')', ' ')
        name = name.replace(',', ' ')
        name = name.replace('，', ' ')
        name = name.replace('/', ' ')

        # 对于 '-' 字符, 有两种选择, 一个是删掉, 一个是替换为 ','
        # name_split.update(name.replace('-','').split())
        name_split.update(name.replace('-',' ').split())

    return name_split

def check_raw_word(raw_word, iata_code=True):
    raw_word = raw_word.lower()

    # 检查是否有带有空格的城市
    for name in dict_hasspace_city:
        if name in raw_word:
            return ('GOOD', (dict_hasspace_city[name], 'space'))

    set_oneword = split_word(raw_word)

    candidates = list()
    for word in set_oneword:
        # 检查是否是 IATA CODE, 如果有则必须要有: 国家代码 / IXP
        if iata_code and word in dict_iata_code:
            if dict_iata_code[word][1] in set_oneword:
                candidates.append((dict_iata_code[word], 'iata'))
            if 'ixp' in set_oneword:
                candidates.append((dict_iata_code[word], 'iata'))

        # 检查是否是 城市名
        if word in dict_city_by_name:
            candidates.append((dict_city_by_name[word], 'name'))

    # 如果有两个候选，看一下是否 A 是 B 的所属州
    if len(candidates) == 2:
        _, _, admin_0, city_0, _  = candidates[0][0]
        _, _, admin_1, city_1, _  = candidates[1][0]
        if city_0 == admin_1:
            return ('GOOD', candidates[1])
        if city_1 == admin_0:
            return ('GOOD', candidates[0])

    # 如果有多个候选，那么看一下他们的坐标是否相近
    if len(candidates) > 0:
        coor_candidates = [x[0][0] for x in candidates]
        for c1 in coor_candidates:
            for c2 in coor_candidates:
                if abs(c1[0] - c2[0]) > 1 or abs(c1[1] - c2[1]) > 1:
                    return ('TBD', candidates)
        return ('GOOD', candidates[0])
    return ('BAD', None)


def check_geoinfo(geohint):
    for i in range(0, 3):
        geoinfo = check_raw_word(geohint[i])
        if geoinfo[0] != 'BAD':
            return geoinfo
    return ('BAD', None)

for idx in range(1, TEMPLATE_NUM+1):
    ROUTER_BIN = f'{TEMPLATE_RESULT_DIR}/template_{idx}/list_good_routers.bin'
    for jdx, one_router in enumerate(pickle.load(open(ROUTER_BIN, 'rb'))):
        # print(jdx)
        geohint = one_router['geohint']
        result = check_geoinfo(one_router['geohint'])
        if result[0] == 'BAD':
            list_bad_routers.append(one_router)
        elif result[0] == 'TBD':
            one_router['candiates'] = result[1]
            list_bad_routers.append(one_router)
        else:
            city_info = result[1][0]
            one_router['coordinate'] = city_info[0]
            one_router['country_code'] = city_info[1]
            one_router['city'] = city_info[3]
            list_good_routers.append(one_router)
            print(one_router)

pickle.dump(list_good_routers, open(f'{DST_FILES_DIR}/list_good_routers.bin', 'wb'))
pickle.dump(list_tbd_routers, open(f'{DST_FILES_DIR}/list_tbd_routers.bin', 'wb'))
pickle.dump(list_bad_routers, open(f'{DST_FILES_DIR}/list_bad_routers.bin', 'wb'))
