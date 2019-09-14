import logging
import random

from common.direction import Direction
from texture.character.characteranimationtype import CharacterAnimationType
from texture.character.charactertexturetype import CharacterTextureType
from texture.filetextureloader import FileTextureLoader
from utilities.utilities import Utility

logger = logging.getLogger(__name__)


class CharacterAnimationObj(object):
    def __init__(self, animationsLeft, animationsRight):
        self.animationsLeft = animationsLeft
        self.animationsRight = animationsRight


class CharacterAnimationManager(object):
    def __init__(self):
        self.characterAnimationObjs = {}
        self.fileTextureLoader = FileTextureLoader()
        self.isLoaded = False


    def init(self):
        for characterTextureType in CharacterTextureType:
            animationsLeft = {}
            animationsRight = {}

            for animationType in CharacterAnimationType:
                animationsLeft[animationType] = self.createAnimations(
                    animationType, characterTextureType, Direction.left)
            for animationType in CharacterAnimationType:
                animationsRight[animationType] = self.createAnimations(
                    animationType, characterTextureType, Direction.right)

            characterAnimationObj = CharacterAnimationObj(
                animationsLeft=animationsLeft,
                animationsRight=animationsRight
            )

            # update head, bodies of stickfigure enemies
            if characterTextureType is CharacterTextureType.stickfigure:
                head = self.getRandomHead()
                body = self.getRandomBody()
                self.updateAllAnimations(characterAnimationObj, 1, 0, head, skip=CharacterAnimationType.dying)
                self.updateAllAnimations(characterAnimationObj, 1, 1, body)

            self.characterAnimationObjs[characterTextureType] = characterAnimationObj


    def getAnimation(
        self,
        characterTextureType,
        characterAnimationType,
        direction,
        subtype=0
    ):
        # delay loading till first invocation, as this is a singleton, and we dont 
        # wanna load stuff when its first included
        if not self.isLoaded:
            self.init()
            self.isLoaded = True

        characterAnimationObj = self.characterAnimationObjs[characterTextureType]

        if direction is Direction.left:
            if subtype >= len(characterAnimationObj.animationsLeft[characterAnimationType]):
                logger.error("Animation {} tried to access subtype no {} of animation with len {}"
                    .format(characterAnimationType, subtype, len(characterAnimationObj.animationsLeft[characterAnimationType])))
            return characterAnimationObj.animationsLeft[characterAnimationType][subtype]
        else:
            if subtype >= len(characterAnimationObj.animationsRight[characterAnimationType]):
                logger.error("Animation {} Tried to access subtype no {} of animation with len {}"
                    .format(characterAnimationType, subtype, len(characterAnimationObj.animationsRight[characterAnimationType])))
            return characterAnimationObj.animationsRight[characterAnimationType][subtype]


    def updateAllAnimations(self, characterAnimationObj, x, y, char, skip=None):
        self.updateAllAnimationsIn(x, y, char, characterAnimationObj.animationsLeft, skip)
        self.updateAllAnimationsIn(x, y, char, characterAnimationObj.animationsRight, skip)


    def updateAllAnimationsIn(self, x, y, char, animations, skip=None):
        for key in animations:
            if key == skip:
                continue

            for animation in animations[key]:
                for animation in animation.arr:
                    animation[y][x] = char


    def createAnimations(self, animationType, characterTextureType, direction):
        animations = []

        if animationType is CharacterAnimationType.dying:
            n = 0
            while n < 2:
                animation = self.fileTextureLoader.readAnimation(
                    characterTextureType=characterTextureType,
                    characterAnimationType=animationType)
                if animation.originalDirection is not direction:
                    Utility.mirrorFrames(animation.arr)

                animations.append(animation)
                n += 1
        else:
            animation = self.fileTextureLoader.readAnimation(
                characterTextureType=characterTextureType,
                characterAnimationType=animationType)
            if animation.originalDirection is not direction:
                Utility.mirrorFrames(animation.arr)
            animations.append(animation)

        for animation in animations:
            Utility.checkAnimation(animation, animationType, characterTextureType)

        return animations


    def getRandomHead(self):
        return random.choice(['^', 'o', 'O', 'v', 'V'])


    def getRandomBody(self):
        return random.choice(['X', 'o', 'O', 'v', 'V', 'M', 'm'])



characterAnimationManager = CharacterAnimationManager()
