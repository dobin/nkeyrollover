import curses
import gzip
import logging

from config import Config
from utilities.colorpalette import ColorPalette
from utilities.colortype import ColorType
import utilities.xp_loader as xp_loader
from utilities.color import Color
import utilities.ansitounicode as ansitounicode

class Map(object): 
    """Draws the map on the screen"""

    def __init__(self, viewport, world): 
        self.viewport = viewport
        self.playerInMapX = 0
        self.world = world
        self.xpmap = None
        self.color = ColorPalette.getColorByColor(Color.grey)
        self.openMap('texture/textures/map/map01.xp')


    def advance(self): 
        pass


    def draw(self): 
        self.drawXp()


    def drawXp(self):
        # Note: This function should be as fast as possible.
        xp_file_layer = self.xpmap['layer_data'][0]
        # performance...
        #if not xp_file_layer['width'] or not xp_file_layer['height']:
        #    raise AttributeError('Attempted to call load_layer_to_console on data that didn\'t have a width or height key, check your data')
        x = self.viewport.getx() + 1
        maxx = x + 78
        while x < maxx:
        #for x in range(xp_file_layer['width']):
            #for y in range(xp_file_layer['height']):
            y = 2
            while y < 24:
                cell_data = xp_file_layer['cells'][x][y]
                if cell_data != '': # dont print empty (space " ") cells
                    char = cell_data['keycode']
                    # logging.info("{}/{}: {}".format(y, x, char))
                    self.viewport.addstr(
                        y=y, x=x, char=char, options=self.color, knownDrawable=True)
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
        #logging.info(str(xpData))

        self.convertToUnicode()

    def convertToUnicode(self): 
        xp_file_layer = self.xpmap['layer_data'][0]
        for x in range(xp_file_layer['width']):
            for y in range(xp_file_layer['height']):  
                char = xp_file_layer['cells'][x][y]['keycode']
                if char != 32 and char != 0:
                    xp_file_layer['cells'][x][y]['keycode'] = chr(ansitounicode.getUnicode(char))
                else: 
                    xp_file_layer['cells'][x][y]['keycode'] = ''


    
