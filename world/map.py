import curses
import gzip
import logging

from config import Config
from utilities.colorpalette import ColorPalette
from utilities.colortype import ColorType
import utilities.xp_loader as xp_loader
from utilities.color import Color
import utilities.ansitounicode as ansitounicode
from texture.phenomena.phenomenatexture import PhenomenaTexture
from texture.phenomena.phenomenatype import PhenomenaType
from texture.texture import Texture
#from world.world import World
from world.viewport import Viewport


class Map(object):
    """Draws the map on the screen"""

    def __init__(self, viewport :Viewport, world):
        self.viewport :Viewport = viewport
        self.playerInMapX :int = 0
        self.world = world
        self.xpmap = None
        self.mapTextures = None
        self.color :Color = ColorPalette.getColorByColor(Color.grey)

        self.openXpMap('data/map/map02.xp')
        self.mapTextures = [ None ] * self.xpmap['width'] # array of len(mapwidth), with arrays
        #self.loadMapTextures('map01')


    def advance(self, deltaTime):
        x = self.viewport.getx() + 1
        maxx = x + 78
        while x < maxx:
            if self.mapTextures[x] is not None:
                for texture in self.mapTextures[x]:
                    texture.advance(deltaTime)
            x += 1


    def draw(self):
        self.drawXp()
        self.drawTextures()


    def drawTextures(self):
        # Note: This function should be as fast as possible.
        x = self.viewport.getx() + 1
        maxx = x + 78
        while x < maxx:
            if self.mapTextures[x] is not None:
                for texture in self.mapTextures[x]:
                    texture.draw(self.viewport)
            x += 1


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
            y = 1
            while y < 24:
                cell_data = xp_file_layer['cells'][x][y]
                if cell_data['keycode'] != '': # dont print empty (space " ") cells
                    char = cell_data['keycode']
                    self.viewport.addstr(
                        y=y, x=x, char=char, options=cell_data['color'], knownDrawable=True)
                y += 1
            x += 1


    def loadMapTextures(self, map):
        t = PhenomenaTexture(parentSprite=None, phenomenaType=PhenomenaType.tree1)
        t.setLocation(50, 8 - t.height)
        self.addTextureToMap(t)

        t = PhenomenaTexture(parentSprite=None, phenomenaType=PhenomenaType.tree4)
        t.setLocation(90, 8 - t.height)
        self.addTextureToMap(t)


    def addTextureToMap(self, texture :Texture):
        x = texture.getLocation().x
        if not self.mapTextures[ x ]:
            self.mapTextures[x] = []

        self.mapTextures[x].append(texture)


    def openXpMap(self, filename):
        with gzip.open(filename, "rb") as f:
            data = f.read()
        xpData = xp_loader.load_xp_string(data)
        self.xpmap = xpData
        self.convertMapAnsiToUnicode()


    def convertMapAnsiToUnicode(self):
        xp_file_layer = self.xpmap['layer_data'][0]
        for x in range(xp_file_layer['width']):
            for y in range(xp_file_layer['height']):
                # {'keycode': 65, 'fore_r': 178, 'fore_g': 134, 'fore_b': 0, 'back_r': 0,
                # 'back_g': 0, 'back_b': 0}
                char = xp_file_layer['cells'][x][y]['keycode']
                color = ColorPalette.getColorByRgb(
                    xp_file_layer['cells'][x][y]['fore_r'],
                    xp_file_layer['cells'][x][y]['fore_g'],
                    xp_file_layer['cells'][x][y]['fore_b']
                )
                # we only accept official palette colors. if it is not recognized, ignore
                # character completely (artefact? misclick?)
                if color is not None:
                    xp_file_layer['cells'][x][y]['color'] = color
                    if char != 32 and char != 0:
                        xp_file_layer['cells'][x][y]['keycode'] = chr(ansitounicode.getUnicode(char))
                    else:
                        xp_file_layer['cells'][x][y]['keycode'] = ''
                else:
                    xp_file_layer['cells'][x][y]['keycode'] = ''