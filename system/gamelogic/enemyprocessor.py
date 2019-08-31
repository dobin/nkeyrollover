import esper

from system.gamelogic.enemy import Enemy


class EnemyProcessor(esper.Processor):
    def __init__(self):
        super().__init__()


    def process(self, deltaTime):
        for ent, player in self.world.get_component(Enemy):
            player.advance(deltaTime)                