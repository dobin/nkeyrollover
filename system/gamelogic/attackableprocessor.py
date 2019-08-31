import esper
import logging

from system.renderable import Renderable
from system.gamelogic.tenemy import tEnemy
from system.gamelogic.attackable import Attackable

logger = logging.getLogger(__name__)

class AttackableProcessor(esper.Processor):
    def __init__(self):
        super().__init__()


    def process(self, dt):

        # if enemies have taken enough damage, make them gonna die
        for ent, (attackable, renderable, enemy) in self.world.get_components(Attackable, Renderable, tEnemy):
            if attackable.getHealth() <= 0:
                if renderable.isActive():
                    enemy.brain.pop()
                    enemy.brain.push('dying')
            