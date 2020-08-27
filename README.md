# Dot Matrix Pattern

This repository contains a selection of files used to print patterns from image files into Animal Crossing: New Horizons' pattern editor.

This is achieved by sending commands to a device which translates them into input from a USB gamepad.

The commands are as follows:

- `Bx`
  - Presses a button
  - `x` is a hexidecimal character 0-D
    - 0 → Y
    - 1 → B
    - 2 → A
    - 3 → X
    - 4 → L
    - 5 → R
    - 6 → ZL
    - 7 → ZR
    - 8 → -
    - 9 → +
    - A → Left stick click
    - B → Right stick click
    - C → Home
    - D → Capture
- `bx`
  - Releases a button
  - `x` is a hexidecimal character 0-D, as above
- `Dx`
  - Presses a direction on the D-pad
  - `x` is a digit 0-8
    - 0 → up
    - 1 → up right
    - 2 → right
    - 3 → down right
    - 4 → down
    - 5 → down left
    - 6 → left
    - 7 → up left
    - 8 → centre
- `d`
  - Releases the D-pad
  - Equivalent to `D8`
- `ax`
  - Moves an axis on a stick
  - `a` is one of:
    - `L` (Left stick x)
    - `M` (left stick y)
    - `R` (Right stick x)
    - `S` (right stick y)
  - `x` is a hexidecimal digit 0-F, representing the signed 4-bit position of the stick within the axis
    - 0 (`0`) is the centre of the axis, -8 (`8`) represents (axis = 0), whereas -7 (`9`) represents (axis = 1) to parallel +7 (`7`), (axis = 255)
    - Complete position table:

      `0` | `1` | `2` | `3` | `4` | `5` | `6` | `7`
      --- | --- | --- | --- | --- | --- | --- | ---
       0  | +19 | +37 | +55 | +73 | +91 |+109 |+127

      `8` | `9` | `A` | `B` | `C` | `D` | `E` | `F`
      --- | --- | --- | --- | --- | --- | --- | ---
      -128| -127| -109| -91 | -73 | -55 | -37 | -19
- `a`
  - Resets an axis on a stick
  - `a` is one of
    - `l` (Left stick x)
    - `m` (left stick y)
    - `r` (Right stick x)
    - `s` (right stick y)
- `Wint.`
  - Waits the specified number of 'frames' (Nintendo Switch hardware reads, 125 per second)
  - `int` is any decimal integer number
- `w`
  - Waits one 'frame' (equivalent to `W1.`)
