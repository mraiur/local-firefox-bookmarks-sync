import requests
import config

def fetch_remote():
    try:
        res = requests.get(config.compare_url)
        if res.status_code == 200:
            return res.json()
        else:
            print('Remote machine not returning valid data')
        return None
    except requests.ConnectionError or requests.JSONDecodeError:
        print('Remote machine not running')
        return None

def push_changes( records ):
    try:
        req = requests.post(config.update_url, json=records)
    except requests.ConnectionError or requests.JSONDecodeError:
        print('Failed to push changes')
        return None