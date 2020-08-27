#!/usr/bin/python3
from typing import Tuple

from acnh_constants import (
    hue_width,
    real_hue_width,
    real_sat_width,
    real_val_width,
    sat_width,
    val_width,
)


def fmap(input: float, min: float, max: float, out_min: float, out_max: float) -> float:
    input -= min
    input /= max
    input *= out_max
    input += out_min
    return input


def imap(input: int, min: int, max: int, out_min: int, out_max: int) -> int:
    input -= min
    input *= out_max
    input //= max
    input += out_min
    return input


def convert(h: float, s: float, v: float) -> Tuple[int, int, int]:
    """Convert 0-360, 0-100, 0-100 HSV to ACNH HSV"""
    return (
        round(fmap(h, 0, real_hue_width, 0, hue_width - 1)),
        round(fmap(s, 0, real_sat_width, 0, sat_width - 1)),
        round(fmap(v, 0, real_val_width, 0, val_width - 1)),
    )


if __name__ == "__main__":
    import sys

    hue_slider_scale = 1
    sat_slider_scale = 1
    val_slider_scale = 1

    if len(sys.argv) == 1:
        h = float(input("hue: "))
        s = float(input("sat: "))
        v = float(input("val: "))
        ext = ""
    elif len(sys.argv) >= 4:
        h, s, v = map(float, sys.argv[1:4])
        ext = " ".join(sys.argv)
    else:
        print(
            "Invalid number of parameters. Usage: {} [<h> <s> <v> [comment]]".format(
                sys.argv[0]
            )
        )
        exit(1)

    nh, ns, nv = convert(h, s, v)
    hue_slider = ["░" for i in range(hue_width)]
    hue_slider[nh] = "█"
    sat_slider = ["[]" for i in range(sat_width)]
    sat_slider[ns] = "██"
    val_slider = ["[]" for i in range(val_width)]
    val_slider[nv] = "██"

    print("ACNH colour is:", ext)
    print("".join(i * hue_slider_scale for i in hue_slider))
    print("".join(i * sat_slider_scale for i in sat_slider))
    print("".join(i * val_slider_scale for i in val_slider))
