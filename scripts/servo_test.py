#!/usr/bin/env python
import pyudev
from servo import Servo
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

def get_servo_board():
    devs = _list_usb_devices( 'Servo_Board_v4' )

    srdev = None
    for dev in devs:
        serialnum = dev["ID_SERIAL_SHORT"]

        if "BUSNUM" in dev:
            srdev = Servo( dev.device_node,
                          busnum = int(dev["BUSNUM"]),
                          devnum = int(dev["DEVNUM"]),
                          serialnum = serialnum )
            break

    return srdev

s = get_servo_board()

if s is None:
    print "Could not find servo board"
    exit(1)

print "This script will sweep all servo outputs back and forth."
print "Plug a single servo one and a time into each output and check it moves."

def set_all(p):
    for x in range(12):
        s[x] = p

quit = False
while not quit:
    set_all(100)
    time.sleep(0.5)
    set_all(-100)
    time.sleep(0.5)
