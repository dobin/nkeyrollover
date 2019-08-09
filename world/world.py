import logging
import random
import curses 


from sprite.coordinates import Coordinates
from sprite.specktexture import SpeckTexture
from entities.direction import Direction
from entities.player.player import Player
from director import Director
from config import Config
from entities.entity import Entity
from entities.entitytype import EntityType
from world.particleemiter import ParticleEmiter
from sprite.sprite import Sprite

logger = logging.getLogger(__name__)


class World(object): 
    def __init__(self, win): 
        self.win = win
        self.textures = []

        self.worldSprite = Sprite(win=self.win, parentSprite=None)
        self.player = Player(
            win=self.win, 
            parentEntity=self.worldSprite, 
            spawnBoundaries={ 'max_y': Config.columns, 'max_x': Config.rows }, 
            world=self)

        self.director = Director(self.win, self)
        self.director.init()
        self.particleEmiter = ParticleEmiter(self.win)

        self.pause = False
        self.gameRunning = True


    def togglePause(self): 
        self.pause = not self.pause

    def quitGame(self): 
        self.gameRunning = False


    def drawWorld(self): 
        self.win.move(Config.areaMoveable['miny'], Config.areaMoveable['minx'])
        self.win.hline('-', Config.columns - 2)
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

        self.player.drawCharacterAttack()
        self.director.drawEnemyAttacks()
        self.particleEmiter.draw()

        for texture in self.textures: 
            texture.draw(self.win)

        if self.pause: 
            self.win.addstr(12, 40, "Paused", curses.color_pair(7))


    def advance(self, deltaTime):
        if self.pause:
            return

        self.player.advance(deltaTime)
        self.director.advanceEnemies(deltaTime)
        self.particleEmiter.advance(deltaTime)

        for texture in self.textures: 
            texture.advance(deltaTime)

            if not texture.isActive: 
                self.textures.remove(texture)

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
