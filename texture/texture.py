import copy
import logging

from sprite.coordinates import Coordinates
from sprite.sprite import Sprite

logger = logging.getLogger(__name__)


class Texture(object): 
    def __init__(self, parentSprite :Sprite, width =0, height =0, offset =None):
        self.parentSprite :Sprite =parentSprite
        self.width :int = width
        self.height :int = height
        self.active :bool = True
        self.offset :Coordinates = Coordinates()
        if offset is not None: 
            self.offset.x = offset.x
            self.offset.y = offset.y


    def draw(self, viewport): 
        pass


    def advance(self, deltaTime :float):
        pass


    def setActive(self, active :bool): 
        self.active = active


    def isActive(self) -> bool: 
        return self.active


    def getLocation(self):
        """Get a copy of the location
        
        The location may depend on the parentSprite, if it is not None
        """        
        if self.parentSprite is None:
            return copy.copy(self.offset)
        else:
            loc = copy.copy(self.parentSprite.getLocation())
            loc.x += self.offset.x
            loc.y += self.offset.y
            return loc


    def setLocation(self, x, y):
        self.offset.x = x
        self.offset.y = y
