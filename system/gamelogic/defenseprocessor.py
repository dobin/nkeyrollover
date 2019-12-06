import esper
import logging

from system.gamelogic.defense import Defense
from system.graphics.renderable import Renderable
from directmessaging import directMessaging, DirectMessageType
from messaging import messaging, MessageType
from utilities.entityfinder import EntityFinder
from utilities.utilities import Utility

logger = logging.getLogger("DefenseProcessor")


class DefenseProcessor(esper.Processor):
    def __init__(self):
        super().__init__()


    def process(self, dt):
        self.advance(dt)
        self.checkDefenseMessages()
        self.checkReceiveDamageMessages()


    def advance(self, dt):
        for ent, defense in self.world.get_component(Defense):
            defense.advance(dt)


    def checkDefenseMessages(self):
        for msg in messaging.getByType(MessageType.Defense):
            location = msg.data['location']
            groupId = msg.data['groupId']

            entity = EntityFinder.findByGroupId(self.world, groupId)
            defense = self.world.component_for_entity(entity, Defense)
            defense.coordinates = location
            defense.isActive = True
            defense.timer.reset()


    def checkReceiveDamageMessages(self):
        for msg in directMessaging.getByType(DirectMessageType.receiveDamage, keep=True):
            sourceRenderable = msg.data['sourceRenderable']
            destinationEntity = msg.data['destinationEntity']

            if self.world.has_component(destinationEntity, Defense):
                defense = self.world.component_for_entity(destinationEntity, Defense)

                if not defense.isActive:
                    continue

                destinationRenderable = self.world.component_for_entity(
                    destinationEntity, Renderable)

                distanceDefense = Utility.distance(
                    sourceRenderable.coordinates, defense.coordinates)
                distanceEnemy = Utility.distance(
                    sourceRenderable.coordinates, destinationRenderable.coordinates)

                # logging.warn("{} {}".format(distanceDefense, distanceEnemy))
                if distanceDefense['sum'] < distanceEnemy['sum']:
                    logging.info("Blocked")
                    msg.data['damage'] = 0
                    # msg.mitigated = True
                else:
                    logging.info("Not Blocked")
