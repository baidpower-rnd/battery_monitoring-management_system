"""
@author: Sohail Akhtar
@date: 11th April 2025
@file: modbus_tcp_slave.py
@brief: This script is used to send data to a Modbus master through TCP using the pymodbus library.
@company: Baid Power Services Pvt. Ltd

Copyright (c) 2025 Baid Power Services, Inc. All Rights Reserved.
"""

from pymodbus.server import StartTcpServer
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext
import logging

# Set up logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)

# Define the data store with sample registers
store = ModbusSlaveContext(
    di=ModbusSequentialDataBlock(0, [0] * 100),  # Discrete Inputs
    co=ModbusSequentialDataBlock(0, [0] * 100),  # Coils
    hr=ModbusSequentialDataBlock(0, [10, 20, 30, 40, 50] * 20),  # Holding Registers
    ir=ModbusSequentialDataBlock(0, [0] * 100)   # Input Registers
)
context = ModbusServerContext(slaves=store, single=True)

# Start the MODBUS TCP server
log.info("Starting MODBUS TCP slave on 0.0.0.0:502")
StartTcpServer(context=context, address=("0.0.0.0", 502))
