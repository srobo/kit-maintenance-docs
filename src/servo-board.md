# Servo Board Maintenance[^1]

## Equipment

 * Laptop
 * Small flat bladed screwdriver
 * Bench PSU
 * Micro USB cable
 * 7.5mm plug[^2] to fork terminals
 * 1x servo

## Set up

 1. Set the bench PSU to **12V±0.1V** with a **100mA±10mA** current limit.

## Procedure

*Execution time*: 1 minutes per board.

 1. Plug the bench PSU into the power input.
 1. Turn on the bench PSU.
 1. Plug the servo board into the laptop using the micro USB cable.
 1. Check that the green LED next to the USB socket lights up.
 1. Check that the board draws no more than **40mA**.
 1. Run `./scripts/servo_test.py` and follow the instructions.

[^2]: Farnell 3882275
