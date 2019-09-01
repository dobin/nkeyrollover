import random
import logging

from ai.brain import Brain
from ai.states import BaseState as State
from texture.character.characteranimationtype import CharacterAnimationType
from utilities.timer import Timer
from sprite.direction import Direction
from config import Config
from sprite.coordinates import Coordinates

import system.renderable 

logger = logging.getLogger(__name__)


class StateAttack(State):
    name = "attack"

    def __init__(self, brain):
        State.__init__(self, brain)


    def on_enter(self):
        meRenderable = self.brain.owner.world.component_for_entity(
            self.brain.owner.entity, system.renderable.Renderable)

        meRenderable.texture.changeAnimation(
            CharacterAnimationType.hitting, 
            meRenderable.direction)
        
        self.setTimer( meRenderable.texture.getAnimationTime() )


    def process(self, dt):
        if self.timeIsUp(): 
            self.brain.pop()
            self.brain.push('idle')  