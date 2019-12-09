import logging
import esper

from game.viewport import Viewport
from messaging import messaging, MessageType
from system.singletons.particleemiter import ParticleEmiter
from utilities.entityfinder import EntityFinder

logger = logging.getLogger(__name__)


class ParticleProcessor(esper.Processor):
    """Create and manage independant particles on the screen"""

    def __init__(
        self,
        viewport :Viewport,
        particleEmiter :ParticleEmiter
    ):
        super().__init__()
        self.viewport :Viewport = viewport
        self.particleEmiter :ParticleEmiter = particleEmiter


    def process(self, dt):
        self.advance(dt)


    def advance(self, dt):
        for particle in self.particleEmiter.particleActive:
            particle.advance(dt)
            if not EntityFinder.isDestinationEmptyForParticle(self.world, particle):
                # Note: it already did damage and everything
                particle.setActive(False)

            if not particle.isActive():
                self.particleEmiter.unuse(particle)