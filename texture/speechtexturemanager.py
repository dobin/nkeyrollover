from entities.direction import Direction
from .texture import Texture


class SpeechTextureManager(object):
    def __init__(self):
        pass

    def getTexture(self, displayText=None, direction=Direction.right): 
        texture = Texture()

        texture.width = 5
        texture.height = 4
        texture.frameCount = 1
        texture.frameTime = [
            1.5,
        ]
        texture.endless = False
        texture.advanceByStep = False

        texture.arr = [
            [
                [ '.', '-', '-', '-', '.' ],
                [ '|', 'h', 'o', 'i', '|' ],
                [ '`', '^', '-', '-', '\'' ],
                [ '/', ' ', ' ', ' ', ' ' ],                        
            ]
        ]

        return texture
