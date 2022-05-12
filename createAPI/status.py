import requests
import json
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import configparser
from library import *


def status():
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8')
    
    url = config['zabbix']['URL']
    HOST_ID = config['host']['host_id']
    AUTH = config['admin']['auth']
    HOST_INTERFACEID = config['host']['host_interfaceid']

    # get interface informatiom by snmp
    interfaces = findIndex()

    # create value mapping
    payload1 = {
            "jsonrpc": "2.0",
            "method": "valuemap.create",
            "params": {
                "hostid": HOST_ID,
                "name": "Interface Status",
                "mappings": [
                    {
                        "type": "0",
                        "value": "1",
                        "newvalue": "up"
                    },
                    {
                        "type": "0",
                        "value": "2",
                        "newvalue": "down"
                    },
                    {
                        "type": "0",
                        "value": "3",
                        "newvalue": "testing"
                    },
                    {
                        "type": "0",
                        "value": "4",
                        "newvalue": "unknown"
                    },
                    {
                        "type": "0",
                        "value": "5",
                        "newvalue": "dormant"
                    },
                    {
                        "type": "0",
                        "value": "6",
                        "newvalue": "notPresent"
                    },
                    {
                        "type": "0",
                        "value": "7",
                        "newvalue": "lowerLayerDown"
                    }
                ]
            },
            "auth": AUTH,
            "id": 1
        }

    response = requests.post(url, json=payload1).json()
    valueMapID = response['result']['valuemapids'][0]

    # calculate intraffic for all interface 
    for interface in interfaces:
        payload2 = {
            "jsonrpc": "2.0",
            "method": "item.create",
            "params": {
                "hostid" : HOST_ID,
                "name": "Status "+interface[1],
                "key_": "interface."+interface[1].replace('/','')+".status",
                "value_type": 3, #numerinc unsigned
                #"value_type": 4, #text
                "type": 20, #snmp agent
                "interfaceid": HOST_INTERFACEID,
                "snmp_oid" : "1.3.6.1.2.1.2.2.1.8."+interface[0],
                #"units" : "bps",
                "delay" : "1m",
                "history" : "7d",
                "trends" : "0s",
                "tags" : [
                    {
                        "tag": "Interface",
                        "value" : interface[1]
                    },
                    {
                        "tag": "Interface Information",
                        "value" : "status"
                    }
                ],
                "valuemapid" : valueMapID
            },
            "auth": AUTH,
            "id": 3
        }
        response = requests.post(url, json=payload2).json()
        return response
       #print(json.dumps(response, indent=3, sort_keys=True))

if __name__ == "__main__":
    status()
