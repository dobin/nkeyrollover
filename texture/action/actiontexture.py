import logging

from texture.animationtexture import AnimationTexture
from texture.texturetype import TextureType
from texture.filetextureloader import fileTextureLoader

logger = logging.getLogger(__name__)


class ActionTexture(AnimationTexture):
    def __init__(self, actionType=None, direction=None, name=''):
        super(ActionTexture, self).__init__(type=TextureType.action, name=name)

        if actionType is not None:
            self.changeAnimation(actionType, direction)


    def changeAnimation(self, actionType, direction):
        self.animation = fileTextureLoader.actionAnimationManager.getAnimation(
            actionType,
            direction)
        self.init()
        self.width = self.animation.width
        self.height = self.animation.height
