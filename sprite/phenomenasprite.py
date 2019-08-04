from enum import Enum
import logging

from texture.phenomenatexturemanager import PhenomenaTextureManager
from entities.direction import Direction
from .arrsprite import ArrSprite

logger = logging.getLogger(__name__)


class PhenomenaSprite(ArrSprite): 
    def __init__(self, parentEntity=None, phenomenaType=None, direction=None):
        super(PhenomenaSprite, self).__init__(parentEntity)
        self.phenomenaTextureManager = PhenomenaTextureManager()

        if phenomenaType is not None: 
            self.changeTexture(phenomenaType, direction)


    def changeTexture(self, phenomenaType, direction):
        self.texture = self.phenomenaTextureManager.getTexture(phenomenaType, direction)
        self.init()