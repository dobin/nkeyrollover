
from enum import Enum
from player.action import Action
from player.direction import Direction

from .sprite import Sprite

class SpeechSprite(Sprite): 

    def initSprite(self, type, direction):
        self.type = Action.speech
    
        self.width = 5
        self.height = 4
        self.frameCount = 1
        self.frameIndex = 0
        self.frameTime = [
            5, 
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

