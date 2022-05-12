import requests
import json
import configparser


def findID():
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8')
    url = config['zabbix']['URL']
    name = config['host']['host_name']
    AUTH = config['admin']['auth']
    
    payload = {
            "jsonrpc": "2.0",
            "method": "host.get",
            "params": {
                "filter":{
                    "host":[
                        name
                    ]
                }
            },
            "auth": AUTH,
            "id": 3
    }
    response = requests.post(url, json=payload).json()
    return response

def findIfID():
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8')
    url = config['zabbix']['URL']
    AUTH = config['admin']['auth']
    Hostid = config['host']['host_id']

    payload = { 
            "jsonrpc": "2.0",
            "method": "hostinterface.get",
            "params": {
                "output" : "extend",
                "hostids" : Hostid
            },
            "auth": AUTH,
            "id": 3
    }   
    response = requests.post(url, json=payload).json()
    return response



if __name__ == "__main__":
    print(findID())
    print(findIfID())
