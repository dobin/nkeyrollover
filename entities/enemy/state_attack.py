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
from system.offensiveattack import OffensiveAttack

import system.gamelogic.tenemy
import system.renderable 

logger = logging.getLogger(__name__)


class StateAttack(State):
    name = "attack"

    def __init__(self, brain):
        State.__init__(self, brain)
        self.attackTimer = Timer() # Timer(0.5, instant=False) # windup and cooldown


    def on_enter(self):
        meRenderable = self.brain.owner.world.component_for_entity(
            self.brain.owner.entity, system.renderable.Renderable)

        self.attackTimer.init()
        meRenderable.texture.changeAnimation(
            CharacterAnimationType.hitting, 
            meRenderable.direction)
        
        self.attackTimer.setTimer(meRenderable.texture.getAnimationTime())
        self.setTimer( meRenderable.texture.getAnimationTime() )

 
    def process(self, dt):
        self.attackTimer.advance(dt)
        meEnemy = self.brain.owner.world.component_for_entity(
            self.brain.owner.entity, system.gamelogic.tenemy.tEnemy) 

        if self.attackTimer.timeIsUp(): 
            logger.warn(self.name + " I'm attacking!")
            self.attackTimer.reset()
            offensiveAttack = self.brain.owner.world.component_for_entity(
                meEnemy.offensiveAttackEntity, 
                OffensiveAttack)
            offensiveAttack.attack()

        if self.timeIsUp():
            # too long attacking. lets switch to chasing
            logger.debug("{}: Too long attacking, switch to chasing".format(self.owner))
            self.brain.pop()
            self.brain.push("chase")