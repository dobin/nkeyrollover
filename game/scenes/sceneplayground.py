from game.scenes.scenebase import SceneBase
from messaging import messaging, MessageType
from common.coordinates import Coordinates
from common.direction import Direction
from system.graphics.particleeffecttype import ParticleEffectType
from utilities.color import Color


class ScenePlayground(SceneBase):
    def __init__(self, viewport, world):
        super().__init__(world=world, viewport=viewport)
        self.name = "Playground"
        self.isShowPlayer = True
        self.isShowMap = True


    def handlePlayerKeyPress(self, key):
        loc = Coordinates(20, 15)
        if key == 49:  # numpad 1
            self.emitParticleEffect(loc, ParticleEffectType.explosion)

        if key == 50:  # numpad 2
            self.emitParticleEffect(loc, ParticleEffectType.dragonExplosion)


    def emitParticleEffect(self, loc, particleEffect):
        messaging.add(
            type=MessageType.EmitParticleEffect,
            data= {
                'location': loc,
                'effectType': particleEffect,
                'damage': None,
                'byPlayer': True,
                'direction': Direction.none,
            }
        )
        messaging.add(
            type=MessageType.EmitTextureMinimal,
            data={
                'char': 'X',
                'timeout': 1,
                'coordinate': loc,
                'color': Color.grey
            }
        )
