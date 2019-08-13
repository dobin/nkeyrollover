import curses
import logging

from config import Config
from sprite.coordinates import Coordinates
from sprite.sprite import Sprite

logger = logging.getLogger(__name__)


class Utility(object):
    @staticmethod
    def distance(coord1 :Coordinates, coord2 :Coordinates):
        res = {
            'x': 0,
            'y': 0,
            'sum': 0,
        }

        res['x'] = abs(coord1.x - coord2.x)
        res['y'] = abs(coord1.y - coord2.y)
        res['sum'] = res['x'] + res['y']

        return res

    
    @staticmethod
    def pointInSprite(coord1 :Coordinates, sprite2 :Sprite):
        coord2 = sprite2.getLocation()
        if coord1.x >= coord2.x and coord1.x < coord2.x + sprite2.texture.width and coord1.y >= coord2.y and coord1.y < coord2.y + sprite2.texture.height:
            return True
        else: 
            return False


    @staticmethod
    def isPointMovable(x, y, width, height): 
        # lower boundary
        if y + height > Config.areaMoveable['maxy']:
            return False

        # upper boundary
        if y <= Config.areaMoveable['miny'] - height: 
            return False

        ## left boundary
        #if x <= Config.areaMoveable['minx']:
        #    return False            

        # right boundary
        #if x + width >= Config.areaMoveable['maxx']:
        #    return False

        return True


    @staticmethod
    def getBorder(loc :Coordinates, distance :int =1, width :int =1):
        locs = []

        basex = loc.x - distance 
        basey = loc.y - distance

        dd = distance * 2

        y = basey
        x = basex

        while y <= basey + dd:
            x = basex
            while x <= basex + dd:
                if y == basey or y == basey + dd: 
                    locs.append( Coordinates(
                        x = x,
                        y = y
                    ))
                elif x == basex or x == basex + dd:
                    locs.append( Coordinates(
                        x = x,
                        y = y
                    ))
                x += 1
            y += 1

        return locs 


    @staticmethod
    def getBorderHalf(loc :Coordinates, distance :int =1, width :int =1, partRight=True):
        locs = []

        basex = loc.x - distance 
        basey = loc.y - distance

        dd = distance * 2

        y = basey
        x = basex
        while y <= basey + dd:
            x = basex
            
            while x <= basex + dd:
                if y == basey or y == basey + dd: 
                    locs.append( Coordinates(
                        x = x,
                        y = y
                    ))
                elif x == basex or x == basex + dd:
                    locs.append( Coordinates(
                        x = x,
                        y = y
                    ))
                x += 1
            y += 1

        return locs


    @staticmethod
    def setupLogger():
        # RECORD debug level is used to record/indicate statistical relevant
        # game events
        DEBUG_LEVELV_NUM = logging.WARN + 1 
        logging.addLevelName(DEBUG_LEVELV_NUM, "RECORD")
        def __record(self, message, *args, **kws):
            if self.isEnabledFor(DEBUG_LEVELV_NUM):
                # Yes, logger takes its '*args' as 'args'.
                self._log(DEBUG_LEVELV_NUM, message, args, **kws) 
        logging.Logger.record = __record


    @staticmethod
    def isIdentical(coord1 :Coordinates, coord2: Coordinates) -> bool:
        if coord1.x == coord2.x and coord1.y == coord2.y: 
            return True
        else:
            return False