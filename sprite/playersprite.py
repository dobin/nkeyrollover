
from enum import Enum
from player.action import Action
from player.direction import Direction

from .sprite import Sprite

class PlayerSprite(Sprite): 
    def __init__(self, action):
        self.type = action
        super().__init__(action, Direction.right)
        self.initSprite(action, Direction.right)
        

    def initSprite(self, action, direction):
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
                    [ ' ', 'o', ' ' ],
                    [ '/', '|', '\\'],
                    [ '/', ' ', '\\']
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
            else: 
                self.arr = [
                    [
                        [ ' ', 'o', ' ' ],
                        [ '/', '|', '\\'],
                        [ '/', '|', ' ']
                    ],
                    [
                        [ ' ', 'O', ' ' ],
                        [ '/', '|', '\\'],
                        [ ' ', '|', '\\']
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
            else: 
                self.arr = [
                    [
                        [ ' ', 'o', ' ' ],
                        [ '-', '|', '\\'],
                        [ '/', ' ', '\\']
                    ],
                    [
                        [ ' ', 'o', ' ' ],
                        [ '/', '|', '\\'],
                        [ '/', ' ', '\\']
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


        if action is Action.hit:
            self.width = 1
            self.height = 1
            self.frameCount = 3
            self.frameIndex = 0
            self.endless = False
            self.isActive = True
            self.advanceByStep = False
            
            self.frameTime = [
                5,
                5,
                5
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

            self.arr = [
                [
                    [ ' ', 'x', ' ' ],
                    [ '/', '|', '\\'],
                    [ '/', ' ', '\\']
                ]
            ]