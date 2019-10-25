import gzip
import logging

from utilities.colorpalette import ColorPalette
import utilities.xp_loader as xp_loader
from utilities.color import Color
import utilities.ansitounicode as ansitounicode
from texture.phenomena.phenomenatexture import PhenomenaTexture
from texture.phenomena.phenomenatype import PhenomenaType
from game.viewport import Viewport
from system.graphics.renderableminimal import RenderableMinimal
from system.graphics.renderable import Renderable
from common.coordinates import Coordinates
from game.mapgenerator import MapGenerator

logger = logging.getLogger(__name__)


class MapManager(object):
    """Draws the map on the screen"""

    def __init__(self, viewport :Viewport):
        self.viewport :Viewport = viewport
        self.playerInMapX :int = 0
        self.xpmap = None
        self.mapRenderables = None
        self.mapGenerator = MapGenerator()


    def loadMap(self, name):
        #self.openXpMap("data/map/{}.xp".format(name))
        self.xpmap = self.mapGenerator.generate()

        # array of len(mapwidth), with arrays
        self.mapRenderables = [None] * self.xpmap['width']
        self.loadMapRenderables(name)


    def getCurrentMapWidth(self) -> int:
        return self.xpmap['width']


    def advance(self, deltaTime):
        if self.mapRenderables is None:
            return

        x = self.viewport.getx() + 1
        maxx = x + 78
        while x < maxx:
            if self.mapRenderables[x] is not None:
                for renderable in self.mapRenderables[x]:
                    renderable.advance(deltaTime)
            x += 1


    def draw(self):
        if self.mapRenderables is None:
            return

        self.drawXp()
        self.drawRenderables()


    def drawRenderables(self):
        # Note: This function should be as fast as possible.
        x = self.viewport.getx() + 1
        maxx = x + 78
        while x < maxx:
            if self.mapRenderables[x] is not None:
                for renderable in self.mapRenderables[x]:
                    renderable.draw()
            x += 1


    def drawXp(self):
        # Note: This function should be as fast as possible.
        xp_file_layer = self.xpmap['layer_data'][0]

        # performance...
        if False:
            if not xp_file_layer['width'] or not xp_file_layer['height']:
                msg = 'Attempted to call load_layer_to_console on data that didn\'t'
                msg += ' have a width or height key, check your data'
                raise AttributeError(msg)

        x = self.viewport.getx() + 1
        maxx = x + 78
        while x < maxx:
            y = 1
            while y < 24:
                cell_data = xp_file_layer['cells'][x][y]
                if cell_data['keycode'] != '':  # dont print empty (space " ") cells
                    char = cell_data['keycode']
                    self.viewport.addstr(
                        y=y,
                        x=x,
                        char=char,
                        color=cell_data['color'],
                        attr=cell_data['attr'],
                        bg=cell_data['bgcolor'],
                        knownDrawable=True,
                        setbg=True)
                y += 1
            x += 1


    def loadMapRenderables(self, map):
        t = PhenomenaTexture(phenomenaType=PhenomenaType.tree1, setbg=True)
        r = Renderable(
            texture=t,
            viewport=self.viewport,
            coordinates=Coordinates(80, 8 - t.height + 1),
            active=True
        )
        self.addTextureToMap(r)

        t = PhenomenaTexture(phenomenaType=PhenomenaType.tree4, setbg=True)
        r = Renderable(
            texture=t,
            viewport=self.viewport,
            coordinates=Coordinates(40, 8 - t.height + 1),
            active=True
        )
        self.addTextureToMap(r)


    def addTextureToMap(self, renderable :RenderableMinimal):
        x = renderable.getLocation().x
        if not self.mapRenderables[x]:
            self.mapRenderables[x] = []

        # We dont add it to esper world, but handle it by ourself in a local
        # array, sorted by x
        self.mapRenderables[x].append(renderable)


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
                # {'keycode': 65, 'fore_r': 178, 'fore_g': 134, 'fore_b': 0, 
                # 'back_r': 0, 'back_g': 0, 'back_b': 0}
                char = xp_file_layer['cells'][x][y]['keycode']
                color = ColorPalette.getColorByRgb(
                    xp_file_layer['cells'][x][y]['fore_r'],
                    xp_file_layer['cells'][x][y]['fore_g'],
                    xp_file_layer['cells'][x][y]['fore_b']
                )
                # we only accept official palette colors. if it is not recognized, i
                # gnore character completely (artefact? misclick?)
                if color is not None:
                    xp_file_layer['cells'][x][y]['color'] = color
                    if char != 32 and char != 0:
                        k = chr(ansitounicode.getUnicode(char))
                        xp_file_layer['cells'][x][y]['keycode'] = k
                    else:
                        xp_file_layer['cells'][x][y]['keycode'] = ''
                else:
                    xp_file_layer['cells'][x][y]['keycode'] = ''
