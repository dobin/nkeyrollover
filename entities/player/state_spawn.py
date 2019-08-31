import random
import logging

from ai.brain import Brain
from ai.states import BaseState as State
from texture.character.characteranimationtype import CharacterAnimationType
from utilities.timer import Timer
from sprite.direction import Direction
from config import Config
from sprite.coordinates import Coordinates
from system.renderable import Renderable

logger = logging.getLogger(__name__)


class StateSpawn(State):
    name = "spawn"

    def __init__(self, brain):
        State.__init__(self, brain)
        self.state = 0
        self.speechTimer = Timer(1.0)
        

    def on_enter(self):
        meRenderable = self.brain.owner.world.component_for_entity(
            self.brain.owner.entity, Renderable)
            
        meRenderable.texture.changeAnimation(
            CharacterAnimationType.standing, 
            meRenderable.direction)
        meRenderable.setActive(True)
        self.state = 0
        self.speechTimer.reset()


    def process(self, dt):
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