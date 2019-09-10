import esper
import logging

from system.gamelogic.ai import Ai
from messaging import messaging, MessageType

logger = logging.getLogger(__name__)


class AiProcessor(esper.Processor):
    def __init__(self):
        super().__init__()


    def process(self, deltaTime):
        for ent, ai in self.world.get_component(Ai):
            ai.advance(deltaTime)

            # remove enemies which are completely dead
            if ai.brain.state.name == 'dead':
                self.world.delete_entity(ent)

                messaging.add(
                    type = MessageType.EntityDead,
                    groupId = None,
                    data = {}
                )
