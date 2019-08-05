import logging

from entities.direction import Direction
from .phenomenatype import PhenomenaType
from .texture import Texture

logger = logging.getLogger(__name__)


class PhenomenaTextureManager(object): 
    def __init__(self):
        self.animationsLeft = {}
        self.animationsRight = {}

        for phenomenatype in PhenomenaType:
            self.animationsLeft[phenomenatype] = self.createTexture(phenomenatype, Direction.left)

        for phenomenatype in PhenomenaType:
            self.animationsRight[phenomenatype] = self.createTexture(phenomenatype, Direction.right)


    def getTexture(self, phenomenaType, direction): 
        if direction is Direction.left:
            return self.animationsLeft[phenomenaType]
        else: 
            return self.animationsRight[phenomenaType]


    def createTexture(self, phenomenaType, direction):
        texture = Texture()

        if phenomenaType is PhenomenaType.hit:
            texture.width = 1
            texture.height = 1
            texture.frameCount = 3
            texture.endless = False
            texture.advanceByStep = False
            
            texture.frameTime = [
                0.1,
                0.1,
                0.1
            ]

            texture.arr = [
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
            texture.width = 2
            texture.height = 2
            texture.frameCount = 3
            texture.endless = False
            texture.advanceByStep = False
            
            texture.frameTime = [
                0.1,
                0.1,
                0.1
            ]

            texture.arr = [
                [
                    [ 'O', 'O' ],
                ],
                [
                    [ 'O', 'O' ],
                ],
                [
                    [ 'O', 'O' ],
                ]                                
            ]

        if phenomenaType is PhenomenaType.hitLine:
            texture.width = 2
            texture.height = 2
            texture.frameCount = 3
            texture.endless = False
            texture.advanceByStep = False
            
            texture.frameTime = [
                0.1,
                0.1,
                0.1
            ]

            texture.arr = [
                [
                    [ '.', '', ''],
                ],
                [
                    [ '.', 'o', ''],
                ],
                [
                    [ '.', 'o', 'O'],
                ]                                
            ]

        if phenomenaType is PhenomenaType.roflcopter: 
            texture.width = 3
            texture.height = 3
            texture.frameCount = 2
            texture.endless = True
            texture.advanceByStep = False

            texture.frameTime = [
                0.2,
                0.2
            ]

            t = self.readfile('textures/roflcopter.ascii')
            texture.width = t['width']
            texture.height = t['height']
            texture.arr = t['arr']

        return texture


    def readfile(self, filename):
        lineList = [line.rstrip('\n') for line in open('texture/textures/roflcopter.ascii')]
        res = []

        # find longest line to make texture
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
            
        texture = {
            'arr': res,
            'width': maxWidth, 
            'height': maxHeight,
        }

        logging.info("Loaded {}: width={} height={} animations={}".format(filename, maxWidth, maxHeight, len(res)))
        return texture
