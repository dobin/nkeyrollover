import logging

from texture.speech.speechanimationmanager import SpeechAnimationManager
from texture.animationtexture import AnimationTexture

logger = logging.getLogger(__name__)


class SpeechTexture(AnimationTexture):
    def __init__(self, displayText=None, time=None):
        super(SpeechTexture, self).__init__()
        self.speechAnimationManager = SpeechAnimationManager()

        if displayText is not None:
            self.changeAnimation(displayText, time)


    def changeAnimation(self, displayText, time):
        logger.info("Speechsprite change!")
        animation = self.speechAnimationManager.getAnimation(
            displayText=displayText,
            time=time)
        self.animation = animation
        self.width = animation.width
        self.height = animation.height
        self.init()
