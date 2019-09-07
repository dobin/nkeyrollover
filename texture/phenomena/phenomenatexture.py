import logging

from texture.phenomena.phenomenaanimationmanager import PhenomenaAnimationManager
from texture.animationtexture import AnimationTexture
from sprite.coordinates import Coordinates

logger = logging.getLogger(__name__)


class PhenomenaTexture(AnimationTexture):
    def __init__(self, phenomenaType=None, direction=None):
        super(PhenomenaTexture, self).__init__()
        self.phenomenaAnimationManager = PhenomenaAnimationManager()

        if phenomenaType is not None:
            self.changeAnimation(phenomenaType, direction)


    def changeAnimation(self, phenomenaType, direction):
        self.animation = self.phenomenaAnimationManager.getAnimation(
            phenomenaType,
            direction)
        self.init()
        self.width = self.animation.width
        self.height = self.animation.height
