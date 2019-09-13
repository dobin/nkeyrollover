import logging
import yaml
import os

from texture.character.characteranimationtype import CharacterAnimationType
from texture.character.charactertexturetype import CharacterTextureType
from texture.animation import Animation
from common.direction import Direction
from utilities.colorpalette import ColorPalette
from utilities.color import Color
from common.coordinates import Coordinates
from texture.action.actiontype import ActionType
from system.gamelogic.weapontype import WeaponType
from common.weaponhitarea import WeaponHitArea

logger = logging.getLogger(__name__)


class FileTextureLoader(object):
    def __init__(self, isUnitTest=False):
        self.isUnitTest = isUnitTest


    def readAnimation(
        self, characterTextureType :CharacterTextureType,
        characterAnimationType :CharacterAnimationType,
        isUnitTest :bool =False
    ) -> Animation:
        ct = characterTextureType.name
        cat = characterAnimationType.name
        filename = "data/textures/character/{}/{}_{}.ascii".format(ct, ct, cat)

        # return fake animation if file does not exist(yet)
        if not os.path.isfile(filename):
            animation = Animation()
            animation.arr = [[['X']]]
            animation.height = 1
            animation.width = 1
            animation.frameCount = 1
            animation.frameTime = [10.0]
            animation.frameColors = [ColorPalette.getColorByColor(Color.white)]
            return animation

        animation = self.readAnimationFile(filename)
        animation.name = "{}_{}".format(ct, cat)

        filenameYaml = "data/textures/character/{}/{}_{}.yaml".format(ct, ct, cat)
        self.loadYamlIntoAnimation(filenameYaml, animation)

        return animation


    def readPhenomena(
        self,
        phenomenaType,
    ) -> Animation:
        phenomenaName = phenomenaType.name
        filename = "data/textures/phenomena/{}.ascii".format(phenomenaName)
        animation = self.readAnimationFile(filename)
        animation.name = phenomenaName

        filenameYaml = "data/textures/phenomena/{}.yaml".format(phenomenaName)
        self.loadYamlIntoAnimation(filenameYaml, animation)
        return animation


    def readAction(
        self,
        actionType,
    ) -> Animation:
        actionName = actionType.name
        filename = "data/textures/action/{}.ascii".format(actionName)
        animation = self.readAnimationFile(filename)
        animation.name = actionName

        filenameYaml = "data/textures/action/{}.yaml".format(actionName)
        self.loadYamlIntoAnimation(filenameYaml, animation)

        # Temporary
        filenameHitDetect = "data/textures/action/{}_hitdetect.ascii".format(actionName)
        animation.hitDetection = self.readHitDetectionFile(filenameHitDetect, actionType)

        return animation


    def readHitDetectionFile(self, filename, actionType):
        if not os.path.isfile(filename):
            chargeHitArea = [
                Coordinates(1, 0),
                Coordinates(3, 0),
                Coordinates(5, 0),
                Coordinates(7, 0),
                Coordinates(9, 0),
                Coordinates(11, 0),
                Coordinates(13, 0),
            ]
            spitfireHitArea = [
                Coordinates(6, 4),
                Coordinates(8, 4),
                Coordinates(10, 4),
                Coordinates(12, 4),

                Coordinates(2, 7),
                Coordinates(4, 7),
                Coordinates(6, 7),
                Coordinates(8, 7),
                Coordinates(10, 7),
                Coordinates(12, 7),

                Coordinates(2, 10),
                Coordinates(4, 10),
                Coordinates(6, 10),
                Coordinates(8, 10),
                Coordinates(10, 10),
                Coordinates(12, 10),

                Coordinates(2, 12),
                Coordinates(4, 12),
                Coordinates(6, 12),
                Coordinates(8, 12),
                Coordinates(10, 12),
                Coordinates(12, 12),

                Coordinates(6, 13),
                Coordinates(8, 13),
                Coordinates(10, 13),
                Coordinates(12, 13),
            ]

            self.weaponHitArea = {
                ActionType.hit: WeaponHitArea(),
                ActionType.hitSquare: WeaponHitArea(),
                ActionType.hitLine: WeaponHitArea(),
                ActionType.charge: WeaponHitArea(
                    hitCd=chargeHitArea, hitCdWidth=14, hitCdHeight=1),
                ActionType.spitfire: WeaponHitArea(
                    hitCd=spitfireHitArea, hitCdWidth=12, hitCdHeight=13),
            }
        else:
            print("AAAAAAAAAAAA")
            pass


    def loadYamlIntoAnimation(self, filename, animation):
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
                    colorType, viewport=None)
            else:
                color = ColorPalette.getColorByStr(color)
                animation.frameColors[n] = ColorPalette.getColorByColor(
                    color)


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
