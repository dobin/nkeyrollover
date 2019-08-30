import random
import logging

from ai.brain import Brain
from ai.states import BaseState as State
from texture.character.characteranimationtype import CharacterAnimationType
from utilities.timer import Timer
from sprite.direction import Direction
from config import Config
from sprite.coordinates import Coordinates
from utilities.utilities import Utility
from utilities.color import Color

logger = logging.getLogger(__name__)


class StateDying(State):
    name = "dying"

    def __init__(self, brain):
        State.__init__(self, brain)


    def on_enter(self):
        me = self.brain.owner

        if random.choice([True, False]): 
            logger.info(self.name + " Death animation deluxe")
            animationIndex = random.randint(0, 1)
            me.world.textureEmiter.makeExplode(me.texture, me.direction, None)
            me.texture.changeAnimation(CharacterAnimationType.dying, me.direction, animationIndex)
            me.setActive(False)
        else: 
            animationIndex = random.randint(0, 1)
            me.texture.changeAnimation(CharacterAnimationType.dying, me.direction, animationIndex)


        self.setTimer( me.enemyInfo.dyingTime )


    def process(self, dt):
        me = self.brain.owner

        if self.timeIsUp():
            logger.info("{}: Died enough, set to inactive".format(self.owner))
            self.brain.pop()
            self.brain.push("idle")
            me.setActive(False)

