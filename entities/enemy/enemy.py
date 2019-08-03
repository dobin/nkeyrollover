import random
import logging

from sprite.charactersprite import CharacterSprite
from entities.player.player import Player
from entities.direction import Direction
from entities.action import Action
from entities.character import Character
from .enemyactionctrl import EnemyActionCtrl
from config import Config
from utilities.timer import Timer

logger = logging.getLogger(__name__)


class Enemy(Character):
    def __init__(self, win, parent, spawnBoundaries, world):
        Character.__init__(self, win, parent, spawnBoundaries, world)
        self.actionCtrl = EnemyActionCtrl(parentEntity=self, world=world)
        self.sprite = CharacterSprite(parentEntity=self)
        self.lastInputTimer = Timer(1.0)
        # make him walk
        self.actionCtrl.changeTo(Action.walking, Direction.left)

        self.init()


    def init(self):
        self.x = random.randint(self.spawnBoundaries['min_x'], self.spawnBoundaries['max_x'])
        self.y = random.randint(self.spawnBoundaries['min_y'], self.spawnBoundaries['max_y'])
        self.direction = Direction.left
        self.lastInputTimer.reset()


    def getInput(self, playerLocation):
        if not self.actionCtrl.getAction() is Action.walking: 
            return

        if not self.lastInputTimer.timeIsUp():
            return
        self.lastInputTimer.reset()

        # to update timers
        self.actionCtrl.changeTo(Action.walking, Direction.left)

        # to make animation run
        self.sprite.advanceStep()

        if playerLocation['x'] > self.x:
            if self.x < Config.columns - self.sprite.width - 1:
                self.x += 1
                self.direction = Direction.right
        else: 
            if self.x > 1:
                self.x -= 1
                self.direction = Direction.left

        if playerLocation['y'] > self.y:
            if self.y < Config.rows - self.sprite.height - 1:
                self.y += 1
        else: 
            if self.y > 2:
                self.y -= 1


    def ressurectMe(self): 
        if self.characterStatus.isAlive(): 
            return

        logger.info("E New enemy at: " + str(self.x) + " / " + str(self.y))
        self.init()
        self.characterStatus.init()
        self.actionCtrl.changeTo(Action.walking, None)


    def advance(self, deltaTime): 
        super(Enemy, self).advance(deltaTime)
        self.lastInputTimer.advance(deltaTime)
        
