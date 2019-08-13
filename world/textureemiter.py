import random

from world.viewport import Viewport
from sprite.coordinates import Coordinates
from texture.specktexture import SpeckTexture
from sprite.direction import Direction


class TextureEmiter(object):
    def __init__(self, viewport :Viewport):
        self.viewport :Viewport = viewport
        self.textures = []


    def showCharAtPos(self, char, timeout, coordinate):
        speckTexture = SpeckTexture(
            char=char, 
            coordinate=coordinate,
            movementX=0, 
            movementY=0, 
            timeArr=[ timeout ], 
            effect=None)
        self.addTexture(speckTexture)


    def makeExplode(self, sprite, charDirection, data):
        frame = sprite.getCurrentFrameCopy()
        pos = sprite.getLocation()

        effect = random.randint(1, 2)

        columnCount = len(frame)
        for (y, rows) in enumerate(frame):
            rowCnt = len(rows)

            for (x, column) in enumerate(rows):
                if column is not '':
                    self.makeEffect(effect, pos, x, y, column, columnCount, rowCnt, charDirection)

        
    def makeEffect(self, effect, pos, x, y, char, columnCount, rowCnt, charDirection): 
        # explode
        if effect == 1: 
            movementX = 0
            movementY = 0

            if y == 0:
                movementY = -1
            if x == 0: 
                movementX = -1

            if y == columnCount - 1:
                movementY = 1
            if x == rowCnt - 1: 
                movementX = 1

            c = Coordinates(
                x = pos.x + x,
                y = pos.y + y,
            )

            speckTexture = SpeckTexture(
                char, 
                c,
                movementX, 
                movementY, 
                [ 0.1, 0.1, 0.1 ], 
                1)
            self.addTexture(speckTexture)

        # push away
        if effect == 2:
            if charDirection is Direction.right: 
                d = -1
            else: 
                d = 1

            c = Coordinates(
                x = pos.x + x,
                y = pos.y + y,
            )

            speckTexture = SpeckTexture(
                char, 
                c,
                d * 2, 
                0, 
                [ 0.05, 0.1, 0.2, 0.4 ], 
                2 )
            self.addTexture(speckTexture)


    def addTexture(self, sprite): 
        self.textures.append(sprite)


    def draw(self): 
        for texture in self.textures: 
            texture.draw(self.viewport)


    def advance(self, deltaTime :float):
        for texture in self.textures: 
            texture.advance(deltaTime)
            if not texture.isActive(): 
                self.textures.remove(texture)