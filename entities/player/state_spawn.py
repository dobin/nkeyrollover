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


class StateSpawn(State):
    name = "spawn"

    def __init__(self, brain):
        State.__init__(self, brain)
        me = self.brain.owner
        self.state = 0
        self.speechTimer = Timer(1.0)
        

    def on_enter(self):
        me = self.brain.owner
        me.texture.changeAnimation(CharacterAnimationType.standing, me.direction)
        me.setActive(True)
        self.state = 0
        self.speechTimer.reset()


    def process(self, dt):
        me = self.brain.owner
        self.speechTimer.advance(dt)

        if self.speechTimer.timeIsUp(): 
            if self.state == 0:
                #me.speechTexture.changeAnimation('I\'m here to chew gum and kick ass')
                self.speechTimer.setTimer(1.5)
                self.speechTimer.reset()
                self.state += 1
            elif self.state == 1:
                #me.speechTexture.changeAnimation('And i\'m all out of gum')
                self.speechTimer.stop()