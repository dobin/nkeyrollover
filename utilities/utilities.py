import curses
import logging

from config import Config


logger = logging.getLogger(__name__)


class Utility(object):
    @staticmethod
    def distance(coord1, coord2):
        res = {
            'x': 0,
            'y': 0,
            'sum': 0,
        }

        res['x'] = abs(coord1['x'] - coord2['x'])
        res['y'] = abs(coord1['y'] - coord2['y'])
        res['sum'] = res['x'] +res['y']

        return res

    @staticmethod
    def pointInSprite(coord1, sprite2):
        coord2 = sprite2.getLocation()
        if coord1['x'] >= coord2['x'] and coord1['x'] < coord2['x'] + sprite2.width and coord1['y'] >= coord2['y'] and coord1['y'] < coord2['y'] + sprite2.height:
            return True
        else: 
            return False

    @staticmethod
    def isPointDrawable(pos): 
        if pos['x'] > Config.areaDrawable['minx'] and pos['y'] > Config.areaDrawable['miny'] and pos['x'] < Config.areaDrawable['maxx'] and pos['y'] < Config.areaDrawable['maxy']:
            return True
        else:
            return False

    @staticmethod
    def isPointMovable(x, y, width, height): 
        # left boundary
        if x <= Config.areaMoveable['minx']:
            logging.info("1: {} / {} ".format(x, Config.areaMoveable['minx']))
            return False

        # upper boundary
        if y <= Config.areaMoveable['miny'] - height: 
            logging.info("2: {} / {} ".format(y, Config.areaMoveable['miny']))
            return False

        # right boundary
        if x + width >= Config.areaMoveable['maxx']:
            logging.info("3")
            return False

        # lower boundary
        if y + height > Config.areaMoveable['maxy']:
            logging.info("4")
            return False

        return True
