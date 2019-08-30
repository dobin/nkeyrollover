import esper

class tEnemy():
    def __init__(self, characterType):
        self.characterType = characterType


class tEnemyProcessor(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self, dt):
        pass
            