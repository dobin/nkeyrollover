import esper
from typing import List
from sprite.coordinates import Coordinates
from entities.character import Character

from config import Config

class Renderable():
    def __init__(self, r :Character, z=0):
        self.r :Character = r
        self.z = z


    def isHitBy(self, hitLocations :List[Coordinates]):
        for hitLocation in hitLocations:
            if self.r.collidesWithPoint(hitLocation):
                return True
        
        return False


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
                if entry.isActive():
                    entry.draw()