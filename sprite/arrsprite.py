import curses
import logging

from enum import Enum
from entities.action import Action
from entities.direction import Direction

logger = logging.getLogger(__name__)


class ArrSprite(object):
    # abstract class
    # cant be used really as no animation is stored in arr
    # initSprite needs to be overwritten to make it work
    def __init__(self, action=None, parentEntity=None):
        self.type = action
        self.initSprite(action=None, direction=Direction.right, animationIndex=None)

        # our position is relative to this
        # if None, its absolute
        # parent needs to be of type Entity
        self.parent = parentEntity
        

    def initSprite(self, action, direction, animationIndex):
        self.width = 0
        self.height = 0
        self.frameCount = 0
        self.frameIndex = 0
        self.frameTime = 0
        self.isActive = False
        self.advanceByStep = False
        self.endless = False
        self.frameTime = []
        self.arr = []
        self.xoffset = 0
        self.yoffset = 0


    def advanceStep(self): 
        if not self.advanceByStep: 
            return

        self.frameIndex = (self.frameIndex + 1) % self.frameCount
 

    def advance(self):
        # no need to advance stuff which is forever
        if self.frameTime is None and self.endless == True: 
            return

        # not active, no work
        if not self.isActive: 
            return

        # done in advanceStep()
        if self.advanceByStep: 
            return

        self.frameTimeLeft = self.frameTimeLeft - 1
        if self.frameTimeLeft == 0:
            # animation ended, check if we need to restart it, 
            # or take the next one
            if self.endless:
                # endless, just advance
                self.frameIndex = (self.frameIndex + 1) % self.frameCount
                self.frameTimeLeft = self.frameTime[ self.frameIndex ]
            else:
                # check if it is the last animation, if yes stop it
                if self.frameIndex == self.frameCount - 1:
                    self.isActive = False
                    return
                else: 
                    self.frameTimeLeft = self.frameTime[ self.frameIndex ]
                    self.frameIndex = (self.frameIndex + 1) % self.frameCount
       

    def draw(self, win):
        if not self.isActive: 
            return

        if self.parent is None: 
            parentPos = { 'x': 0, 'y': 0 }
        else: 
            parentPos = self.parent.getLocation()

        for (y, rows) in enumerate(self.arr[ self.frameIndex ]):
            for (x, column) in enumerate(rows):
                if column is not '':
                    win.addch(
                        y + self.yoffset + parentPos['y'], 
                        x + self.xoffset + parentPos['x'], 
                        column, 
                        curses.color_pair(1))


    def getCurrentFrameCopy(self): 
        return self.arr[self.frameIndex].copy()