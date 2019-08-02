
from enum import Enum
from entities.action import Action
from entities.direction import Direction

from .arrsprite import ArrSprite

class PhenomenaSprite(ArrSprite): 
    def initSprite(self, action, direction, animationIndex):
        self.xoffset = 0
        self.yoffset = 0

        if action is Action.hit:
            self.width = 1
            self.height = 1
            self.frameCount = 3
            self.frameIndex = 0
            self.endless = False
            self.isActive = True
            self.advanceByStep = False
            
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