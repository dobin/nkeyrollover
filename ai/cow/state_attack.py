import logging

from stackfsm.states import BaseState as State
from utilities.timer import Timer
from system.graphics.renderable import Renderable
from texture.action.actiontype import ActionType
from common.direction import Direction
from directmessaging import directMessaging, DirectMessageType


import system.gamelogic.enemy
import system.graphics.renderable
import system.groupid
from messaging import messaging, MessageType

logger = logging.getLogger(__name__)


class StateAttack(State):
    name = "attack"

    def __init__(self, brain):
        State.__init__(self, brain)
        self.attackTimer = Timer()  # Timer(0.5, instant=False) # windup and cooldown


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

        # self.attackTimer.setTimer(meEnemy.enemyInfo.attackTime)
        # self.setTimer(meEnemy.enemyInfo.attackTime)

        self.stepsTodo = 30
        self.attackTimer.setTimer(0.1)
        self.setTimer(3.0)


    def process(self, dt):
        self.attackTimer.advance(dt)

        if self.attackTimer.timeIsUp():
            logger.info("{} -------- > I'm attacking".format(self.owner))

            if self.stepsTodo > 0:
                self.attackTimer.reset()
                self.stepsTodo -= 1
                meRenderable = self.brain.owner.world.component_for_entity(
                    self.brain.owner.entity, Renderable)
                meGroupId = self.brain.owner.world.component_for_entity(
                    self.brain.owner.entity, system.groupid.GroupId)
                location = meRenderable.getWeaponBaseLocation()

                actionTextureType = ActionType.charge
                messaging.add(
                    type=MessageType.EmitActionTexture,
                    data={
                        'actionTextureType': actionTextureType,
                        'location': location,
                        'fromPlayer': False,
                        'damage': 100,
                        'direction': meRenderable.direction,
                    }
                )
                directMessaging.add(
                    groupId = meGroupId.getId(),
                    type = DirectMessageType.moveEnemy,
                    data = {
                        'x': -1,
                        'y': 0,
                        'dontChangeDirection': False,
                    },
                )
            else:
                self.attackTimer.stop()

        if self.timeIsUp():
            # too long attacking. lets switch to chasing
            logger.info("{}: ---------- Too long attacking, switch to chasing".format(self.owner))
            self.brain.pop()
            self.brain.push("chase")
