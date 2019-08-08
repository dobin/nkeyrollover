import logging

from .world import World
from sprite.particle import Particle
from .particleeffecttype import ParticleEffectType

logger = logging.getLogger(__name__)



class ParticleEmiter(object): 
    def __init__(
        self,
        world :World,
    ):
        self.world = world

        self.particlePool = []
        self.particleActive = []
        n = 0
        while n < 32:
            self.particlePool.append( Particle() )
            n += 1

    
    def emit(self, x :int, y :int, effectType :ParticleEffectType): 
        if effectType is ParticleEffectType.explosion: 
            particleCount = 16
            life = 30
            n = 0
            while n < particleCount: 
                particle = self.particlePool.pop()
                angle = (360.0 / particleCount) * n

                particle.init(
                    x=x, y=y, life=life, angle=angle, speed=0.1, fadeout=True, 
                    byStep=False, charType=0, active=True)

                self.particleActive.append(particle)
                n += 1


    def advance(self, dt): 
        for particle in self.particleActive: 
            particle.advance(dt) 

            if particle.isActive() == False: 
                self.particleActive.remove( particle )
                self.particlePool.append(particle)


    def draw(self, win):
        for particle in self.particleActive: 
            particle.draw(win)