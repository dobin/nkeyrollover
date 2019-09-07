import logging

from texture.phenomena.phenomenatype import PhenomenaType
from config import Config
from entities.weapontype import WeaponType
from utilities.recordholder import RecordHolder
from utilities.timer import Timer
from messaging import messaging, MessageType

logger = logging.getLogger(__name__)


class OffensiveAttack():
    def __init__(self, parentChar, parentRenderable, world):
        self.parentChar = parentChar
        self.parentRenderable = parentRenderable
        self.world = world

        # really necessary?
        self.durationTimer = Timer(0.0, active=False)
        self.durationTimer.setTimer(Config.playerAttackAnimationLen)
        self.durationTimer.reset()

        self.cooldownTimer :Timer = Timer(Config.playerAttacksCd, instant=True)

        self.weaponType :WeaponType = WeaponType.hit
        self.selectedWeaponKey :str = '1'

        if parentChar.isPlayer:
            self.damage = {
                WeaponType.hit: 35,
                WeaponType.hitSquare: 35,
                WeaponType.hitLine: 35,
                WeaponType.jumpKick: 30
            }
        else: 
            self.damage = {
                WeaponType.hit: 20,
                WeaponType.hitSquare: 20,
                WeaponType.hitLine: 20,
                WeaponType.jumpKick: 20
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
        logger.info("Switch to weaopn: " + str(weaponType))
        self.weaponType = weaponType


    def weaponTypeToAnimationType(self, weaponType):
        if self.weaponType is WeaponType.hit:
            return PhenomenaType.hit
        elif self.weaponType is WeaponType.hitSquare:
            return PhenomenaType.hitSquare
        elif self.weaponType is WeaponType.hitLine:
            return PhenomenaType.hitLine
        elif self.weaponType is WeaponType.jumpKick:
            return PhenomenaType.hit


    def attack(self):
        if not self.cooldownTimer.timeIsUp():
            RecordHolder.recordPlayerAttackCooldown(
                self.weaponType, time=self.cooldownTimer.getTimeLeft())
            return
        self.cooldownTimer.reset()  # activate cooldown

        self.durationTimer.reset()  # will setActive(false) when time is up

        actionTextureType = None
        if self.weaponType is WeaponType.hit:
            actionTextureType = PhenomenaType.hit
        elif self.weaponType is WeaponType.hitSquare:
            actionTextureType = PhenomenaType.hitSquare
        elif self.weaponType is WeaponType.hitLine:
            actionTextureType = PhenomenaType.hitLine

        location = self.parentRenderable.getWeaponBaseLocation()
        direction = self.parentRenderable.getDirection()

        # EmitActionTexture will create Attack message for the player/enemy
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


    def advance(self, deltaTime :float):
        self.cooldownTimer.advance(deltaTime)
        self.durationTimer.advance(deltaTime)


    def getWeaponStr(self):
        return self.selectedWeaponKey
