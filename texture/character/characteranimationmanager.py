import logging

from sprite.direction import Direction
from texture.character.characteranimationtype import CharacterAnimationType
from texture.animation import Animation
from .charactertype import CharacterType
from texture.filetextureloader import FileTextureLoader
from utilities.color import Color
from utilities.colorpalette import ColorPalette
from utilities.utilities import Utility

logger = logging.getLogger(__name__)


class CharacterAnimationManager(object):
    def __init__(
        self, characterType :CharacterType, head=None, body=None,
    ):
        self.animationsLeft = {}
        self.animationsRight = {}
        self.fileTextureLoader = FileTextureLoader()
        self.characterType = characterType

        for animationType in CharacterAnimationType:
            self.animationsLeft[animationType] = self.createAnimations(
                animationType, characterType, Direction.left)
        for animationType in CharacterAnimationType:
            self.animationsRight[animationType] = self.createAnimations(
                animationType, characterType, Direction.right)

        # update head, bodies of stickfigure enemies
        if characterType is CharacterType.stickfigure:
            if head is not None:
                self.updateAllAnimations(1, 0, head, skip=CharacterAnimationType.dying)

            if body is not None:
                self.updateAllAnimations(1, 1, body)


    def updateAllAnimations(self, x, y, char, skip=None):
        self.updateAllAnimationsIn(x, y, char, self.animationsLeft, skip)
        self.updateAllAnimationsIn(x, y, char, self.animationsRight, skip)


    def updateAllAnimationsIn(self, x, y, char, animations, skip=None):
        for key in animations:
            if key == skip:
                continue

            for animation in animations[key]:
                for animation in animation.arr:
                    animation[y][x] = char


    def getAnimation(self, characterAnimationType, direction, subtype=0):
        if direction is Direction.left:
            if subtype >= len(self.animationsLeft[characterAnimationType]):
                logger.error("Animation {} tried to access subtype no {} of animation with len {}"
                    .format(characterAnimationType, subtype, len(self.animationsLeft[characterAnimationType])))
            return self.animationsLeft[characterAnimationType][subtype]
        else:
            if subtype >= len(self.animationsRight[characterAnimationType]):
                logger.error("Animation {} Tried to access subtype no {} of animation with len {}"
                    .format(characterAnimationType, subtype, len(self.animationsRight[characterAnimationType])))
            return self.animationsRight[characterAnimationType][subtype]


    def createAnimations(self, animationType, characterType, direction):
        animations = []

        if animationType is CharacterAnimationType.dying:
            n = 0
            while n < 2:
                animation = self.fileTextureLoader.readAnimation(
                    characterType=characterType,
                    characterAnimationType=animationType)
                if direction is Direction.left:
                    self.mirrorFrames(animation.arr)

                animations.append(animation)
                n += 1
        else:
            animation = self.fileTextureLoader.readAnimation(
                characterType=characterType,
                characterAnimationType=animationType)
            if direction is Direction.left:
                self.mirrorFrames(animation.arr)                
            animations.append(animation)

        for animation in animations:
            Utility.checkAnimation(animation, animationType, self.characterType)

        return animations


    def mirrorFrames(self, arr):
        for a in arr:
            for line in a:
                n = 0
                while n < len(line) / 2:
                    cl = line[n]
                    cr = line[ len(line) - 1 - n ]

                    cl = self.swapChar(cl)
                    cr = self.swapChar(cr)

                    line[n] = cr
                    line[ len(line) - 1 - n ] = cl
                    n += 1


    def swapChar(self, char):
        if char == ')':
            return '('
        elif char == '(':
            return ')'

        elif char == '/':
            return '\\'
        elif char == '\\':
            return '/'

        elif char == '`':
            return '\''
        elif char == '\'':
            return '`'

        elif char == '>':
            return '<'
        elif char == '<':
            return '>'

        else:
            return char
