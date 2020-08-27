import sys
import typing
from functools import wraps

import io_lib
from acnh_constants import hue_width, sat_width, val_width
from acnh_types import ACNHColour, ACNHColourMap, ACNHImage
from io_lib import Button, Hat

WAIT_BAR = 250  # time to reset HSL bar to either end
WAIT_MOVE = 10  # time between moves
WAIT_COLOURS = 280  # time to reset active colour to #0
WAIT_GRID_RESET = 500  # time to reset grid position to 0,0
_print = print

DEBUG = False


@wraps(_print)
def print(*args, **kw):
    if DEBUG:
        _print(*args, **kw)
        sys.stdout.flush()


def set_bar(position: int, width: int):
    rposition = width - position - 1
    if position < rposition:
        reset_vec = Hat.LEFT
        ctr = position
        active_vec = Hat.RIGHT
    else:
        reset_vec = Hat.RIGHT
        ctr = rposition
        active_vec = Hat.LEFT
    print(f"Resetting bar: {'<-' if reset_vec == Hat.LEFT else '->'}")
    io_lib.press_and_release(reset_vec, WAIT_BAR, WAIT_MOVE)

    print(f"Setting bar: {'<-' if active_vec == Hat.LEFT else '->'} {ctr}")
    for _ in range(ctr):
        io_lib.press_and_release(active_vec, WAIT_MOVE, WAIT_MOVE)
    print("Moving to next bar")
    io_lib.press_and_release(Hat.DOWN, WAIT_MOVE, WAIT_MOVE)
    print("Done")


def create_colour(colour: ACNHColour):
    print("Setting hue")
    set_bar(colour[0], hue_width)
    print("Setting sat")
    set_bar(colour[1], sat_width)
    print("Setting val")
    set_bar(colour[2], val_width)
    print("Done")


def create_colourmap(colour_map: ACNHColourMap):
    print("Moving to far left")
    io_lib.press_and_release(Button.L, WAIT_COLOURS, WAIT_MOVE)
    print("Opening colour map")
    io_lib.press_and_release(Button.X, WAIT_MOVE, WAIT_MOVE)
    io_lib.press_and_release(Hat.UP_RIGHT, WAIT_MOVE, WAIT_MOVE)
    io_lib.press_and_release(Button.A, WAIT_MOVE, WAIT_MOVE * 4)
    for i, colour in enumerate(colour_map):
        print(f"Creating colour map ({i} of 15)")
        create_colour(colour)
        io_lib.press_and_release(Button.R, WAIT_MOVE, WAIT_MOVE)
    print("Exiting colour map")
    io_lib.press_and_release(Button.A, WAIT_MOVE, WAIT_MOVE * 4)
    print("Done")


def ready_field():
    print("Switching to pen tool")
    io_lib.press_and_release(Hat.DOWN_LEFT, WAIT_MOVE, WAIT_MOVE)
    io_lib.press_and_release(Button.A, WAIT_MOVE, WAIT_MOVE)
    print("Moving cursor")
    io_lib.press_and_release(Hat.UP_LEFT, WAIT_GRID_RESET, WAIT_MOVE)
    print("Field is ready")


def quickest_change(
    current_colour: int, target_colour: int
) -> typing.Tuple[Button, int]:
    right = (target_colour - current_colour) % 16
    left = (-right) % 16
    if left < right:
        return Button.L, left
    else:
        return Button.R, right


def draw(image: ACNHImage):
    io_lib.init()
    print("Setting colour map... ", end="")
    create_colourmap(image[0])
    print("Done\nReadying field... ", end="")
    ready_field()

    print("Done\nDrawing pattern... ", end="")
    current_colour = 0
    for lrow, rrow in zip(*([iter(image[1])] * 2)):
        for pix in lrow:
            vector, count = quickest_change(current_colour, pix)
            current_colour = pix
            for _ in range(count):
                io_lib.press_and_release(vector, WAIT_MOVE, WAIT_MOVE)
            io_lib.press_and_release(Button.A, WAIT_MOVE, WAIT_MOVE)
            io_lib.press_and_release(Hat.RIGHT, WAIT_MOVE, WAIT_MOVE)
        io_lib.press_and_release(Hat.DOWN, WAIT_MOVE, WAIT_MOVE)
        for pix in reversed(rrow):
            vector, count = quickest_change(current_colour, pix)
            current_colour = pix
            for _ in range(count):
                io_lib.press_and_release(vector, WAIT_MOVE, WAIT_MOVE)
            io_lib.press_and_release(Button.A, WAIT_MOVE, WAIT_MOVE)
            io_lib.press_and_release(Hat.LEFT, WAIT_MOVE, WAIT_MOVE)
        io_lib.press_and_release(Hat.DOWN, WAIT_MOVE, WAIT_MOVE)
