
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
                0.1,
                0.1,
                0.1
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

        if action is Action.roflcopter: 
            self.width = 3
            self.height = 3
            self.frameCount = 2
            self.frameIndex = 1
            self.endless = True
            self.isActive = True
            self.advanceByStep = False

            self.frameTime = [
                0.2,
                0.2
            ]
            self.frameTimeLeft = self.frameTime[self.frameIndex]

            texture = self.readfile('textures/roflcopter.ascii')
            self.width = texture['width']
            self.height = texture['height']
            self.arr = texture['arr']

    def readfile(self, filename):
        lineList = [line.rstrip('\n') for line in open('sprite/textures/roflcopter.ascii')]


        res = []

        max = 0
        for line in lineList: 
            if len(line) > max: 
                max = len(line)


        tmp = []
        for line in lineList: 
            if line == '': 
                res.append(tmp)
                tmp = []
            else: 
                line += ' ' * (max - len(line))
                tmp.append(list(line))
        res.append(tmp)
            
        texture = {
            'arr': res,
            'width': max, 
            'height': 0,
        }

        return texture
