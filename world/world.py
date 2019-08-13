import logging
import random
import curses 

from sprite.coordinates import Coordinates
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
from .textureemiter import TextureEmiter

logger = logging.getLogger(__name__)


class World(object): 
    """The game world in which all game object live"""

    def __init__(self, win): 
        self.win = win
        self.viewport :Viewport =Viewport(win=win, world=self)
        self.worldSprite :Sprite = Sprite(viewport=self.viewport, parentSprite=None)
        self.player :Player = Player(
            viewport=self.viewport, 
            parentEntity=self.worldSprite, 
            world=self)
        self.director :Director = Director(self.viewport, self)
        self.director.init()
        self.particleEmiter :ParticleEmiter = ParticleEmiter(viewport=self.viewport)
        self.textureEmiter :TextureEmiter = TextureEmiter(viewport=self.viewport)
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
        self.textureEmiter.draw()

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
        self.textureEmiter.advance(deltaTime)
        self.director.worldUpdate()


    def getPlayer(self):
        return self.player

