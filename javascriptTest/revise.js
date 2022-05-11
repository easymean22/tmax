"url = \""+URL+"\";

data ={ 
            \"jsonrpc\": \"2.0\",
            \"method\": \"item.get\",
            \"params\": {
                \"output\": \"extend\",
                \"hostids\" : "+HOST_ID+",
                \"search\": {
                    \"key_\": \""+interface[1].replace('/','')+".bandwidth\"
                },
            },  
            \"auth\": \""+AUTH+"\",
            \"id\": 1
};

params = JSON.parse(value);
req = new HttpRequest();
req.addHeader(\'Content-Type: application/json-rpc\');
req.addHeader(\'Authorization: Basic \'+params.authentication);

resp = req.post(url, JSON.stringify(data));
if (req.getStatus() != 201 && req.getStatus() != 200) {
        throw \'Response code: \'+req.getStatus();
}

resp = JSON.parse(resp);
bandwidth = resp[\"result\"][0][\"lastvalue\"];

if (bandwidth == 0){
return \"unsupported\";
} else {
return value*800/bandwidth;
}
"
