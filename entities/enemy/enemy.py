from entities.player.player import Player
from .enemyactionctrl import EnemyActionCtrl
from entities.direction import Direction
from entities.action import Action

import random
from config import Config
from entities.character import Character
import logging
from sprite.charactersprite import CharacterSprite

logger = logging.getLogger(__name__)


class Enemy(Character):
    def __init__(self, win, parent, coordinates, world):
        Character.__init__(self, win, parent, coordinates, world)
        self.actionCtrl = EnemyActionCtrl(parentEntity=self, world=world)
        self.sprite = CharacterSprite(parentEntity=self)
        
        # make him walk
        self.actionCtrl.changeTo(Action.walking, Direction.left)

        self.coordinates = coordinates
        self.speed = Config.secToFrames(1)
        self.init()


    def init(self):
        self.x = random.randint(self.coordinates['min_x'], self.coordinates['max_x'])
        self.y = random.randint(self.coordinates['min_y'], self.coordinates['max_y'])
        self.direction = Direction.left
        self.lastInput = 0


    def getInput(self, playerLocation):
        if not self.actionCtrl.getAction() is Action.walking: 
            return
        if not self.lastInput > self.speed: 
            return

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

        self.lastInput = 0


    def ressurectMe(self): 
        if self.characterStatus.isAlive(): 
            return

        logger.info("E New enemy at: " + str(self.x) + " / " + str(self.y))
        self.init()
        self.characterStatus.init()
        self.actionCtrl.changeTo(Action.walking, None)


    def advance(self): 
        super(Enemy, self).advance()
        self.lastInput += 1
        
