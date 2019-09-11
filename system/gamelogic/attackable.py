import logging

from utilities.timer import Timer

logger = logging.getLogger(__name__)


class Attackable():
    def __init__(self, initialHealth=100):
        self.health = initialHealth
        self.initialHealth = initialHealth

        self.isStunned = False
        self.stunTimer = Timer(0.0)
        self.stunTimer.setActive(False)


    def resetHealth(self):
        self.health = self.initialHealth


    def adjustHealth(self, health :int):
        self.health += health
        logger.info("Got damage: {}  new health: {}".format(health, self.health))


    def getHealth(self):
        return self.health


    def advance(self, dt):
        self.stunTimer.advance(dt)
