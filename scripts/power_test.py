#!/usr/bin/env python3

"""
Power board test script.

This will:

 - hopefully not crash
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
    #devices.sort(key=lambda x: x.serial_number)
    for device in devices:
        yield USBDevice(
            serial=0,#device.serial_number,
            busnum=device.bus,
            devnum=device.address,
            node=device,
        )

class PowerBoard(object):
    """A single power board interface (backed by a USBDevice)."""

    def __init__(self, device: USBDevice) -> None:
        """Construct power board from `USBDevice`."""
        self.device = device
        self._configuration: Optional[usb.core.Endpoint]
        self._configuration = None

    def open(self) -> None:
        """
        Open connection to the USB device.

        If we have alread set up for this device, this raises a `ValueError`.
        """
        if self._configuration is not None:
            raise ValueError("Power board is already opened")
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

    def output(self, *, channel: int, value: int) -> None:
        """
        Drive one of the outputs to a required state.
        """
        channel = int(channel)
        if not (0 <= channel < 6):
            raise ValueError("Channel must be between 0 and 6")

        value = int(value)
        if not (0 <= value <= 1):
            raise ValueError("Values must be between 0 and 1")

        self._output(channel, value)

    def _open(self) -> None:
        self._configuration = usb.util.find_descriptor(self.device.node)
        self._configuration.set()
        pass;

    def _close(self) -> None:
        self.device.node.finalize()

    def _output(self, channel: int, value: int) -> None:
        self.device.node.ctrl_transfer(0, 64, value, channel, "\0")



def main() -> None:
    """Run the program as from the command-line."""
    power_board_devices = list(_enumerate_usb_devices(product=0x0010, vendor=0x1BDA))

    if len(power_board_devices) == 0:
        print("Could not find a power board on USB")
        exit(1)

    if len(power_board_devices) > 1:
        print("Multiple servo boards found, please connect only one.")
        for board in power_board_devices:
            print("  Device: {}".format(board.serial))

    (power_board_device,) = power_board_devices

    with PowerBoard(power_board_device) as power_board:
        print("This script will turn the outputs H0, H1, L0 and L1 on incrementally.")
        print("The power board should shutdown all outputs and start beeping when the last output turns on")

        print("Turning on H0")
        power_board.output(channel=0,value=1)
        time.sleep(2)

        print("Turning on H1")
        power_board.output(channel=1,value=1)
        time.sleep(2)

        print("Turning on L0")
        power_board.output(channel=2,value=1)
        time.sleep(2)

        print("Turning on L1")
        power_board.output(channel=3,value=1)

        print("The power board should have now shutdown all outputs and started beeping. If not then there is an issue with the over current protection and the board is a fail.")


if __name__ == "__main__":
    main()
