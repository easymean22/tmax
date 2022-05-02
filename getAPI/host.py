import requests
import json
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from variable import *


def findHost(name):
    url = URL

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
            "auth": "e4b2faf37a2cc90dd38a8630bfe9b9da",
            "id": 3
    }
    response = requests.post(url, json=payload).json()
    return json.dumps(response, indent=3, sort_keys=True)


if __name__ == "__main__":
    print(findHost('PICOS switch1'))
