import logging
import copy
import random

from utilities.color import Color
from utilities.colorpalette import ColorPalette
from asciimatics.screen import Screen

logger = logging.getLogger(__name__)


class MapGenerator(object):
    def __init__(self):
        self.topborder = 8


    def generate(self):
        width = 800
        height = 25

        cells = self.generateCity(width, height)

        xpmap = {
            'layer_data': [
                {
                    'width': width,
                    'height': height,
                    'cells': cells,
                }
            ],
            'width': width,
            'height': height,
        }

        return xpmap


    def generateCity(self, width, height):
        # generate complete map
        color, attr = ColorPalette.getColorByColor(Color.black)
        bg, _ = ColorPalette.getColorByColor(Color.black)
        emptyCell = {
            'keycode': '',
            'color': color,
            'bgcolor': bg,
            'attr': attr,
        }
        cells = [[copy.copy(emptyCell) for i in range(height)] for j in range(width)]

        # fill map

        # street border
        y = self.topborder
        x = 0
        while x < width:
            cells[x][y]['keycode'] = '─'
            cells[x][y]['attr'] = Screen.A_BOLD
            x += 1

        # street horizontal
        y = self.topborder + 7
        x = 0
        while x < width:
            if x % 6 == 0:
                cells[x][y]['keycode'] = '─'
                cells[x + 1][y]['keycode'] = '─'
                cells[x][y]['attr'] = Screen.A_BOLD
                cells[x + 1][y]['attr'] = Screen.A_BOLD
            x += 1

        # street vertical/diagonal
        y = self.topborder + 7
        x = 0
        logging.info("W: {}".format(width))
        while x < width - 40:
            if x % 80 == 0:
                # logging.info("L: {}".format(x))
                xx = 0
                yy = 24
                while xx < 16:
                    cells[x + xx][yy]['keycode'] = '/'
                    cells[x + xx][yy]['attr'] = Screen.A_BOLD
                    xx += 1
                    yy -= 1
            x += 1

        # buildings
        x = 0
        while x < width - 8:
            xOff = random.choice([-1, -2, 0, 1, 2])
            theight = random.choice([4, 5, 6, 7])
            yOff = self.topborder - theight + 1
            twidth = random.choice([4, 5, 6])

            x += xOff
            y = yOff
            #logging.info("Create tower: {}/{}  height: {}  width: {}".format(
            #    x, y, height, width
            #))
            #logging.info("Y: {} {} {}".format(self.topborder, theight, y))

            c = self.createTower(theight, twidth)
            self.insertArr(cells, c, x, y)

            x += twidth

        return cells


    def createTower(self, height, width):
        color, attr = ColorPalette.getColorByColor(Color.black)
        bg, _ = ColorPalette.getColorByColor(Color.black)
        emptyCell = {
            'keycode': '',
            'color': color,
            'bgcolor': bg,
            'attr': attr,
        }
        cells = [[copy.copy(emptyCell) for i in range(height)] for j in range(width)]

        m = ' '
        bgColors = random.choice([
            ColorPalette.getColorByColor(Color.blue),
            ColorPalette.getColorByColor(Color.blue),
            ColorPalette.getColorByColor(Color.black),
        ])
        # attr = random.choice(
        #     None,
        #     Screen.A_BOLD
        # )

        x = 0
        while x < len(cells):
            y = 0
            while y < len(cells[x]):
                # corner bottom left
                if x == 0 and y == len(cells[0]) - 1:
                    cells[x][y]['keycode'] = '┴'
                    cells[x][y]['attr'] = Screen.A_BOLD
                # corner top left
                elif x == 0 and y == 0:
                    cells[x][y]['keycode'] = '┌'
                    cells[x][y]['attr'] = Screen.A_BOLD

                # corner bottom right
                elif x == len(cells) - 1 and y == len(cells[0]) - 1:
                    cells[x][y]['keycode'] = '┴'
                    cells[x][y]['attr'] = Screen.A_BOLD
                # corner top right
                elif x == len(cells) - 1 and y == 0:
                    cells[x][y]['keycode'] = '┐'
                    cells[x][y]['attr'] = Screen.A_BOLD

                elif x == 0:
                    cells[x][y]['keycode'] = '│'
                    cells[x][y]['attr'] = Screen.A_BOLD
                elif x == len(cells) - 1:
                    cells[x][y]['keycode'] = '│'
                    cells[x][y]['attr'] = Screen.A_BOLD
                elif y == 0:
                    cells[x][y]['keycode'] = '─'
                    cells[x][y]['attr'] = Screen.A_BOLD
                elif y == len(cells[0]) - 1:
                    cells[x][y]['keycode'] = '─'
                    cells[x][y]['attr'] = Screen.A_BOLD

                else:
                    cells[x][y]['keycode'] = m
                    cells[x][y]['bgcolor'] = bgColors[0]  # no attr for bgcolor

                y += 1

            x += 1

        # logging.info("A: {}".format(cells))
        return cells


    def insertArr(self, cells, source, xOff, yOff):
        #logging.info("I: {} / {}".format(
        #    xOff, yOff
        #))

        x = 0
        while x < len(source):
            y = 0
            while y < len(source[x]):
                #logging.info("I: {} {} / {} {}".format(
                #    x, xOff, y, yOff
                #))
                cells[x + xOff][y + yOff] = source[x][y]
                y += 1

            x += 1
