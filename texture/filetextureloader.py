import logging
import yaml
import io

from texture.character.characteranimationtype import CharacterAnimationType
from texture.character.charactertype import CharacterType
from texture.animation import Animation
from sprite.direction import Direction
from utilities.colorpalette import ColorPalette

logger = logging.getLogger(__name__)


class FileTextureLoader(object):
    def __init__(self):
        pass


    def readAnimation(
        self, characterType :CharacterType,
        characterAnimationType :CharacterAnimationType
    ) -> Animation:
        ct = characterType.name
        cat = characterAnimationType.name
        filename = "data/textures/{}/{}_{}.ascii".format(ct, ct, cat)
        animation = self.readAnimationFile(filename)
        animation.name = "{}_{}".format(ct, cat)

        filenameYaml = "data/textures/{}/{}_{}.yaml".format(ct, ct, cat)
        self.loadYamlIntoAnimation(filenameYaml, animation)

        return animation


    def readPhenomena(
        self,
        phenomenaName :str,
    ) -> Animation:
        filename = "data/textures/{}.ascii".format(phenomenaName)
        animation = self.readAnimationFile(filename)
        animation.name = phenomenaName

        filenameYaml = "data/textures/{}.yaml".format(phenomenaName)
        self.loadYamlIntoAnimation(filenameYaml, animation)
        return animation 


    def loadYamlIntoAnimation(self, filename, animation): 
        with open(filename, 'r') as stream:
            data = yaml.safe_load(stream)

        animation.endless = data['endless']
        animation.advanceByStep = data['advanceByStep']
        animation.frameColors = data['frameColors']

        # FrameTime can be non-existing, e.g. if 'advanceByStep' = True
        # Therefore, frameTime will be None
        if 'frameTime' in data:
            animation.frameTime = data['frameTime']

        if 'direction' in data:
            if data['direction'] == 'left':
                animation.originalDirection = Direction.left
            elif data['direction'] == 'right':
                animation.originalDirection = Direction.right
            else: 
                animation.originalDirection = Direction.none

        # colors: 
        # - Color: white, brightblue, ...
        # - ColorType: mapColor
        for (n, color) in enumerate(data['frameColors']):
            if color.startswith('ColorType.'):
                color = color.split('.')[1]
                colorType = ColorPalette.getColorTypeByStr(color)
                animation.frameColors[n] = ColorPalette.getColorByColorType(colorType, viewport=None)
            else:
                color = ColorPalette.getColorByStr(color)
                animation.frameColors[n] = ColorPalette.getColorByColor(color)


    def readAnimationFile(self, filename :str) -> Animation:
        lineList = [line.rstrip('\n') for line in open(filename)]
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
#        d = {
#            'arr': res,
#            'width': maxWidth,
#            'height': maxHeight,
#            'frameCount': len(res),
#        }

        logger.debug("Loaded {}: width={} height={} animations={}".format(
            filename, animation.width, animation.height, animation.frameCount))

        return animation