import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from pysnmp.hlapi import *
from variable import *

HOST = HOST_IP # Host ip
PORT = HOST_PORT # snmp default port number
COMMUNITY = HOST_COMMUNITY  #switch's community string
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
            if errorStatus:  # SNMP agent errors
                print('%s at %s' % (errorStatus.prettyPrint(),
                    varBinds[int(errorIndex)-1] if errorIndex else '?'))
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

