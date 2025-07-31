import unittest
from unittest.mock import patch, MagicMock
from terra_ac_modbus import TerraACModbusClient

class TestTerraACModbusClient(unittest.TestCase):

    @patch('terra_ac_modbus.ModbusTcpClient')
    def setUp(self, mock_client_class):
        self.mock_client = MagicMock()
        mock_client_class.return_value = self.mock_client
        self.client = TerraACModbusClient()
        self.client.connect()

    def tearDown(self):
        self.client.close()

    def test_get_serial_number(self):
        self.mock_client.read_holding_registers.return_value.isError.return_value = False
        self.mock_client.read_holding_registers.return_value.registers = [0x1234, 0x5678, 0x9ABC, 0xDEF0]
        result = self.client.get_serial_number()
        self.assertEqual(result, [0x1234, 0x5678, 0x9ABC, 0xDEF0])

    def test_set_charging_current_limit(self):
        self.mock_client.write_registers.return_value.isError.return_value = False
        result = self.client.set_charging_current_limit(16.0)  # 16A
        self.assertIsNotNone(result)
        self.mock_client.write_registers.assert_called_once()

    def test_get_voltage_l1(self):
        self.mock_client.read_holding_registers.return_value.isError.return_value = False
        self.mock_client.read_holding_registers.return_value.registers = [2300, 0]  # 230.0 V
        voltage = self.client.get_voltage_l1()
        self.assertEqual(voltage, 230.0)

    def test_lock_socket(self):
        self.mock_client.write_register.return_value.isError.return_value = False
        response = self.client.lock_socket()
        self.assertIsNotNone(response)
        self.mock_client.write_register.assert_called_once_with(0x4103, 1, unit=1)

if __name__ == '__main__':
    unittest.main()
