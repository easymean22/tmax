import requests
import json
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from library import *
from variable import *


def ifType():
    url = URL

    # get interface informatiom by snmp
    interfaces = findIndex()

    # calculate intraffic for all interface 
    for interface in interfaces:
        payload = {
            "jsonrpc": "2.0",
            "method": "item.create",
            "params": {
                "hostid" : HOST_ID,
                "name": "Type "+interface[1],
                "key_": "interface."+interface[1].replace('/','')+".type",
                "value_type": 3, #numerinc unsigned
                #"value_type": 4, #text
                "type": 20, #snmp agent
                "interfaceid": HOST_INTERFACEID,
                "snmp_oid" : "1.3.6.1.2.1.2.2.1.3."+interface[0],
                #"units" : "bps",
                "delay" : "1h",
                "history" : "7d",
                "trends" : "0s",
                "tags" : [
                    {
                        "tag": "Interface",
                        "value" : interface[1]
                    },
                    {
                        "tag": "Interface Information",
                        "value" : "type"
                    }
                ],
                "description": "The type of interface.  Additional values for ifType are assigned by the Internet Assigned Numbers Authority (IANA), through updating the syntax of the IANAifType textual convention. ethernetCsmacd(6), -- for all ethernet-like interfaces,-- regardless of speed, as per RFC3635"
            },
            "auth": AUTH,
            "id": 3
        }
        response = requests.post(url, json=payload).json()
        print(json.dumps(response, indent=3, sort_keys=True))

if __name__ == "__main__":
    ifType()
