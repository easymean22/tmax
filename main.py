import getAPI.auth as auth
import getAPI.host as host
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



