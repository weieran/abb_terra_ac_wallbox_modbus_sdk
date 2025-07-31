from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusException

class TerraACModbusClient:
    def __init__(self, ip="192.168.2.20", port=502, unit_id=1):
        self.ip = ip
        self.port = port
        self.unit_id = unit_id
        self.client = ModbusTcpClient(host=ip, port=port)

    def connect(self):
        return self.client.connect()

    def close(self):
        self.client.close()

    def read_registers(self, address, count=2):
        try:
            response = self.client.read_holding_registers(address, count, unit=self.unit_id)
            if response.isError():
                raise ModbusException(response)
            return response.registers
        except ModbusException as e:
            print(f"Read failed: {e}")
            return None

    def write_register(self, address, value):
        try:
            response = self.client.write_register(address, value, unit=self.unit_id)
            if response.isError():
                raise ModbusException(response)
            return response
        except ModbusException as e:
            print(f"Write failed: {e}")
            return None

    def write_registers(self, address, values):
        try:
            response = self.client.write_registers(address, values, unit=self.unit_id)
            if response.isError():
                raise ModbusException(response)
            return response
        except ModbusException as e:
            print(f"Write failed: {e}")
            return None

    # High-level API methods below

    def get_serial_number(self):
        return self.read_registers(0x4000, 4)

    def get_firmware_version(self):
        return self.read_registers(0x4004, 2)

    def get_user_settable_max_current(self):
        regs = self.read_registers(0x4006, 2)
        return regs[0] * 0.001 if regs else None

    def get_charging_state(self):
        return self.read_registers(0x400C, 2)

    def get_charging_current_l1(self):
        regs = self.read_registers(0x4010, 2)
        return regs[0] * 0.001 if regs else None

    def get_voltage_l1(self):
        regs = self.read_registers(0x4016, 2)
        return regs[0] * 0.1 if regs else None

    def get_active_power(self):
        regs = self.read_registers(0x401C, 2)
        return regs[0] if regs else None

    def get_energy_delivered(self):
        regs = self.read_registers(0x401E, 2)
        return regs[0] if regs else None

    def set_charging_current_limit(self, amperes):
        value = int(amperes * 1000)
        return self.write_registers(0x4100, [value, 0])

    def lock_socket(self):
        return self.write_register(0x4103, 1)

    def unlock_socket(self):
        return self.write_register(0x4103, 0)

    def start_charging(self):
        return self.write_register(0x4105, 0)

    def stop_charging(self):
        return self.write_register(0x4105, 1)

    def set_communication_timeout(self, seconds):
        return self.write_register(0x4106, seconds)


if __name__ == "__main__":
    charger = TerraACModbusClient()
    if charger.connect():
        print("Connected to charger.")
        print("Firmware version:", charger.get_firmware_version())
        charger.close()
    else:
        print("Connection failed.")
