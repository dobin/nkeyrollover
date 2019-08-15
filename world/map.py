import curses
import gzip
import logging

from config import Config
from utilities.colorpalette import ColorPalette
from utilities.colortype import ColorType
import utilities.xp_loader as xp_loader
from utilities.color import Color


class Map(object): 
    """Draws the map on the screen"""

    def __init__(self, viewport, world): 
        self.viewport = viewport
        self.playerInMapX = 0
        self.world = world
        self.xpmap = None
        self.color = ColorPalette.getColorByColor(Color.grey)
        self.openMap('texture/textures/map/test4.xp')


    def advance(self): 
        pass


    def draw(self): 
        self.drawXp()


    def drawXp(self):
        xp_file_layer = self.xpmap['layer_data'][0]
        if not xp_file_layer['width'] or not xp_file_layer['height']:
            raise AttributeError('Attempted to call load_layer_to_console on data that didn\'t have a width or height key, check your data')

        x = self.viewport.getx()
        maxx = x + 78
        while x < maxx:
        #for x in range(xp_file_layer['width']):
            #for y in range(xp_file_layer['height']):
            y = 2
            while y < 24:
                cell_data = xp_file_layer['cells'][x][y]
                if cell_data != 32: # dont print empty (space " ") cells
                    char = chr(cell_data['keycode'])
                    self.viewport.addstr(y, x, char, self.color)
                y += 1
            x += 1


    def drawDiagonal(self, x, y, len):
        n = 0
        while n != len: 
            x += 1
            y -= 1

            n += 1

            self.viewport.addstr(
                x, 
                y,
                '/', 
                ColorPalette.getColorByColorType(ColorType.worldmap, None))


    def openMap(self, filename): 
        with gzip.open(filename, "rb") as f: 
            data = f.read()

        xpData = xp_loader.load_xp_string(data)
        self.xpmap = xpData
        