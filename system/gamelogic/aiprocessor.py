import esper

from system.gamelogic.ai import Ai

class AiProcessor(esper.Processor):
    def __init__(self):
        super().__init__()


    def process(self, deltaTime):
        for ent, ai in self.world.get_component(Ai):
            ai.advance(deltaTime)