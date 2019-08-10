from enum import Enum
import curses
import logging 
import inspect

from texture.speechanimationmanager import SpeechAnimationManager
from sprite.direction import Direction
from texture.animationtexture import AnimationTexture
from sprite.sprite import Sprite

logger = logging.getLogger(__name__)


class SpeechTexture(AnimationTexture): 
    def __init__(
        self, parentSprite :Sprite =None, displayText :str =None, 
        direction :Direction =Direction.right
    ):
        super(SpeechTexture, self).__init__(parentSprite)
        self.speechAnimationManager = SpeechAnimationManager() 

        if displayText is not None: 
            self.changeAnimation(displayText, direction)


    def changeAnimation(self, displayText=None, direction=Direction.right):
        logger.info("Speechsprite change!")
        self.init()
        self.animation = self.speechAnimationManager.getAnimation(displayText, direction)
        self.offset.x = 1
        self.offset.y = -4
        self.width = self.animation.width
        self.height = self.animation.height