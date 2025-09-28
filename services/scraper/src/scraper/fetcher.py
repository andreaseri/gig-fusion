import requests
from time import sleep

def fetch_url(url, timeout=10):
    resp = requests.get(url, timeout=timeout)
    resp.raise_for_status()
    return resp.text
