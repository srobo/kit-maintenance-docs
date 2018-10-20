#!/usr/bin/env python
import pyudev
from power import Power
import time

def _list_usb_devices(model, subsystem=None):
    "Create a sorted list of USB devices of the given type"
    def _udev_compare_serial(x, y):
        """Compare two udev serial numbers"""
        return cmp(x["ID_SERIAL_SHORT"],
                   y["ID_SERIAL_SHORT"])

    udev = pyudev.Context()
    devs = list(udev.list_devices( ID_MODEL = model, subsystem=subsystem ))
    # Sort by serial number
    devs.sort( cmp = _udev_compare_serial )
    return devs

def get_power_board():
    devs = _list_usb_devices( 'Power_board_v4' )

    srdev = None
    for dev in devs:
        serialnum = dev["ID_SERIAL_SHORT"]

        if "BUSNUM" in dev:
            srdev = Power( dev.device_node,
                          busnum = int(dev["BUSNUM"]),
                          devnum = int(dev["DEVNUM"]),
                          serialnum = serialnum )
            break

    return srdev

p = get_power_board()

if p is None:
    print("Could not find power board")
    exit(1)

print("This script will turn the outputs H0, H1, L0 and L1 on incrementally.")
print("The power board should shutdown all outputs and start beeping when the last output turns on")

print("Turning on H0")
p.output[0] = 1
time.sleep(2)

print("Turning on H1")
p.output[1] = 1
time.sleep(2)

print("Turning on L0")
p.output[2] = 1
time.sleep(2)

print("Turning on L1")
p.output[3] = 1

print("The power board should have now shutdown all outputs and started beeping. If not then there is an issue with the over current protection and the board is a fail.")
