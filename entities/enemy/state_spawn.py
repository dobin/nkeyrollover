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

class StateSpawn(State):
    name = "spawn"

    def __init__(self, brain):
        State.__init__(self, brain)


    def on_enter(self):
        meEnemy = self.brain.owner.world.component_for_entity(
            self.brain.owner.entity, system.gamelogic.enemy.Enemy) 

        self.setTimer( meEnemy.enemyInfo.spawnTime )


    def process(self, dt):
        if self.timeIsUp():
            self.brain.pop()

            if Config.devMode: 
                # make him come straight at us, sucker
                self.brain.push("chase")
            else: 
                self.brain.push("wander")