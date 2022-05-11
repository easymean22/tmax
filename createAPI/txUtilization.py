import requests
import json
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from library import *
from variable import *


def txUtilization():
    url = URL

    # get interface informatiom by snmp
    interfaces = findIndex()

    for interface in interfaces:
        payload = {
            "jsonrpc": "2.0",
            "method": "item.create",
            "params": {
                "hostid" : HOST_ID,
                "name": "Tx utilization "+interface[1],
                "key_": "interface."+interface[1].replace('/','')+".txutilization",
                #"value_type": 3, #numerinc unsigned
                "value_type": 4, #text
                "type": 20, #snmp agent
                "interfaceid": HOST_INTERFACEID,
                "snmp_oid" : "1.3.6.1.2.1.2.2.1.16."+interface[0], #in octect oid = 1.3.6.1.2.1.2.2.1.10.+index
                "units" : "%",
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
                        "value" : "Tx utilization"
                    }
                ],
                "preprocessing": [
                    {
                        "type": "10",
                        "params": "",
                        "error_handler": "1",
                        "error_handler_params": ""
                    },
                    {
                        "type": "21",
                        "params" :"url = \""+URL+"\";\ndata ={            \"jsonrpc\": \"2.0\",            \"method\": \"item.get\",            \"params\": {                \"output\": \"extend\",                \"hostids\" : "+str(HOST_ID)+",                \"search\": {                    \"key_\": \""+interface[1].replace('/','')+".bandwidth\"                },            },            \"auth\": \""+AUTH+"\",            \"id\": 1}; params = JSON.parse(value);req = new HttpRequest();req.addHeader(\'Content-Type: application/json-rpc\');req.addHeader(\'Authorization: Basic \'+params.authentication);resp = req.post(url, JSON.stringify(data));if (req.getStatus() != 201 && req.getStatus() != 200) {        throw \'Response code: \'+req.getStatus();}resp = JSON.parse(resp);bandwidth = resp[\"result\"][0][\"lastvalue\"];if (bandwidth == 0){ return \"unsupported\";} else {return value*800/bandwidth;}",
                        "error_handler": "0",
                        "error_handler_params": ""
                    }
                ]
            },
            "auth": AUTH,
            "id": 3
        }
        response = requests.post(url, json=payload).json()
        print(json.dumps(response, indent=3, sort_keys=True))

if __name__ == "__main__":
    txUtilization()
