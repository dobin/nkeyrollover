import logging

from entities.direction import Direction
from .characteranimationtype import CharacterAnimationType
from .texture import Texture

logger = logging.getLogger(__name__)


class CharacterTextureManager(object): 
    def __init__(self):
        self.animationsLeft = {}
        self.animationsRight = {}

        for animationType in CharacterAnimationType:
            self.animationsLeft[animationType] = self.createTexture(animationType, Direction.left)

        for animationType in CharacterAnimationType:
            self.animationsRight[animationType] = self.createTexture(animationType, Direction.right)


    def getTexture(self, characterAnimationType, direction, subtype=0):
        if direction is Direction.left:
            if subtype >= len(self.animationsLeft[characterAnimationType]):
                logging.error("Tried to access subtype no {} of animation with len {}".format(subtype, len(self.animationsLeft[characterAnimationType])))
            return self.animationsLeft[characterAnimationType][subtype]
        else: 
            if subtype >= len(self.animationsRight[characterAnimationType]):
                logging.error("Tried to access subtype no {} of animation with len {}".format(subtype, len(self.animationsRight[characterAnimationType])))
            return self.animationsRight[characterAnimationType][subtype]


    def createTexture(self, animationType, direction):
        textures = []
        
        if animationType is CharacterAnimationType.standing:
            texture = Texture()
            texture.width = 3
            texture.height = 3
            texture.frameCount = 1
            texture.frameTime = []
            texture.advanceByStep = False
            texture.endless = True

            texture.arr = [
                [
                    [ '', 'o', '' ],
                    [ '/', '|', '\\'],
                    [ '/', '', '\\']
                ]
            ]
            textures.append(texture)

        if animationType is CharacterAnimationType.walking:
            texture = Texture()
            texture.width = 3
            texture.height = 3
            texture.frameCount = 2
            texture.frameTime = [
                0.01, 
                0.01
            ]
            texture.endless = True
            texture.advanceByStep = True

            if direction is Direction.right:
                texture.arr = [
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
                texture.arr = [
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
            textures.append(texture)            

        if animationType is CharacterAnimationType.hitting:
            texture = Texture()
            texture.width = 3
            texture.height = 3
            texture.endless = False
            texture.frameCount = 2
            texture.frameTime = [
                1.0, 
                1.0
            ]
            texture.advanceByStep = False

            if direction is Direction.right:
                texture.arr = [
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
                texture.arr = [
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
            textures.append(texture)

        if animationType is CharacterAnimationType.shrugging:
            texture = Texture()
            texture.width = 3
            texture.height = 3
            texture.frameCount = 2
            texture.endless = True
            texture.advanceByStep = False

            texture.frameTime = [
                0.1,
                0.5
            ]

            texture.arr = [
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
            textures.append(texture)


        if animationType is CharacterAnimationType.dying:
            n = 0
            while n < 2:
                texture = Texture()
                texture.width = 3
                texture.height = 3
                texture.frameCount = 1
                texture.frameTime = []
                texture.advanceByStep = False
                texture.frameTime = None
                texture.endless = True

                if n == 0:
                    texture.arr = [
                        [
                            [ '', 'x', '' ],
                            [ '/', '|', '\\'],
                            [ '/', '', '\\']
                        ]
                    ]
                elif n == 1: 
                    texture.arr = [
                        [
                            [ '', 'X', '' ],
                            [ '/', '|', '\\'],
                            [ '/', '', '\\']
                        ]
                    ]
                    
                textures.append(texture)
                n += 1


        return textures
