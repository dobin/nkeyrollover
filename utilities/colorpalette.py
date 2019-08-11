from enum import Enum, IntEnum
import logging
import curses

from entities.entitytype import EntityType
from .colortype import ColorType
from world.viewport import Viewport

logger = logging.getLogger(__name__)


class Color(IntEnum): 
    green = 1
    magenta = 2
    red = 3
    yellow = 4
    blue = 5
    cyan = 6
    white = 7


class ColorPalette(object):
    @staticmethod
    def cursesInitColor():
        # Initialize color pairs
        curses.start_color()    
        curses.init_pair(1, curses.COLOR_GREEN, 0)
        curses.init_pair(2, curses.COLOR_MAGENTA, 0)
        curses.init_pair(3, curses.COLOR_RED, 0)
        curses.init_pair(4, curses.COLOR_YELLOW, 0)
        curses.init_pair(5, curses.COLOR_BLUE, 0)
        curses.init_pair(6, curses.COLOR_CYAN, 0)
        curses.init_pair(7, curses.COLOR_WHITE, 0)
        # for skill indication
        curses.init_pair(8, curses.COLOR_WHITE, curses.COLOR_GREEN)
        curses.init_pair(9, curses.COLOR_WHITE, curses.COLOR_RED)

        # intro
        curses.init_pair(10, curses.COLOR_BLACK, curses.COLOR_BLUE )


    @staticmethod
    def getColorByColor(color :Color):
        return curses.color_pair(int(color))


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
        elif colorType is ColorType.sprite: # only init?
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
        color = 0

        # for unittests using MockWin
        # we always import 'curses', and dont know if we are being unittested
        # in the unittest, we use Viewport, which has method isUnitTest
        if hasattr(viewport, 'isUnitTest'):
            return color

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