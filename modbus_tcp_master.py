from pymodbus.client import ModbusTcpClient
import time
import json

# Set up the Modbus client with port 502
client = ModbusTcpClient('127.0.0.1', port=502)  # Replace with your Modbus server's IP address and port
client.connect()

# Function to read coils
def read_coils():
    # print("Reading coils...")
    result = client.read_coils(address=1, count=8)  # Reading 8 coils starting at address 1
    if result.isError():
        return {"error": f"Error reading coils: {result}"}
    else:
        # Convert the coil bits to 0 and 1
        coils = [1 if bit else 0 for bit in result.bits]
        return coils

# Function to read holding registers and interpret them as specific parameters
def read_holding_registers():
    # print("Reading holding registers...")
    result = client.read_holding_registers(address=1, count=6)  # Reading 6 holding registers starting at address 1
    if result.isError():
        return {"error": f"Error reading holding registers: {result}"}
    else:
        # Assume each register represents a specific parameter
        holding_registers = {
            "voltage": result.registers[0],  # Register 0 holds voltage
            "current": result.registers[1],  # Register 1 holds current
            "power": result.registers[2],    # Register 2 holds power
            "energy": result.registers[3],   # Register 3 holds energy
            "frequency": result.registers[4], # Register 4 holds frequency
            "temperature": result.registers[5] # Register 5 holds temperature
        }
        return holding_registers

# Main loop
try:
    while True:
        # Read coils and holding registers
        coils_data = read_coils()
        holding_registers_data = read_holding_registers()

        # Merge the first three coil values with fault1, fault2, fault3
        faults = {
            "fault1": coils_data[0],  # First coil corresponds to fault1
            "fault2": coils_data[1],  # Second coil corresponds to fault2
            "fault3": coils_data[2]   # Third coil corresponds to fault3
        }

        # Add faults after temperature in the holding register data
        holding_registers_data["fault1"] = faults["fault1"]
        holding_registers_data["fault2"] = faults["fault2"]
        holding_registers_data["fault3"] = faults["fault3"]

        data = holding_registers_data

        # Print the output in JSON format
        print(json.dumps(data, indent=4))

        time.sleep(5)  # Wait 5 seconds before repeating
except KeyboardInterrupt:
    print("Modbus TCP master application terminated.")
finally:
    client.close()  # Always close the connection when done
