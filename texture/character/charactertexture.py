from enum import Enum
import logging

from sprite.direction import Direction
from texture.animationtexture import AnimationTexture
from sprite.sprite import Sprite
from texture.character.characteranimationmanager import CharacterAnimationManager
from entities.entity import Entity
from texture.character.characteranimationtype import CharacterAnimationType
from .charactertype import CharacterType

logger = logging.getLogger(__name__)


class CharacterTexture(AnimationTexture):
    def __init__(
            self, 
            characterType :CharacterType,
            parentSprite :Sprite =None, 
            characterAnimationType :CharacterAnimationType =None, 
            direction :Direction =Direction.none, 
            head :str =None,
            body :str =None,
        ):
        super(CharacterTexture, self).__init__(parentSprite)

        self.characterAnimationManager = CharacterAnimationManager(
            head=head, body=body, characterType=characterType)

        if characterAnimationType is not None: 
            self.changeAnimation(characterAnimationType, direction)
            self.setActive(True)
        else: 
            self.setActive(False)


    def changeAnimation(
            self, 
            characterAnimationType :CharacterAnimationType, 
            direction :Direction, 
            subtype :int =0
        ):

        self.animation = self.characterAnimationManager.getAnimation(
            characterAnimationType, direction, subtype)
        self.init()            
        self.width = self.animation.width
        self.height = self.animation.height
