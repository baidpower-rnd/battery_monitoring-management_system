# python==3.11.1
# pysnmp==7.1.19
# Author: Sohail Akhtar

import asyncio
from pysnmp.hlapi.v3arch.asyncio import *

async def run():
    snmpEngine = SnmpEngine()

    target_ip = "192.168.0.193"  # Replace with target IP
    community_string = "public"  # Replace with correct community string
    base_oid_prefix = "1.3.6.1.7.1.4.1.2.13.103.101.116.95.98.109.115.95.98.97.110.107.49"

    # Build list of OIDs from 1 to 61 appended to base OID
    oid_list = [f"{base_oid_prefix}.{i}" for i in range(1, 62)]

    # Create ObjectType list for all OIDs
    object_types = [ObjectType(ObjectIdentity(oid)) for oid in oid_list]

    # SNMP get_cmd can accept multiple ObjectTypes
    iterator = get_cmd(
        snmpEngine,
        CommunityData(community_string, mpModel=0),
        await UdpTransportTarget.create((target_ip, 161)),
        ContextData(),
        *object_types  # unpack list to arguments
    )

    errorIndication, errorStatus, errorIndex, varBinds = await iterator

    if errorIndication:
        print("Error:", errorIndication)
    elif errorStatus:
        print(
            "{} at {}".format(
                errorStatus.prettyPrint(),
                errorIndex and varBinds[int(errorIndex) - 1][0] or "?"
            )
        )
    else:
        for varBind in varBinds:
            #print(varBind[0].prettyPrint(), " = ", varBind[1].prettyPrint())
            print(varBind[1].prettyPrint())

    snmpEngine.close_dispatcher()

if __name__ == "__main__":
    asyncio.run(run())

