import logging
import math 

from entities.weapontype import WeaponType

logger = logging.getLogger(__name__)


class CharacterStatus(object): 
    def __init__(self): 
        self.init()

    def init(self):
        self.healthMax = 100
        self.manaMax = 100

        self.health = 100
        self.mana = 100

        self.healthRegen = 1
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
            WeaponType.laser: 50,
            WeaponType.cleave: 50,
        }
    

    def isAlive(self) -> bool: 
        if self.health > 0:
            return True
        else: 
            return False


    def getDamage(self, weaponType :WeaponType): 
        return self.weaponDamage[weaponType]


    def getHit(self, damage :float): 
        self.health -= damage
        logger.info("New health: " + str(self.health))


    def enemyHit(self, damage :float, isAttack :bool):
        # lifesteal
        if isAttack:
            inc = int(damage * self.lifesteal)
            self.health += inc


    def increaseHealthBy(self, hp :int):
        if self.health <= self.healthMax: 
            self.health += hp


    def heal(self, hp :int): 
        self.health += hp


    def advance(self, deltaTime): 
        pass
