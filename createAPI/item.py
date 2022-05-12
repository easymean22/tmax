import requests
import json
import configparser


def item(itemName):
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8')
    
    url = config['zabbix']['URL']
    HOST_ID = config['host']['host_id']
    AUTH = config['admin']['auth']
    HOST_INTERFACEID = config['host']['host_interfaceid']


    payload = {
            "jsonrpc": "2.0",
            "method": "item.create",
            "params": {
                "hostid" : HOST_ID,
                "name": "Operation system",
                "key_": "system.operatingsystem",
                "value_type": 4, #text
                "type": 20, #snmp agent
                "interfaceid": HOST_INTERFACEID,
                "snmp_oid" : "1.3.6.1.2.1.1.1.0", 
                #"units" :,
                "delay" : "1h",
                "history" : "7d",
                "trends" : "0s",
                "tags" : [
                    {
                        "tag": "Device Information",
                        "value" : "Hardware details"
                    }
                ]
                },
            "auth": AUTH,
            "id": 3
    }
    response = requests.post(url, json=payload).json()
    return response
    #print(json.dumps(response, indent=3, sort_keys=True))


if __name__ == "__main__":
    print(itemName())
