from pysnmp.hlapi import *
from variable import *
import pdb

HOST = HOST_IP # Host ip
PORT = HOST_PORT # snmp default port number
COMMUNITY = HOST_COMMUNITY  #switch's community string
mib2 = '1.3.6.1.2.1.'


engine = SnmpEngine()
host = UdpTransportTarget((HOST, PORT))
community = CommunityData(COMMUNITY, mpModel=1)
identity_obj_list = [
        ObjectType(ObjectIdentity(mib2+'2.2.1.2')) # OID
        #ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysName', 0))
]

for identity_obj in identity_obj_list:
    for errorIndication, errorStatus, errorIndex, varBinds in nextCmd(engine,community,host,ContextData(),identity_obj):
        if errorIndication:  # SNMP engine errors
            print(errorIndication)
        else:
            if errorStatus:  # SNMP agent errors
                print('%s at %s' % (errorStatus.prettyPrint(),
                    varBinds[int(errorIndex)-1] if errorIndex else '?'))
            else:
                for varBind in varBinds:  # SNMP response contents
                    pdb.set_trace()
                    oid, value = [x.prettyPrint() for x in varBind]
                    if 
                    #print(' = '.join([x.prettyPrint() for x in varBind]))


