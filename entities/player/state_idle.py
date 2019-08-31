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


class StateIdle(State):
    name = "idle"

    def __init__(self, brain):
        State.__init__(self, brain)

    def on_enter(self):
        meRenderable = self.brain.owner.world.component_for_entity(
            self.brain.owner.entity, Renderable)
        meRenderable.texture.changeAnimation(
            CharacterAnimationType.standing, 
            meRenderable.direction)

    def on_exit(self):
        pass