import esper
import logging

logger = logging.getLogger(__name__)


class Attackable():
    def __init__(self, initialHealth=100):
        self.health = initialHealth
        self.initialHealth = initialHealth

    def resetHealth(self):
        self.health = self.initialHealth

    def handleHit(self, damage :int):
        self.health -= damage
        logger.info("Got damage: {}  new health: {}".format(damage, self.health))

    def getHealth(self):
        return self.health
