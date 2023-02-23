from ripe.atlas.cousteau import AtlasRequest

def get_all_probe():
    # url_path = "/api/v2/anchors"
    base_path = "/api/v2/probes"
    idx = 0
    while True:
        idx += 1
        url_path = base_path + f'?page={idx}'
        request = AtlasRequest(**{"url_path": url_path})
        (is_success, response) = request.get()

        if not is_success:
            break
        for result in response['results']:
            print_raw_result(result)
            # deal_with_result(result)

        if response['next'] is None:
            break

def print_raw_result(result):
    result.pop('tags', None)
    result.pop('status', None)
    result.pop('status_since', None)
    print(result)

get_all_probe()
