import curses
import logging

from enum import Enum
from player.action import Action
from player.direction import Direction

logger = logging.getLogger(__name__)


class Sprite(object): 
    def __init__(self, type):
        self.type = type
        self.initSprite(type, Direction.right)


    def initSprite(self, type, direction): 
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


    def advanceStep(self): 
        if not self.advanceByStep: 
            return

        self.frameIndex = (self.frameIndex + 1) % self.frameCount
 

    def advance(self):
        if self.frameTime == 0 or self.frameCount == 1: 
            return

        if not self.isActive: 
            return

        if self.advanceByStep: 
            return

        self.frameTimeLeft = self.frameTimeLeft - 1
        if self.frameTimeLeft == 0:
            if self.endless:
                self.frameIndex = (self.frameIndex + 1) % self.frameCount
                self.frameTimeLeft = self.frameTime[ self.frameIndex ]
            else: 
                self.frameTimeLeft = self.frameTime[ self.frameIndex ]

                if self.frameIndex == self.frameCount - 1:
                    self.isActive = False
                    return
                else: 
                    self.frameIndex = (self.frameIndex + 1) % self.frameCount
       

    def draw(self, win, basex, basey):
        # if not self.isActive: 
        #    return

        for (y, rows) in enumerate(self.arr[ self.frameIndex ]):
            for (x, column) in enumerate(rows):
                win.addch(basey + y, basex + x, column, curses.color_pair(1))
