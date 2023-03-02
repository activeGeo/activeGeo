import os

SRC_WEBSITES_PATH = os.path.realpath('../../src/websites.txt')
EACH_TEMPLATE_DIR = './result'

TEMPLATE_0_DIR = f'{EACH_TEMPLATE_DIR}/template_0'
os.system(f'mkdir -p {TEMPLATE_0_DIR}')
os.system(f'ln -sf {SRC_WEBSITES_PATH} {TEMPLATE_0_DIR}/bad_websites.txt')

TEMPLATE_NUM = len([x for x in os.listdir('.') if x.startswith('template')])

for i in range(1, TEMPLATE_NUM+1):
    NOW_RESULT_DIR = f'./result/template_{i-1}'
    os.system(f'python3 ./template_{i}.py {NOW_RESULT_DIR}/bad_websites.txt {i}')
