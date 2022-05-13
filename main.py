import getAPI.auth as auth
import getAPI.host as host
import createAPI.items as create
import createAPI.item as createSingle
import configparser
import library



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

    if config['item']['Hardware model name'] == 'true':
        res = createSingle.hwItem('Hardware model name')
        if 'result' in res:
            print("CREATE Hardware model name")
    if config['item']['Operation system'] == 'true':
        res = createSingle.hwItem('Operation system')
        if 'result' in res:
            print("CREATE Operation system")
    if config['item']['Serial Number'] == 'true':
        res = createSingle.hwItem('Serial Number')
        if 'result' in res:
            print("CREATE Serial Number")
    if config['item']['description'] == 'true':
        res = createSingle.hwItem('description')
        if 'result' in res:
            print("CREATE description")
    if config['item']['location'] == 'true':
        res = createSingle.hwItem('location')
        if 'result' in res:
            print("CREATE location")
    if config['item']['system name'] == 'true':
        res = createSingle.hwItem('system name')
        if 'result' in res:
            print("CREATE system name")
    if config['item']['Vendor'] == 'true':
        res = createSingle.hwItem('Vendor')
        if 'result' in res:
            print("CREATE Vendor")
    if config['item']['CPU Utilization'] == 'true':
        res = createSingle.pfItem('CPU Utilization')
        if 'result' in res:
            print("CREATE CPU Utilization")
    if config['item']['Total Memory'] == 'true':
        res = createSingle.pfItem('Total Memory')
        if 'result' in res:
            print("CREATE Total Memory")
    if config['item']['Used Memory'] == 'true':
        res = createSingle.pfItem('Used Memory')
        if 'result' in res:
            print("CREATE Used Memory")
    if config['item']['inTraffic'] == 'true':
        res = create.inTraffic()
        if 'result' in res:
            print("CREATE inTraffic")
    if config['item']['outTraffic'] == 'true':
        res = create.outTraffic()
        if 'result' in res:
            print("CREATE outTraffic")
    if config['item']['inDiscards'] == 'true':
        res = create.inDiscards()
        if 'result' in res:
            print("CREATE inDiscards")
    if config['item']['outDiscards'] == 'true':
        res = create.outDiscards()
        if 'result' in res:
            print("CREATE outDiscards")
    if config['item']['inError'] == 'true':
        res = create.inError()
        if 'result' in res:
            print("CREATE inError")
    if config['item']['outError'] == 'true':
        res = create.outError()
        if 'result' in res:
            print("CREATE outError")
    if config['item']['status'] == 'true':
        res = create.status()
        if 'result' in res:
            print("CREATE status")
    if config['item']['type'] == 'true':
        res = create.ifType()
        if 'result' in res:
            print("CREATE ifType")
    if config['item']['bandwidth'] == 'true':
        res = create.ifSpeed()
        if 'result' in res:
            print("CREATE bandwidth")
    if config['item']['rxUtilization'] == 'true':
        create.ifSpeed()
        create.rxUtilization()
        if 'result' in res:
            print("CREATE rxUtilization")
    if config['item']['txUtilization'] == 'true':
        create.ifSpeed()
        res = create.txUtilization()
        if 'result' in res:
            print("CREATE txUtilization")
