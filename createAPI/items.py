import requests
import json
import os
import sys 
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from library import *
import configparser
import pdb


def status():
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8')
    
    url = config['zabbix']['URL']
    HOST_ID = config['host']['host_id']
    AUTH = config['admin']['auth']
    HOST_INTERFACEID = config['host']['host_interfaceid']

    # get interface informatiom by snmp
    interfaces = findIndex()


    # value mapping test
    payload0 = { 
        "jsonrpc": "2.0",
        "method": "valuemap.get",
        "params": {
            "output": "extend",
            "search": {
                "name" :config['host']['host_name']+" Interface Status",
                }
        },
        "auth": AUTH,
        "id": 1
    }
    response = requests.post(url, json=payload0).json()
    if response['result']:
        valueMapID = response['result'][0]["valuemapid"]
    else: # create value mapping
        payload1 = { 
            "jsonrpc": "2.0",
            "method": "valuemap.create",
            "params": {
                "hostid": HOST_ID,
                "name": config['host']['host_name']+" Interface Status",
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




def outError():
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8')
    
    url = config['zabbix']['URL']
    HOST_ID = config['host']['host_id']
    AUTH = config['admin']['auth']
    HOST_INTERFACEID = config['host']['host_interfaceid']

    # get interface informatiom by snmp
    interfaces = findIndex()

    # calculate intraffic for all interface 
    for interface in interfaces:
        payload = { 
            "jsonrpc": "2.0",
            "method": "item.create",
            "params": {
                "hostid" : HOST_ID,
                "name": "Out Error "+interface[1],
                "key_": "interface."+interface[1].replace('/','')+".outerror",
                "value_type": 3, #numerinc unsigned
                #"value_type": 4, #text
                "type": 20, #snmp agent
                "interfaceid": HOST_INTERFACEID,
                "snmp_oid" : "1.3.6.1.2.1.2.2.1.20."+interface[0], #in octect oid = 1.3.6.1.2.1.2.2.1.10.+index
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
                        "value" : "out error"
                    }
                ],
                "preprocessing": [ #get 'simple change' to catch peak
                    {
                        "type": "9",
                        "params": "",
                        "error_handler": "1",
                        "error_handler_params": ""
                    }
                ]
                },
            "auth": AUTH,
            "id": 3
        }
        response = requests.post(url, json=payload).json()
    return response
    #print(json.dumps(response, indent=3, sort_keys=True))



def inTraffic():
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8')

    url = config['zabbix']['URL']
    HOST_ID = config['host']['host_id']
    AUTH = config['admin']['auth']
    HOST_INTERFACEID = config['host']['host_interfaceid']

    # get interface informatiom by snmp
    interfaces = findIndex()

    # calculate intraffic for all interface 
    for interface in interfaces:
        payload = { 
            "jsonrpc": "2.0",
            "method": "item.create",
            "params": {
                #"hostid" : "10520",
                "hostid" : HOST_ID,
                "name": "In traffic "+interface[1],
                "key_": "interface."+interface[1].replace('/','')+".intraffic",
                "value_type": 3, #numerinc unsigned
                #"value_type": 4, #text
                "type": 20, #snmp agent
                "interfaceid": HOST_INTERFACEID,
                "snmp_oid" : "1.3.6.1.2.1.2.2.1.10."+interface[0], #in octect oid = 1.3.6.1.2.1.2.2.1.10.+index
                "units" : "bps",
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
                        "value" : "in traffic"
                    }
                ],
                "preprocessing": [ #change per second(Octet*8)
                    {
                        "type": "1",
                        "params": "8",
                        "error_handler": "1",
                        "error_handler_params": ""
                    },
                    {
                        "type": "10",
                        "params": "",
                        "error_handler": "1",
                        "error_handler_params": ""
                    }
                ]
                },
            "auth": AUTH,
            "id": 3
        }
        response = requests.post(url, json=payload).json()
    return response


def ifSpeed():
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8')
    url = config['zabbix']['URL']
    HOST_ID = config['host']['host_id']
    AUTH = config['admin']['auth']
    HOST_INTERFACEID = config['host']['host_interfaceid']

    # get interface informatiom by snmp
    interfaces = findIndex()

    # value mapping test
    payload0 = {
        "jsonrpc": "2.0",
        "method": "valuemap.get",
        "params": {
            "output": "extend",
            "search": {
                "name" :config['host']['host_name']+" Bandwidth",
                }
        },
        "auth": AUTH,
        "id": 1
        }
    response = requests.post(url, json=payload0).json()
    if response['result']:
        valueMapID = response['result'][0]["valuemapid"]
    else: # create value mapping
        payload1 = { 
            "jsonrpc": "2.0",
            "method": "valuemap.create",
            "params": {
                "hostid": HOST_ID,
                "name": config['host']['host_name']+" Bandwidth",
                "mappings": [
                    {
                        "type": "0",
                        "value": "0",
                        "newvalue": "unsupported"
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
                "name": "Bandwidth "+interface[1],
                "key_": "interface."+interface[1].replace('/','')+".bandwidth",
                "value_type": 3, #numerinc unsigned
                #"value_type": 4, #text
                "type": 20, #snmp agent
                "interfaceid": HOST_INTERFACEID,
                "snmp_oid" : "1.3.6.1.2.1.2.2.1.5."+interface[0],
                "units" : "bps",
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
                        "value" : "bandwidth"
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


def ifType():
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8')
    
    url = config['zabbix']['URL']
    HOST_ID = config['host']['host_id']
    AUTH = config['admin']['auth']
    HOST_INTERFACEID = config['host']['host_interfaceid']

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
    return response
    #print(json.dumps(response, indent=3, sort_keys=True))




def rxUtilization():
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8')
    
    url = config['zabbix']['URL']
    HOST_ID = config['host']['host_id']
    AUTH = config['admin']['auth']
    HOST_INTERFACEID = config['host']['host_interfaceid']

    # get interface informatiom by snmp
    interfaces = findIndex()

    for interface in interfaces:
        payload = { 
            "jsonrpc": "2.0",
            "method": "item.create",
            "params": {
                "hostid" : HOST_ID,
                "name": "Rx utilization "+interface[1],
                "key_": "interface."+interface[1].replace('/','')+".rxutilization",
                #"value_type": 3, #numerinc unsigned
                "value_type": 4, #text
                "type": 20, #snmp agent
                "interfaceid": HOST_INTERFACEID,
                "snmp_oid" : "1.3.6.1.2.1.2.2.1.10."+interface[0], #in octect oid = 1.3.6.1.2.1.2.2.1.10.+index
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
                        "value" : "Rx utilization"
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
                        "params" :"url = \""+url+"\";\ndata ={            \"jsonrpc\": \"2.0\",            \"method\": \"item.get\",            \"params\": {                \"output\": \"extend\",                \"hostids\" : "+str(HOST_ID)+",                \"search\": {                    \"key_\": \""+interface[1].replace('/','')+".bandwidth\"                },            },            \"auth\": \""+AUTH+"\",            \"id\": 1}; params = JSON.parse(value);req = new HttpRequest();req.addHeader(\'Content-Type: application/json-rpc\');req.addHeader(\'Authorization: Basic \'+params.authentication);resp = req.post(url, JSON.stringify(data));if (req.getStatus() != 201 && req.getStatus() != 200) {        throw \'Response code: \'+req.getStatus();}resp = JSON.parse(resp);bandwidth = resp[\"result\"][0][\"lastvalue\"];if (bandwidth == 0){ return \"unsupported\";} else {return value*800/bandwidth;}",
                        "error_handler": "0",
                        "error_handler_params": ""
                    }
                ]
            },
            "auth": AUTH,
            "id": 3
        }
        response = requests.post(url, json=payload).json()
    return response
    #print(json.dumps(response, indent=3, sort_keys=True))



def outDiscards():
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8')
    
    url = config['zabbix']['URL']
    HOST_ID = config['host']['host_id']
    AUTH = config['admin']['auth']
    HOST_INTERFACEID = config['host']['host_interfaceid']

    # get interface informatiom by snmp
    interfaces = findIndex()

    # calculate intraffic for all interface 
    for interface in interfaces:
        payload = { 
            "jsonrpc": "2.0",
            "method": "item.create",
            "params": {
                "hostid" : HOST_ID,
                "name": "Out Discards "+interface[1],
                "key_": "interface."+interface[1].replace('/','')+".outdiscards",
                "value_type": 3, #numerinc unsigned
                #"value_type": 4, #text
                "type": 20, #snmp agent
                "interfaceid": HOST_INTERFACEID,
                "snmp_oid" : "1.3.6.1.2.1.2.2.1.19."+interface[0],
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
                        "value" : "out discards"
                    }
                ],
                "preprocessing": [ #get 'simple change' to catch a peak
                    {
                        "type": "9",
                        "params": "",
                        "error_handler": "1",
                        "error_handler_params": ""
                    }
                ]
                },
            "auth": AUTH,
            "id": 3
        }
        response = requests.post(url, json=payload).json()
    return response
    #print(json.dumps(response, indent=3, sort_keys=True))




def inError():
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8')
    
    url = config['zabbix']['URL']
    HOST_ID = config['host']['host_id']
    AUTH = config['admin']['auth']
    HOST_INTERFACEID = config['host']['host_interfaceid']

    # get interface informatiom by snmp
    interfaces = findIndex()

    # calculate intraffic for all interface 
    for interface in interfaces:
        payload = { 
            "jsonrpc": "2.0",
            "method": "item.create",
            "params": {
                "hostid" : HOST_ID,
                "name": "In Error "+interface[1],
                "key_": "interface."+interface[1].replace('/','')+".inerror",
                "value_type": 3, #numerinc unsigned
                #"value_type": 4, #text
                "type": 20, #snmp agent
                "interfaceid": HOST_INTERFACEID,
                "snmp_oid" : "1.3.6.1.2.1.2.2.1.14."+interface[0],
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
                        "value" : "in error"
                    }
                ],
                "preprocessing": [ #get 'simple change' to catch a peak
                    {   
                        "type": "9",
                        "params": "", 
                        "error_handler": "1",
                        "error_handler_params": ""
                    }
                ]
                },
            "auth": AUTH,
            "id": 3
        }
        response = requests.post(url, json=payload).json()
        #print(json.dumps(response, indent=3, sort_keys=True))
    return response



def txUtilization():
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8')
    
    url = config['zabbix']['URL']
    HOST_ID = config['host']['host_id']
    AUTH = config['admin']['auth']
    HOST_INTERFACEID = config['host']['host_interfaceid']

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
                        "params" :"url = \""+url+"\";\ndata ={            \"jsonrpc\": \"2.0\",            \"method\": \"item.get\",            \"params\": {                \"output\": \"extend\",                \"hostids\" : "+str(HOST_ID)+",                \"search\": {                    \"key_\": \""+interface[1].replace('/','')+".bandwidth\"                },            },            \"auth\": \""+AUTH+"\",            \"id\": 1}; params = JSON.parse(value);req = new HttpRequest();req.addHeader(\'Content-Type: application/json-rpc\');req.addHeader(\'Authorization: Basic \'+params.authentication);resp = req.post(url, JSON.stringify(data));if (req.getStatus() != 201 && req.getStatus() != 200) {        throw \'Response code: \'+req.getStatus();}resp = JSON.parse(resp);bandwidth = resp[\"result\"][0][\"lastvalue\"];if (bandwidth == 0){ return \"unsupported\";} else {return value*800/bandwidth;}",
                        "error_handler": "0",
                        "error_handler_params": ""
                    }
                ]
            },
            "auth": AUTH,
            "id": 3
        }
        response = requests.post(url, json=payload).json()
    return response
    #print(json.dumps(response, indent=3, sort_keys=True))


def outTraffic():
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8')

    url = config['zabbix']['URL']
    HOST_ID = config['host']['host_id']
    AUTH = config['admin']['auth']
    HOST_INTERFACEID = config['host']['host_interfaceid']

    # get interface informatiom by snmp
    interfaces = findIndex()

    # calculate intraffic for all interface 
    for interface in interfaces:
        payload = { 
            "jsonrpc": "2.0",
            "method": "item.create",
            "params": {
                "hostid" : HOST_ID,
                "name": "Out traffic "+interface[1],
                "key_": "interface."+interface[1].replace('/','')+".outtraffic",
                "value_type": 3, #numerinc unsigned
                "type": 20, #snmp agent
                "interfaceid": HOST_INTERFACEID,
                "snmp_oid" : "1.3.6.1.2.1.2.2.1.16."+interface[0], #out octect oid = 1.3.6.1.2.1.2.2.1.10.+index
                "units" : "bps",
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
                        "value" : "out traffic"
                    }
                ],
                "preprocessing": [ #change per second(Octet*8)
                    {
                        "type": "1",
                        "params": "8",
                        "error_handler": "1",
                        "error_handler_params": ""
                    },
                    {
                        "type": "10",
                        "params": "",
                        "error_handler": "1",
                        "error_handler_params": ""
                    }
                ]
                },
            "auth": AUTH,
            "id": 3
        }
        response = requests.post(url, json=payload).json()
    return response
    #print(json.dumps(response, indent=3, sort_keys=True))



def inDiscards():
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8')

    url = config['zabbix']['URL']
    HOST_ID = config['host']['host_id']
    AUTH = config['admin']['auth']
    HOST_INTERFACEID = config['host']['host_interfaceid']

    # get interface informatiom by snmp
    interfaces = findIndex()

    # calculate intraffic for all interface
    for interface in interfaces:
        payload = {
            "jsonrpc": "2.0",
            "method": "item.create",
            "params": {
                "hostid" : HOST_ID,
                "name": "In Discards "+interface[1],
                "key_": "interface."+interface[1].replace('/','')+".indiscards",
                "value_type": 3, #numerinc unsigned
                #"value_type": 4, #text
                "type": 20, #snmp agent
                "interfaceid": HOST_INTERFACEID,
                "snmp_oid" : "1.3.6.1.2.1.2.2.1.13."+interface[0],
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
                        "value" : "in discards"
                    }
                ],
                "preprocessing": [ #get 'simple change' to catch a peak
                    {
                        "type": "9",
                        "params": "",
                        "error_handler": "1",
                        "error_handler_params": ""
                    }
                ]
                },
            "auth": AUTH,
            "id": 3
        }
        response = requests.post(url, json=payload).json()
    return response
    #print(json.dumps(response, indent=3, sort_keys=True))


