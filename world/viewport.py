import logging
import copy

from sprite.coordinates import Coordinates
from config import Config
from messaging import messaging, Messaging, Message, MessageType

logger = logging.getLogger(__name__)


class Viewport(object): 
    def __init__(self, win, world):
        self.win = win
        self.world = world
        self.x = 0
        # For performance reason, we pre-allocate coords for use in getScreenCoords()
        self.viewportCoords = Coordinates()

    
    def getx(self): 
        return self.x 


    def addstr(self, y, x, char, options=None, knownDrawable=False):
        # Note: This function should be as fast as possible. 

        x = x - self.x # getScreenCoords() - fast version

        if not knownDrawable:
            if not self.isPointDrawableXY(x, y): 
                return

        if options is None:
            self.win.addstr(y, x, char)
        else: 
            self.win.addstr(y, x, char, options)


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
        self.x += x


    def advance(self, deltaTime):
        # Check if we need to scroll the window
        for message in messaging.get():
            if message.type is MessageType.PlayerLocation:
                playerScreenCoords = self.getScreenCoords ( 
                    message.data )
                if playerScreenCoords.x >= Config.moveBorderRight:
                    self.adjustViewport(1)
                if playerScreenCoords.x <= Config.moveBorderLeft:
                    self.adjustViewport(-1)