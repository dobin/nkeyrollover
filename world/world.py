
from sprite.specksprite import SpeckSprite

class World(object): 
    def __init__(self, win): 
        self.win = win
        self.sprites = []


    def makeExplode(self, sprite, data):
        frame = sprite.getCurrentFrameCopy()

        columnCount = len(frame)
        for (y, rows) in enumerate(frame):
            rowCnt = len(rows)

            for (x, column) in enumerate(rows):
                if column is not '':
                    movementX = 0
                    movementY = 0

                    if y == 0:
                        movementY = -1
                    if x == 0: 
                        movementX = -1

                    if y == columnCount:
                        movementY = 1
                    if x == rowCnt: 
                        movementX = 1

                    speckSprite = SpeckSprite(
                        column, 
                        sprite.x + x,
                        sprite.y + y,
                        movementX, 
                        movementY)
                    self.addSprite(speckSprite)
        

    def addSprite(self, sprite): 
        pass


    def draw(self):
        pass


    def advance(self):
        pass