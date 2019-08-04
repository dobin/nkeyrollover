import curses
import logging
from enum import Enum

from entities.entity import Entity
from entities.direction import Direction
from config import Config
from utilities.utilities import Utility

logger = logging.getLogger(__name__)


class ArrSprite(object):
    # abstract class
    # cant be used really as no animation is stored in arr
    # initSprite needs to be overwritten to make it work
    def __init__(self, parentEntity=None):
        self.texture = None

        if not isinstance(parentEntity, Entity):
            logging.error("ArrSprite: Tried to use non-Entity class as parent: " + str(parentEntity))
        else:
            # our position is relative to this
            # if None, its absolute
            self.parent = parentEntity

        self.init()

    
    def init(self):
        self.frameIndex = 0
        self.frameTimeLeft = 0        
        self.isActive = True
        self.xoffset = 0
        self.yoffset = 0

        # set the initial frametime
        # therefore, this init() has to be called after changeTexture()
        if self.texture is not None:
            if not self.texture.endless and self.texture.frameTime:
                self.frameTimeLeft = self.texture.frameTime[self.frameIndex]



    def advanceStep(self):
        if not self.texture.advanceByStep:
            return

        self.frameIndex = (self.frameIndex + 1) % self.texture.frameCount
 

    def setActive(self, active):
        self.isActive = active
        

    def active(self):
        return self.isActive


    def advance(self, deltaTime):
        if self.texture is None: 
            return

        # no need to advance stuff which is forever
        if (self.texture.frameTime is None or len(self.texture.frameTime) == 0) and self.texture.endless == True: 
            return

        # not active, no work
        if not self.isActive: 
            return

        # done in advanceStep()
        if self.texture.advanceByStep: 
            return

        self.frameTimeLeft -= deltaTime
        if self.frameTimeLeft <= 0:
            # animation ended, check if we need to restart it, 
            # or take the next one
            if self.texture.endless:
                # endless, just advance
                self.frameIndex = (self.frameIndex + 1) % self.texture.frameCount
                self.frameTimeLeft = self.texture.frameTime[ self.frameIndex ]
            else:
                # check if it is the last animation, if yes stop it
                if self.frameIndex == self.texture.frameCount - 1:
                    self.setActive(False)
                    return
                else: 
                    self.frameTimeLeft = self.texture.frameTime[ self.frameIndex ]
                    self.frameIndex = (self.frameIndex + 1) % self.texture.frameCount
    

    def getLocation(self): 
        if self.parent is None: 
            pos = { 'x': 0, 'y': 0 }
        else: 
            pos = self.parent.getLocation()

        pos['x'] += self.xoffset
        pos['y'] += self.yoffset

        return pos


    def getAnimationTime(self): 
        n = 0.0
        for time in self.texture.frameTime: 
            n += time
        return n


    def draw(self, win):
        if not self.isActive:
            # logging.debug("Drawing nonactive sprite")
            return

        pos = self.getLocation()

        for (y, rows) in enumerate(self.texture.arr[ self.frameIndex ]):
            for (x, column) in enumerate(rows):
                if column is not '':
                    p = {
                        'x': pos['x'] + x,
                        'y': pos['y'] + y,
                    }

                    if Utility.isPointDrawable(p):
                        win.addstr(
                            p['y'],
                            p['x'],
                            column, 
                            self.parent.currentColor)


    def getCurrentFrameCopy(self): 
        return self.texture.arr[self.frameIndex].copy()