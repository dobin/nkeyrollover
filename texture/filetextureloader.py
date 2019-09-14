import logging
import yaml
import os

from texture.character.characteranimationtype import CharacterAnimationType
from texture.character.charactertexturetype import CharacterTextureType
from texture.animation import Animation
from common.direction import Direction
from texture.phenomena.phenomenatype import PhenomenaType
from utilities.colorpalette import ColorPalette
from utilities.color import Color
from common.coordinates import Coordinates
from texture.action.actiontype import ActionType
from system.gamelogic.weapontype import WeaponType
from common.weaponhitarea import WeaponHitArea
from common.weapondata import WeaponData
from typing import List

logger = logging.getLogger(__name__)


class FileTextureLoader(object):
    def __init__(self):
        pass


    def readAnimation(
        self, characterTextureType :CharacterTextureType,
        characterAnimationType :CharacterAnimationType,
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
        phenomenaType :PhenomenaType,
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
        actionType :ActionType,
    ) -> Animation:
        actionName = actionType.name
        filename = "data/textures/action/{}.ascii".format(actionName)
        animation = self.readAnimationFile(filename)
        animation.name = actionName

        filenameYaml = "data/textures/action/{}.yaml".format(actionName)
        self.loadYamlIntoAnimation(filenameYaml, animation)

        return animation


    def readWeapon(
        self,
        weaponType: WeaponType
    ) -> WeaponData:
        weaponName = weaponType.name

        filename = "data/weapons/{}.yaml".format(weaponName)
        if not os.path.isfile(filename):
            logger.debug("No weapon definition in {}, skipping".format(
                filename
            ))
            return None

        weaponData = self.readWeaponYamlFile(filename)

        filenameHitDetect = "data/weapons/{}_hitdetect.ascii".format(weaponName)
        weaponData.weaponHitArea = self.readHitDetectionFile(
            filenameHitDetect, weaponType)

        return weaponData


    def readWeaponYamlFile(self, filename :str) -> WeaponData:
        weapon = WeaponData()

        with open(filename, 'r') as stream:
            data = yaml.safe_load(stream)

        try:
            weapon.actionTextureType = ActionType[data['actionTextureType']]
            weapon.hitDetectionDirection = Direction[data['hitDetectionDirection']]
            weapon.damage = int(data['damage'])
        except TypeError as error:
            raise Exception("Error, missing field in yaml file {}, error {}".format(
                filename, error
            ))

        return weapon


    def readHitDetectionFile(
        self,
        filename :str,
        weaponType :WeaponType
    ) -> WeaponHitArea:
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
            hitAreaStandard = [
                Coordinates(0, 0),
                Coordinates(0, 1),
                Coordinates(1, 0),
                Coordinates(1, 1)
            ]

            weaponHitArea = {
                WeaponType.unittest: WeaponHitArea(
                    hitCd=hitAreaStandard, width=2, height=2),
                WeaponType.hit: WeaponHitArea(
                    hitCd=hitAreaStandard, width=2, height=2),
                WeaponType.hitSquare: WeaponHitArea(
                    hitCd=hitAreaStandard, width=2, height=2),
                WeaponType.hitLine: WeaponHitArea(
                    hitCd=hitAreaStandard, width=2, height=2),
                WeaponType.charge: WeaponHitArea(
                    hitCd=chargeHitArea, width=14, height=1),
                WeaponType.spitfire: WeaponHitArea(
                    hitCd=spitfireHitArea, width=12, height=13),
            }
            return weaponHitArea[weaponType]

        lineList = [line.rstrip('\n') for line in open(filename)]
        (res, maxWidth, maxHeight) = self.parseAnimationLineList(lineList)

        hitCd = []
        for (z, anim) in enumerate(res):
            for (y, rows) in enumerate(anim):
                for (x, column) in enumerate(rows):
                    if column == 'x':
                        hitCd.append(Coordinates(x, y))

        weaponHitArea = WeaponHitArea(
            hitCd=hitCd,
            width=maxWidth,
            height=maxHeight
        )

        return weaponHitArea


    def loadYamlIntoAnimation(self, filename :str, animation :Animation):
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

        (res, maxWidth, maxHeight) = self.parseAnimationLineList(lineList)

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


    def parseAnimationLineList(
        self,
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
