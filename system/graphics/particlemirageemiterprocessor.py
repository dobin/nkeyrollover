import logging
import esper

from game.viewport import Viewport
from messaging import messaging, MessageType
from system.singletons.particleemiter import ParticleEmiter
from utilities.entityfinder import EntityFinder

logger = logging.getLogger(__name__)


class ParticleMirageEmiterProcessor(esper.Processor):
    """Create and manage independant particles on the screen"""

    def __init__(
        self,
        particleEmiter :ParticleEmiter
    ):
        super().__init__()
        self.particleEmiter :ParticleEmiter = particleEmiter


    def process(self, dt):
        self.checkMessages()


    def checkMessages(self):
        for message in messaging.getByType(MessageType.EmitMirageParticleEffect):
            self.particleEmiter.emit(
                loc=message.data['location'],
                effectType=message.data['effectType'],
                direction=message.data['direction'],
                byPlayer=message.data['byPlayer'],
                damage=message.data['damage'],
            )
