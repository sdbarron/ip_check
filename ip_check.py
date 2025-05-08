import requests
import json
import os
import os.path
import sys
import psycopg2
#from psycopg2 import sql

def get_current_ip() -> str:
    try:
        response = requests.get("https://checkip.amazonaws.com")
        #response.raise_for_status()
        return response.content.decode().removesuffix('\n')
    except:
        return None

#region file

#def get_file_path() -> str:
#    try:
#        path = os.path.join(os.getenv("HOME"), ".recent_ip", "recent_ip.txt")
#        print(path)
#        create = os.makedirs(os.path.join(os.getenv("HOME"), ".recent_ip"), exist_ok=True)
#        return path
#    except:
#        return None

#def get_file_stored_ip() -> str:
#    try:
#        file = open(get_file_path(), "r")
#        ip = file.read()
#        file.close()
#        return ip
#    except:
#        ip = ""

#def put_file_stored_ip(ip):
#    try:
#        file = open(get_file_path(), "w")
#        file.write(ip)
#        file.close()
#    finally:
#        pass    

#endregion file

#region postgres
def get_db_params():
    try:
        file = open(os.path.join(os.getcwd(),"credentials.cfg"), "r")
        dbname = file.readline().removesuffix('\n')
        user = file.readline().removesuffix('\n')
        password = file.readline().removesuffix('\n')
        host = file.readline().removesuffix('\n')
        port = file.readline().removesuffix('\n')
        db_params = {
                        'dbname': dbname,
                        'user': user,
                        'password': password,
                        'host': host,
                        'port': port
                    }
        return db_params
    except:
        return {}

def get_db_stored_ip() -> str:
    try:
        db_params = get_db_params()
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()
        cursor.execute('SELECT addr FROM ip.ip_hist order by log desc limit 1')
        addr=cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return addr
    except Exception as e:
        return None
    
def put_db_stored_ip(addr):
    try:
        db_params = get_db_params()
        conn = psycopg2.connect(**db_params)
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute('insert into ip.ip_hist (addr) values(%s)',[addr])
        #cursor.commit
        #conn.commit

        cursor.close
        conn.close
        return None
    except Exception as e:
        return None

#endregion postgres  

curr = get_current_ip()
prev = get_db_stored_ip()
put_db_stored_ip(curr)

if curr == "":    #Couldn't get current IP Address 😳
    sys.exit(-1)
elif curr != prev:  #IP Address Changed
    sys.exit(-2)
else:
    pass
