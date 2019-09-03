import logging

from texture.speechanimationmanager import SpeechAnimationManager
from sprite.direction import Direction

logger = logging.getLogger(__name__)


class SpeechBubble(object):
    def __init__(
        self, renderable
    ):
        self.renderable = renderable
        self.speechAnimationManager = SpeechAnimationManager()


    def showText(self, displayText=None, time=1.5, direction=Direction.right):
        logger.info("Speechsprite change!")
        animation = self.speechAnimationManager.getAnimation(
            displayText=displayText, 
            time=time,
            direction=direction)
        self.renderable.texture.animation = animation
        self.renderable.texture.width = animation.width
        self.renderable.texture.height = animation.height
        self.renderable.texture.init()
        self.renderable.setActive(True)