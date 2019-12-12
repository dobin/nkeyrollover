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
            return color.name, None

        if color is Color.brightwhite:
            color = Screen.COLOUR_WHITE
            attr = Screen.A_BOLD
        elif color is Color.white:
            color = Screen.COLOUR_WHITE
            attr = Screen.A_NORMAL

        elif color is Color.grey:
            color = Screen.COLOUR_BLACK
            attr = Screen.A_BOLD
        elif color is Color.black:
            color = Screen.COLOUR_BLACK
            attr = Screen.A_NORMAL

        elif color is Color.brightblue:
            color = Screen.COLOUR_BLUE
            attr = Screen.A_BOLD
        elif color is Color.blue:
            color = Screen.COLOUR_BLUE
            attr = Screen.A_NORMAL

        elif color is Color.brightcyan:
            color = Screen.COLOUR_CYAN
            attr = Screen.A_BOLD
        elif color is Color.cyan:
            color = Screen.COLOUR_CYAN
            attr = Screen.A_NORMAL

        elif color is Color.brightyellow:
            color = Screen.COLOUR_YELLOW
            attr = Screen.A_BOLD
        elif color is Color.yellow:
            color = Screen.COLOUR_YELLOW
            attr = Screen.A_NORMAL

        elif color is Color.brightred:
            color = Screen.COLOUR_RED
            attr = Screen.A_BOLD
        elif color is Color.red:
            color = Screen.COLOUR_RED
            attr = Screen.A_NORMAL
        elif color is Color.brightmagenta:

            color = Screen.COLOUR_MAGENTA
            attr = Screen.A_BOLD
        elif color is Color.magenta:
            color = Screen.COLOUR_MAGENTA
            attr = Screen.A_NORMAL

        elif color is Color.brightgreen:
            color = Screen.COLOUR_GREEN
            attr = Screen.A_BOLD
        elif color is Color.green:
            color = Screen.COLOUR_GREEN
            attr = Screen.A_NORMAL

        else:
            logger.error("Unknown color: " + str(color))

        return color, attr


    @staticmethod
    def getColorByColorType(colorType: ColorType):
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
