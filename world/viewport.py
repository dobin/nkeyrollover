import logging
import copy

from sprite.coordinates import Coordinates
from config import Config

logger = logging.getLogger(__name__)


class Viewport(object): 
    def __init__(self, win, world):
        self.win = win
        self.world = world
        self.x = 0

    
    def addstr(self, y, x, char, options=None):
        i = Coordinates(
            x = x, 
            y = y,
        )
        c = self.getScreenCoords(i)
        
        if not self.isPointDrawable(c):
            return

        if options is None:
            self.win.addstr(c.y, c.x, char)
        else: 
            self.win.addstr(c.y, c.x, char, options)


    def getScreenCoords(self, coords):
        c = copy.copy(coords)
        c.x += self.x
        return c


    def isPointDrawable(self, coord :Coordinates): 
        if coord.x > Config.areaDrawable['minx'] and coord.y > Config.areaDrawable['miny'] and coord.x < Config.areaDrawable['maxx'] and coord.y < Config.areaDrawable['maxy']:
            return True
        else:
            return False

    def adjustViewport(self, x): 
        logging.info("-------- Adjust: " + str(x))
        self.x += x