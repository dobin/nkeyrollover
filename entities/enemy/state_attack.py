import logging

from ai.states import BaseState as State
from utilities.timer import Timer
from system.offensiveattack import OffensiveAttack

import system.gamelogic.enemy
import system.renderable
import system.groupid
from messaging import messaging, Messaging, Message, MessageType

logger = logging.getLogger(__name__)


class StateAttack(State):
    name = "attack"

    def __init__(self, brain):
        State.__init__(self, brain)
        self.attackTimer = Timer() # Timer(0.5, instant=False) # windup and cooldown


    def on_enter(self):
        meEnemy = self.brain.owner.world.component_for_entity(
            self.brain.owner.entity, system.gamelogic.enemy.Enemy)
        meGroupId = self.brain.owner.world.component_for_entity(
            self.brain.owner.entity, system.groupid.GroupId)

        self.attackTimer.init()
        messaging.add(
            type=MessageType.EntityAttack,
            groupId=meGroupId.getId(),
            data=None
        )

        self.attackTimer.setTimer(meEnemy.enemyInfo.attackTime)
        self.setTimer(meEnemy.enemyInfo.attackTime)


    def process(self, dt):
        self.attackTimer.advance(dt)
        meEnemy = self.brain.owner.world.component_for_entity(
            self.brain.owner.entity, system.gamelogic.enemy.Enemy)

        if self.attackTimer.timeIsUp():
            logger.info(self.name + " I'm attacking, via offensiveattack!")
            self.attackTimer.reset()
            offensiveAttack = self.brain.owner.world.component_for_entity(
                meEnemy.offensiveAttackEntity,
                OffensiveAttack)
            offensiveAttack.attack()

        if self.timeIsUp():
            # too long attacking. lets switch to chasing
            logger.info("{}: Too long attacking, switch to chasing".format(self.owner))
            self.brain.pop()
            self.brain.push("chase")