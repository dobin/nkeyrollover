import logging

from entities.direction import Direction
from .phenomenatype import PhenomenaType
from .animation import Animation

logger = logging.getLogger(__name__)


class PhenomenaAnimationManager(object): 
    def __init__(self):
        self.animationsLeft = {}
        self.animationsRight = {}

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
                    [ 'O', 'O' ],
                    [ 'O', 'O' ],
                ],
                [
                    [ 'O', 'O' ],
                    [ 'O', 'O' ],
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
            animation.width = 3
            animation.height = 3
            animation.frameCount = 2
            animation.endless = True
            animation.advanceByStep = False

            animation.frameTime = [
                0.2,
                0.2
            ]

            t = self.readfile('animations/roflcopter.ascii')
            animation.width = t['width']
            animation.height = t['height']
            animation.arr = t['arr']

        return animation


    def readfile(self, filename):
        lineList = [line.rstrip('\n') for line in open('texture/textures/roflcopter.ascii')]
        res = []

        # find longest line to make animation
        maxWidth = 0
        for line in lineList: 
            if len(line) > maxWidth: 
                maxWidth = len(line)


        maxHeight = 0
        tmp = []
        for line in lineList: 
            if line == '': 
                res.append(tmp)
                if len(tmp) > maxHeight: 
                    maxHeight = len(tmp)
                tmp = []
            else: 
                line += ' ' * (maxWidth - len(line))
                tmp.append(list(line))
        res.append(tmp)
            
        d = {
            'arr': res,
            'width': maxWidth, 
            'height': maxHeight,
        }

        logging.info("Loaded {}: width={} height={} animations={}".format(filename, maxWidth, maxHeight, len(res)))
        return d
