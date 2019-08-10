import curses

from sprite.coordinates import Coordinates
from utilities.utilities import Utility
from .texture import Texture
from world.viewport import Viewport
from utilities.colorpalette import ColorPalette
from utilities.colortype import ColorType


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
        self.time = 0


    def advance(self, deltaTime):
        self.time += deltaTime

        if not self.time >= self.timeArr[ self.idx ]: 
            return 

        self.time = 0

        self.offset.x += self.movementX
        self.offset.y += self.movementY
        self.idx += 1

        if self.idx == len(self.timeArr): 
            self.setActive(False)

    
    def draw(self, viewport :Viewport):
        if not self.isActive(): 
            return

        c = self.getLocation()

        viewport.addstr(
                c.y, 
                c.x,
                self.char, 
                ColorPalette.getColorByColorType(ColorType.specktexture, None))

