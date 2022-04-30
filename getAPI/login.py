import requests
import json


def main():
    url = "http://localhost/zabbix/api_jsonrpc.php"

    payload = {
        "jsonrpc" : "2.0",
        "method": "user.login",
        "params": {
            "user": "Admin",
            "password": "zabbix"
            },
        "id": 1,
        "auth": None
    }
    """
    payload = {
        "jsonrpc" : "2.0",
        "method": "apiinfo.version",
        "params": {},
        "id": 1,
        "auth": None
    }
    """

    response = requests.post(url, json=payload).json()
    print(response)


if __name__ == "__main__":
    main()
