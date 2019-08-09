import logging

from entities.direction import Direction
from .characteranimationtype import CharacterAnimationType
from .animation import Animation

logger = logging.getLogger(__name__)


class CharacterAnimationManager(object): 
    def __init__(self, head=None, body=None):
        self.animationsLeft = {}
        self.animationsRight = {}

        for animationType in CharacterAnimationType:
            self.animationsLeft[animationType] = self.createAnimation(animationType, Direction.left)

        for animationType in CharacterAnimationType:
            self.animationsRight[animationType] = self.createAnimation(animationType, Direction.right)

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
                logging.error("Tried to access subtype no {} of animation with len {}".format(subtype, len(self.animationsLeft[characterAnimationType])))
            return self.animationsLeft[characterAnimationType][subtype]
        else: 
            if subtype >= len(self.animationsRight[characterAnimationType]):
                logging.error("Tried to access subtype no {} of animation with len {}".format(subtype, len(self.animationsRight[characterAnimationType])))
            return self.animationsRight[characterAnimationType][subtype]


    def createAnimation(self, animationType, direction):
        animations = []
        
        if animationType is CharacterAnimationType.standing:
            animation = Animation()
            animation.width = 3
            animation.height = 3
            animation.frameCount = 1
            animation.frameTime = []
            animation.advanceByStep = False
            animation.endless = True

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
            animation.frameCount = 2
            animation.frameTime = [
                0.01, 
                0.01
            ]
            animation.endless = True
            animation.advanceByStep = True

            if direction is Direction.right:
                animation.arr = [
                    [
                        [ '', 'O', '' ],
                        [ '/', '|', '\\'],
                        [ '', '|', '\\']
                    ],
                    [
                        [ '', 'o', '' ],
                        [ '/', '|', '\\'],
                        [ '/', '|', '']
                    ]                
                ]
            else: 
                animation.arr = [
                    [
                        [ '', 'o', '' ],
                        [ '/', '|', '\\'],
                        [ '/', '|', '']
                    ],
                    [
                        [ '', 'O', '' ],
                        [ '/', '|', '\\'],
                        [ '', '|', '\\']
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
                1.0, 
                1.0
            ]
            animation.advanceByStep = False

            if direction is Direction.right:
                animation.arr = [
                    [
                        [ '', 'o', '' ],
                        [ '/', '|', '-'],
                        [ '/', '', '\\']
                    ],
                    [
                        [ '', 'o', '' ],
                        [ '/', '|', '+'],
                        [ '/', '', '\\']
                    ]
                ]
            else: 
                animation.arr = [
                    [
                        [ '', 'o', '' ],
                        [ '-', '|', '\\'],
                        [ '/', '', '\\']
                    ],
                    [
                        [ '', 'o', '' ],
                        [ '+', '|', '\\'],
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

        return animations
