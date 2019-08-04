from enum import Enum
import curses
import logging 
import inspect

from texture.speechtexturemanager import SpeechTextureManager
from entities.direction import Direction
from .arrsprite import ArrSprite

logger = logging.getLogger(__name__)


class SpeechSprite(ArrSprite): 
    def __init__(self, parentEntity=None, displayText=None, direction=Direction.right):
        super(SpeechSprite, self).__init__(parentEntity)
        self.speechTextureManager = SpeechTextureManager() 

        if displayText is not None: 
            self.changeTexture(displayText, direction)


    def changeTexture(self, displayText=None, direction=Direction.right):
        logging.info("Speechsprite change!")
        self.texture = self.speechTextureManager.getTexture(displayText, direction)
        self.init()
        self.xoffset = 1
        self.yoffset = -4
