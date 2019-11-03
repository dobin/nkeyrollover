import logging
import yaml

from texture.animation import Animation
from common.direction import Direction
from utilities.colorpalette import ColorPalette
from typing import List

logger = logging.getLogger(__name__)


class TextureHelper(object):
    @staticmethod
    def loadYamlIntoAnimation(filename :str, animation :Animation):
        with open(filename, 'r') as stream:
            data = yaml.safe_load(stream)

        try:
            animation.endless = data['endless']
            animation.advanceByStep = data['advanceByStep']
            animation.frameColors = data['frameColors']
        except TypeError as error:
            raise Exception("Error, missing field in yaml file {}, error {}".format(
                filename, error
            ))

        # FrameTime can be non-existing, e.g. if 'advanceByStep' = True,
        # or if it is one frame and endless...
        # Therefore, frameTime will be None, as defined in Animation
        if 'frameTime' in data:
            animation.frameTime = data['frameTime']
            # convert to float
            for (idx, frameTimeEntry) in enumerate(animation.frameTime):
                animation.frameTime[idx] = float(frameTimeEntry)

        if 'direction' in data:
            if data['direction'] == 'left':
                animation.originalDirection = Direction.left
            elif data['direction'] == 'right':
                animation.originalDirection = Direction.right
            else:
                animation.originalDirection = Direction.none

        # colors:
        # - <Color>: white, brightblue, ...
        # - ColorType.<ColorType>: background, world, ...
        for (n, color) in enumerate(data['frameColors']):
            if color.startswith('ColorType.'):
                color = color.split('.')[1]
                colorType = ColorPalette.getColorTypeByStr(color)
                animation.frameColors[n] = ColorPalette.getColorByColorType(
                    colorType)
            else:
                color = ColorPalette.getColorByStr(color)
                animation.frameColors[n] = ColorPalette.getColorByColor(
                    color)


    @staticmethod
    def readAnimationFile(filename :str) -> Animation:
        with open(filename) as f:
            lineList = f.readlines()

        for (idx, msg) in enumerate(lineList):
            lineList[idx] = lineList[idx].lstrip('\n')
            lineList[idx] = lineList[idx].rstrip('\n')

        (res, maxWidth, maxHeight) = TextureHelper.parseAnimationLineList(lineList)

        # replace whitespace ' ' with ''
        for (z, anim) in enumerate(res):
            for (y, rows) in enumerate(anim):
                for (x, column) in enumerate(rows):
                    if res[z][y][x] == ' ':
                        res[z][y][x] = ''
                    if res[z][y][x] == '€':
                        res[z][y][x] = ' '

        animation = Animation()
        animation.arr = res
        animation.width = maxWidth
        animation.height = maxHeight
        animation.frameCount = len(res)

        logger.debug("Loaded {}: width={} height={} animations={}".format(
            filename, animation.width, animation.height, animation.frameCount))

        return animation


    @staticmethod
    def parseAnimationLineList(
        lineList :List[List[str]]
    ) -> (List[List[List[str]]], int, int):
        res = []
        # find longest line to make animation
        maxWidth = 0
        for line in lineList:
            if len(line) > maxWidth:
                maxWidth = len(line)

        maxHeight = 0
        tmp = []
        for line in lineList:
            if line == '':
                # empty line, means new animation.
                # collect previous lines as a single animation frame
                res.append(tmp)
                if len(tmp) > maxHeight:
                    maxHeight = len(tmp)
                tmp = []
            else:
                # make all lines same length
                if not len(line) == maxWidth:
                    line += ' ' * (maxWidth - len(line))
                # build animation frame
                tmp.append(list(line))
        # fix if only one animation frame exists in file (no empty line)
        if maxHeight == 0:
            maxHeight = len(tmp)
        res.append(tmp)

        return (res, maxWidth, maxHeight)
