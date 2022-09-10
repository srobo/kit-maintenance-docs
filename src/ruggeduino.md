# Ruggeduino Maintenance[^1]

## Equipment

 * Laptop
 * Full size USB cable
 * Ruggeduino test shield

## Set up

 1. Ensure [avrdude][] is installed on the laptop.
 1. Ensure the current user has write access to the serial port the ruggeduinos
    use, typically `/dev/ttyACM0`. On linux you may need to run `sudo usermod -a
    -G dialout $(whoami)`, then logout and back in again.

## Procedure

*Execution time*: 30 seconds per board.

 1. Plug the test shield into the Ruggeduino.
 1. Plug the Ruggeduino into the laptop.
 1. Run `./scripts/ruggeduino_test.py` and follow the instructions.

[avrdude]: https://www.nongnu.org/avrdude/
