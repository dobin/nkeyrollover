
from entities.action import Action

import curses

class SpeckSprite(object): 
    def __init__(self, char, x, y, movementX, movementY, timeArr): 
        self.char = char
        self.movementX = movementX
        self.movementY = movementY
        self.x = x
        self.y = y
        
        self.idx = 0
        self.timeArr = timeArr
        self.time = 0
        self.isActive = True


    def advance(self):
        self.time += 1

        if not self.time == self.timeArr[ self.idx ]: 
            return 

        self.time = 0

        self.x += self.movementX
        self.y += self.movementY
        self.idx += 1

        if self.idx == len(self.timeArr): 
            self.isActive = False


    
    def draw(self, win):
        if not self.isActive: 
            return

        win.addch(
                self.y, 
                self.x,
                self.char, 
                curses.color_pair(1))

