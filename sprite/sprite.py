import curses
import logging

from enum import Enum
from player.action import Action
from player.direction import Direction

logger = logging.getLogger(__name__)


class Sprite(object): 
    def __init__(self, type):
        self.type = type
        self.initSprite(type)


    def initSprite(self, type):

        if type is Action.standing:
            self.width = 3
            self.height = 3
            self.frameCount = 1
            self.frameIndex = 0
            self.frameTime = 0
            self.isActive = True

            self.arr = [
                [
                    [ ' ', 'o', ' ' ],
                    [ '/', '|', '\\'],
                    [ '/', ' ', '\\']
                ]
            ]

        if type is Action.walking:
            self.width = 3
            self.height = 3
            self.frameCount = 2
            self.frameIndex = 0
            self.isActive = True
            self.frameTime = [
                10, 
                10
            ]
            self.frameTimeLeft = self.frameTime[self.frameIndex]
            self.endless = False

            self.arr = [
                [
                    [ ' ', 'O', ' ' ],
                    [ '/', '|', '\\'],
                    [ ' ', '|', '\\']
                ],
                [
                    [ ' ', 'o', ' ' ],
                    [ '/', '|', '\\'],
                    [ '/', '|', ' ']
                ]                
            ]

        if type is Action.hitting:
            self.width = 3
            self.height = 3
            self.endless = False
            self.frameCount = 2
            self.frameIndex = 0
            self.frameTime = [
                50, 
                100
            ]
            self.frameTimeLeft = self.frameTime[self.frameIndex]
            self.isActive = True

            self.arr = [
                [
                    [ ' ', 'o', ' ' ],
                    [ '/', '|', '-'],
                    [ '/', ' ', '\\']
                ],
                [
                    [ ' ', 'o', ' ' ],
                    [ '/', '|', '\\'],
                    [ '/', ' ', '\\']
                ]
            ]

        if type is Action.shrugging:
            self.width = 3
            self.height = 3
            self.frameCount = 2
            self.frameIndex = 1
            self.endless = True
            self.isActive = True

            self.frameTime = [
                100,
                50
            ]
            self.frameTimeLeft = self.frameTime[self.frameIndex]

            self.arr = [
                [
                    [ ' ', 'o', ' ' ],
                    [ '/', '|', '\\'],
                    [ '/', ' ', '\\']
                ],
                [
                    [ ' ', 'o', ' ' ],
                    [ '^', '|', '^'],
                    [ '/', ' ', '\\']
                ]                
            ]


        if type is Action.hit:
            self.width = 1
            self.height = 1
            self.frameCount = 3
            self.frameIndex = 0
            self.endless = False
            self.isActive = True
            
            self.frameTime = [
                10,
                10,
                10
            ]
            self.frameTimeLeft = self.frameTime[self.frameIndex]


            self.arr = [
                [
                    [ '.', ],
                ],
                [
                    [ 'o', ],
                ],
                [
                    [ 'O', ],
                ]                                
            ]


    def advance(self):
        if self.frameTime == 0 or self.frameCount == 1: 
            return

        if not self.isActive: 
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
