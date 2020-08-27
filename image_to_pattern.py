import os
import typing

from PIL import Image  # type: ignore

from acnh_types import ACNHColour, ACNHColourMap, ACNHImage, HSVColour
from rgb_to_acnh import convert

max_colours = 15
width = 32
height = 32


def simplify_image(img: str) -> Image:
    os.system("python gimp_plugin.py " + img)
    return Image.open(img + ".out.png").convert("RGBA")


def convert_image(img: str) -> ACNHImage:
    pattern = simplify_image(img)
    return _convert_image(pattern)


def load_image(img: str) -> ACNHImage:
    pattern = Image.open(img + ".out.png")
    assert pattern.width == width
    assert pattern.height == height
    assert pattern.mode == "P"
    assert len(pattern.palette.getdata()[1]) == max_colours * 3
    return _convert_image(pattern.convert("RGBA"))


def _convert_image(img: Image) -> ACNHImage:
    pixel_lookup: typing.Dict[HSVColour, ACNHColour] = {}
    colour_map: typing.List[ACNHColour] = []
    pixels: typing.List[typing.List[int]] = []

    for y in range(height):
        row = []
        for x in range(width):
            r, g, b, a = img.getpixel((x, y))
            if a < 128:
                row.append(15)
            else:
                if (r, g, b) in pixel_lookup:
                    row.append(colour_map.index(pixel_lookup[r, g, b]))
                else:
                    p = pixel_lookup[r, g, b] = convert(r, g, b)
                    row.append(len(colour_map))
                    colour_map.append(p)
        pixels.append(row)

    return typing.cast(ACNHColourMap, tuple(colour_map)), pixels
