from player.player import Player
from .enemyaction import EnemyAction
from player.direction import Direction
from player.action import Action

import random
from config import Config

import logging

logger = logging.getLogger(__name__)


class Enemy(Player):
    def __init__(self, win, coordinates):
        Player.__init__(self, win, coordinates)
        self.coordinates = coordinates
        self.speed = Config.secToFrames(1)
        self.playerAction = EnemyAction()
        self.init()


    def init(self):
        self.x = random.randint(self.coordinates['min_x'], self.coordinates['max_x'])
        self.y = random.randint(self.coordinates['min_y'], self.coordinates['max_y'])
        self.direction = Direction.left
        self.lastInput = 0


    def getInput(self, playerLocation):
        if not self.playerAction.type is Action.walking: 
            return
        if not self.lastInput > self.speed: 
            return

        self.playerAction.changeTo(Action.walking, Direction.left)

        if playerLocation['x'] > self.x:
            self.x += 1
        else: 
            self.x -= 1

        if playerLocation['y'] > self.y:
            self.y += 1
        else: 
            self.y -= 1

        self.lastInput = 0


    def ressurectMe(self): 
        if self.playerStatus.isAlive(): 
            return

        logger.info("E New enemy at: " + str(self.x) + " / " + str(self.y))
        self.init()
        self.playerStatus.init()
        self.playerAction.changeTo(Action.walking, None)


    def advance(self): 
        super(Enemy, self).advance()
        self.lastInput += 1
        
