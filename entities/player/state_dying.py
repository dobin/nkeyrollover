import random
import logging

from ai.brain import Brain
from ai.states import BaseState as State
from texture.character.characteranimationtype import CharacterAnimationType
from utilities.timer import Timer
from sprite.direction import Direction
from config import Config
from sprite.coordinates import Coordinates

logger = logging.getLogger(__name__)


class StateDying(State):
    name = "dying"

    def __init__(self, brain):
        State.__init__(self, brain)


    def on_enter(self):
        me = self.brain.owner
        me.texture.changeAnimation(CharacterAnimationType.dying, me.direction)
        self.setTimer(1.0)
        

    def process(self, dt):
        me = self.brain.owner

        if self.timeIsUp():
            logger.info("Player died enough. deactive")
            me.setActive(False)


