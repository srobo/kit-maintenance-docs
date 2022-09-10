#!/usr/bin/env python
import subprocess
import time

# TODO: lookup the serial port
# TODO: remove requirement that we're in the scripts directory

test_fw = "firmware/ruggeduino_test-1.hex"
fw = "firmware/ruggeduino-1.hex"

def flash_ruggeduino(fw_hex):
    subprocess.check_call(["avrdude", "-p", "atmega328p", "-c", "arduino",
                           "-P" ,"/dev/ttyACM0",  "-D", "-U",
                           "flash:w:{0}:i".format(fw_hex)])

print("Flashing test firmware:")
flash_ruggeduino(test_fw)
print("Look at the LED. Slow flash = PASS; Fast flash = FAIL;")
time.sleep(5)
print("Flashing SR firmware:")
flash_ruggeduino(fw)
