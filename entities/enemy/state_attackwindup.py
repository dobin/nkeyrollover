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
import system.gamelogic.enemy

logger = logging.getLogger(__name__)


class StateAttackWindup(State): 
    name = 'attackwindup'

    def on_enter(self):
        meRenderable = self.brain.owner.world.component_for_entity(
            self.brain.owner.entity, system.renderable.Renderable)
        meEnemy = self.brain.owner.world.component_for_entity(
            self.brain.owner.entity, system.gamelogic.enemy.Enemy) 


        meRenderable.texture.changeAnimation(
            CharacterAnimationType.hitwindup, 
            meRenderable.direction)

        self.setTimer( meEnemy.enemyInfo.windupTime )

    def process(self, dt):
        if self.timeIsUp():
            # windup animation done, lets do the attack
            self.brain.pop()
            self.brain.push("attack")