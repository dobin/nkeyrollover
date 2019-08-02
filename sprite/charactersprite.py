
from enum import Enum
from entities.action import Action
from entities.direction import Direction

from .arrsprite import ArrSprite

class CharacterSprite(ArrSprite): 
    def initSprite(self, action, direction, animationIndex):
        super(CharacterSprite, self).initSprite(action=action, direction=None, animationIndex=None)
        self.xoffset = 0
        self.yoffset = 0

        if action is Action.standing:
            self.width = 3
            self.height = 3
            self.frameCount = 1
            self.frameIndex = 0
            self.frameTime = []
            self.isActive = True
            self.advanceByStep = False
            self.frameTime = None
            self.endless = True

            self.arr = [
                [
                    [ '', 'o', '' ],
                    [ '/', '|', '\\'],
                    [ '/', '', '\\']
                ]
            ]

        if action is Action.walking:
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
            self.endless = True
            self.advanceByStep = True

            if direction is Direction.right:
                self.arr = [
                    [
                        [ '', 'O', '' ],
                        [ '/', '|', '\\'],
                        [ '', '|', '\\']
                    ],
                    [
                        [ '', 'o', '' ],
                        [ '/', '|', '\\'],
                        [ '/', '|', '']
                    ]                
                ]
            else: 
                self.arr = [
                    [
                        [ '', 'o', '' ],
                        [ '/', '|', '\\'],
                        [ '/', '|', '']
                    ],
                    [
                        [ '', 'O', '' ],
                        [ '/', '|', '\\'],
                        [ '', '|', '\\']
                    ]
                ]                

        if action is Action.hitting:
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
            self.advanceByStep = False

            if direction is Direction.right:
                self.arr = [
                    [
                        [ '', 'o', '' ],
                        [ '/', '|', '-'],
                        [ '/', '', '\\']
                    ],
                    [
                        [ '', 'o', '' ],
                        [ '/', '|', '\\'],
                        [ '/', '', '\\']
                    ]
                ]
            else: 
                self.arr = [
                    [
                        [ '', 'o', '' ],
                        [ '-', '|', '\\'],
                        [ '/', '', '\\']
                    ],
                    [
                        [ '', 'o', '' ],
                        [ '/', '|', '\\'],
                        [ '/', '', '\\']
                    ]
                ]

        if action is Action.shrugging:
            self.width = 3
            self.height = 3
            self.frameCount = 2
            self.frameIndex = 1
            self.endless = True
            self.isActive = True
            self.advanceByStep = False

            self.frameTime = [
                100,
                50
            ]
            self.frameTimeLeft = self.frameTime[self.frameIndex]

            self.arr = [
                [
                    [ '', 'o', '' ],
                    [ '/', '|', '\\'],
                    [ '/', '', '\\']
                ],
                [
                    [ '', 'o', '' ],
                    [ '^', '|', '^'],
                    [ '/', '', '\\']
                ]                
            ]


        if action is Action.dying:
            self.width = 3
            self.height = 3
            self.frameCount = 1
            self.frameIndex = 0
            self.frameTime = []
            self.isActive = True
            self.advanceByStep = False
            self.frameTime = None
            self.endless = True

            if animationIndex == 0:
                self.arr = [
                    [
                        [ '', 'x', '' ],
                        [ '/', '|', '\\'],
                        [ '/', '', '\\']
                    ]
                ]
            elif animationIndex == 1: 
                self.arr = [
                    [
                        [ '', 'X', '' ],
                        [ '/', '|', '\\'],
                        [ '/', '', '\\']
                    ]
                ]
            elif animationIndex == 2:
                pass