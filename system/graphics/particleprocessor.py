import logging
import esper

from game.viewport import Viewport
from messaging import messaging, MessageType
from system.singletons.particleemiter import ParticleEmiter

logger = logging.getLogger(__name__)


class ParticleProcessor(esper.Processor):
    """Create and manage independant particles on the screen"""

    def __init__(
        self,
        viewport :Viewport
    ):
        super().__init__()
        self.viewport :Viewport = viewport
        self.particleEmiter = ParticleEmiter(viewport=viewport)


    def process(self, dt):
        self.checkMessages()
        self.advance(dt)
        self.render()


    def checkMessages(self):
        for message in messaging.getByType(MessageType.EmitParticleEffect):
            self.particleEmiter.emit(
                loc=message.data['location'],
                effectType=message.data['effectType'],
                direction=message.data['direction'],
                byPlayer=message.data['byPlayer'],
                damage=message.data['damage']
            )


    def advance(self, dt):
        for particle in self.particleEmiter.particleActive:
            particle.advance(dt)

            if not particle.isActive():
                self.particleEmiter.unuse(particle)


    def render(self):
        for particle in self.particleEmiter.particleActive:
            particle.draw()
