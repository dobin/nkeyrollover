import logging
import math

from utilities.apm import Apm
from entities.weapontype import WeaponType

logger = logging.getLogger(__name__)


class CharacterStatus(object):
    def __init__(self):
        self.init()

    def init(self):
        self.manaMax = 100
        self.mana = 100
        self.manaRegen = 1

        self.damage = 35

        self.points = 0
        self.lifesteal = 0.1

        self.weaponDamage = {
            WeaponType.hit: 50,
            WeaponType.hitSquare: 25,
            WeaponType.hitLine: 25,
            WeaponType.jumpKick: 50,

            WeaponType.explosion: 100,
            WeaponType.laser: 100,
            WeaponType.cleave: 100,
        }

        self.apm = Apm()


    def getDamage(self, weaponType :WeaponType):
        return self.weaponDamage[weaponType]

    def advance(self, deltaTime):
        pass

    def handleKeyPress(self, time :float):
        self.apm.tick(time)

    def getApm(self):
        return self.apm
