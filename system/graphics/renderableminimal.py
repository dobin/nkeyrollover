
class RenderableMinimal(object):
    def __init__(self, texture, coordinates, active=True):
        self.texture = texture
        self.coordinates = coordinates
        self.active = active


    def advance(self, dt):
        pass


    def isActive(self):
        return self.active


    def setActive(self, active):
        self.active = active


    def getLocation(self):
        return self.coordinates
