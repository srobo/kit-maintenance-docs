#!/usr/bin/env python
import pyudev
from motor import Motor
import time
import math

def _list_usb_devices(model, subsystem=None):
    "Create a sorted list of USB devices of the given type"
    udev = pyudev.Context()
    devs = list(udev.list_devices( ID_MODEL = model, subsystem=subsystem ))
    # Sort by serial number
    devs.sort( key = lambda x: x['ID_SERIAL_SHORT'] )
    return devs

def get_motor_board():
    devs = _list_usb_devices( 'MCV4B', 'tty')

    srdev = None
    for dev in devs:
        serialnum = dev["ID_SERIAL_SHORT"]

        if "DEVNAME" in dev:
            srdev = Motor( dev["DEVNAME"], 0, 0,
                          serialnum = serialnum )
            break

    return srdev


def main():
    m = get_motor_board()

    if m is None:
        print("Could not find motor board")
        exit(1)

    print("This script will spin each motor forwards and backwards")

    for x in [100*math.sin(2*math.pi*(x/100.0)) for x in range(100)]:
        m.m0.power = x
        m.m1.power = x
        time.sleep(0.05)


if __name__ == '__main__':
    main()
