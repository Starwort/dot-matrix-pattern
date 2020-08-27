import typing

RGBColour = typing.Tuple[int, int, int]
HSVColour = typing.Tuple[int, int, int]
ACNHColour = typing.Tuple[int, int, int]
ACNHColourMap = typing.Tuple[
    ACNHColour,
    ACNHColour,
    ACNHColour,
    ACNHColour,
    ACNHColour,
    ACNHColour,
    ACNHColour,
    ACNHColour,
    ACNHColour,
    ACNHColour,
    ACNHColour,
    ACNHColour,
    ACNHColour,
    ACNHColour,
    ACNHColour,
]
ACNHImage = typing.Tuple[ACNHColourMap, typing.List[typing.List[int]]]
