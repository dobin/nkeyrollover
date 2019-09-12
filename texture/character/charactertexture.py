import logging

from common.direction import Direction
from texture.animationtexture import AnimationTexture
from texture.character.characteranimationmanager import CharacterAnimationManager
from texture.character.characteranimationtype import CharacterAnimationType
from .charactertype import CharacterType

logger = logging.getLogger('CharacterTexture')


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
        super(CharacterTexture, self).__init__(name=name)
        self.previousAnimation = None

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
            subtype :int =0,
            interrupt=False
    ):
        # interupt the current animation
        if interrupt:
            if self.previousAnimation is None:
                # store current animation, to restore it later
                logging.info("{}: Interrupt, store current: {}".format(
                    self.name, self.animation))
                self.previousAnimation = self.animation
            else:
                # we are already interrupted. overwrite current animation, but dont
                # touch the self.previousAnimation one
                logging.warning("{}: Animation to {}, but already interrupted in {} (prev {})".format(
                    self.name,
                    characterAnimationType,
                    self.animation,
                    self.previousAnimation
                ))
                pass
        #else:
        #    self.previousAnimation = None

        # cow: ignore walking
        if not interrupt and self.previousAnimation is not None:
            logging.info("{}: Wanted to change state to {}, but its not interrupted=True, while I am".format(
                self.name,
                characterAnimationType
            ))
            return


        logger.info("{}: Change texture to: {}".format(
            self.name, characterAnimationType))

        self.characterAnimationType = characterAnimationType
        self.animation = self.characterAnimationManager.getAnimation(
            characterAnimationType, direction, subtype)
        self.init()
        self.width = self.animation.width
        self.height = self.animation.height


    def advance(self, deltaTime):
        super().advance(deltaTime)

        if self.previousAnimation is not None and self.isActive() is False:
            logging.info("{}: Reset to: {}".format(
                self.name,
                self.previousAnimation))
            self.animation = self.previousAnimation
            self.previousAnimation = None
            self.setActive(True)
