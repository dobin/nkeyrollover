import copy
import logging

from sprite.coordinates import Coordinates
from sprite.sprite import Sprite

logger = logging.getLogger(__name__)


class Texture(object):
    def __init__(self, width =0, height =0):
        self.width :int = width
        self.height :int = height
        self.active :bool = True


    def draw(self, viewport):
        pass


    def advance(self, deltaTime :float):
        pass


    def advanceStep(self):
        pass


    def setActive(self, active :bool):
        self.active = active


    def isActive(self) -> bool:
        return self.active
