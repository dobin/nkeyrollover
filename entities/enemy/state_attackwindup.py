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

from messaging import messaging, Messaging, Message, MessageType


class StateAttackWindup(State): 
    name = 'attackwindup'

    def on_enter(self):
        meGroupId = self.brain.owner.world.component_for_entity(
            self.brain.owner.entity, system.groupid.GroupId)
        meEnemy = self.brain.owner.world.component_for_entity(
            self.brain.owner.entity, system.gamelogic.enemy.Enemy) 

        messaging.add(
            type=MessageType.attackWindup, 
            groupId=meGroupId.getId(),
            data=None
        )

        self.setTimer( meEnemy.enemyInfo.windupTime )

    def process(self, dt):
        if self.timeIsUp():
            # windup animation done, lets do the attack
            self.brain.pop()
            self.brain.push("attack")