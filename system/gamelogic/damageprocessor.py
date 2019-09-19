import esper
import logging

from system.graphics.renderable import Renderable
from system.groupid import GroupId
from system.gamelogic.attackable import Attackable
from messaging import messaging, MessageType
from directmessaging import directMessaging, DirectMessageType

logger = logging.getLogger(__name__)


class DamageProcessor(esper.Processor):
    def __init__(self):
        super().__init__()


    def process(self, dt):
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
