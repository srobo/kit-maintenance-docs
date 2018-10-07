#!/usr/bin/env python3

"""
Servo board test script.

This will:

 - open up a servo board over USB
 - initialise the switch mode power supply output
 - sweep all servo outputs back and forth
"""

import time
from typing import Any, Iterable, NamedTuple, Optional

import usb.core
import usb.util


class USBDevice(NamedTuple):
    """A single device found on USB."""

    serial: str
    node: usb.core.Device
    busnum: int
    devnum: int


def _enumerate_usb_devices(*, product: int, vendor: int) -> Iterable[USBDevice]:
    """Create a sorted list of USB devices of the given type."""
    devices = list(usb.core.find(find_all=True, idProduct=product, idVendor=vendor))
    devices.sort(key=lambda x: x.serial_number)
    for device in devices:
        yield USBDevice(
            serial=device.serial_number,
            busnum=device.bus,
            devnum=device.address,
            node=device,
        )


class ServoBoard(object):
    """A single servo board interface (backed by a USBDevice)."""

    def __init__(self, device: USBDevice) -> None:
        """Construct servo board from `USBDevice`."""
        self.device = device
        self._configuration: Optional[usb.core.Endpoint]
        self._configuration = None

    def open(self) -> None:
        """
        Open connection to the USB device.

        If we have alread set up for this device, this raises a `ValueError`.
        """
        if self._configuration is not None:
            raise ValueError("Servo board is already opened")
        self._open()

    def close(self) -> None:
        """
        Close connection to USB device, freeing up resources.

        This is idempotent.
        """
        if self._configuration is None:
            # Idempotent, do nothing
            return
        self._close()
        self._configuration = None

    def __enter__(self) -> "ServoBoard":
        """Enter context manager, opening the connection."""
        self.open()
        return self

    def __exit__(self, exc_type: Any, exc_value: Any, exc_tb: Any) -> None:
        """Leave context manager, closing the connection if it is not already closed."""
        self.close()

    def drive(self, *, channel: int, value: int) -> None:
        """
        Drive one of the servo PWM channels to a particular value.

        The values range between -100 and 100, with -100 representing a 1.25µs
        on-time, 100 representing a 1.75µs on-time, and linearly interpolating
        between for intermediate values.
        """
        channel = int(channel)
        if not (0 <= channel < 12):
            raise ValueError("Channel must be between 0 and 12")

        value = int(value)
        if not (-100 <= value <= 100):
            raise ValueError("Values must be between -100 and 100")

        self._drive(channel, value)

    def _open(self) -> None:
        self._configuration = usb.util.find_descriptor(self.device.node)
        self._configuration.set()

        self._enable_switchmode()

    def _enable_switchmode(self) -> None:
        self.device.node.ctrl_transfer(0, 64, 0, 12, b"")

    def _close(self) -> None:
        self.device.node.finalize()

    def _drive(self, channel: int, value: int) -> None:
        self.device.node.ctrl_transfer(0, 64, value, channel, b"")


def main() -> None:
    """Run the program as from the command-line."""
    servo_board_devices = list(_enumerate_usb_devices(product=0x0011, vendor=0x1BDA))

    if len(servo_board_devices) == 0:
        print("Could not find a servo board on USB")
        exit(1)

    if len(servo_board_devices) > 1:
        print("Multiple servo boards found, please connect only one.")
        for board in servo_board_devices:
            print("  Device: {}".format(board.serial))

    (servo_board_device,) = servo_board_devices

    with ServoBoard(servo_board_device) as servo_board:
        print("This script will sweep all servo outputs back and forth.")
        print("Plug a single servo one and a time into each output and check it moves.")

        def set_all(p: int) -> None:
            """Drive all servo channels to the same value."""
            for x in range(12):
                servo_board.drive(channel=x, value=p)

        try:
            while True:
                set_all(100)
                time.sleep(0.5)
                set_all(-100)
                time.sleep(0.5)
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    main()
