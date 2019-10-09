import logging

from stackfsm.states import BaseState as State
import system.graphics.renderable
import system.gamelogic.enemy

logger = logging.getLogger(__name__)


class StateDying(State):
    name = "dying"

    def __init__(self, brain):
        State.__init__(self, brain)


    def on_enter(self):
        meEnemy = self.brain.owner.world.component_for_entity(
            self.brain.owner.entity, system.gamelogic.enemy.Enemy)

        self.setTimer(meEnemy.enemyInfo.dyingTime)


    def process(self, dt):
        if self.timeIsUp():
            logger.info("{}: Died enough, set to dead".format(self.owner))
            self.brain.pop()
            self.brain.push("dead")
