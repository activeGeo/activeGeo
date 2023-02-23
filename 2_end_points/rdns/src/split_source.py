import ast


SRC_FILE_PATH = '../src/rapid7_data/source.txt'
DST_FILE_PATH = '../src/rapid7_data/data-{}.txt'

THRESHOLD = 256 * 256 * 32

with open(SRC_FILE_PATH, 'r') as srcfile:
    NOW_IDX = 0
    NOW_NUM = 0
    NOW_FILE = open(DST_FILE_PATH.format(NOW_IDX), 'w')
    for (_, row) in enumerate(srcfile):
        one_json = ast.literal_eval(row.strip())
        if one_json['type'] == 'cname': continue

        NOW_FILE.writelines(row)
        NOW_NUM += 1
        if one_json['name'].split('.')[-1] == '255' and NOW_NUM >= THRESHOLD:
            print(NOW_IDX)
            NOW_NUM = 0
            NOW_IDX += 1
            NOW_FILE = open(DST_FILE_PATH.format(NOW_IDX), 'w')
