import getAPI.auth as auth
import configparser
import createAPI.hardware


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8')

    #login and get AUTH token
    res = auth.getToken()
    config['admin']['AUTH'] = res['result']
    with open('config.ini', 'w', encoding='utf-8') as configfile:
         config.write(configfile)
    
    #get host id

    #get host information by snmp

    #get host interface id

    # 
    #print(getAPI.host.findHost('PICOS switch1'))
    #print(createAPI.hardware.operationSystem())
