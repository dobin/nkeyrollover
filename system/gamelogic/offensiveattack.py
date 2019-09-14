import logging
import copy

from config import Config
from system.gamelogic.weapontype import WeaponType
from utilities.timer import Timer
from messaging import messaging, MessageType
from texture.filetextureloader import FileTextureLoader

logger = logging.getLogger(__name__)


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

        fileTextureLoader = FileTextureLoader()
        self.weaponData = {}
        for weaponType in WeaponType:
            self.weaponData[weaponType] = fileTextureLoader.readWeapon(weaponType)


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

        actionTextureType = self.weaponData[self.weaponType].actionTextureType
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
                'damage': self.weaponData[self.weaponType].damage,
                'direction': direction,
            }
        )


    def advance(self, deltaTime :float):
        self.cooldownTimer.advance(deltaTime)
        self.durationTimer.advance(deltaTime)


    def getCurrentWeaponHitArea(self):
        wha = self.weaponData[self.weaponType].weaponHitArea
        return copy.deepcopy(wha)


    def getWeaponStr(self):
        return self.selectedWeaponKey
