import typing
from colorsys import rgb_to_hsv as _rgb_to_hsv

from acnh_constants import real_hue_width, real_sat_width, real_val_width
from hsv_to_acnh import convert as _convert


def rgb_to_hsv(r: int, g: int, b: int) -> typing.Tuple[float, float, float]:
    """Convert a 24-bit colour into a 0-360, 0-100, 0-100 HSV colour"""
    _r = r / 255
    _g = g / 255
    _b = b / 255
    _h, _s, _v = _rgb_to_hsv(_r, _g, _b)
    return _h * real_hue_width, _s * real_sat_width, _v * real_val_width


def convert(r: int, g: int, b: int) -> typing.Tuple[int, int, int]:
    """Convert a 24-bit RGB colour into an ACNH HSV colour"""
    return _convert(*rgb_to_hsv(r, g, b))


if __name__ == "__main__":
    import sys
    from acnh_constants import hue_width, sat_width, val_width

    hue_slider_scale = 1
    sat_slider_scale = 1
    val_slider_scale = 1

    if len(sys.argv) == 1:
        r = int(input("r: "))
        g = int(input("g: "))
        b = int(input("b: "))
        ext = ""
    elif len(sys.argv) >= 4:
        r, g, b = map(int, sys.argv[1:4])
        ext = " ".join(sys.argv[4:])
    else:
        print(
            "Invalid number of parameters. Usage: {} [<r> <g> <b> [comment]]".format(
                sys.argv[0]
            )
        )
        exit(1)

    nh, ns, nv = convert(r, g, b)
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
