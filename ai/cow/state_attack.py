import logging

from stackfsm.states import BaseState as State
from utilities.timer import Timer
from system.graphics.renderable import Renderable
from common.direction import Direction
from directmessaging import directMessaging, DirectMessageType
from system.gamelogic.offensiveattack import OffensiveAttack
import system.gamelogic.enemy
import system.graphics.renderable
import system.groupid
from messaging import messaging, MessageType

logger = logging.getLogger(__name__)


class StateAttack(State):
    name = "attack"

    def __init__(self, brain):
        State.__init__(self, brain)
        self.attackMoveTimer = Timer()  # Timer(0.5, instant=False) # windup and cooldown


    def on_enter(self):
        meEnemy = self.brain.owner.world.component_for_entity(
            self.brain.owner.entity, system.gamelogic.enemy.Enemy)
        meGroupId = self.brain.owner.world.component_for_entity(
            self.brain.owner.entity, system.groupid.GroupId)

        messaging.add(
            type=MessageType.EntityAttack,
            groupId=meGroupId.getId(),
            data=None
        )

        # self.attackTimer.setTimer(meEnemy.enemyInfo.attackTime)
        # self.setTimer(meEnemy.enemyInfo.attackTime)
        self.stepsTodo = 30
        self.attackMoveTimer.init()
        self.attackMoveTimer.setTimer(0.1)
        self.setTimer(3.0)

        # even though we attack multiple times (each step)
        # only send EntityAttack once (change animation)
        messaging.add(
            type=MessageType.EntityAttack,
            groupId=meGroupId.getId(),
            data={}
        )


    def process(self, dt):
        self.attackMoveTimer.advance(dt)

        # check if we got stunned
        meAttackable = self.brain.owner.world.component_for_entity(
            self.brain.owner.entity, system.gamelogic.attackable.Attackable)
        if meAttackable.isStunned:
            self.brain.pop()
            self.brain.push("chase")

        # check if we should do one attack step
        if self.attackMoveTimer.timeIsUp():
            logger.info("{}: I'm attacking, step {}".format(self.owner, self.stepsTodo))

            if self.stepsTodo > 0:
                self.attackMoveTimer.reset()
                self.stepsTodo -= 1

                meRenderable = self.brain.owner.world.component_for_entity(
                    self.brain.owner.entity, Renderable)
                meGroupId = self.brain.owner.world.component_for_entity(
                    self.brain.owner.entity, system.groupid.GroupId)

                if self.stepsTodo % 2 == 0:
                    offensiveAttack = self.brain.owner.world.component_for_entity(
                        self.brain.owner.entity, OffensiveAttack)
                    offensiveAttack.attack()

                if meRenderable.direction is Direction.left:
                    x = -1
                else:
                    x = 1
                directMessaging.add(
                    groupId = meGroupId.getId(),
                    type = DirectMessageType.moveEnemy,
                    data = {
                        'x': x,
                        'y': 0,
                        'dontChangeDirection': False,
                        'updateTexture': False,
                        'force': True
                    },
                )
            else:
                self.attackMoveTimer.stop()

        if self.timeIsUp():
            # too long attacking. lets switch to chasing
            logger.info("{}: Too long attacking, switch to chasing".format(
                self.owner))
            self.brain.pop()
            self.brain.push("chase")
