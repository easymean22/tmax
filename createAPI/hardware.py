import requests
import json


def operationSystem():
    url = "http://localhost/zabbix/api_jsonrpc.php"


    payload = {
            "jsonrpc": "2.0",
            "method": "item.create",
            "params": {
                "hostid" : "10520",
                "name": "Operation system",
                "key_": "system.operatingsystem",
                "value_type": 4, #text
                "type": 20, #snmp agent
                "interfaceid": "16",
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
            "auth": "e4b2faf37a2cc90dd38a8630bfe9b9da",
            "id": 3
    }
    response = requests.post(url, json=payload).json()
    print(json.dumps(response, indent=3, sort_keys=True))


if __name__ == "__main__":
    operatingSystem()