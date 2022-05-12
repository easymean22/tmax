import configparser
import requests
import json
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
"""

def getToken():
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8')
    ID = config['zabbix']['ID']
    PW = config['zabbix']['PW']
    url = config['zabbix']['URL']
    payload = {
        "jsonrpc" : "2.0",
        "method": "user.login",
        "params": {
            "user": ID,
            "password": PW
            },
        "id": 1,
        "auth": None
    }

    response = requests.post(url, json=payload).json()
    return response


if __name__ == "__main__":
    print(getToken())
