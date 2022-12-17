def get_api_key(path='apikey_map.txt'):
    with open(path) as f:
        api_key = f.readline()
        return api_key
