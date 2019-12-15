import logging

from ai.stickfigure.state_chase import StateChase
import system.graphics.renderable
from messaging import messaging, MessageType
from system.graphics.particleeffecttype import ParticleEffectType
from common.direction import Direction
from utilities.timer import Timer
from stackfsm.states import BaseState as State

logger = logging.getLogger(__name__)


class RamboStateStanding(State):
    name = "standing"

    def __init__(self, brain):
        super().__init__(brain)
        self.canAttackTimer = Timer()


    def on_enter(self):
        self.canAttackTimer.setTimer(2.0)

        meGroupId = self.brain.owner.world.component_for_entity(
                self.brain.owner.entity, system.groupid.GroupId)
        messaging.add(
            type=MessageType.EntityStanding,
            groupId=meGroupId.getId(),
            data=None
        )

    def process(self, dt):
        self.canAttackTimer.advance(dt)
        self.tryAttack()


    def tryAttack(self):
        if self.canAttackTimer.timeIsUp():
            self.brain.pop()
            self.brain.push("attacking")
