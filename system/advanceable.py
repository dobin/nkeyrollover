import esper

class Advanceable():
    def __init__(self, r):
        self.r = r

class AdvanceableProcessor(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self, dt):
        for ent, rend in self.world.get_component(Advanceable):
            rend.r.advance(dt)
