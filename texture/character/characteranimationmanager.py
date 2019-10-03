import logging
import random
import os

from common.direction import Direction
from texture.character.characteranimationtype import CharacterAnimationType
from texture.character.charactertexturetype import CharacterTextureType
from utilities.utilities import Utility
from texture.animation import Animation
from utilities.colorpalette import ColorPalette
from utilities.color import Color
from texture.texturehelper import TextureHelper

logger = logging.getLogger(__name__)


class CharacterAnimationObj(object):
    def __init__(self, animationsLeft, animationsRight):
        self.animationsLeft = animationsLeft
        self.animationsRight = animationsRight


class CharacterAnimationManager(object):
    def __init__(self):
        self.characterAnimationObjs = {}


    def loadFiles(self):
        self.characterAnimationObjs = {}

        for characterTextureType in CharacterTextureType:
            animationsLeft = {}
            animationsRight = {}

            for animationType in CharacterAnimationType:
                animationsLeft[animationType] = self.createAnimations(
                    animationType, characterTextureType, Direction.left)
            for animationType in CharacterAnimationType:
                animationsRight[animationType] = self.createAnimations(
                    animationType, characterTextureType, Direction.right)

            # fix dragon atm
            if characterTextureType is CharacterTextureType.dragon:
                self.fixInsideWhitespace(animationsLeft)
                self.fixInsideWhitespace(animationsRight)

            characterAnimationObj = CharacterAnimationObj(
                animationsLeft=animationsLeft,
                animationsRight=animationsRight
            )

            # update head, bodies of stickfigure enemies
            if characterTextureType is CharacterTextureType.stickfigure:
                head = self.getRandomHead()
                body = self.getRandomBody()
                self.updateAllAnimations(
                    characterAnimationObj,
                    1,
                    0,
                    head,
                    skip=CharacterAnimationType.dying)
                self.updateAllAnimations(characterAnimationObj, 1, 1, body)

            self.characterAnimationObjs[characterTextureType] = characterAnimationObj


    def getAnimation(
        self,
        characterTextureType,
        characterAnimationType,
        direction,
        subtype=0
    ):
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


    def fixInsideWhitespace(self, animations):
        for key in animations:
            for animation in animations[key]:
                for a in animation.arr:
                    for line in a:
                        self.fixLineWhitespace(line)


    def fixLineWhitespace(self, line):
        left = 0
        r = 0

        n = 0
        while n < len(line):
            if line[n] != '':
                left = n
                break
            n += 1

        n = len(line) - 1
        while n > 0:
            if line[n] != '':
                r = n
                break
            n -= 1

        n = left
        while n < r:
            if line[n] == '':
                line[n] = ' '
            n += 1


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
                animation = self.readAnimation(
                    characterTextureType=characterTextureType,
                    characterAnimationType=animationType)
                if animation.originalDirection is not direction:
                    Utility.mirrorFrames(animation.arr)

                animations.append(animation)
                n += 1
        else:
            animation = self.readAnimation(
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


    def readAnimation(
        self, characterTextureType :CharacterTextureType,
        characterAnimationType :CharacterAnimationType,
    ) -> Animation:
        ct = characterTextureType.name
        cat = characterAnimationType.name
        filename = "data/textures/character/{}/{}_{}.ascii".format(ct, ct, cat)

        # return fake animation if file does not exist(yet)
        if not os.path.isfile(filename):
            animation = Animation()
            animation.arr = [[['X', 'X', 'X'], ['X', 'X', 'X'], ['X', 'X', 'X']]]
            animation.height = 3
            animation.width = 3
            animation.frameCount = 1
            animation.frameTime = [10.0]
            animation.frameColors = [ColorPalette.getColorByColor(Color.white)]
            logger.debug("Could not find animation {}, replacing".format(
                filename
            ))
            return animation

        animation = TextureHelper.readAnimationFile(filename)
        animation.name = "{}_{}".format(ct, cat)

        filenameYaml = "data/textures/character/{}/{}_{}.yaml".format(ct, ct, cat)
        TextureHelper.loadYamlIntoAnimation(filenameYaml, animation)

        return animation
