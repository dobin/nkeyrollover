import esper
import logging

from system.graphics.renderable import Renderable
from system.groupid import GroupId
from system.gamelogic.attackable import Attackable
from system.gamelogic.player import Player
from system.gamelogic.enemy import Enemy
from messaging import messaging, MessageType
from directmessaging import directMessaging, DirectMessageType
from config import Config
from utilities.timer import Timer
from system.singletons.damagestat import damageStat
from system.graphics.particleeffecttype import ParticleEffectType

logger = logging.getLogger(__name__)


class OnhitProcessor(esper.Processor):
    """If an AttackAt collides with an attackable, emit some effects"""

    def __init__(self):
        super().__init__()


    def process(self, dt):
        for msg in messaging.getByType(MessageType.AttackAt):
            hitLocations = msg.data['hitLocations']
            #damage = msg.data['damage']
            byPlayer = msg.data['byPlayer']
            direction = msg.data['direction']
            #knockback = msg.data['knockback']
            #stun = msg.data['stun']
            
            #if 'onHitEffect' in msg.data:
            #    onHitEffect = msg.data['onHitEffect']
            #else:
            #    onHitEffect = None
            onHitEffect = True

            if onHitEffect:
                self.handleOnHit(hitLocations, direction, byPlayer)


    def handleOnHit(self, hitLocations, direction, byPlayer):
            for entity, renderable in self.world.get_component(
                Renderable
            ):
                isPlayer = self.world.has_component(entity, Player)
                isEnemy = self.world.has_component(entity, Enemy)

                if renderable.isHitBy(hitLocations):
                    particleLocations = renderable.getHitLocationsOf(hitLocations)

                    if not isPlayer and not isEnemy:
                        # its environment. allow
                        pass
                    else:
                        # enemy can attack player, and vice-versa
                        if not byPlayer ^ isPlayer:
                            continue

                    for particleLocation in particleLocations:
                        messaging.add(
                            type=MessageType.EmitParticleEffect,
                            data={
                                'location': particleLocation,
                                'effectType': ParticleEffectType.impact,
                                'damage': 0,
                                'byPlayer': True,
                                'direction': direction,
                            }
                        )
