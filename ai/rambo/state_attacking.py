import logging

from ai.stickfigure.state_chase import StateChase
import system.graphics.renderable
from messaging import messaging, MessageType
from system.graphics.particleeffecttype import ParticleEffectType
from common.direction import Direction
from utilities.timer import Timer
from stackfsm.states import BaseState as State
from utilities.entityfinder import EntityFinder
from ai.aihelper import AiHelper
from directmessaging import directMessaging, DirectMessageType

logger = logging.getLogger(__name__)


class RamboStateAttacking(State):
    name = "attacking"

    def __init__(self, brain):
        super().__init__(brain)
        self.cooldownTimer = Timer()
        self.attackingTimer = Timer()


    def on_enter(self):
        self.cooldownTimer.setTimer(0.5)
        self.attackingTimer.setTimer(4.0)

        playerEntity = EntityFinder.findPlayer(self.brain.owner.world)
        if playerEntity is None:
            return

        meRenderable = self.brain.owner.world.component_for_entity(
            self.brain.owner.entity, system.graphics.renderable.Renderable)
        meGroupId = self.brain.owner.world.component_for_entity(
                self.brain.owner.entity, system.groupid.GroupId)

        self.turnIfNecessary(playerEntity, meRenderable, meGroupId)

        # attack
        messaging.add(
            type=MessageType.EntityAttack,
            groupId=meGroupId.getId(),
            data=None
        )
    

    def turnIfNecessary(self, playerEntity, meRenderable, meGroupId):
        playerRenderable = self.brain.owner.world.component_for_entity(
            playerEntity, system.graphics.renderable.Renderable)
        x, y = AiHelper.getVectorToPlayer(
            source=meRenderable.coordinates, 
            dest=playerRenderable.getLocation())

        if x > 0:
            playerDir = Direction.right
            cx = 1
        else: 
            playerDir = Direction.left
            cx = -1

        if playerDir is not meRenderable.getDirection():
            directMessaging.add(
                groupId = meGroupId.getId(),
                type = DirectMessageType.moveEnemy,
                data = {
                    'x': cx,
                    'y': 0,
                    'dontChangeDirection': False,
                    'updateTexture': False,
                    'force': False,
                },
            )


    def process(self, dt):
        self.cooldownTimer.advance(dt)
        self.attackingTimer.advance(dt)
        self.tryShooting()


    def tryShooting(self):
        if self.attackingTimer.timeIsUp():
            self.brain.pop()
            self.brain.push('standing')

        if self.cooldownTimer.timeIsUp():
            meRenderable = self.brain.owner.world.component_for_entity(
                self.brain.owner.entity, system.graphics.renderable.Renderable)
            locCenter = meRenderable.getAttackBaseLocation()
            messaging.add(
                type=MessageType.EmitParticleEffect,
                data= {
                    'location': locCenter,
                    'effectType': ParticleEffectType.bullet,
                    'damage': 50,
                    'byPlayer': False,
                    'direction': meRenderable.getDirection(),
                }
            )
            self.cooldownTimer.reset()
