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

        if characterType is CharacterType.stickfigure or characterType is CharacterType.player:
            for animationType in CharacterAnimationType:
                self.animationsLeft[animationType] = self.createAnimationStickfigure(
                    animationType, Direction.left)
            for animationType in CharacterAnimationType:
                self.animationsRight[animationType] = self.createAnimationStickfigure(
                    animationType, Direction.right)

            if head is not None: 
                self.updateAllAnimations(1, 0, head, skip=CharacterAnimationType.dying)

            if body is not None:
                self.updateAllAnimations(1, 1, body)

        elif characterType is CharacterType.cow:
            for animationType in CharacterAnimationType:
                self.animationsLeft[animationType] = self.createAnimationCow(
                    animationType, Direction.left)
            for animationType in CharacterAnimationType:
                self.animationsRight[animationType] = self.createAnimationCow(
                    animationType, Direction.right)
                    
        else:
            logger.error("Unknown character type: " + str(characterType))


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


    def createAnimationStickfigure(self, animationType, direction):
        animations = []
        if self.characterType is CharacterType.player:
            color = ColorPalette.getColorByColor(Color.brightwhite)
        else: 
            color = ColorPalette.getColorByColor(Color.white)
        
        if animationType is CharacterAnimationType.standing:
            animation = Animation()
            animation.width = 3
            animation.height = 3
            animation.frameCount = 1
            animation.frameTime = []
            animation.advanceByStep = False
            animation.endless = True
            animation.frameColors = [
                color,
            ]
            animation.arr = [
                [
                    [ '', 'o', '' ],
                    [ '/', '|', '\\'],
                    [ '/', '', '\\']
                ]
            ]
            animations.append(animation)

        if animationType is CharacterAnimationType.walking:
            animation = Animation()
            animation.width = 3
            animation.height = 3
            animation.frameCount = 4
            animation.frameTime = None # by step
            animation.endless = True
            animation.advanceByStep = True
            animation.frameColors = [
                color,
                color,
                color,
                color,
            ]

            if direction is Direction.right:
                animation.arr = [
                    [
                        [ '', 'o', '' ],
                        [ '/', '|', '\\'],
                        [ '', '>', '\\']
                    ],
                    [
                        [ '', 'o', '' ],
                        [ '/', '|', '\\'],
                        [ '', '|', '\\']
                    ],
                    [
                        [ '', 'o', '' ],
                        [ '/', '|', '\\'],
                        [ '', '|', '>']
                    ],
                    [
                        [ '', 'o', '' ],
                        [ '/', '|', '\\'],
                        [ '/', '', '\\']
                    ]                    
                ]
            else: 
                animation.arr = [
                    [
                        [ '', 'o', '' ],
                        [ '/', '|', '\\'],
                        [ '/', '<', '']
                    ],
                    [
                        [ '', 'o', '' ],
                        [ '/', '|', '\\'],
                        [ '/', '|', '']
                    ],
                    [
                        [ '', 'o', '' ],
                        [ '/', '|', '\\'],
                        [ '<', '|', '']
                    ],
                    [
                        [ '', 'o', '' ],
                        [ '/', '|', '\\'],
                        [ '/', '', '\\']
                    ]
                ]
            animations.append(animation)            

        if animationType is CharacterAnimationType.hitting:
            animation = Animation()
            animation.width = 3
            animation.height = 3
            animation.endless = False
            animation.frameCount = 2
            animation.frameTime = [
                0.8, 
                0.2
            ]
            animation.frameColors = [
                color,
                color,
            ]            
            animation.advanceByStep = False

            if direction is Direction.right:
                animation.arr = [
                    [
                        [ '', 'o', '' ],
                        [ '/', '|', '+'],
                        [ '/', '', '\\']
                    ],
                    [
                        [ '', 'o', '' ],
                        [ '/', '|', '-'],
                        [ '/', '', '\\']
                    ]
                ]
            else: 
                animation.arr = [
                    [
                        [ '', 'o', '' ],
                        [ '+', '|', '\\'],
                        [ '/', '', '\\']
                    ],
                    [
                        [ '', 'o', '' ],
                        [ '-', '|', '\\'],
                        [ '/', '', '\\']
                    ]
                ]
            animations.append(animation)

        if animationType is CharacterAnimationType.shrugging:
            animation = Animation()
            animation.width = 3
            animation.height = 3
            animation.frameCount = 2
            animation.endless = True
            animation.advanceByStep = False
            animation.frameColors = [
                color,
                color,
            ]   
            animation.frameTime = [
                0.1,
                0.5
            ]

            animation.arr = [
                [
                    [ '', 'o', '' ],
                    [ '/', '|', '\\'],
                    [ '/', '', '\\']
                ],
                [
                    [ '', 'o', '' ],
                    [ '^', '|', '^'],
                    [ '/', '', '\\']
                ]                
            ]
            animations.append(animation)


        if animationType is CharacterAnimationType.dying:
            n = 0
            while n < 2:
                animation = Animation()
                animation.width = 3
                animation.height = 3
                animation.frameCount = 1
                animation.frameTime = []
                animation.advanceByStep = False
                animation.frameTime = None
                animation.endless = True
                animation.frameColors = [
                    ColorPalette.getColorByColor(Color.grey),
                ]   
                if n == 0:
                    animation.arr = [
                        [
                            [ '', 'x', '' ],
                            [ '/', '|', '\\'],
                            [ '/', '', '\\']
                        ]
                    ]
                elif n == 1: 
                    animation.arr = [
                        [
                            [ '', 'X', '' ],
                            [ '/', '|', '\\'],
                            [ '/', '', '\\']
                        ]
                    ]
                    
                animations.append(animation)
                n += 1


        if animationType is CharacterAnimationType.hitwindup:
            animation = Animation()
            animation.width = 3
            animation.height = 3
            animation.frameCount = 1
            animation.frameTime = []
            animation.advanceByStep = False
            animation.endless = True
            animation.frameColors = [
                color,
            ]   
            if direction is direction.right:
                animation.arr = [
                    [
                        [ '\\', 'o', '' ],
                        [ '', '|', '\\'],
                        [ '/', '', '\\']
                    ]
                ]
            else: 
                animation.arr = [
                    [
                        [ '', 'o', '/' ],
                        [ '/', '|', ''],
                        [ '/', '', '\\']
                    ]
                ]

            animations.append(animation)

        for animation in animations:
            Utility.checkAnimation(animation, animationType, self.characterType)

        return animations


    def createAnimationCow(self, animationType, direction):
        animations = []
        color = ColorPalette.getColorByColor(Color.white)

        if animationType is CharacterAnimationType.standing:
            animation = Animation()

            fileAnimation = self.fileTextureLoader.readAnimation(
                characterType=CharacterType.cow, characterAnimationType=animationType)

            animation.width = fileAnimation['width']
            animation.height = fileAnimation['height']
            animation.arr = fileAnimation['arr']
            if direction is Direction.left: 
                self.mirrorFrames(animation.arr)
            animation.frameCount = 1
            animation.frameTime = []
            animation.advanceByStep = False
            animation.endless = True
            animation.frameColors = [
                color,
            ]   
            animations.append(animation)

        if animationType is CharacterAnimationType.walking:
            animation = Animation()

            fileAnimation = self.fileTextureLoader.readAnimation(
                characterType=CharacterType.cow, characterAnimationType=animationType)

            animation.width = fileAnimation['width']
            animation.height = fileAnimation['height']
            animation.arr = fileAnimation['arr']
            if direction is Direction.left: 
                self.mirrorFrames(animation.arr)

            animation.frameCount = 2
            animation.frameColors = [
                color,
                color,
            ]               
            animation.frameTime = None
            animation.endless = True
            animation.advanceByStep = True

            animations.append(animation)

        if animationType is CharacterAnimationType.hitting:
            animation = Animation()

            fileAnimation = self.fileTextureLoader.readAnimation(
                characterType=CharacterType.cow, characterAnimationType=animationType)

            animation.width = fileAnimation['width']
            animation.height = fileAnimation['height']
            animation.arr = fileAnimation['arr']
            if direction is Direction.left: 
                self.mirrorFrames(animation.arr)

            animation.endless = False
            animation.frameCount = 2
            animation.frameTime = [
                0.8, 
                0.2
            ]
            animation.frameColors = [
                color,
                color,
            ]                     
            animation.advanceByStep = False

            animations.append(animation)

        if animationType is CharacterAnimationType.dying:
            animations = []
            animation = Animation()

            fileAnimation = self.fileTextureLoader.readAnimation(
                characterType=CharacterType.cow, characterAnimationType=animationType)

            animation.width = fileAnimation['width']
            animation.height = fileAnimation['height']
            animation.arr = fileAnimation['arr']
            if direction is Direction.left: 
                self.mirrorFrames(animation.arr)

            animation.frameCount = 1
            animation.frameColors = [
                color,
            ]                     
            animation.frameTime = []
            animation.advanceByStep = False
            animation.frameTime = None
            animation.endless = True

            animations.append(animation)
            animations.append(animation)

        if animationType is CharacterAnimationType.hitwindup:
            animation = Animation()

            fileAnimation = self.fileTextureLoader.readAnimation(
                characterType=CharacterType.cow, characterAnimationType=animationType)

            animation.width = fileAnimation['width']
            animation.height = fileAnimation['height']
            animation.arr = fileAnimation['arr']
            if direction is Direction.left: 
                self.mirrorFrames(animation.arr)

            animation.frameCount = 2
            animation.frameColors = [
                color,
                color,
            ]                     
            animation.frameTime = []
            animation.advanceByStep = False
            animation.endless = True

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

        else:
            return char
