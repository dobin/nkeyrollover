import logging
import esper

from game.viewport import Viewport
from messaging import messaging, MessageType
from directmessaging import directMessaging, DirectMessageType
import system.gamelogic.attackable
import system.gamelogic.enemy
import system.gamelogic.player
import system.graphics.renderable
import system.groupid
from system.singletons.particleemiter import ParticleEmiter

logger = logging.getLogger(__name__)


class ParticleProcessor(esper.Processor):
    """Create and manage independant particles on the screen"""

    def __init__(
        self,
        viewport :Viewport
    ):
        self.viewport :Viewport = viewport
        self.particleEmiter = ParticleEmiter(viewport=viewport)


    def process(self, dt):
        self.checkMessages()
        self.advance(dt)
        self.render()


    def checkMessages(self):
        for message in messaging.getByType(MessageType.EmitParticleEffect):
            hitLocations = self.particleEmiter.emit(
                loc=message.data['location'],
                effectType=message.data['effectType'],
                direction=message.data['direction'],
            )
            byPlayer = message.data['byPlayer']
            damage = message.data['damage']

            if damage is not None:
                self.handleHitLocations(hitLocations, byPlayer, damage)


    def handleHitLocations(self, hitLocations, byPlayer, damage):
        for ent, (groupId, renderable, attackable) in self.world.get_components(
            system.groupid.GroupId,
            system.graphics.renderable.Renderable,
            system.gamelogic.attackable.Attackable,
        ):
            if renderable.isHitBy(hitLocations):
                directMessaging.add(
                    groupId=groupId.id,
                    type=DirectMessageType.receiveDamage,
                    data={
                        'damage': damage,
                        'byPlayer': byPlayer,
                    }
                )


    def advance(self, dt):
        for particle in self.particleEmiter.particleActive:
            particle.advance(dt)

            if not particle.isActive():
                self.particleEmiter.unuse(particle)


    def render(self):
        for particle in self.particleEmiter.particleActive:
            particle.draw()
