import logging

from stackfsm.states import BaseState as State
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

        self.setTimer(meEnemy.enemyInfo.attackWindupTime)


    def process(self, dt):
        # if we get stunned at any time, cancel attackwindup
        meAttackable = self.brain.owner.world.component_for_entity(
            self.brain.owner.entity, system.gamelogic.attackable.Attackable)
        if meAttackable.isStunned:
            self.brain.pop()
            self.brain.push("chase")

        if self.timeIsUp():
            # windup time done, lets do the attack
            self.brain.pop()
            self.brain.push("attack")
