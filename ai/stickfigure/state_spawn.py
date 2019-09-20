import logging

from stackfsm.states import BaseState as State
from config import Config
import system.graphics.renderable

logger = logging.getLogger(__name__)


class StateSpawn(State):
    name = "spawn"

    def __init__(self, brain):
        State.__init__(self, brain)


    def on_enter(self):
        pass


    def process(self, dt):
        # if the screen moves by itself, we may have not a playerlocation
        # and he will see us standing around stupidly
        # for message in messaging.getByType(MessageType.PlayerLocation):

        # just check regularly...
        if self.timeIsUp():
            if self.isMeOnScreen():
                self.brain.pop()
                if Config.devMode:
                    # make him come straight at us, sucker
                    self.brain.push("chase")
                else:
                    self.brain.push("wander")


            self.setTimer(0.2)


    def isMeOnScreen(self):
        meRenderable = self.brain.owner.world.component_for_entity(
            self.brain.owner.entity, system.graphics.renderable.Renderable)

        return meRenderable.isOnScreen(wiggle=4)
