# plc_conn

plc_conn is a Python library tailored to provide an intuitive interface for controlling Mitsubishi (e.g., MEL_FX5U) and Siemens PLCs.

# Features

- Multiple PLC Support: Connect seamlessly to a wide range of Mitsubishi and Siemens PLCs.
- Read Operations: Extract boolean values, 16-bit, and 32-bit integers from PLCs.
- Write Operations: Relay boolean, 16-bit, and 32-bit integers to PLCs.
- Flexible Logging: Optional logging capability for enhanced debugging and tracking.



# Basic Usage
Here's a basic usage example to get you started:

```
from plc_conn import plc_utils

plc = plc_utils.PLC(instance_id=0,
                    ip_address="127.0.0.1",
                    port=502,
                    plc_type="MEL_FX5U",
                    log=False)

# Reading from the PLC
value = plc.read_bool("M100")  # or "X1" "Y1"
print(value)

# Writing to the PLC
op = plc.write_bool("M100", True)
print(op)  # "success" or "failure" or "unconfirmed"
```

# Supported PLC Types
Mitsubishi:
"MEL_FX5U" - Mitsubishi FX5U
"MEL_QSER" - Mitsubishi Qseries
"MEL_FX3U" - Mitsubishi FX3U
Siemens:
"SMN_S300" - SIEMENS S300
"SMN_S1200" - SIEMENS S1200
"SMN_S1500" - SIEMENS S1500
"SMN_S200" - SIEMENS S200 smart
For any other PLC type you may open an issue, I will try my best to add the functionality.

# License
This project adopts the MIT License. Kindly check the LICENSE.md file for comprehensive details.

