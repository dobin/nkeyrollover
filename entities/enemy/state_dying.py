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

import system.renderable
import system.gamelogic.tenemy

logger = logging.getLogger(__name__)


class StateDying(State):
    name = "dying"

    def __init__(self, brain):
        State.__init__(self, brain)


    def on_enter(self):
        meRenderable = self.brain.owner.world.component_for_entity(
            self.brain.owner.entity, system.renderable.Renderable)
        meEnemy = self.brain.owner.world.component_for_entity(
            self.brain.owner.entity, system.gamelogic.tenemy.tEnemy) 


        if random.choice([True, False]): 
            logger.info(self.name + " Death animation deluxe")
            animationIndex = random.randint(0, 1)
            meEnemy.world.textureEmiter.makeExplode(
                meRenderable.texture, 
                meRenderable.direction, 
                None)
            meRenderable.texture.changeAnimation(
                CharacterAnimationType.dying, 
                meRenderable.direction, 
                animationIndex)
            meRenderable.setActive(False)
        else: 
            animationIndex = random.randint(0, 1)
            meRenderable.texture.changeAnimation(
                CharacterAnimationType.dying, 
                meRenderable.direction, 
                animationIndex)


        self.setTimer( meEnemy.enemyInfo.dyingTime )


    def process(self, dt):
        meRenderable = self.brain.owner.world.component_for_entity(
            self.brain.owner.entity, system.renderable.Renderable)

        if self.timeIsUp():
            logger.info("{}: Died enough, set to inactive".format(self.owner))
            self.brain.pop()
            self.brain.push("idle")
            meRenderable.setActive(False)
