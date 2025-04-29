"""
@author: Arinam Chandra
@date: 09th April 2025
@file: modbus.py
@brief: This script is used to read data from a Modbus slave using the minimalmodbus library.
@company: Baid Power Services Pvt. Ltd

Copyright (c) 2025 Baid Power Services, Inc. All Rights Reserved.
"""

# Imports
import minimalmodbus

BPS_mb_slave_addr = 1      # Modbus address of slave
BPS_slave_st_reg_addr = 0  # Starting register address (0 corresponds to 3001, 1 to 3002, etc.)
BPS_slave_reg_num = 10     # Number of registers to read
BPS_mb_function_code = 4   # Function code for reading holding registers

# MODBUS slave address
BPS_mb_slave = minimalmodbus.Instrument('/dev/ttyUSB0', BPS_mb_slave_addr)

BPS_mb_slave.serial.baudrate = 9600                                 # BaudRate
BPS_mb_slave.serial.bytesize = 8                                    # Number of data bits to be requested
BPS_mb_slave.serial.parity = minimalmodbus.serial.PARITY_NONE
BPS_mb_slave.serial.stopbits = 1                                    # Number of stop bits
BPS_mb_slave.serial.timeout = 1                                     # Timeout time in seconds
BPS_mb_slave.mode = minimalmodbus.MODE_RTU

# Pre-execution clean up
BPS_mb_slave.clear_buffers_before_each_transaction = True
BPS_mb_slave.close_port_after_each_call = True

# Quarry through MODBUS
print("Requesting Data From Slave...")
data = BPS_mb_slave.read_registers(BPS_slave_st_reg_addr, BPS_slave_reg_num, BPS_mb_function_code)

# Data output
print("")
print(f"Data Table...")
print(" --------------------------------------")
print("|  Register Address   ||      Value     |")
print(" --------------------------------------")
for i in range(len(data)):
    BPS_slave_reg_address = 3001 + i
    print(f"|      {str(BPS_slave_reg_address):^5}           ||     {str(data[i]):^5}     |")
print(" --------------------------------------")
print("")

# Close MODBUS
BPS_mb_slave.serial.close()
print("Ports Now Closed")
