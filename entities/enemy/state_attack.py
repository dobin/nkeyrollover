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


class StateAttack(State):
    name = "attack"

    def __init__(self, brain):
        State.__init__(self, brain)
        self.attackTimer = Timer() # Timer(0.5, instant=False) # windup and cooldown


    def on_enter(self):
        me = self.brain.owner
        self.attackTimer.init()
        me.texture.changeAnimation(CharacterAnimationType.hitting, me.direction)
        
        self.attackTimer.setTimer(me.texture.getAnimationTime())
        self.setTimer( me.texture.getAnimationTime() )

 
    def process(self, dt):
        self.attackTimer.advance(dt)
        me = self.brain.owner

        if self.attackTimer.timeIsUp(): 
            logger.warn(self.name + " I'm attacking!")
            self.attackTimer.reset()
            me.characterAttack.attack()

        if self.timeIsUp():
            # too long attacking. lets switch to chasing
            logger.debug("{}: Too long attacking, switch to chasing".format(self.owner))
            self.brain.pop()
            self.brain.push("chase")