from enum import Enum, IntEnum
import logging
import curses

from entities.entitytype import EntityType
from .colortype import ColorType
from world.viewport import Viewport

logger = logging.getLogger(__name__)


class Color(IntEnum): 
    brightwhite = 1
    white = 2
    grey = 3
    black = 4

    brightblue = 5
    blue = 6
    brightcyan = 7
    cyan = 8

    brightyellow = 9
    yellow = 10

    brightred = 11
    red = 12
    brightmagenta = 13
    magenta = 14

    brightgreen = 15
    green = 16


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
        curses.init_pair(8, curses.COLOR_BLACK, 0)

        # for skill indication
        curses.init_pair(9, curses.COLOR_WHITE, curses.COLOR_GREEN)
        curses.init_pair(10, curses.COLOR_WHITE, curses.COLOR_RED)

        # intro
        curses.init_pair(11, curses.COLOR_BLACK, curses.COLOR_BLUE )


    @staticmethod
    def getColorByColor(color :Color):
        if color is Color.brightwhite: 
            return curses.color_pair(7) | curses.A_BOLD
        elif color is Color.white: 
            return curses.color_pair(7)
        elif color is Color.grey: 
            return curses.color_pair(8) | curses.A_BOLD
        elif color is Color.black: 
            return curses.color_pair(8)

        elif color is Color.brightblue: 
            return curses.color_pair(5) | curses.A_BOLD
        elif color is Color.blue: 
            return curses.color_pair(5)
        elif color is Color.brightcyan: 
            return curses.color_pair(6) | curses.A_BOLD
        elif color is Color.cyan: 
            return curses.color_pair(6)

        elif color is Color.brightyellow: 
            return curses.color_pair(4) | curses.A_BOLD
        elif color is Color.yellow: 
            return curses.color_pair(4)

        elif color is Color.brightred: 
            return curses.color_pair(3) | curses.A_BOLD
        elif color is Color.red: 
            return curses.color_pair(3)
        elif color is Color.brightmagenta: 
            return curses.color_pair(2) | curses.A_BOLD
        elif color is Color.magenta: 
            return curses.color_pair(2)

        elif color is Color.brightgreen: 
            return curses.color_pair(1) | curses.A_BOLD
        elif color is Color.green: 
            return curses.color_pair(1)

        else: 
            logging.error("Unknown color: " + str(color))
            return curses.color_pair(1)


    @staticmethod
    def getColorByColorType(colorType: ColorType, viewport :Viewport):
        color = 0

        # for unittests using MockWin
        # we always import 'curses', and dont know if we are being unittested
        # in the unittest, we use Viewport, which has method isUnitTest
        if hasattr(viewport, 'isUnitTest'):
            return color

        if colorType is ColorType.particle:
            color = ColorPalette.getColorByColor(Color.brightmagenta)
        
        elif colorType is ColorType.sprite: # only init?
            color = ColorPalette.getColorByColor(Color.green)
        
        elif colorType is ColorType.specktexture:
            color = ColorPalette.getColorByColor(Color.grey)
        
        elif colorType is ColorType.worldmap:
            color = ColorPalette.getColorByColor(Color.grey)
        
        elif colorType is ColorType.scene:
            color = ColorPalette.getColorByColor(Color.white)
        
        elif colorType is ColorType.world:
            color = ColorPalette.getColorByColor(Color.grey)
        
        elif colorType is ColorType.menu:
            color = ColorPalette.getColorByColor(Color.white)
        
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
            return curses.color_pair(5)
        elif entityType is EntityType.takedamage:
            return curses.color_pair(3)
        elif entityType is EntityType.weapon:
            return curses.color_pair(4)
        else: 
            logging.error("unknown color type: " + str(entityType))
            return curses.color_pair(1)