import logging
import random
import curses 

from sprite.specksprite import SpeckSprite
from entities.direction import Direction
from entities.player.player import Player
from director import Director
from config import Config

logger = logging.getLogger(__name__)


class World(object): 
    def __init__(self, win): 
        self.win = win
        self.sprites = []

        self.player = Player(
            win=self.win, 
            parent=None, 
            spawnBoundaries={ 'max_y': Config.columns, 'max_x': Config.rows }, 
            world=self)
        self.director = Director(self.win, self)


    def drawWorld(self): 
        self.win.move(8, 1)
        self.win.hline('-', 78)
        self.drawDiagonal(8, 45, 15)

    def drawDiagonal(self, x, y, len):
        n = 0
        while n != len: 
            x += 1
            y -= 1

            n += 1

            self.win.addstr(
                x, 
                y,
                '/', 
                curses.color_pair(7))

    def draw(self):
        # order here is Z axis
        self.drawWorld()
        self.director.drawEnemies()
        self.player.draw()

        for sprite in self.sprites: 
            sprite.draw(self.win)



    def advance(self, deltaTime):
        self.player.advance(deltaTime)
        self.director.advanceEnemies(deltaTime)

        for sprite in self.sprites: 
            sprite.advance(deltaTime)

            if not sprite.isActive: 
                self.sprites.remove(sprite)

        self.director.worldUpdate()


    def getPlayer(self):
        return self.player


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

            speckSprite = SpeckSprite(
                char, 
                pos['x'] + x,
                pos['y'] + y,
                movementX, 
                movementY, 
                [ 0.1, 0.1, 0.1 ], 
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
                [ 0.05, 0.1, 0.2, 0.4 ], 
                2 )
            self.addSprite(speckSprite)



    def addSprite(self, sprite): 
        self.sprites.append(sprite)
