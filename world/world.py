import logging
import random
import curses 


from sprite.coordinates import Coordinates
from texture.specktexture import SpeckTexture
from sprite.direction import Direction
from entities.player.player import Player
from world.director import Director
from config import Config
from entities.entity import Entity
from entities.entitytype import EntityType
from world.particleemiter import ParticleEmiter
from sprite.sprite import Sprite
from .map import Map
from .viewport import Viewport

logger = logging.getLogger(__name__)


class World(object): 
    """The game world in which all game object live"""

    def __init__(self, win): 
        self.win = win
        self.textures = []
        self.viewport :Viewport =Viewport(win=win, world=self)
        self.worldSprite :Sprite = Sprite(viewport=self.viewport, parentSprite=None)
        self.player :Player = Player(
            viewport=self.viewport, 
            parentEntity=self.worldSprite, 
            world=self)
        self.director :Director = Director(self.viewport, self)
        self.director.init()
        self.particleEmiter :ParticleEmiter = ParticleEmiter(viewport=self.viewport)
        self.map :Map = Map(win=win, world=self)
        
        self.pause :bool = False
        self.gameRunning :bool = True
        self.gameTime :float =0.0


    def togglePause(self): 
        self.pause = not self.pause


    def quitGame(self): 
        self.gameRunning = False


    def draw(self):
        # order here is Z axis
        self.map.draw()
        self.director.drawEnemies()
        self.player.draw()

        self.player.drawCharacterAttack()
        self.director.drawEnemyAttacks()
        self.particleEmiter.draw()

        for texture in self.textures: 
            texture.draw(self.viewport)

        if self.pause: 
            self.win.addstr(12, 40, "Paused", curses.color_pair(7))


    def getGameTime(self): 
        return self.gameTime


    def advance(self, deltaTime):
        if self.pause:
            return

        self.gameTime += deltaTime
        self.map.advance()
        self.player.advance(deltaTime)
        self.director.advanceEnemies(deltaTime)
        self.particleEmiter.advance(deltaTime)

        for texture in self.textures: 
            texture.advance(deltaTime)
            if not texture.isActive(): 
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
