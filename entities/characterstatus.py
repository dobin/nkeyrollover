import logging
import math 

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
    

    def isAlive(self): 
        if self.health > 0:
            return True
        else: 
            return False


    def getDamage(self): 
        return self.damage


    def getHit(self, damage): 
        self.health -= damage
        logger.info("New health: " + str(self.health))


    def enemyHit(self, damage, isAttack): 
        if isAttack:
            # implement lifesteal, 10% of damage taken by the enemy
            inc = int(damage * 0.1)
            self.health += inc


    def increaseHealthBy(self, hp): 
        if self.health <= self.healthMax: 
            self.health += hp


    def advance(self, deltaTime): 
        pass
