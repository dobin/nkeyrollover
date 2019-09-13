import logging
import copy

from texture.action.actiontype import ActionType
from config import Config
from system.gamelogic.weapontype import WeaponType
from utilities.timer import Timer
from messaging import messaging, MessageType
from common.coordinates import Coordinates

logger = logging.getLogger(__name__)


class WeaponHitArea(object):
    def __init__(self, hitCd=None, hitCdWidth=None, hitCdHeight=None):
        if hitCd is None:
            self.hitCd = [
                Coordinates(0, 0),
                Coordinates(1, 0),
                Coordinates(0, 1),
                Coordinates(1, 1),
            ]
        else:
            self.hitCd = hitCd

        if hitCdWidth is None:
            self.hitCdWidth = 2
        else:
            self.hitCdWidth = hitCdWidth

        if hitCdHeight is None:
            self.hitCdHeight = 2
        else:
            self.hitCdHeight = 2


class OffensiveAttack():
    def __init__(self, parentChar, parentRenderable):
        self.parentChar = parentChar
        self.parentRenderable = parentRenderable

        # really necessary?
        self.durationTimer = Timer(0.0, active=False)
        self.durationTimer.setTimer(Config.playerAttackAnimationLen)
        self.durationTimer.reset()

        self.cooldownTimer :Timer = Timer(Config.playerAttacksCd, instant=True)

        self.weaponType :WeaponType = WeaponType.hit
        self.selectedWeaponKey :str = '1'

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
            WeaponType.hit: WeaponHitArea(),
            WeaponType.hitSquare: WeaponHitArea(),
            WeaponType.hitLine: WeaponHitArea(),
            WeaponType.jumpKick: WeaponHitArea(),
            WeaponType.charge: WeaponHitArea(
                hitCd=chargeHitArea, hitCdWidth=14, hitCdHeight=1),
            WeaponType.spitfire: WeaponHitArea(
                hitCd=spitfireHitArea, hitCdWidth=12, hitCdHeight=13),
        }

        if parentChar.isPlayer:
            self.damage = {
                WeaponType.hit: 35,
                WeaponType.hitSquare: 35,
                WeaponType.hitLine: 35,
                WeaponType.jumpKick: 30,
            }
        else:
            self.damage = {
                WeaponType.hit: 20,
                WeaponType.hitSquare: 20,
                WeaponType.hitLine: 20,
                WeaponType.jumpKick: 20,
                WeaponType.charge: 10,
                WeaponType.spitfire: 90,
            }


    def switchWeaponByKey(self, key :str):
        self.selectedWeaponKey = key
        if key == '1':
            self.switchWeapon(WeaponType.hit)

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
        self.durationTimer.reset()  # will setActive(false) when time is up

        actionTextureType = self.weaponTypeToAnimationType(self.weaponType)
        location = self.parentRenderable.getWeaponBaseLocation()
        direction = self.parentRenderable.getDirection()

        # EmitActionTexture will create Attack message for the player/enemy
        # (data['damage'] is not None)
        # as we dont know here what the attack locations are,
        # as they depend on the specific attack
        messaging.add(
            type=MessageType.EmitActionTexture,
            data={
                'actionTextureType': actionTextureType,
                'location': location,
                'fromPlayer': self.parentChar.isPlayer,
                'damage': self.damage[self.weaponType],
                'direction': direction,
            }
        )


    def weaponTypeToAnimationType(self, weaponType):
        if self.weaponType is WeaponType.hit:
            return ActionType.hit
        elif self.weaponType is WeaponType.hitSquare:
            return ActionType.hitSquare
        elif self.weaponType is WeaponType.hitLine:
            return ActionType.hitLine
        elif self.weaponType is WeaponType.jumpKick:
            return ActionType.hit
        elif self.weaponType is WeaponType.charge:
            return ActionType.charge
        elif self.weaponType is WeaponType.spitfire:
            return ActionType.spitfire
        else:
            raise Exception('Unknown weaponType {}'.format(weaponType))


    def advance(self, deltaTime :float):
        self.cooldownTimer.advance(deltaTime)
        self.durationTimer.advance(deltaTime)


    def getCurrentWeaponHitArea(self):
        wha = self.weaponHitArea[self.weaponType]
        return copy.deepcopy(wha)



    def getWeaponStr(self):
        return self.selectedWeaponKey
