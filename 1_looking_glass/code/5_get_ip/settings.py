import os
import pickle

MACHINE_IPS = ['45.32.149.108', '173.199.123.79']

FORMER_RESULT_DIR = '../4_filter_by_api/result'
LG_LIST = pickle.load(open(f'{FORMER_RESULT_DIR}/list_good_routers.bin', 'rb'))

RESULT_DIR = f'./result'

LG_DIR = '../../'
DST_DIR = f'{LG_DIR}/pickle_bin/'
os.system(f'mkdir -p {DST_DIR}')
