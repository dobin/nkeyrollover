import logging
import os
import yaml

from common.direction import Direction
from system.gamelogic.weapontype import WeaponType
from utilities.utilities import Utility
from common.weaponhitarea import WeaponHitArea
from common.weapondata import WeaponData
from common.coordinates import Coordinates
from texture.action.actiontype import ActionType
from texture.texturehelper import TextureHelper

logger = logging.getLogger("weaponAnimationManager")


class WeaponAnimationManager(object):
    def __init__(self):
        self.weaponData = {}


    def loadFiles(self):
        self.weaponData = {}
        for weaponType in WeaponType:
            self.loadWeaponData(weaponType)


    def loadWeaponData(self, weaponType):
        weaponName = weaponType.name
        filename = "data/weapons/{}.yaml".format(weaponName)
        if not os.path.isfile(filename):
            logger.debug("No weapon definition in {}, skipping".format(
                filename
            ))
            return None

        weaponData = self.readWeaponYamlFile(filename)

        filenameHitDetect = "data/weapons/{}_hitdetect.ascii".format(weaponName)
        weaponData.weaponHitArea[Direction.left] = self.readHitDetectionFile(
            filename=filenameHitDetect,
            weaponType=weaponType,
            direction=Direction.left,
            weaponHitDirection=weaponData.hitDetectionDirection)
        weaponData.weaponHitArea[Direction.right] = self.readHitDetectionFile(
            filename=filenameHitDetect,
            weaponType=weaponType,
            direction=Direction.right,
            weaponHitDirection=weaponData.hitDetectionDirection)

        self.weaponData[weaponType] = weaponData


    def getWeaponData(
        self,
        weaponType: WeaponType
    ) -> WeaponData:

        return self.weaponData[weaponType]


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
        weaponType :WeaponType,
        direction :Direction,
        weaponHitDirection :Direction
    ) -> WeaponHitArea:
        if not os.path.isfile(filename):
            # default, if file would not exist
            hitAreaStandard = [
                Coordinates(0, 0),
                Coordinates(0, 1),
                Coordinates(1, 0),
                Coordinates(1, 1)
            ]
            weaponHitArea = WeaponHitArea(
                hitCd=hitAreaStandard, width=2, height=2),
            return weaponHitArea

        lineList = [line.rstrip('\n') for line in open(filename)]
        (res, maxWidth, maxHeight) = TextureHelper.parseAnimationLineList(lineList)

        if direction is not weaponHitDirection:
            Utility.mirrorFrames(res)

        # only add positions indicated by 'x', ignore all other chars
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