import esper
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

    def handleHit(self, damage :int):
        self.health -= damage
        logger.info("Got damage: {}  new health: {}".format(damage, self.health))

    def heal(self, healAmount):
        self.health += healAmount

    def getHealth(self):
        return self.health

    def advance(self, dt): 
        #if self.stunTimer.isActive():
        #    logging.info("XXXX Stun timer: {}".format(self.stunTimer.timeLeft))
        self.stunTimer.advance(dt)