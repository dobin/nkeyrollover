
from enum import Enum
from entities.action import Action
from entities.direction import Direction

from .arrsprite import ArrSprite

class SpeechSprite(ArrSprite): 

    def initSprite(self, action, direction, animationIndex):
        self.action = Action.speech
    
        self.width = 5
        self.height = 4
        self.frameCount = 1
        self.frameIndex = 0
        self.frameTime = [
            50, 
        ]
        self.frameTimeLeft = self.frameTime[self.frameIndex]
        self.endless = False
        self.isActive = True
        self.advanceByStep = False
        self.xoffset = 1
        self.yoffset = -4

        self.arr = [
            [
                [ '.', '-', '-', '-', '.' ],
                [ '|', 'h', 'o', 'i', '|' ],
                [ '`', '^', '-', '-', '\'' ],
                [ '/', ' ', ' ', ' ', ' ' ],                        
            ]
        ]

