# Motor Board Maintenance[^1]

## Equipment

 * Laptop
 * Small flat bladed screwdriver
 * Bench PSU
 * Micro USB cable
 * 7.5mm plug[^2] to fork terminals
 * 2x motors with 5mm plugs[^3]

## Set up

 1. Set the bench PSU to **12V±0.1V** with a **4A±100mA** current limit.

## Procedure

*Execution time*: 1 minutes per board.

 1. Plug the bench PSU into the power input.
 1. Plug the motors into the outputs.
 1. Turn on the bench PSU
 1. Check that the green power LED in the centre of the board lights up.
 1. Check that the board draws no more than **40mA**
 1. Plug the motor board into the laptop using the micro USB cable.
 1. Check that the green LED (next to the USB socket) lights up.
 1. Run `./scripts/motor_test.py` and follow the instructions.

[^2]: Farnell 3882275
[^4]: Farnell 3881854
