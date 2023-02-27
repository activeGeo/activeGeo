import os
import random
import pickle

BIN_DIR = os.path.expanduser(f'../pickle_bin')

dict_client_info = pickle.load(open(f'{BIN_DIR}/dict_client_info.bin', 'rb'))

'''
2. Make Train and Test
'''
TRAIN_NUM = int(len(dict_client_info) * 0.8)

ok_train_set = set(random.sample([*dict_client_info], TRAIN_NUM))
ok_test_set  = dict_client_info.keys() - ok_train_set

print('length of train:', len(ok_train_set))
print('length of test:', len(ok_test_set))

pickle.dump(ok_train_set, open(f'{DST_DIR}/ok_train_set.bin', 'wb'))
pickle.dump(ok_test_set, open(f'{DST_DIR}/ok_test_set.bin', 'wb'))
