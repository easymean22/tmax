url = "http://localhost/zabbix/api_jsonrpc.php";

data ={ 
            "jsonrpc": "2.0",
            "method": "item.get",
            "params": {
                "output": "extend",
                "hostids" : 10520,
                "search": {
                    "key_": "bandwidth"
                },  
                "sortfield": "name"
            },  
            "auth": "e4b2faf37a2cc90dd38a8630bfe9b9da",
            "id": 1
};

params = JSON.parse(value);
req = new HttpRequest();
req.addHeader('Content-Type: application/json-rpc');
req.addHeader('Authorization: Basic '+params.authentication);

resp = req.post(url, JSON.stringify(data));
if (req.getStatus() != 201 && req.getStatus() != 200) {
        throw 'Response code: '+req.getStatus();
}

resp = JSON.parse(resp);
result= JSON.stringify(resp.result[1])

return result;

