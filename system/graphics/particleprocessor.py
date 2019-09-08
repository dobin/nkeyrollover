import logging
import esper

from config import Config
from common.direction import Direction
from common.particle import Particle
from world.particleeffecttype import ParticleEffectType
from world.viewport import Viewport
from messaging import messaging, MessageType
from directmessaging import directMessaging, DirectMessageType
import system.gamelogic.attackable
import system.gamelogic.enemy
import system.gamelogic.player
import system.graphics.renderable
import system.groupid

logger = logging.getLogger(__name__)


class ParticleProcessor(esper.Processor):
    """Create and manage independant particles on the screen"""

    def __init__(
        self,
        viewport :Viewport
    ):
        self.viewport :Viewport = viewport
        self.particlePool = []
        self.particleActive = []
        n = 0
        while n < Config.maxParticles:
            self.particlePool.append(Particle(viewport=viewport))
            n += 1


    def process(self, dt):
        self.checkMessages()
        self.advance(dt)
        self.render()


    def checkMessages(self):
        for message in messaging.getByType(MessageType.EmitParticleEffect):
            hitLocations = self.emit(
                loc=message.data['location'],
                effectType=message.data['effectType'],
                direction=message.data['direction'],
            )
            byPlayer = message.data['byPlayer'],
            damage = message.data['damage']

            if damage is not None:
                self.handleHitLocations(hitLocations, byPlayer, damage)


    def handleHitLocations(self, hitLocations, byPlayer, damage):
        for ent, (groupId, renderable, attackable, enemy) in self.world.get_components(
            system.groupid.GroupId,
            system.graphics.renderable.Renderable,
            system.gamelogic.attackable.Attackable,
            system.gamelogic.enemy.Enemy
        ):
            if renderable.isHitBy(hitLocations):
                directMessaging.add(
                    groupId=groupId.id,
                    type=DirectMessageType.receiveDamage,
                    data=damage
                )


    def advance(self, dt):
        for particle in self.particleActive:
            particle.advance(dt)

            if not particle.isActive():
                self.particleActive.remove(particle)
                self.particlePool.append(particle)


    def render(self):
        for particle in self.particleActive:
            particle.draw()


    def emit(
        self, loc, effectType :ParticleEffectType,
        direction :Direction = Direction.none
    ):
        particleList = []
        if effectType is ParticleEffectType.explosion:
            particleCount = 16
            life = 40
            n = 0
            while n < particleCount:
                particle = self.particlePool.pop()
                angle = (360.0 / particleCount) * n

                particle.init(
                    x=loc.x, y=loc.y, life=life, angle=angle,
                    speed=0.1, fadeout=True, byStep=False, charType=0,
                    active=True)

                self.particleActive.append(particle)
                particleList.append(particle)
                n += 1

        if effectType is ParticleEffectType.laser:
            particleCount = 16
            life = 60
            n = 0
            while n < particleCount:
                particle = self.particlePool.pop()
                if direction is Direction.right:
                    angle = 0.0
                    xinv = 1
                else:
                    angle = 180
                    xinv = -1

                basex = loc.x + (xinv * 6)  # distance from char
                particle.init(
                    x=basex + n * xinv, y=loc.y, life=life, angle=angle,
                    speed=0.0, fadeout=True, byStep=False, charType=0,
                    active=True)

                self.particleActive.append(particle)
                particleList.append(particle)
                n += 1

        if effectType is ParticleEffectType.cleave:
            particleCount = 7
            life = 60
            n = 0

            if direction is Direction.right:
                xinv = 2
            else:
                xinv = -1

            # for debug, source
            # particle = self.particlePool.pop()
            # particle.init(
            #         x=loc.x, y=loc.y, life=life, angle=0,
            #         speed=0.0, fadeout=True, byStep=False, charType=0,
            #         active=True)
            # particleList.append(particle)
            # self.particleActive.append(particle)

            while n < particleCount:
                particle = self.particlePool.pop()

                basex = loc.x + xinv  # distance from char
                logger.debug("New particle at: {}/{}".format(basex + xinv, loc.y + n))
                particle.init(
                    x=basex + xinv, y=loc.y + n - int(particleCount / 2) + 1,
                    life=life,
                    angle=0,
                    speed=0.0,
                    fadeout=True,
                    byStep=False,
                    charType=0,
                    active=True)

                self.particleActive.append(particle)
                particleList.append(particle)
                n += 1

        return particleList

