import logging

from system.graphics.particleeffecttype import ParticleEffectType
from common.direction import Direction
from config import Config
from system.graphics.particle import Particle
from common.coordinates import Coordinates
from messaging import messaging, MessageType

logger = logging.getLogger(__name__)


class ParticleEmiter(object):
    """Creates and manages particles.

    * Called from ParticleProcessor
    * Has state
    """
    def __init__(self, viewport):
        self.viewport = viewport

        # particlePool is private, and only used in ParticleEmiter
        self.particlePool = []
        n = 0
        while n < Config.maxParticles:
            self.particlePool.append(Particle(viewport=viewport))
            n += 1

        # particleActive is being used by ParticleProcessor, its basically public
        self.particleActive = []


    def unuse(self, particle):
        self.particleActive.remove(particle)
        self.particlePool.append(particle)


    def emit(
        self,
        byPlayer :bool,
        damage: int,
        loc :Coordinates,
        effectType :ParticleEffectType,
        direction :Direction = Direction.none,
    ):
        if effectType is ParticleEffectType.explosion:
            self.createExplosion(loc, direction, byPlayer, damage)
        if effectType is ParticleEffectType.laser:
            self.createLaser(loc, direction, byPlayer, damage)
        if effectType is ParticleEffectType.cleave:
            self.createCleave(loc, direction, byPlayer, damage)
        if effectType is ParticleEffectType.dragonExplosion:
            self.createDragonExplosion(loc, direction, byPlayer, damage)


    def createDragonExplosion(self, loc, direction, byPlayer, damage):
        particleCount = 16
        life = 40
        n = 0
        while n < particleCount:
            particle = self.particlePool.pop()
            angle = (360.0 / particleCount) * n

            particle.init(
                x=loc.x, y=loc.y, life=life, angle=angle,
                speed=0.1, fadeout=True, byStep=False, charType=1,
                active=True,
                damage=damage, damageEveryStep=True, byPlayer=byPlayer)

            # advance them out of the center a bit
            particle.makeStep(0.6, adjustLife=False)

            self.particleActive.append(particle)
            n += 1


    def createExplosion(self, loc, direction, byPlayer, damage):
        particleCount = 16
        life = 40
        n = 0
        while n < particleCount:
            particle = self.particlePool.pop()
            angle = (360.0 / particleCount) * n

            particle.init(
                x=loc.x, y=loc.y, life=life, angle=angle,
                speed=0.1, fadeout=True, byStep=False, charType=0,
                active=True,
                damage=damage, damageEveryStep=True, byPlayer=byPlayer)

            self.particleActive.append(particle)
            n += 1


    def createLaser(self, loc, direction, byPlayer, damage):
        particleList = []

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
                active=True,
                damage=damage)

            self.particleActive.append(particle)
            particleList.append(particle)
            n += 1

        self.createDamage(particleList, damage, byPlayer)


    def createCleave(self, loc, direction, byPlayer, damage):
        particleList = []

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

            if direction is Direction.left:
                angle = 180
            else:
                angle = 0

            basex = loc.x + xinv  # distance from char
            x = basex + xinv
            y = loc.y + n - int(particleCount / 2) + 1
            particle.init(
                x=x, y=y,
                life=life,
                angle=angle,
                speed=0.1,
                fadeout=True,
                byStep=False,
                charType=0,
                active=True,
                damage=damage,
                damageEveryStep=True)

            self.particleActive.append(particle)
            particleList.append(particle)
            n += 1

        self.createDamage(particleList, damage, byPlayer)


    def createDamage(self, hitLocations, damage, byPlayer):
        messaging.add(
            type=MessageType.AttackAt,
            data= {
                'hitLocations': hitLocations,
                'damage': damage,
                'byPlayer': byPlayer,
            }
        )
