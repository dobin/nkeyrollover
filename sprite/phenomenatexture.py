from enum import Enum
import logging

from texture.phenomenaanimationmanager import PhenomenaAnimationManager
from entities.direction import Direction
from .animationtexture import AnimationTexture

logger = logging.getLogger(__name__)


class PhenomenaTexture(AnimationTexture): 
    def __init__(self, parentSprite=None, phenomenaType=None, direction=None):
        super(PhenomenaTexture, self).__init__(parentSprite)
        self.phenomenaAnimationManager = PhenomenaAnimationManager()

        if phenomenaType is not None: 
            self.changeAnimation(phenomenaType, direction)


    def changeAnimation(self, phenomenaType, direction):
        self.animation = self.phenomenaAnimationManager.getAnimation(phenomenaType, direction)
        self.init()
        self.width = self.animation.width
        self.height = self.animation.height