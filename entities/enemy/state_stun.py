import random
import logging

from ai.states import BaseState as State
import system.gamelogic.enemy

logger = logging.getLogger(__name__)


class StateStun(State):
    name = "stun"

    def __init__(self, brain):
        State.__init__(self, brain)

    def on_enter(self):
        meEnemy = self.brain.owner.world.component_for_entity(
            self.brain.owner.entity, system.gamelogic.enemy.Enemy)

        self.setTimer(meEnemy.enemyInfo.stunTime)


    def process(self, dt):
        if self.timeIsUp():
            self.brain.pop() # restore previous state


    def on_exit(self):
        pass