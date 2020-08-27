import typing
from enum import Enum
from functools import wraps
from time import sleep

import serial  # type: ignore

_print = print
DEBUG = False


@wraps(_print)
def print(*args, **kw):
    if DEBUG:
        _print(*args, **kw)


def value_map(val: float, lb: float, ub: float, t_lb: float, t_ub: float) -> float:
    adjusted_value = val - lb
    adjusted_ub = ub - lb
    adjusted_t_ub = t_ub - t_lb
    transformed_value = adjusted_value * adjusted_t_ub / adjusted_ub
    return transformed_value + t_lb


class Button(Enum):
    Y = "0"
    B = "1"
    A = "2"
    X = "3"
    L = "4"
    R = "5"
    ZL = "6"
    ZR = "7"
    MINUS = "8"
    PLUS = "9"
    LCLICK = "A"
    RCLICK = "B"
    HOME = "C"
    CAPTURE = "D"


class Hat(Enum):
    UP = "0"
    UP_RIGHT = "1"
    RIGHT = "2"
    DOWN_RIGHT = "3"
    DOWN = "4"
    DOWN_LEFT = "5"
    LEFT = "6"
    UP_LEFT = "7"
    CENTRE = "8"


def stick_position(x_or_y: int) -> str:
    if x_or_y == 0:
        return "0"
    tmp = value_map(x_or_y, -127, 127, 1, 15)
    return hex(round(tmp))[-1]


def stick_command(x: int, y: int, side: Hat = Hat.LEFT) -> str:
    _x, _y = stick_position(x), stick_position(y)
    if side == Hat.LEFT:
        return f"L{_x}M{_y}"
    else:
        return f"R{_x}S{_y}"


switch = serial.Serial()


def init() -> None:
    global switch
    j = 0
    while True:
        print(
            f"\x1b[3;34m[io_lib.py:init()] Trying to connect to /dev/ttyACM{j}...",
            end="\x1b[0m",
        )

        try:
            switch = serial.Serial(f"/dev/ttyACM{j}")
        except KeyboardInterrupt:
            print("\x1b[1;33m [ User Cancel ]\x1b[0m")
            exit(1)
        except:
            try:
                print("\x1b[1;31m [    Error    ]\x1b[0m")
            except KeyboardInterrupt:
                print("\x1b[1;33m [ User Cancel ]\x1b[0m")
                exit(1)
        else:
            print("\x1b[1;32m [   Success   ]\x1b[0m")
            break
        j += 1


def send_data(data: str) -> None:
    switch.write(bytes(data, encoding="ascii"))


def send_stick(x: int, y: int, side: Hat = Hat.LEFT) -> None:
    send_data(stick_command(x, y, side))


def hat_command(
    up: bool = False, left: bool = False, down: bool = False, right: bool = False
) -> str:
    vertical = up - down
    horizontal = left - right

    if vertical == 1 and horizontal == 1:
        return "D" + Hat.UP_LEFT.value
    if vertical == 1 and horizontal == -1:
        return "D" + Hat.UP_RIGHT.value
    if vertical == 1:
        return "D" + Hat.UP.value

    if vertical == -1 and horizontal == 1:
        return "D" + Hat.DOWN_LEFT.value
    if vertical == -1 and horizontal == -1:
        return "D" + Hat.DOWN_RIGHT.value
    if vertical == -1:
        return "D" + Hat.DOWN.value

    if horizontal == 1:
        return "D" + Hat.LEFT.value
    if horizontal == -1:
        return "D" + Hat.RIGHT.value

    return "d"


Pressable = typing.Union[Button, Hat]


def send_hat(
    up: bool = False, left: bool = False, down: bool = False, right: bool = False
) -> None:
    send_data(hat_command(up, left, down, right))


def wait(n: int) -> None:
    send_data(f"W{n}.")
    if n:
        sleep(n / 150)


def press(button: typing.Union[typing.Iterable[Pressable], Pressable]) -> None:
    if isinstance(button, Button):
        send_data(f"B{button.value}")
        print("PRESS", button.name)
    elif isinstance(button, Hat):
        send_data(f"D{button.value}")
        print("MOVE", button.name)
    else:
        for i in button:
            press(i)


def release(button: typing.Union[typing.Iterable[Pressable], Pressable]) -> None:
    if isinstance(button, Button):
        send_data(f"b{button.value}")
        print("RELEASE", button.name)
    elif isinstance(button, Hat):
        send_data(f"d")
        print("NEUTRAL", button.name)
    else:
        for i in button:
            release(i)


@typing.overload
def hat(direction: Hat) -> None:
    ...


@typing.overload
def hat(
    up: bool = False, left: bool = False, down: bool = False, right: bool = False
) -> None:
    ...


def hat(up=False, left=False, down=False, right=False):
    if isinstance(up, Hat):
        send_data(f"D{up.value}")
    else:
        send_hat(up, left, down, right)


def press_and_release(
    buttons: typing.Union[typing.Iterable[Pressable], Pressable],
    hold_for: int,
    wait_after: int,
) -> None:
    press(buttons)
    wait(hold_for)
    release(buttons)
    wait(wait_after)
