import logging
from asciimatics.screen import Screen

from .colortype import ColorType
from game.viewport import Viewport
from .color import Color
import game.isunittest

logger = logging.getLogger(__name__)


class ColorPalette(object):
    @staticmethod
    def getColorByStr(s):
        return Color[s]


    @staticmethod
    def getColorTypeByStr(s):
        return ColorType[s]


    @staticmethod
    def getColorByColor(color :Color):
        if game.isunittest.getIsUnitTest():
            return color.name

        if color is Color.brightwhite:
            return Screen.COLOUR_WHITE | Screen.A_BOLD
        elif color is Color.white:
            return Screen.COLOUR_WHITE
        elif color is Color.grey:
            return Screen.COLOUR_BLACK | Screen.A_BOLD
        elif color is Color.black:
            return Screen.COLOUR_BLACK

        elif color is Color.brightblue:
            return Screen.COLOUR_BLUE | Screen.A_BOLD
        elif color is Color.blue:
            return Screen.COLOUR_BLUE
        elif color is Color.brightcyan:
            return Screen.COLOUR_CYAN | Screen.A_BOLD
        elif color is Color.cyan:
            return Screen.COLOUR_CYAN

        elif color is Color.brightyellow:
            return Screen.COLOUR_YELLOW | Screen.A_BOLD
        elif color is Color.yellow:
            return Screen.COLOUR_YELLOW

        elif color is Color.brightred:
            return Screen.COLOUR_RED | Screen.A_BOLD
        elif color is Color.red:
            return Screen.COLOUR_RED
        elif color is Color.brightmagenta:
            return Screen.COLOUR_MAGENTA | Screen.A_BOLD
        elif color is Color.magenta:
            return Screen.COLOUR_MAGENTA

        elif color is Color.brightgreen:
            return Screen.COLOUR_GREEN | Screen.A_BOLD
        elif color is Color.green:
            return Screen.COLOUR_GREEN

        else:
            logger.error("Unknown color: " + str(color))
            return Screen.COLOUR_WHITE


    @staticmethod
    def getColorByColorType(colorType: ColorType, viewport :Viewport):
        color = 0

        if colorType is ColorType.particle:
            color = ColorPalette.getColorByColor(Color.brightmagenta)

        elif colorType is ColorType.sprite:  # only init?
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

        elif colorType is ColorType.background:
            color = ColorPalette.getColorByColor(Color.white)


        else:
            logger.error("Unknown colortype " + str(colorType))

        return color


    @staticmethod
    # see console.txt for rexpaint palette information
    def getColorByRgb(r :int, g :int, b :int):
        if r == 255 and g == 255 and b == 255:
            return ColorPalette.getColorByColor(Color.brightwhite)
        elif r == 229 and g == 229 and b == 229:
            return ColorPalette.getColorByColor(Color.white)
        elif r == 77 and g == 77 and b == 77:
            return ColorPalette.getColorByColor(Color.grey)
        elif r == 0 and g == 0 and b == 0:
            return ColorPalette.getColorByColor(Color.black)

        elif r == 0 and g == 0 and b == 255:
            return ColorPalette.getColorByColor(Color.brightblue)
        elif r == 0 and g == 0 and b == 205:
            return ColorPalette.getColorByColor(Color.blue)
        elif r == 0 and g == 255 and b == 255:
            return ColorPalette.getColorByColor(Color.brightcyan)
        elif r == 0 and g == 205 and b == 205:
            return ColorPalette.getColorByColor(Color.cyan)
        elif r == 255 and g == 255 and b == 255:
            return ColorPalette.getColorByColor(Color.brightwhite)

        elif r == 255 and g == 255 and b == 0:
            return ColorPalette.getColorByColor(Color.brightyellow)
        elif r == 205 and g == 205 and b == 0:
            return ColorPalette.getColorByColor(Color.yellow)

        elif r == 255 and g == 0 and b == 0:
            return ColorPalette.getColorByColor(Color.brightred)
        elif r == 205 and g == 0 and b == 0:
            return ColorPalette.getColorByColor(Color.red)
        elif r == 255 and g == 0 and b == 255:
            return ColorPalette.getColorByColor(Color.brightmagenta)
        elif r == 205 and g == 0 and b == 205:
            return ColorPalette.getColorByColor(Color.magenta)

        elif r == 0 and g == 255 and b == 0:
            return ColorPalette.getColorByColor(Color.brightgreen)
        elif r == 0 and g == 205 and b == 0:
            return ColorPalette.getColorByColor(Color.green)

        else:
            logger.debug("Unknown color: {}/{}/{}".format(r, g, b))
            return None
