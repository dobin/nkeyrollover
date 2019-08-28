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

import esper
from system.advanceable import Advanceable, AdvanceableProcessor
from system.renderable import Renderable, RenderableProcessor

logger = logging.getLogger(__name__)


class World(object): 
    """The game world in which all game object live"""

    def __init__(self, win):
        self.esperWorld = esper.World()
        self.win = win
        self.viewport :Viewport =Viewport(win=win, world=self)
        self.worldSprite :Sprite = Sprite(viewport=self.viewport, parentSprite=None)
        
        # Player
        player :Player = Player(
            viewport=self.viewport, 
            parentEntity=self.worldSprite, 
            world=self)
        self.player = self.esperWorld.create_entity()
        self.esperWorld.add_component(self.player, Renderable(r=player))
        self.esperWorld.add_component(self.player, Advanceable(r=player))
        self.playerObj = player

        # /Player

        self.director :Director = Director(self.viewport, self)
        self.director.init()
        self.particleEmiter :ParticleEmiter = ParticleEmiter(viewport=self.viewport)
        self.textureEmiter :TextureEmiter = TextureEmiter(viewport=self.viewport)
        self.map :Map = Map(viewport=self.viewport, world=self)
        
        self.pause :bool = False
        self.gameRunning :bool = True
        self.gameTime :float =0.0
        self.showStats = False
        self.showEnemyWanderDestination = False

        renderableProcessor = RenderableProcessor()
        advanceableProcessor = AdvanceableProcessor()
        self.esperWorld.add_processor(renderableProcessor)
        self.esperWorld.add_processor(advanceableProcessor)        


    def togglePause(self): 
        self.pause = not self.pause


    def toggleStats(self): 
        self.showStats = not self.showStats


    def toggleShowEnemyWanderDestination(self): 
        self.showEnemyWanderDestination = not self.showEnemyWanderDestination


    def draw(self):
        # order here is Z axis
        self.map.draw()
        self.director.drawEnemies()
        #self.player.draw()

        #self.player.drawCharacterAttack()
        #self.director.drawEnemyAttacks()
        self.textureEmiter.draw()
        self.particleEmiter.draw() # should be on top

        if self.showStats:
            self.drawStats()

        if self.pause: 
            self.win.addstr(12, 40, "Paused", curses.color_pair(7))


    def getGameTime(self): 
        return self.gameTime


    def advance(self, deltaTime):
        if self.pause:
            return

        self.esperWorld.process(deltaTime)

        self.gameTime += deltaTime
        self.map.advance(deltaTime)
        #self.player.advance(deltaTime)
        self.director.advanceEnemies(deltaTime)
        self.particleEmiter.advance(deltaTime)
        self.textureEmiter.advance(deltaTime)
        self.director.worldUpdate()


    def getPlayer(self):
        return self.playerObj


    def drawStats(self): 
        x = 4
        y = 4

        o = []

        o.append('Enemies:')
        o.append('  Alive     : ' + str( self.director.numEnemiesAlive() ))
        o.append('  Attacking : ' + str( self.director.numEnemiesAttacking() ))
        o.append('  Chasing   : ' + str( self.director.numEnemiesChasing() ))
        o.append('  Wadndering: ' + str( self.director.numEnemiesWandering() ))

        n = 0
        while n < len(o):
            self.win.addstr(y + n, x, o[n])
            n += 1


    def quitGame(self): 
        self.gameRunning = False
