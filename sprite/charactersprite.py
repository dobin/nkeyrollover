from enum import Enum
import logging

from entities.direction import Direction
from .arrsprite import ArrSprite
from texture.charactertexturemanager import CharacterTextureManager

logger = logging.getLogger(__name__)


class CharacterSprite(ArrSprite):
    def __init__(self, parentEntity=None, characterAnimationType=None, direction=None, head=None, body=None):
        super(CharacterSprite, self).__init__(parentEntity)

        self.characterTextureManager = CharacterTextureManager(head, body)
        if characterAnimationType is not None: 
            self.changeTexture(characterAnimationType, direction)


    def changeTexture(self, characterAnimationType, direction, subtype=0):
        self.texture = self.characterTextureManager.getTexture(characterAnimationType, direction, subtype)
        self.init()

        

