import requests
import json
import configparser

def pfItem(itemName):
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8')
        
    url = config['zabbix']['URL']
    HOST_ID = config['host']['host_id']
    AUTH = config['admin']['auth']
    HOST_INTERFACEID = config['host']['host_interfaceid']

    OID ={
            "CPU Utilization":"1.3.6.1.4.1.35098.1.1.0",
            "Total Memory":"1.3.6.1.4.1.35098.1.2.0",
            "Used Memory":"1.3.6.1.4.1.35098.1.3.0"
    }

    payload = {
            "jsonrpc": "2.0",
            "method": "item.create",
            "params": {
                "hostid" : HOST_ID,
                "name": itemName,
                "key_": "system."+itemName.lower().replace(" ",""),
                "value_type": 3,
                "type": 20, #snmp agent
                "interfaceid": HOST_INTERFACEID,
                "snmp_oid" : OID[itemName],
                #"units" :,
                "delay" : "1m",
                "history" : "7d",
                "trends" : "0s",
                "tags" : [
                    {
                        "tag": "Device Performance",
                        "value" : ""
                    }
                ]
                    },
            "auth": AUTH,
            "id": 3
    }
    response = requests.post(url, json=payload).json()
    return response


def hwItem(itemName):
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8')
    
    url = config['zabbix']['URL']
    HOST_ID = config['host']['host_id']
    AUTH = config['admin']['auth']
    HOST_INTERFACEID = config['host']['host_interfaceid']

    OID ={
            "Hardware model name": "1.3.6.1.2.1.47.1.1.1.1.13.1",
            "Operation system":"1.3.6.1.2.1.1.1.0",
            "Serial Number":"1.3.6.1.2.1.47.1.1.1.1.11.1",
            "description":"1.3.6.1.2.1.1.1.0",
            "location":"1.3.6.1.2.1.1.6.0",
            "system name":"1.3.6.1.2.1.1.5.0",
            "Vendor":"1.3.6.1.2.1.1.1.0"
            }
    payload = {
            "jsonrpc": "2.0",
            "method": "item.create",
            "params": {
                "hostid" : HOST_ID,
                "name": itemName,
                "key_": "system."+itemName.lower().replace(" ",""),
                "value_type": 4, #text
                "type": 20, #snmp agent
                "interfaceid": HOST_INTERFACEID,
                "snmp_oid" : OID[itemName], 
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
