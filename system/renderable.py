import esper

from config import Config

class Renderable():
    def __init__(self, r, z=0):
        self.r = r
        self.z = z


class RenderableProcessor(esper.Processor):
    def __init__(self):
        super().__init__()

        # list of HEIGHT lists
        self.order = [[] for i in range(Config.rows)]

    def process(self, dt):
        for l in self.order: 
            l.clear()
        
        # add all elements to draw in the correct Z order
        # which is by y coordinates
        for ent, rend in self.world.get_component(Renderable):
            self.order[ rend.r.coordinates.y ].append(rend.r)
            
        for l in self.order:
            for entry in l:
                entry.draw()