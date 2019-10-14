import logging

from common.direction import Direction
from texture.animationtexture import AnimationTexture
from texture.character.characteranimationtype import CharacterAnimationType
from texture.character.charactertexturetype import CharacterTextureType
from texture.texturetype import TextureType
from texture.filetextureloader import fileTextureLoader

logger = logging.getLogger('CharacterTexture')


class CharacterTexture(AnimationTexture):
    def __init__(
            self,
            characterTextureType :CharacterTextureType =None,
            characterAnimationType :CharacterAnimationType =None,
            direction :Direction =Direction.none,
            name = '',
    ):
        super(CharacterTexture, self).__init__(type=TextureType.character, name=name)
        self.previousAnimation = None
        self.previousFrameIndex = None
        self.previousFrameTimeLeft = None

        self.characterTextureType = characterTextureType
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
        logger.info("{}: Change texture to: {}  (irq: {})".format(
            self.name, characterAnimationType, interrupt))

        # interupt the current animation
        if interrupt:
            if self.previousAnimation is None:
                # store current animation, to restore it later
                self.previousAnimationStore()
            else:
                # we are already interrupted. overwrite current animation, but dont
                # touch the self.previousAnimation one
                logger.info(
                    "{}: Animation to {}, but already int in {} (prev {})".format(
                        self.name,
                        characterAnimationType,
                        self.animation,
                        self.previousAnimation
                    )
                )
        else:
            # if we have a new animation which does not interrupt,
            # remove previously stored one
            self.previousAnimationClear()

        self.setActive(True)
        self.characterAnimationType = characterAnimationType
        self.animation = fileTextureLoader.characterAnimationManager.getAnimation(
            characterTextureType=self.characterTextureType,
            characterAnimationType=characterAnimationType,
            direction=direction,
            subtype=subtype)
        self.init()
        self.width = self.animation.width
        self.height = self.animation.height


    def setCharacterTextureType(self, characterTextureType):
        logging.info("Set Character texture to: {}".format(characterTextureType))
        self.characterTextureType = characterTextureType


    def advance(self, deltaTime):
        super().advance(deltaTime)

        if self.previousAnimation is not None and self.isActive() is False:
            self.previousAnimationRestore()


    def previousAnimationStore(self):
        logger.info("{}: Interrupt, store current: {}".format(
            self.name, self.animation))
        self.previousAnimation = self.animation
        self.previousFrameIndex = self.frameIndex
        self.previousFrameTimeLeft = self.frameTimeLeft


    def previousAnimationRestore(self):
        logger.info("{}: Reset Animation to: {}".format(
            self.name, self.previousAnimation))
        self.animation = self.previousAnimation
        self.frameIndex = self.previousFrameIndex
        self.frameTimeLeft = self.previousFrameTimeLeft
        self.previousAnimationClear()
        self.setActive(True)


    def previousAnimationClear(self):
        self.previousAnimation = None
        self.previousFrameIndex = None
        self.previousFrameTimeLeft = None
