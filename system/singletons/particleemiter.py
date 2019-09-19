import logging

from system.graphics.particleeffecttype import ParticleEffectType
from common.direction import Direction
from config import Config
from system.graphics.particle import Particle
from common.coordinates import Coordinates

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
        loc :Coordinates,
        effectType :ParticleEffectType,
        direction :Direction = Direction.none
    ):
        particleList = None

        if effectType is ParticleEffectType.explosion:
            particleList = self.createExplosion(loc, direction)
        if effectType is ParticleEffectType.laser:
            particleList = self.createLaser(loc, direction)
        if effectType is ParticleEffectType.cleave:
            particleList = self.createCleave(loc, direction)
        if effectType is ParticleEffectType.dragonExplosion:
            particleList = self.createDragonExplosion(loc, direction)

        return particleList


    def createDragonExplosion(self, loc, direction):
        particleList = []
        particleCount = 16
        life = 40
        n = 0
        while n < particleCount:
            particle = self.particlePool.pop()
            angle = (360.0 / particleCount) * n

            particle.init(
                x=loc.x, y=loc.y, life=life, angle=angle,
                speed=0.1, fadeout=True, byStep=False, charType=1,
                active=True)

            # advance them out of the center a bit
            particle.makeStep(0.6, adjustLife=False)

            self.particleActive.append(particle)
            particleList.append(particle)
            n += 1

        return particleList


    def createExplosion(self, loc, direction):
        particleList = []
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

        return particleList


    def createLaser(self, loc, direction):
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
                active=True)

            self.particleActive.append(particle)
            particleList.append(particle)
            n += 1

        return particleList


    def createCleave(self, loc, direction):
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