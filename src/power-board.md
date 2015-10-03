# Power Board Maintenance[^1]

## Equipment

 * Laptop
 * Small flat bladed screwdriver
 * Spare case panels
 * Bench PSU
 * High-current PSU (>30A @ 12V)
 * Multimeter
 * 4x 96W loads[^2]
 * Micro USB cable
 * XT60 male to spade terminals (for Bench PSU)
 * XT60 male to 7.62mm plug[^3] (for high current PSU)
 * External power connector shorting plug[^4]

## Set up

 1. Set the bench PSU to **12V** with a **200mA** current limit.

## Procedure

*Execution time*: UNKNOWN

 1. Ensure that the procedure outlined in the *General Maintenance* document has been carried out.
 1. Inspect the case for any cracks or missing pieces and replace panels as necessary.
 1. Tug the battery wires and check that the ring terminals are not loose and that the insulation has not pulled back.
 1. Connect the battery wires to the bench PSU.
 1. Connect the power board to the laptop with the micro USB cable.
 1. Turn on the bench PSU and the power board (don't forget the external power connector).
 1. Check that the board draws no more than **????mA**.
 1. Check that the 5V output measures **5V±100mV**.
 1. Check that the fan is spinning.
 1. Slowly turn the bench PSU voltage down to **9V**. When passing **10.2V** the power board should shut off all outputs and start beeping. When passing **9.6V** the power board should turn off completely.
 1. Slowly turn the bench PSU voltage up to **12V**. When passing **11.1V** the power board should turn back on.
 1. Turn off the bench PSU and power board.
 1. Connect the battery wires to the high current PSU.
 1. Connect the dummy loads to the power board outputs `H0`, `H1`, `L0` and `L1`.
 1. Turn on the high current PSU and the power board.
 1. Run `XXXXXXX` and follow the instructions.

[^2]: 1.5Ω 100W resistor to 7.5mm camcon plug (Farnell 3882275)
[^3]: Farnell 1793033
[^4]: 5mm camcon plug (Farnell 3881854) shorted
