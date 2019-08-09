import curses

from sprite.coordinates import Coordinates
from utilities.utilities import Utility


class SpeckTexture(object): 
    def __init__(self, char, coordinate, movementX, movementY, timeArr, effect): 
        self.char = char
        self.effect = effect
        self.movementX = movementX
        self.movementY = movementY
        self.coordinate = coordinate
        
        self.idx = 0
        self.timeArr = timeArr
        self.time = 0
        self.isActive = True


    def advance(self, deltaTime):
        self.time += deltaTime

        if not self.time >= self.timeArr[ self.idx ]: 
            return 

        self.time = 0

        self.coordinate.x += self.movementX
        self.coordinate.y += self.movementY
        self.idx += 1

        if self.idx == len(self.timeArr): 
            self.isActive = False

    
    def draw(self, win):
        if not self.isActive: 
            return

        c = Coordinates(
            x = self.coordinate.x,
            y = self.coordinate.y,
        )

        if Utility.isPointDrawable(c):
            win.addch(
                    self.coordinate.y, 
                    self.coordinate.x,
                    self.char, 
                    curses.color_pair(1))

