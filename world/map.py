import curses

from config import Config
from utilities.colorpalette import ColorPalette
from utilities.colortype import ColorType


class Map(object): 
    """Draws the map on the screen"""

    def __init__(self, win, world): 
        self.win = win
        self.playerInMapX = 0
        self.world = world


    def advance(self): 
        pass


    def draw(self): 
        self.win.move(Config.areaMoveable['miny'], Config.areaMoveable['minx'])
        self.win.hline('-', Config.columns - 2)

        # idx = self.world.worldSprite.coordinates.x + 45
        # self.drawDiagonal(8, idx, 15)
        self.drawDiagonal(8, 45, 15)
        self.drawDiagonal(8, 90, 15)
        #self.drawBlock()


    def drawDiagonal(self, x, y, len):
        n = 0
        while n != len: 
            x += 1
            y -= 1

            n += 1

            self.world.viewport.addstr(
                x, 
                y,
                '/', 
                ColorPalette.getColorByColorType(ColorType.worldmap, None))
