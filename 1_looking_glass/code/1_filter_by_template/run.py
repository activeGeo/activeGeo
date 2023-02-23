import os

SRC_WEBSITES_PATH = os.path.realpath('../../src/websites.txt')
EACH_TEMPLATE_DIR = './result'

TEMPLATE_0_DIR = f'{EACH_TEMPLATE_DIR}/template_0'
os.system(f'mkdir -p {TEMPLATE_0_DIR}')
os.system(f'ln -sf {SRC_WEBSITES_PATH} {TEMPLATE_0_DIR}/bad_websites.txt')

for i in range(6, 7):
    NOW_RESULT_DIR = f'./result/template_{i-1}'
    os.system(f'python3 ./template_{i}.py {NOW_RESULT_DIR}/bad_websites.txt {i}')
