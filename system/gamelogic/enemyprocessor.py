import esper

from system.gamelogic.tenemy import tEnemy


class EnemyProcessor(esper.Processor):
    def __init__(self):
        super().__init__()


    def process(self, deltaTime):
        for ent, player in self.world.get_component(tEnemy):
            player.advance(deltaTime)                