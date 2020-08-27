import typing

from rgb_to_acnh import convert as _convert


def convert(hex: int) -> typing.Tuple[int, int, int]:
    """Converts a 24-bit RGB hex colour to ACNH HSV"""
    return _convert((hex & 0xFF0000) >> 16, (hex & 0xFF00) >> 8, hex & 0xFF)


if __name__ == "__main__":
    import sys
    from acnh_constants import hue_width, sat_width, val_width

    hue_slider_scale = 1
    sat_slider_scale = 1
    val_slider_scale = 1

    if len(sys.argv) == 1:
        hex = int(input("hex: "), base=16)
        ext = ""
    elif len(sys.argv) >= 2:
        hex = int(sys.argv[1], base=16)
        ext = " ".join(sys.argv[2:])
    else:
        print(
            "Invalid number of parameters. Usage: {} [<hex> [comment]]".format(
                sys.argv[0]
            )
        )
        exit(1)

    nh, ns, nv = convert(hex)
    hue_slider = ["░" for i in range(hue_width)]
    hue_slider[nh] = "█"
    sat_slider = ["[]" for i in range(sat_width)]
    sat_slider[ns] = "██"
    val_slider = ["[]" for i in range(val_width)]
    val_slider[nv] = "██"

    print("ACNH colour is:", ext)
    print(
        "".join(i * hue_slider_scale for i in hue_slider),
        f"({nh:02} -> | <- {29-nh:02})",
    )
    print(
        "".join(i * sat_slider_scale for i in sat_slider),
        f"({ns:02} -> | <- {14-ns:02})",
    )
    print(
        "".join(i * val_slider_scale for i in val_slider),
        f"({nv:02} -> | <- {14-nv:02})",
    )
