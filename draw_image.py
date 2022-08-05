import os

import click

import draw_pattern
import image_to_pattern


@click.command()
@click.argument("fname", type=str)
@click.option(
    "--draw/--no-draw",
    "-d/-D",
    default=True,
    help="Draw/don't draw the pattern after generating; default draw",
)
@click.option(
    "--convert/--use-existing",
    "-c/-u",
    default=True,
    help=(
        "Convert input/use existing output; default convert, "
        "do not add .out.png extension"
    ),
)
def cli(fname, draw, convert):
    if convert:
        pattern = image_to_pattern.convert_image(fname)
        print(f"Generated pattern from {fname}")
    else:
        pattern = image_to_pattern.load_image(fname)
    os.system(f"chafa {fname+'.out.png'!r}")
    if draw:
        draw_pattern.draw(pattern)


if __name__ == "__main__":
    cli()
