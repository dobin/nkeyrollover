import logging

from ai.states import BaseState as State
import system.gamelogic.enemy
import system.groupid
from messaging import messaging, MessageType

logger = logging.getLogger(__name__)



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