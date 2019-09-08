import logging

from common.direction import Direction
from texture.animationtexture import AnimationTexture
from texture.character.characteranimationmanager import CharacterAnimationManager
from texture.character.characteranimationtype import CharacterAnimationType
from .charactertype import CharacterType

logger = logging.getLogger(__name__)


class CharacterTexture(AnimationTexture):
    def __init__(
            self,
            characterType :CharacterType,
            characterAnimationType :CharacterAnimationType =None,
            direction :Direction =Direction.none,
            head :str =None,
            body :str =None,
            name = '',
    ):
        super(CharacterTexture, self).__init__(name)

        self.characterAnimationManager = CharacterAnimationManager(
            head=head, body=body, characterType=characterType)

        self.characterAnimationType = characterAnimationType
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
        logger.debug("{} Change texture to: {}".format(
            self.name, characterAnimationType))

        self.characterAnimationType = characterAnimationType
        self.animation = self.characterAnimationManager.getAnimation(
            characterAnimationType, direction, subtype)
        self.init()
        self.width = self.animation.width
        self.height = self.animation.height
