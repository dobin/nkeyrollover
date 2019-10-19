import logging

from texture.animationtexture import AnimationTexture
from texture.texturetype import TextureType
from texture.filetextureloader import fileTextureLoader

logger = logging.getLogger(__name__)


class PhenomenaTexture(AnimationTexture):
    def __init__(
        self, phenomenaType=None, direction=None, name='Phenomena', setbg=False
    ):
        super(PhenomenaTexture, self).__init__(
            type=TextureType.phenomena, name=name, setbg=setbg)

        if phenomenaType is not None:
            self.changeAnimation(phenomenaType, direction)


    def changeAnimation(self, phenomenaType, direction):
        self.animation = fileTextureLoader.phenomenaAnimationManager.getAnimation(
            phenomenaType,
            direction)
        self.init()
        self.width = self.animation.width
        self.height = self.animation.height
