
class RenderableMinimal(object): 
    def __init__(self, texture, coordinate, active=True): 
        self.texture = texture
        self.coordinates = coordinate
        self.active = active


    def advance(self, dt):
        pass


    def isActive(self):
        return self.active


    def setActive(self, active):
        self.active = active
