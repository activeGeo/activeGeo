import ast
import reverse_geocode

def deal_with_line(line):
    result = ast.literal_eval(line)
    position = result['geometry']
    if position is None or result['country_code'] is None:
        return

    if position['type'] != 'Point':
        raise Exception(f'position is not Point: {result}')

    result['geometry']['coordinates'].reverse()
    # country, city = get_city_from_coor(result['geometry']['coordinates'])
    coor = tuple(result['geometry']['coordinates']),
    position = reverse_geocode.search(coor)[0]
    if result['address_v4']:
        value = {
            'ip': result['address_v4'],
            'type': 'v4',
            'coordinate': result['geometry']['coordinates'],
        }
        value.update(position)
        print(value)
    if result['address_v6']:
        value = {
            'ip': result['address_v6'],
            'type': 'v6',
            'coordinate': result['geometry']['coordinates'],
        }
        value.update(position)
        print(value)


def deal_ripe_altas(file_list):
    for source_file in file_list:
        with open(source_file, 'r') as f:
            line = f.readline()
            while line:
                deal_with_line(line)
                line = f.readline()
            f.close()

file_list = [
    '../data/0_rawdata_from_api.jsonb'
]
deal_ripe_altas(file_list)
