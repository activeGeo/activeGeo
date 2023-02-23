import ast
import pickle

src_file = open('../data/1_ripe_result.jsonb', 'r')

us_v4_probes = {}
for _, row in enumerate(src_file):
    one_json = ast.literal_eval(row.strip())
    if one_json['type'] == 'v4' and one_json['country_code'] != 'US':
        us_v4_probes[one_json['ip']] = one_json

pickle.dump(us_v4_probes, open(f'../pickle_bin/not_us_probes.bin', 'wb'))
