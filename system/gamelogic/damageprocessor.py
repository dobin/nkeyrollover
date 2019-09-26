import esper
import logging

from system.graphics.renderable import Renderable
from system.groupid import GroupId
from system.gamelogic.attackable import Attackable
from system.gamelogic.player import Player
from messaging import messaging, MessageType
from directmessaging import directMessaging, DirectMessageType
from config import Config

logger = logging.getLogger(__name__)


class DamageProcessor(esper.Processor):
    def __init__(self):
        super().__init__()


    def process(self, dt):
        damageSumPlayer = 0
        for msg in messaging.getByType(MessageType.AttackAt):
            for entity, (meAtk, groupId, renderable) in self.world.get_components(
                Attackable, GroupId, Renderable
            ):
                hitLocations = msg.data['hitLocations']
                damage = msg.data['damage']
                byPlayer = msg.data['byPlayer']

                if renderable.isHitBy(hitLocations):
                    directMessaging.add(
                        groupId=groupId.id,
                        type=DirectMessageType.receiveDamage,
                        data={
                            'damage': damage,
                            'byPlayer': byPlayer,
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