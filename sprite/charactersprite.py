from enum import Enum
import logging

from entities.direction import Direction
from .arrsprite import ArrSprite
from texture.charactertexturemanager import CharacterTextureManager
from entities.entity import Entity
from texture.characteranimationtype import CharacterAnimationType

logger = logging.getLogger(__name__)


class CharacterSprite(ArrSprite):
    def __init__(
            self, 
            parentEntity :Entity =None, 
            characterAnimationType :CharacterAnimationType =None, 
            direction :Direction =None, 
            head :str =None, 
            body :str =None
        ):
        super(CharacterSprite, self).__init__(parentEntity)

        self.characterTextureManager = CharacterTextureManager(head, body)
        if characterAnimationType is not None: 
            self.changeTexture(characterAnimationType, direction)


    def changeTexture(
            self, 
            characterAnimationType :CharacterAnimationType, 
            direction :Direction, 
            subtype :int =0
        ):
        self.texture = self.characterTextureManager.getTexture(characterAnimationType, direction, subtype)
        self.init()

        

