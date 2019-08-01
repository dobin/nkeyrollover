import logging

logger = logging.getLogger(__name__)


class PlayerStatus(object): 
    def __init__(self): 
        self.init()

    def init(self):
        self.healthMax = 100
        self.manaMax = 100

        self.health = 100
        self.mana = 100

        self.healthRegen = 1
        self.manaRegen = 1

        self.points = 0
    
    def isAlive(self): 
        if self.health > 0:
            return True
        else: 
            return False


    def getHit(self, damage): 
        self.health -= damage
        logger.info("New health: " + str(self.health))

    def advance(self): 
        pass
