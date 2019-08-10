import logging

from config import Config
from sprite.direction import Direction
from sprite.particle import Particle
from .particleeffecttype import ParticleEffectType
from utilities.utilities import Utility

logger = logging.getLogger(__name__)


class ParticleEmiter(object): 
    def __init__(
        self,
        win
    ):
        self.win = win
        self.particlePool = []
        self.particleActive = []
        n = 0
        while n < Config.maxParticles:
            self.particlePool.append( Particle(win=win) )
            n += 1

    
    def emit(self, loc, effectType :ParticleEffectType, direction :Direction = Direction.none):
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

                basex = loc.x + (xinv * 6) # distance from char
                particle.init(
                    x=basex + n * xinv, y=loc.y, life=life, angle=angle, 
                    speed=0.0, fadeout=True, byStep=False, charType=0, 
                    active=True)

                self.particleActive.append(particle)
                particleList.append(particle)
                n += 1

        if effectType is ParticleEffectType.cleave: 
            particleCount = 8
            life = 60
            n = 0
            while n < particleCount: 
                particle = self.particlePool.pop()
                if direction is Direction.right: 
                    xinv = 4
                else: 
                    xinv = -1

                    c = Utility.getBorderHalf(loc, 2, 1, partRight=False)
                    for h in c:
                        particle.init(
                            x=h.x, y=h.y, life=life, angle=0, 
                            speed=0.0, fadeout=True, byStep=False, charType=0, 
                            active=True)


                self.particleActive.append(particle)
                particleList.append(particle)
                n += 1                

        return particleList


    def advance(self, dt): 
        for particle in self.particleActive: 
            particle.advance(dt) 

            if not particle.isActive(): 
                self.particleActive.remove( particle )
                self.particlePool.append(particle)


    def draw(self):
        for particle in self.particleActive: 
            particle.draw()