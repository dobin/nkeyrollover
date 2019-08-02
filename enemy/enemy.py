from player.player import Player
from .enemyactionctrl import EnemyActionCtrl
from player.direction import Direction
from player.action import Action

import random
from config import Config
from player.figure import Figure
import logging

logger = logging.getLogger(__name__)


class Enemy(Figure):
    def __init__(self, win, coordinates):
        Figure.__init__(self, win, coordinates)
        self.coordinates = coordinates
        self.speed = Config.secToFrames(1)
        self.actionCtrl = EnemyActionCtrl(self)
        self.init()


    def init(self):
        self.x = random.randint(self.coordinates['min_x'], self.coordinates['max_x'])
        self.y = random.randint(self.coordinates['min_y'], self.coordinates['max_y'])
        self.direction = Direction.left
        self.lastInput = 0


    def getInput(self, playerLocation):
        if not self.actionCtrl.type is Action.walking: 
            return
        if not self.lastInput > self.speed: 
            return

        # to update timers
        self.actionCtrl.changeTo(Action.walking, Direction.left)

        # to make animation run
        self.actionCtrl.advanceStep()

        if playerLocation['x'] > self.x:
            if self.x < Config.columns - 4:
                self.x += 1
        else: 
            if self.x > 2:
                self.x -= 1

        if playerLocation['y'] > self.y:
            if self.y < Config.rows - 4:
                self.y += 1
        else: 
            if self.y > 2:
                self.y -= 1

        self.lastInput = 0


    def ressurectMe(self): 
        if self.playerStatus.isAlive(): 
            return

        logger.info("E New enemy at: " + str(self.x) + " / " + str(self.y))
        self.init()
        self.playerStatus.init()
        self.actionCtrl.changeTo(Action.walking, None)


    def advance(self): 
        super(Enemy, self).advance()
        self.lastInput += 1
        
