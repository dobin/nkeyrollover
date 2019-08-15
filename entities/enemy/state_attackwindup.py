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


class StateAttackWindup(State): 
    name = 'attackwindup'

    def on_enter(self):
        me = self.brain.owner
        me.texture.changeAnimation(CharacterAnimationType.hitwindup, me.direction)

        self.setTimer( me.enemyInfo.windupTime )

    def process(self, dt):
        if self.timeIsUp():
            # windup animation done, lets do the attack
            self.brain.pop()
            self.brain.push("attack")