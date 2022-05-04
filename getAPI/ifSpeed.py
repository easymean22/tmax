import requests
import json
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from variable import *


def ifSpeed():
    url = URL

    payload = {
            "jsonrpc": "2.0",
            "method": "item.get",
            "params": {
                "output": "extend",
                "hostids" : HOST_ID,
                "search": {
                    "key_": "bandwidth"
                },
                "sortfield": "name"
            },
            "auth": AUTH,
            "id": 3
    }

    response = requests.post(url, json=payload).json()
    return json.dumps(response, indent=3, sort_keys=True)


if __name__ == "__main__":
    print(ifSpeed())
