import esper
import logging

from system.graphics.renderable import Renderable
from system.groupid import GroupId
from system.gamelogic.attackable import Attackable
from system.gamelogic.player import Player
from messaging import messaging, MessageType
from directmessaging import directMessaging, DirectMessageType
from config import Config
from utilities.timer import Timer
from system.singletons.damagestat import damageStat
from system.graphics.particleeffecttype import ParticleEffectType

logger = logging.getLogger(__name__)


class DamageProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
        self.dmgTimer = Timer(1.0)


    def process(self, dt):
        self.dmgTimer.advance(dt)
        if self.dmgTimer.timeIsUp():
            damageStat.addDamage(-10)
            self.dmgTimer.reset()

        damageSumPlayer = 0
        for msg in messaging.getByType(MessageType.AttackAt):
            for entity, (meAtk, groupId, renderable) in self.world.get_components(
                Attackable, GroupId, Renderable
            ):
                hitLocations = msg.data['hitLocations']
                damage = msg.data['damage']
                byPlayer = msg.data['byPlayer']
                direction = msg.data['direction']
                knockback = msg.data['knockback']
                stun = msg.data['stun']

                if 'sourceRenderable' in msg.data:
                    sourceRenderable = msg.data['sourceRenderable']
                else:
                    sourceRenderable = None

                if renderable.isHitBy(hitLocations):
                    directMessaging.add(
                        groupId=groupId.id,
                        type=DirectMessageType.receiveDamage,
                        data={
                            'damage': damage,
                            'byPlayer': byPlayer,
                            'direction': direction,
                            'knockback': knockback,
                            'stun': stun,

                            'sourceRenderable': sourceRenderable,
                            'destinationEntity': entity,
                            'hitLocations': hitLocations,
                        }
                    )

                    if byPlayer:
                        damageSumPlayer += damage

        # check if we should announce our awesomeness
        if damageSumPlayer > Config.announceDamage:
            # find player
            for ent, (groupId, player) in self.world.get_components(
                GroupId, Player
            ):
                directMessaging.add(
                    groupId = groupId.getId(),
                    type = DirectMessageType.activateSpeechBubble,
                    data = {
                        'text': 'Cowabunga!',
                        'time': 1.0,
                    }
                )

        damageStat.addDamage(damageSumPlayer)
