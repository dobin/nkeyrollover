import logging

from ai.stickfigure.state_chase import StateChase
import system.graphics.renderable
from messaging import messaging, MessageType
from system.graphics.particleeffecttype import ParticleEffectType
from common.direction import Direction
from utilities.timer import Timer

logger = logging.getLogger(__name__)


class DragonStateChase(StateChase):
    def __init__(self, brain):
        super().__init__(brain)
        self.canSkillTimer = Timer()


    def on_enter(self):
        super().on_enter()
        self.canSkillTimer.setTimer(3.0)


    def process(self, dt):
        super().process(dt)
        self.canSkillTimer.advance(dt)


    def trySkill(self):
        if self.canSkillTimer.timeIsUp():
            meRenderable = self.brain.owner.world.component_for_entity(
                self.brain.owner.entity, system.graphics.renderable.Renderable)
            locCenter = meRenderable.getLocationCenter()
            messaging.add(
                type=MessageType.EmitParticleEffect,
                data= {
                    'location': locCenter,
                    'effectType': ParticleEffectType.dragonExplosion,
                    'damage': 50,
                    'byPlayer': False,
                    'direction': Direction.none,
                }
            )
            self.canSkillTimer.reset()
