import esper

class Renderable():
    def __init__(self, r):
        self.r = r


class RenderableProcessor(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self, dt):
        for ent, rend in self.world.get_component(Renderable):
            rend.r.draw()
            