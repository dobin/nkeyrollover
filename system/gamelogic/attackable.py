import esper
import logging

from system.renderable import Renderable

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


class AttackableProcessor(esper.Processor):
    def __init__(self):
        super().__init__()


    def process(self, dt):
        # if enemies have taken enough damage, make them gonna die
        for ent, (attackable, renderable) in self.world.get_components(Attackable, Renderable):
            if attackable.getHealth() <= 0:
                if renderable.r.isActive():
                    renderable.r.brain.pop()
                    renderable.r.brain.push('dying')
            