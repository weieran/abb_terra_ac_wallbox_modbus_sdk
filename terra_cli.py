import argparse
from terra_ac_modbus import TerraACModbusClient

def main():
    parser = argparse.ArgumentParser(description="CLI for ABB Terra AC Wallbox via Modbus TCP")
    parser.add_argument("action", choices=[
        "status", "start", "stop", "lock", "unlock",
        "set_current", "get_power", "get_voltage", "get_energy"
    ])
    parser.add_argument("--amperes", type=float, help="Charging current in amperes")
    parser.add_argument("--ip", default="192.168.2.20", help="Charger IP address")
    parser.add_argument("--unit", type=int, default=1, help="Modbus unit ID")

    args = parser.parse_args()
    charger = TerraACModbusClient(ip=args.ip, unit_id=args.unit)

    if not charger.connect():
        print("Failed to connect to charger.")
        return

    try:
        if args.action == "status":
            fw = charger.get_firmware_version()
            volts = charger.get_voltage_l1()
            current = charger.get_charging_current_l1()
            power = charger.get_active_power()
            energy = charger.get_energy_delivered()
            print(f"Firmware: {fw}\nVoltage L1: {volts} V\nCurrent L1: {current} A\nPower: {power} W\nEnergy Delivered: {energy} Wh")

        elif args.action == "start":
            charger.start_charging()
            print("Started charging session.")

        elif args.action == "stop":
            charger.stop_charging()
            print("Stopped charging session.")

        elif args.action == "lock":
            charger.lock_socket()
            print("Locked socket.")

        elif args.action == "unlock":
            charger.unlock_socket()
            print("Unlocked socket.")

        elif args.action == "set_current":
            if args.amperes is None:
                print("--amperes is required for set_current")
            else:
                charger.set_charging_current_limit(args.amperes)
                print(f"Set charging current to {args.amperes} A")

        elif args.action == "get_power":
            print(f"Power: {charger.get_active_power()} W")

        elif args.action == "get_voltage":
            print(f"Voltage L1: {charger.get_voltage_l1()} V")

        elif args.action == "get_energy":
            print(f"Energy Delivered: {charger.get_energy_delivered()} Wh")

    finally:
        charger.close()

if __name__ == "__main__":
    main()
