def get_api_key(path='models/apikey_map.txt'):
    with open(path) as f:
        api_key = f.readline()
        return api_key