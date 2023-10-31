from plc_conn import plc_utils

plc = plc_utils.PLC(instance_id=0,
                    ip_address="127.0.0.1",
                    port=502,
                    plc_type="MEL_FX5U",
                    log=False)
print(type(plc))
# read a single register from the PLC
value = plc.read_bool("M100")  # or "X1" "Y1"
print(value)
# read a 16 bit integer from the PLC
value = plc.read_int16("D100")
print(value)
# read 32 bit from the PLC
value = plc.read_int32("D100")
print(value)

# write a single register to the PLC
op = plc.write_bool("M100", True)  # or control output  "Y1"
print(op)  # "success" or "failure" or "unconfirmed"
# write a 16 bit integer to the PLC
op = plc.write_int16("D100", 1234)
print(op)  # "success" or "failure" or "unconfirmed"
# write 32 bit to the PLC
op = plc.write_int32("D100", 12345678)
print(op)  # "success" or "failure" or "unconfirmed"
