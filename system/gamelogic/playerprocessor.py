import esper
import logging

import system.gamelogic.player

logger = logging.getLogger(__name__)


class PlayerProcessor(esper.Processor):
    def __init__(self):
        super().__init__()


    def process(self, deltaTime):
        self.advance(deltaTime)


    def advance(self, deltaTime):
        for ent, player in self.world.get_component(
            system.gamelogic.player.Player
        ):
            player.advance(deltaTime)
