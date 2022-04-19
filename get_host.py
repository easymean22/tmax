import requests
import json


def main():
    url = "http://localhost/zabbix/api_jsonrpc.php"


    payload = {
            "jsonrpc": "2.0",
            "method": "host.get",
            "params": {
                "filter":{
                    "host":[
                        "PICOS switch1"
                    ]
                }
            },
            "auth": "e4b2faf37a2cc90dd38a8630bfe9b9da",
            "id": 3
    }
    response = requests.post(url, json=payload).json()
    print(json.dumps(response, indent=3, sort_keys=True))
    #print(response)


if __name__ == "__main__":
    main()
