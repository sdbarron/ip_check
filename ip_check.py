import requests
import json
import os
import os.path
import sys

def get_current_ip() -> str:
    try:
        response = requests.get("https://checkip.amazonaws.com")
        #response.raise_for_status()
        return response.content.decode()
    except:
        return None

def get_file_path() -> str:
    try:
        path = os.path.join(os.getenv("HOME"), ".recent_ip", "recent_ip.txt")
        print(path)
        create = os.makedirs(os.path.join(os.getenv("HOME"), ".recent_ip"), exist_ok=True)
        return path
    except:
        return None

def get_stored_ip() -> str:
    try:
        file = open(get_file_path(), "r")
        ip = file.read()
        file.close()
        return ip
    except:
        ip = ""

def put_stored_ip(ip) -> str:
    try:
        file = open(get_file_path(), "w")
        file.write(ip)
        file.close()
    finally:
        pass    

curr = get_current_ip()
prev = get_stored_ip()
if curr == None:
    sys.exit(-1)
elif curr != prev:
    put_stored_ip(curr)
    sys.exit(-2)
else:
    pass
 