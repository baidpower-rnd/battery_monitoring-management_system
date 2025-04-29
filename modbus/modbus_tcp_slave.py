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
