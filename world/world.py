from sprite.specksprite import SpeckSprite
import logging
from entities.direction import Direction

logger = logging.getLogger(__name__)

class World(object): 
    def __init__(self, win): 
        self.win = win
        self.sprites = []


    def makeExplode(self, sprite, charDirection, data):
        frame = sprite.getCurrentFrameCopy()
        pos = sprite.getLocation()

        effect = 2

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

            speckSprite = SpeckSprite(
                char, 
                pos['x'] + x,
                pos['y'] + y,
                movementX, 
                movementY, 
                [ 10, 10, 10], 
                1)
            self.addSprite(speckSprite)

        # push away
        if effect == 2:
            if charDirection is Direction.right: 
                d = -1
            else: 
                d = 1

            speckSprite = SpeckSprite(
                char, 
                pos['x'] + x,
                pos['y'] + y,
                d * 2, 
                0, 
                [ 5, 10, 20, 40 ], 
                2 )
            self.addSprite(speckSprite)



    def addSprite(self, sprite): 
        self.sprites.append(sprite)


    def draw(self):
        for sprite in self.sprites: 
            sprite.draw(self.win)


    def advance(self):
        for sprite in self.sprites: 
            sprite.advance()

            if not sprite.isActive: 
                self.sprites.remove(sprite)