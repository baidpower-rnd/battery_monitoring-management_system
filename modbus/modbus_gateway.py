"""
@author: Sohail Akhtar, Arinam Chandra
@date: 12th April 2025
@file: modbus_gateway.py
@brief: Reads data from a MODBUS RTU slave and serves it as a MODBUS TCP slave.
@company: Baid Power Services Pvt. Ltd

Copyright (c) 2025 Baid Power Services, Inc. All Rights Reserved.
"""

# Imports
import minimalmodbus
from pymodbus.server import StartTcpServer
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext
import logging
import time
import threading

# Configure logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)

# MODBUS RTU Configuration
BPS_mb_slave_addr = 1      # Modbus address of slave
BPS_slave_st_reg_addr = 0  # Starting register address (0 = 3001)
BPS_slave_reg_num = 10     # Number of registers to read
BPS_mb_function_code = 4   # Function code for input registers

# Initialize RTU slave
try:
    BPS_mb_slave = minimalmodbus.Instrument('/dev/ttyUSB0', BPS_mb_slave_addr)
    BPS_mb_slave.serial.baudrate = 9600
    BPS_mb_slave.serial.bytesize = 8
    BPS_mb_slave.serial.parity = minimalmodbus.serial.PARITY_NONE
    BPS_mb_slave.serial.stopbits = 1
    BPS_mb_slave.serial.timeout = 1
    BPS_mb_slave.mode = minimalmodbus.MODE_RTU
    BPS_mb_slave.clear_buffers_before_each_transaction = True
    BPS_mb_slave.close_port_after_each_call = True
except Exception as e:
    log.error(f"Failed to initialize RTU slave: {e}")
    exit(1)

# MODBUS TCP Configuration
store = ModbusSlaveContext(
    di=ModbusSequentialDataBlock(0, [0] * 100),  # Discrete Inputs
    co=ModbusSequentialDataBlock(0, [0] * 100),  # Coils
    hr=ModbusSequentialDataBlock(0, [0] * 100),  # Holding Registers
    ir=ModbusSequentialDataBlock(0, [0] * 100)   # Input Registers
)
context = ModbusServerContext(slaves=store, single=True)

# Function to read RTU and update TCP registers
def update_tcp_registers():
    while True:
        try:
            log.info("Reading data from RTU slave...")
            data = BPS_mb_slave.read_registers(
                BPS_slave_st_reg_addr, BPS_slave_reg_num, BPS_mb_function_code
            )
            # Update TCP holding registers
            store.setValues(3, 0, data)
            log.info(f"Updated TCP registers: {data}")

            # Print table
            print("\nData Table...")
            print(" --------------------------------------")
            print("|  Register Address   ||      Value     |")
            print(" --------------------------------------")
            for i in range(len(data)):
                reg_address = 3001 + i
                print(f"|      {str(reg_address):^5}           ||     {str(data[i]):^5}     |")
            print(" --------------------------------------\n")

        except Exception as e:
            log.error(f"Error reading RTU slave: {e}")
        time.sleep(5)  # Refresh every 5 seconds

# Start the update thread
update_thread = threading.Thread(target=update_tcp_registers, daemon=True)
update_thread.start()

# Start the MODBUS TCP server
log.info("Starting MODBUS TCP slave on 0.0.0.0:502")
StartTcpServer(context=context, address=("0.0.0.0", 502))
