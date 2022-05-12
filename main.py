import getAPI.auth as auth
import getAPI.host as host
import createAPI.items as create
import configparser
import library
import pdb



if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8')

    #login and get AUTH token
    res = auth.getToken()
    config['admin']['AUTH'] = res['result']
    with open('config.ini', 'w', encoding='utf-8') as configfile:
         config.write(configfile)
         print("GET AUTH TOKEN.")
    
    #get host id
    res = host.findID()
    config['host']['host_id'] = str(res['result'][0]['hostid'])
    with open('config.ini', 'w', encoding='utf-8') as configfile:
         config.write(configfile)
         print("GET HOST ID..")

    #get host interface id
    res = host.findIfID()
    config['host']['host_interfaceid'] = str(res['result'][0]['interfaceid'])
    with open('config.ini', 'w', encoding='utf-8') as configfile:
         config.write(configfile)
         print("GET HOST INTERFACE ID...")

    
    #get host information
    print("INITIALIZE THE SWITCH INFORMATION")
    library.snmpWalk()


    if config['item']['inTraffic'] == 'true':
        print(create.inTraffic())
    if config['item']['outTraffic'] == 'true':
        print(create.outTraffic())
    if config['item']['inDiscards'] == 'true':
        print(create.inDiscards())
    if config['item']['outDiscards'] == 'true':
        print(create.outDiscards())
    if config['item']['inError'] == 'true':
        print(create.inError())
    if config['item']['outError'] == 'true':
        print(create.outError())
    if config['item']['status'] == 'true':
        print(create.status())
    if config['item']['type'] == 'true':
        print(create.ifType())
    if config['item']['bandwidth'] == 'true':
        print(create.ifSpeed())
    if config['item']['rxUtilization'] == 'true':
        print(create.ifSpeed())
        print(create.rxUtilization())
    if config['item']['txUtilization'] == 'true':
        print(create.ifSpeed())
        print(create.txUtilization())

