import pickle

a = pickle.load(open('../pickle_bin/dict_city_by_name.bin', 'rb'))
print(a['toronto'])
