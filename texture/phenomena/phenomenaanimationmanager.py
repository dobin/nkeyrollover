import logging

from sprite.direction import Direction
from texture.phenomena.phenomenatype import PhenomenaType
from texture.animation import Animation
from texture.filetextureloader import FileTextureLoader

logger = logging.getLogger("phenomentaanimationmanager")


class PhenomenaAnimationManager(object): 
    def __init__(self):
        self.animationsLeft = {}
        self.animationsRight = {}
        self.fileTextureLoader = FileTextureLoader()

        for phenomenatype in PhenomenaType:
            self.animationsLeft[phenomenatype] = self.createAnimation(phenomenatype, Direction.left)

        for phenomenatype in PhenomenaType:
            self.animationsRight[phenomenatype] = self.createAnimation(phenomenatype, Direction.right)


    def getAnimation(self, phenomenaType, direction): 
        if direction is Direction.left:
            return self.animationsLeft[phenomenaType]
        else: 
            return self.animationsRight[phenomenaType]


    def createAnimation(self, phenomenaType, direction):
        animation = Animation()

        if phenomenaType is PhenomenaType.hit:
            animation.width = 1
            animation.height = 1
            animation.frameCount = 3
            animation.endless = False
            animation.advanceByStep = False
            
            animation.frameTime = [
                0.1,
                0.1,
                0.1
            ]

            animation.arr = [
                [
                    [ 'O', ],
                ],
                [
                    [ 'o', ],
                ],
                [
                    [ '.', ],
                ]                                
            ]

        if phenomenaType is PhenomenaType.hitSquare:
            animation.width = 2
            animation.height = 2
            animation.frameCount = 3
            animation.endless = False
            animation.advanceByStep = False
            
            animation.frameTime = [
                0.1,
                0.1,
                0.1
            ]

            animation.arr = [
                [
                    [ 'O', 'O' ],
                    [ 'O', 'O' ],
                ],
                [
                    [ 'o', 'o' ],
                    [ 'o', 'o' ],
                ],
                [
                    [ '.', '.' ],
                    [ '.', '.' ],
                ]
            ]

        if phenomenaType is PhenomenaType.hitLine:
            animation.width = 4
            animation.height = 1
            animation.frameCount = 3
            animation.endless = False
            animation.advanceByStep = False
            
            animation.frameTime = [
                0.1,
                0.1,
                0.1, 
                0.1
            ]

            if direction is Direction.right:
                animation.arr = [
                    [
                        [ '.', '', '', ''],
                    ],
                    [
                        [ '.', 'o', '', ''],
                    ],
                    [
                        [ '.', 'o', 'O', 'O'],
                    ]                                
                ]
            else:
                animation.arr = [
                    [
                        [ '', '', '', '.'],
                    ],
                    [
                        [ '', '', 'o', '.'],
                    ],
                    [
                        [ 'O', 'O', 'o', '.'],
                    ]                                
                ]

        if phenomenaType is PhenomenaType.roflcopter: 
            animation.frameCount = 2
            animation.endless = True
            animation.advanceByStep = False

            animation.frameTime = [
                0.2,
                0.2
            ]

            t = self.fileTextureLoader.readAnimationFile('texture/textures/roflcopter.ascii')
            animation.width = t['width']
            animation.height = t['height']
            animation.arr = t['arr']

        if phenomenaType is PhenomenaType.intro: 
            animation.frameCount = 2
            animation.endless = True
            animation.advanceByStep = False

            animation.frameTime = [
                0.1,
                0.5,
            ]

            t = self.fileTextureLoader.readAnimationFile('texture/textures/intro.ascii')
            animation.width = t['width']
            animation.height = t['height']
            animation.arr = t['arr']

        return animation

