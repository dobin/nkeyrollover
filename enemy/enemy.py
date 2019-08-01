from player.player import Player
from player.playeraction import Action
from player.direction import Direction
import random

import logging

logger = logging.getLogger(__name__)


class Enemy(Player):
    def __init__(self, win, coordinates):
        Player.__init__(self, win, coordinates)
        self.coordinates = coordinates
        self.init()

    def init(self):
        self.x = random.randint(self.coordinates['min_x'], self.coordinates['max_x'])
        self.y = random.randint(self.coordinates['min_y'], self.coordinates['max_y'])
        logger.warning("New enemy at: " + str(self.x) + " / " + str(self.y))
        self.direction = Direction.left

    def getInput(self): 
        pass

    def ressurectMe(self): 
        if self.playerStatus.isAlive(): 
            return

        self.init()
        self.playerStatus.init()
        self.playerAction.changeTo(Action.walking, None)

