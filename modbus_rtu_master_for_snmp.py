"""
@minimalmodbus==2.1.1
@author: Arinam Chandra, Sohail Akhtar
@date: 09th April 2025
@file: modbus_rtu_master.py
@brief: This script is used to read data from a Modbus slave using the minimalmodbus library.
@company: Baid Power Services Pvt. Ltd

Copyright (c) 2025 Baid Power Services, Inc. All Rights Reserved.
"""


import minimalmodbus

def fetch_modbus_value():
    BPS_mb_slave_addr = 1      # Modbus address of slave
    BPS_slave_st_reg_addr = 0  # Register address (3002 is 1 in Modbus addressing)
    BPS_slave_reg_num = 2      # Read only 1 register # 1
    BPS_mb_function_code = 4   # Function code for reading holding registers

    # MODBUS slave address
    BPS_mb_slave = minimalmodbus.Instrument('/dev/ttyUSB0', BPS_mb_slave_addr)

    BPS_mb_slave.serial.baudrate = 9600                                 # BaudRate
    BPS_mb_slave.serial.bytesize = 8                                    # Number of data bits
    BPS_mb_slave.serial.parity = minimalmodbus.serial.PARITY_NONE
    BPS_mb_slave.serial.stopbits = 1                                    # Number of stop bits
    BPS_mb_slave.serial.timeout = 1                                     # Timeout in seconds
    BPS_mb_slave.mode = minimalmodbus.MODE_RTU

    # Pre-execution clean up
    BPS_mb_slave.clear_buffers_before_each_transaction = True
    BPS_mb_slave.close_port_after_each_call = True

    # Read the Modbus register
    try:
        data = BPS_mb_slave.read_registers(BPS_slave_st_reg_addr, BPS_slave_reg_num, BPS_mb_function_code)
        return data[0], data[1]  # Return the first register value (3002)
    except Exception as e:
        return -1  # Return error code if reading fails

if __name__ == '__main__':
    print(fetch_modbus_value())  # This will print the value of register 3002
