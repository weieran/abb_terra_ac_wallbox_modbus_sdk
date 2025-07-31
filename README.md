# Terra AC Modbus SDK

Python SDK and CLI to control ABB Terra AC Wallbox via Modbus TCP.

## Features

- Read charger information (firmware, power, voltage, energy, state)
- Start/stop charging sessions
- Lock/unlock charging cable (for socket-based chargers)
- Set current limits and communication timeout

## Files

- `terra_ac_modbus.py`: Main SDK library
- `terra_cli.py`: CLI tool for quick control from terminal
- `test_terra_ac_modbus.py`: Unit tests using `unittest` and `unittest.mock`

## Requirements

```bash
python3 -m venv venv
. venv/bin/activate
pip3 install pymodbus==3.5.1
```

## CLI Usage

```bash
python3 terra_cli.py status
python3 terra_cli.py start
python3 terra_cli.py stop
python3 terra_cli.py set_current --amperes 16
python3 terra_cli.py lock
python3 terra_cli.py unlock
```

## Run Unit Tests

```bash
python3 -m unittest test_terra_ac_modbus.py
```