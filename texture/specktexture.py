import curses
import logging

from sprite.coordinates import Coordinates
from utilities.utilities import Utility
from .texture import Texture
from world.viewport import Viewport
from utilities.colorpalette import ColorPalette
from utilities.colortype import ColorType
from utilities.timer import Timer



class SpeckTexture(Texture): 
    def __init__(self, char, coordinate, movementX, movementY, timeArr, effect): 
        super(SpeckTexture, self).__init__(
            parentSprite=None, width=1, height=1, offset=coordinate)

        self.char = char
        self.effect = effect
        self.movementX = movementX
        self.movementY = movementY
        
        self.idx = 0
        self.timeArr = timeArr
        self.timer = Timer( self.timeArr[ 0 ] )
        self.color = ColorPalette.getColorByColorType(ColorType.specktexture, None)


    def advance(self, deltaTime):
        self.timer.advance(deltaTime)

        if self.timer.timeIsUp():
            self.idx += 1

            if self.idx == len(self.timeArr): 
                self.setActive(False)
                return

            self.timer.setTimer(self.timeArr[ self.idx ])
            self.timer.reset()
            self.timer.start()
            self.offset.x += self.movementX
            self.offset.y += self.movementY

    
    def draw(self, viewport :Viewport):
        if not self.isActive(): 
            return

        c = self.getLocation()

        viewport.addstr(
                c.y, 
                c.x,
                self.char, 
                self.color)

