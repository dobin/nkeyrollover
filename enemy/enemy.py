from player.player import Player

from player.direction import Direction


class Enemy(Player):
    def __init__(self, win):
        Player.__init__(self, win)
        self.x = 20
        self.y = 10
        self.direction = Direction.left

    def getInput(self): 
        pass


