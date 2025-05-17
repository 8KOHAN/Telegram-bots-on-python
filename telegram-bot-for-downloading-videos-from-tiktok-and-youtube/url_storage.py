import json
import os

URL_STORAGE_FILE = "url_storage.json"

def load_url_storage():
    if os.path.exists(URL_STORAGE_FILE):
        with open(URL_STORAGE_FILE, "r") as file:
            return json.load(file)
    return{}

def save_url_storage(data):
    with open(URL_STORAGE_FILE, "w") as file:
        json.dump(data, file)

url_storage = load_url_storage()
