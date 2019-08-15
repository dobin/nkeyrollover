import curses

from sprite.coordinates import Coordinates
from utilities.utilities import Utility
from .texture import Texture
from world.viewport import Viewport
from utilities.colorpalette import ColorPalette
from utilities.colortype import ColorType
from utilities.color import Color
from utilities.timer import Timer


class StaticTexture(Texture): 
    def __init__(self, char :str, coordinate :Coordinates, color :Color, time :float): 
        super(StaticTexture, self).__init__(
            parentSprite=None, width=1, height=1, offset=coordinate)

        self.char = char
        self.timer = Timer(time)
        self.color = ColorPalette.getColorByColor(color)


    def advance(self, deltaTime):
        self.timer.advance(deltaTime)

        if self.timer.timeIsUp():
            self.setActive(False)

    
    def draw(self, viewport :Viewport):
        if not self.isActive():
            return

        c = self.getLocation()

        viewport.addstr(
                c.y, 
                c.x,
                self.char, 
                self.color)

