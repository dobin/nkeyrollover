import logging
import copy

from config import Config
from system.gamelogic.weapontype import WeaponType
from utilities.timer import Timer
from messaging import messaging, MessageType
from game.offenseloader.fileoffenseloader import fileOffenseLoader
from common.direction import Direction
from utilities.color import Color
from utilities.utilities import Utility
from common.coordinates import Coordinates

logger = logging.getLogger(__name__)


class OffensiveAttack():
    def __init__(self, parentChar, parentRenderable):
        self.parentChar = parentChar
        self.parentRenderable = parentRenderable

        self.cooldownTimer :Timer = Timer(Config.playerAttacksCd, instant=True)

        self.weaponType :WeaponType = WeaponType.hitWhip
        self.selectedWeaponKey :str = '1'

        # coordinates are based on left side orientation of renderable
        self.weaponBaseLocation = Coordinates(0, -1)


    def switchWeaponByKey(self, key :str):
        self.selectedWeaponKey = key
        if key == '1':
            self.switchWeapon(WeaponType.hitWhip)

        if key == '2':
            self.switchWeapon(WeaponType.hitSquare)

        if key == '3':
            self.switchWeapon(WeaponType.hitLine)

        if key == '4':
            self.switchWeapon(WeaponType.jumpKick)


    def switchWeapon(self, weaponType :WeaponType):
        logger.info("{} Switch to weapon: {}".format(
            self.parentChar, weaponType))
        self.weaponType = weaponType


    def attack(self):
        self.cooldownTimer.reset()  # activate cooldown

        weaponData = fileOffenseLoader.weaponManager.getWeaponData(
            self.weaponType)
        direction = self.parentRenderable.getDirection()
        actionTextureType = weaponData.actionTextureType

        # handle weapon offset
        location = self.getWeaponBaseLocation()

        messaging.add(
            type=MessageType.EmitActionTexture,
            data={
                'actionTextureType': actionTextureType,
                'location': location,
                'fromPlayer': self.parentChar.isPlayer,
                'damage': weaponData.damage,
                'direction': direction,
            }
        )

        if weaponData.damage is not None:
            weaponHitArea = copy.deepcopy(weaponData.weaponHitArea[direction])
            Utility.updateCoordinateListWithBase(
                weaponHitArea=weaponHitArea, loc=location, direction=direction)

            messaging.add(
                type=MessageType.AttackAt,
                data= {
                    'hitLocations': weaponHitArea.hitCd,
                    'damage': weaponData.damage,
                    'byPlayer': self.parentChar.isPlayer,
                    'direction': direction,
                }
            )

            if Config.showAttackDestinations:
                for hitlocation in weaponHitArea.hitCd:
                    messaging.add(
                        type=MessageType.EmitTextureMinimal,
                        data={
                            'char': 'X',
                            'timeout': 0.2,
                            'coordinate': hitlocation,
                            'color': Color.grey
                        }
                    )

        if self.parentChar.isPlayer:
            # indicate we are attacking, e.g. for playing attack animation
            messaging.add(
                type=MessageType.PlayerAttack,
                data={
                    # for playerProcessor
                    'attackAnimationLength': weaponData.animationLength,

                    # for characterAnimationProcessor
                    'characterAttackAnimationType': weaponData.characterAnimationType
                }
            )
        else:
            # enemy AI state machine is doing it itself
            pass


    def advance(self, deltaTime :float):
        self.cooldownTimer.advance(deltaTime)


    def getCurrentWeaponHitArea(self):
        direction = self.parentRenderable.getDirection()

        weaponData = fileOffenseLoader.weaponManager.getWeaponData(
            self.weaponType)
        wha = copy.deepcopy(weaponData.weaponHitDetect[direction])

        loc = self.getWeaponBaseLocation()
        Utility.updateCoordinateListWithBase(
            wha,
            loc,
            direction)

        return wha


    def getWeaponBaseLocation(self):
        """The position of the attack weapon of the char. 
        Used to:
        - As Enemy/AI: check if we can attack player (chase)
        - Use as baseline for attack texture (and therefore also hit detection)
        """
        # Slow
        loc = copy.copy(self.parentRenderable.getLocation())

        loc.y += self.weaponBaseLocation.y
        if self.parentRenderable.direction is Direction.left:
            loc.x += self.weaponBaseLocation.x
        else:
            loc.x += (self.parentRenderable.texture.width) - self.weaponBaseLocation.x

        weaponData = fileOffenseLoader.weaponManager.getWeaponData(
            self.weaponType)
        if self.parentRenderable.direction is Direction.left:
            loc.x += weaponData.locationOffset.x
        else:
            loc.x -= weaponData.locationOffset.x
        loc.y += weaponData.locationOffset.y

        return loc


    def getWeaponStr(self):
        return self.selectedWeaponKey
