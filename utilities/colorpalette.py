from enum import Enum
import logging
import curses

from entities.entitytype import EntityType
from .colortype import ColorType
from world.viewport import Viewport

logger = logging.getLogger(__name__)


class Color(Enum): 
    green = 1
    magenta = 2
    red = 3
    yellow = 4
    blue = 5
    cyan = 6
    white = 7

class ColorPalette(object):
    @staticmethod
    def getColorByColor(color :Color):
        return int(color)

    @staticmethod
    def getColorByColorType(colorType: ColorType, viewport :Viewport):
        color = 0

        # for unittests using MockWin
        # we always import 'curses', and dont know if we are being unittested
        # in the unittest, we use Viewport, which has method isUnitTest
        if hasattr(viewport, 'isUnitTest'):
            return color

        if colorType is ColorType.particle:
            color = curses.color_pair(7)
        elif colorType is ColorType.sprite:
            color = curses.color_pair(1)
        elif colorType is ColorType.specktexture:
            color = curses.color_pair(1)
        elif colorType is ColorType.worldmap:
            color = curses.color_pair(7)
        elif colorType is ColorType.scene:
            color = curses.color_pair(7)
        elif colorType is ColorType.world:
            color = curses.color_pair(7)
        elif colorType is ColorType.menu:
            color = curses.color_pair(7) | curses.A_BOLD 
        else: 
            logging.error("Unknown colortype " + str(colorType))

        return color

    @staticmethod 
    def getColorByEntityType(entityType: EntityType, viewport :Viewport):
        if entityType is EntityType.player: 
            return curses.color_pair(7) | curses.A_BOLD 
        elif entityType is EntityType.enemy:
            return curses.color_pair(2)
        elif entityType is EntityType.takedamage:
            return curses.color_pair(3)
        elif entityType is EntityType.weapon:
            return curses.color_pair(4)
        else: 
            logging.error("unknown color type: " + str(entityType))
            return curses.color_pair(1)