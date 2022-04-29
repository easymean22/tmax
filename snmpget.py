from pysnmp.hlapi import *
from variable import *

HOST = HOST_IP # Host ip
PORT = HOST_PORT # snmp default port number
COMMUNITY = HOST_COMMUNITY  #switch's community string


engine = SnmpEngine()
host = UdpTransportTarget((HOST, PORT))
community = CommunityData(COMMUNITY, mpModel=1)
identity_obj_list = [
        ObjectType(ObjectIdentity('1.3.6.1.2.1.2.2.1.2.1')) # OID
        #ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysName', 0))
]


for identity_obj in identity_obj_list:
    iterator = getCmd(engine, community, host, ContextData(), identity_obj)
    errorIndication, errorStatus, errorIndex, varBinds = next(iterator)
    if errorIndication:  # SNMP engine errors
        print(errorIndication)
    else:
        if errorStatus:  # SNMP agent errors
            print('%s at %s' % (errorStatus.prettyPrint(),
                  varBinds[int(errorIndex)-1] if errorIndex else '?'))
        else:
            for varBind in varBinds:  # SNMP response contents
                print(' = '.join([x.prettyPrint() for x in varBind]))



