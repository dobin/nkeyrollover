import logging

from common.coordinates import Coordinates
from config import Config

logger = logging.getLogger(__name__)


class Viewport(object):
    def __init__(self, win, world):
        self.win = win
        self.world = world
        # For performance reason, we pre-allocate coords for use in getScreenCoords()
        self.viewportCoords = Coordinates()
        self.x = 0
        self.reset()


    def reset(self):
        self.x = 0


    def getx(self):
        return self.x


    def getRightX(self):
        return self.x + Config.columns - 2


    def addstrStatic(self, y, x, char, color, attr=0, bg=0):
        """Print at a static location (does not move with map)"""
        self.win.print_at(char, x, y, color, attr, bg=bg)


    def addstr(
        self, y, x, char, color, attr=0, bg=0, knownDrawable=False, setbg=False
    ):
        # Note: This function should be as fast as possible.

        x = x - self.x  # getScreenCoords() - fast version

        if not knownDrawable:
            if not self.isPointDrawableXY(x, y):
                return

        if not setbg:
            # we dont actively set a background. assume existing background color
            # if set
            ret = self.win.get_from(x, y)
            if ret is not None and ret[3] != 0:  # ret[3] is bg color
                bg = ret[3]

        self.win.print_at(char, x, y, color, attr, bg=bg)


    def getScreenCoords(self, coords):
        """Returns the screen coordinates of the point coords

        Note that we dont return a copy, but a reference to an internal var.
        """
        self.viewportCoords.x = coords.x - self.x
        self.viewportCoords.y = coords.y
        return self.viewportCoords


    def isPointDrawable(self, coord :Coordinates):
        if coord.x > Config.areaDrawable['minx'] and coord.y > Config.areaDrawable['miny'] and coord.x < Config.areaDrawable['maxx'] and coord.y < Config.areaDrawable['maxy']:
            return True
        else:
            return False


    def isPointDrawableXY(self, x: int, y: int):
        if x > Config.areaDrawable['minx'] and y > Config.areaDrawable['miny'] and x < Config.areaDrawable['maxx'] and y < Config.areaDrawable['maxy']:
            return True
        else:
            return False


    def adjustViewport(self, x):
        if self.x + x > 0:
            self.x += x
            return True
        else:
            return False
