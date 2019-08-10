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


class Idle(State):
    name = "idle"

    def __init__(self, brain):
        State.__init__(self, brain)

    def on_enter(self):
        me = self.brain.owner
        me.texture.changeAnimation(CharacterAnimationType.standing, me.direction)

    def on_exit(self):
        pass


class Spawn(State):
    name = "spawn"

    def __init__(self, brain):
        State.__init__(self, brain)


    def on_enter(self):
        me = self.brain.owner
        me.texture.changeAnimation(CharacterAnimationType.standing, me.direction)
        me.setActive(True)


    def process(self, dt):
        pass


class Attack(State):
    name = "attack"

    def __init__(self, brain):
        State.__init__(self, brain)


    def on_enter(self):
        me = self.brain.owner
        me.texture.changeAnimation(CharacterAnimationType.hitting, me.direction)
        
        self.setTimer( me.texture.getAnimationTime() )


    def process(self, dt):
        me = self.brain.owner
        if self.timeIsUp(): 
            self.brain.pop()
            self.brain.push('idle')            


class Walking(State):
    name = "walking"

    def __init__(self, brain):
        State.__init__(self, brain)


    def on_enter(self):
        me = self.brain.owner
        me.texture.changeAnimation(CharacterAnimationType.walking, me.direction)
        self.setTimer(1.0)
        

    def process(self, dt):
        me = self.brain.owner

        if self.timeIsUp():
            self.brain.pop()
            self.brain.push('idle')


class Dying(State):
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
            logging.info("Player died enough. deactive")
            me.setActive(False)


