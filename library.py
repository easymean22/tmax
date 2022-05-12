import os
import sys
import configparser
from pysnmp.hlapi import *


def snmpWalk():
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8')
    HOST = config['host']['host_ip'] # Host ip
    PORT = config['host']['host_port'] # snmp default port number
    COMMUNITY = config['host']['host_community']  #switch's community string
    #mib2 = '1.3.6.1.2.1.'

    engine = SnmpEngine()
    host = UdpTransportTarget((HOST, PORT))
    community = CommunityData(COMMUNITY, mpModel=1)
    identity_obj_list = [
        ObjectType(ObjectIdentity('1.3.6.1.2.1.2.1')) # OID
        #ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysName', 0))
    ]

    f= open('./current_status', mode='w')
    for identity_obj in identity_obj_list:
        for errorIndication, errorStatus, errorIndex, varBinds in nextCmd(engine,community,host,ContextData(),identity_obj):
            if errorIndication:  # SNMP engine errors
                print(errorIndication)
            else:
                if errorStatus:  # SNMP agent error
                    print('%s at %s' % (errorStatus.prettyPrint(),varBinds[int(errorIndex)-1] if errorIndex else '?'))
                else:
                    for varBind in varBinds:  # SNMP response contents
                        snmpVersion, value = [x.prettyPrint() for x in varBind]
                        oid = snmpVersion.lstrip('SNMPv2-SMI::')
                        oid = oid.replace('mib-2','1.3.6.1.2.1')
                        oid = oid.replace('transmission','1.3.6.1.2.1.10' )
                        f.write(' = '.join([oid, value]))
                        f.write('\n')
                        #pdb.set_trace()
                        #f.write(' = '.join([x.prettyPrint() for x in varBind]))
    f.close()


def findIndex():
    # snmpwalk.py -> current_status -> findIndex()
    # result = ['index', 'interface_description']
    result = []
    sys.path.append(os.path.dirname(__file__))
    f = open('../current_status', 'r')
    lines = f.readlines()
    for line in lines:
        if line.startswith('1.3.6.1.2.1.2.2.1.2.'):
            key, value = line.split(' = ')
            key = key.replace('1.3.6.1.2.1.2.2.1.2.','')
            value = value.replace('\n','')
            result.append([key, value])
    return result

if __name__ == "__main__":
    print(findIndex())


