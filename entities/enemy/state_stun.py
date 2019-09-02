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


class StateStun(State):
    name = "idle"

    def __init__(self, brain):
        State.__init__(self, brain)

    def on_enter(self):
        pass

    def on_exit(self):
        pass