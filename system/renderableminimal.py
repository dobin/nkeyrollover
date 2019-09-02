import esper
import logging

from utilities.timer import Timer
from utilities.color import Color
from utilities.colorpalette import ColorPalette
from utilities.colortype import ColorType
from world.viewport import Viewport
from sprite.coordinates import Coordinates


class RenderableMinimal(object): 
    def __init__(self, texture, coordinate, active=True): 
        self.texture = texture
        self.coordinates = coordinate
        self.active = active


    def advance(self, dt):
        pass


    def isActive(self):
        return self.active


    def setActive(self, active):
        self.active = active


class TextureChar(object): 
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


class RenderablePhenomena(RenderableMinimal): 
    def __init__(self, texture, coordinate):
        super(RenderablePhenomena, self).__init__(
            texture=texture,
            coordinate=coordinate
        )
