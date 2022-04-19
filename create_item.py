import requests
import json


def main():
    url = "http://localhost/zabbix/api_jsonrpc.php"


    {
            "jsonrpc": "2.0",
            "method": "item.create",
            "params": {
                "name": "Free disk space on /home/joe/",
                "key_": "vfs.fs.size[/home/joe/,free]",
                "hostid": "10084",
                "type": 0,
                "value_type": 3,
                "interfaceid": "1",
                "delay": 30
                },
            "auth": "e4b2faf37a2cc90dd38a8630bfe9b9da",
            "id": 3
    }
    response = requests.post(url, json=payload).json()
    print(response)


if __name__ == "__main__":
    main()
