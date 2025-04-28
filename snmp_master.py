# python==3.11.1
# pysnmp==7.1.19
# Author: Sohail Akhtar

import asyncio
from pysnmp.hlapi.v3arch.asyncio import *

async def run():
    # Define the SNMP engine
    snmpEngine = SnmpEngine()

    # Define the target IP address and the OID
    target_ip = "192.168.0.192"  # Replace with the target IP address
    community_string = "public"  # Replace with the correct SNMP community string
    oid_to_query = ".1.3.6.1.4.1.9999.1.4.1.2.13.103.101.116.95.98.109.115.95.118.97.108.117.101.1"  # This is sysServices, you can modify this with the desired OID

    # Create the SNMP command
    iterator = get_cmd(
        snmpEngine,
        CommunityData(community_string, mpModel=0),
        await UdpTransportTarget.create((target_ip, 161)),  # SNMP target
        ContextData(),
        ObjectType(ObjectIdentity(oid_to_query)),  # Target the provided OID
    )

    # Execute the command and get results
    errorIndication, errorStatus, errorIndex, varBinds = await iterator

    # Handle errors
    if errorIndication:
        print("Error: ", errorIndication)
    elif errorStatus:
        print(
            "{} at {}".format(
                errorStatus.prettyPrint(),
                errorIndex and varBinds[int(errorIndex) - 1][0] or "?",
            )
        )
    else:
        # Print the results of the query
        for varBind in varBinds:
            print(" = ".join([x.prettyPrint() for x in varBind]))

    # Close the SNMP engine after use
    snmpEngine.close_dispatcher()

# Run the asynchronous function
asyncio.run(run())
