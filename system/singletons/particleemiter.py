import logging

from system.graphics.particleeffecttype import ParticleEffectType
from common.direction import Direction
from config import Config
from system.graphics.particle import Particle
from common.coordinates import Coordinates
from messaging import messaging, MessageType
from utilities.colorpalette import ColorPalette
from utilities.color import Color

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

        self.dispatch = {
            ParticleEffectType.explosion: self.createExplosion,
            ParticleEffectType.laser: self.createLaser,
            ParticleEffectType.cleave: self.createCleave,
            ParticleEffectType.dragonExplosion: self.createDragonExplosion,
            ParticleEffectType.floatingDamage: self.createFloatingDamage,
            ParticleEffectType.hitBurst: self.createHitBurst,
            ParticleEffectType.disappear: self.createDisappear,
            ParticleEffectType.appear: self.createAppear,
            ParticleEffectType.char: self.createChar,
            ParticleEffectType.impact: self.createImpact,
            ParticleEffectType.bullet: self.createBullet,
        }


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
        self.dispatch[effectType](loc, direction, byPlayer, damage)


    def createChar(self, loc, direction, byPlayer, damage):
        particle = self.particlePool.pop()
        x = loc.x
        y = loc.y
        particle.init(
            x=x, y=y,
            life=100,
            angle=0,
            speed=0.0,
            fadeout=True,
            byStep=False,
            charType=3,
            active=True,
            damage=damage,
            damageEveryStep=False,
            color=ColorPalette.getColorByColor(Color.green))
        self.particleActive.append(particle)


    def createHitBurst(self, loc, direction, byPlayer, damage):
        particleCount = 5
        life = 20
        spacingAngle = 10.0

        n = 0
        while n < particleCount:
            particle = self.particlePool.pop()
            if direction is Direction.right:
                angle = (spacingAngle * particleCount / 2) - (spacingAngle * n)
            else:
                angle = 180 + (spacingAngle * particleCount / 2) - (spacingAngle * n)

            x = loc.x
            y = loc.y
            particle.init(
                x=x, y=y,
                life=life,
                angle=angle,
                speed=0.1,
                fadeout=True,
                byStep=False,
                charType=3,
                active=True,
                damage=damage,
                damageEveryStep=False,
                color=ColorPalette.getColorByColor(Color.grey))

            self.particleActive.append(particle)
            n += 1


    def createFloatingDamage(self, loc, direction, byPlayer, damage):
        dmgStr = str(damage)

        speed = 0.1
        if byPlayer:
            color = ColorPalette.getColorByColor(Color.brightcyan)
        else:
            color = ColorPalette.getColorByColor(Color.red)

        n = 0
        for char in dmgStr:
            particle = self.particlePool.pop()
            particle.init(
                x=loc.x + n,
                y=loc.y - 1,
                life=10,
                angle=90,
                speed=speed,
                fadeout=False,
                byStep=False,
                charType=0,
                active=True,
                damage=0,
                damageEveryStep=False,
                byPlayer=byPlayer,
                color=color)
            particle.char = dmgStr[n]
            self.particleActive.append(particle)

            n += 1


    def createDragonExplosion(self, loc, direction, byPlayer, damage):
        particleCount = 16
        life = 40
        n = 0
        while n < particleCount:
            particle = self.particlePool.pop()
            angle = (360.0 / particleCount) * n

            particle.init(
                x=loc.x, y=loc.y, life=life, angle=angle,
                speed=0.1, fadeout=True, byStep=False, charType=2,
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
                x=loc.x, y=loc.y, 
                life=life, 
                angle=angle,
                speed=0.1, 
                fadeout=True, 
                byStep=False, 
                charType=1,
                active=True,
                damage=damage, 
                damageEveryStep=True, 
                byPlayer=byPlayer)

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
                speed=0.0, fadeout=True, byStep=False, charType=1,
                active=True,
                damage=damage)

            self.particleActive.append(particle)
            particleList.append(particle)
            n += 1

        self.createDamage(particleList, damage, byPlayer, direction)


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
        #         speed=0.0, fadeout=True, byStep=False, charType=1,
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
                charType=1,
                active=True,
                damage=damage,
                damageEveryStep=True)

            self.particleActive.append(particle)
            particleList.append(particle)
            n += 1

        self.createDamage(particleList, damage, byPlayer, direction)


    def createDamage(self, hitLocations, damage, byPlayer, direction):
        messaging.add(
            type=MessageType.AttackAt,
            data= {
                'hitLocations': hitLocations,
                'damage': damage,
                'byPlayer': byPlayer,
                'direction': direction,
                'knockback': False,
                'stun': False,
                'sourceRenderable': None,
            }
        )


    def createDisappear(self, loc, direction, byPlayer, damage):
        particleCount = 4
        life = 20
        n = 0
        while n < particleCount:
            particle = self.particlePool.pop()
            angle = (360.0 / particleCount) * n

            particle.init(
                x=loc.x, y=loc.y, life=life, angle=angle,
                speed=0.1, fadeout=True, byStep=False, charType=1,
                active=True,
                damage=damage, damageEveryStep=False, byPlayer=byPlayer)

            self.particleActive.append(particle)
            n += 1


    def createAppear(self, loc, direction, byPlayer, damage):
        particleCount = 8
        life = 20
        n = 0
        while n < particleCount:
            particle = self.particlePool.pop()
            angle = (360.0 / particleCount) * n

            particle.init(
                x=loc.x, y=loc.y, life=life, angle=angle,
                speed=0.1, fadeout=True, byStep=False, charType=1,
                active=True,
                damage=damage, damageEveryStep=False, byPlayer=byPlayer)

            self.particleActive.append(particle)
            n += 1


    def createImpact(self, loc, direction, byPlayer, damage):
        particle = self.particlePool.pop()

        particle.init(
            x=loc.x, y=loc.y,
            life=10,
            angle=0,
            speed=0.0,
            fadeout=True,
            byStep=False,
            charType=4,
            active=True,
            damage=0,
            damageEveryStep=False,
            color=ColorPalette.getColorByColor(Color.red))

        self.particleActive.append(particle)


    def createBullet(self, loc, direction, byPlayer, damage):
        particle = self.particlePool.pop()

        if direction is Direction.left:
            angle = 180
        else:
            angle = 0

        particle.init(
            x=loc.x, y=loc.y,
            life=100,
            angle=angle,
            speed=0.1,
            fadeout=False,
            byStep=False,
            charType=5,
            active=True,
            damage=10,
            damageEveryStep=True,
            byPlayer=byPlayer,
            color=ColorPalette.getColorByColor(Color.red))

        self.particleActive.append(particle)
