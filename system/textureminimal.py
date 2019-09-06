import logging

from utilities.timer import Timer
from utilities.color import Color
from utilities.colorpalette import ColorPalette
from utilities.colortype import ColorType


class TextureMinimal(object): 
    def __init__(
        self, 
        char :str, 
        colorArr, 
        timeArr,
        movementX :int =0, 
        movementY :int =0,

    ):
        self.width = 1
        self.height = 1
        self.char = char
        self.movementX = movementX
        self.movementY = movementY
        self.timeArr = timeArr
        self.colorArr = colorArr

        self.idx = 0
        self.timer = Timer( self.timeArr[ 0 ] )
        self.color = ColorPalette.getColorByColorType(ColorType.specktexture, None)

    def advance(self, dt):
        self.timer.advance(dt)

