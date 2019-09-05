import logging

from ai.states import BaseState as State
from config import Config
import system.renderable
import system.gamelogic.enemy

logger = logging.getLogger(__name__)


class StateSpawn(State):
    name = "spawn"

    def __init__(self, brain):
        State.__init__(self, brain)


    def on_enter(self):
        self.setTimer(0.1)


    def process(self, dt):
        if self.timeIsUp():
            self.brain.pop()

            if Config.devMode:
                # make him come straight at us, sucker
                logger.info("{} From Spawn To Chase".format(self.owner))
                self.brain.pop()
                self.brain.push("chase")
            else:
                self.brain.pop()
                self.brain.push("wander")