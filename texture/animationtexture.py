import curses
import logging
from enum import Enum

from sprite.coordinates import Coordinates
from entities.entity import Entity
from sprite.direction import Direction
from config import Config
from utilities.utilities import Utility
from texture.texture import Texture
from sprite.sprite import Sprite
from texture.animation import Animation

logger = logging.getLogger(__name__)


class AnimationTexture(Texture):
    # abstract class
    # cant be used really as no animation is stored in arr
    # initSprite needs to be overwritten to make it work
    def __init__(self, parentSprite :Sprite =None):
        super(AnimationTexture, self).__init__(parentSprite=parentSprite)
        self.animation :Animation = None
        self.init()
        
    
    def init(self):
        self.setActive(True)
        self.offset.x = 0
        self.offset.y = 0
        self.resetAnimation()


    def resetAnimation(self): 
        """Start animation from the beginning"""
        self.frameIndex = 0
        self.frameTimeLeft = 0

        # set the initial frametime
        # therefore, this init() has to be called after changeTexture()
        if self.animation is not None:
            if not self.animation.endless and self.animation.frameTime:
                self.frameTimeLeft = self.animation.frameTime[self.frameIndex]


    def advanceStep(self):
        """Advance entity animation when it has moved one square"""
        if not self.animation.advanceByStep:
            return

        self.frameIndex = (self.frameIndex + 1) % self.animation.frameCount
 

    def advance(self, deltaTime):
        if self.animation is None: 
            return

        # no need to advance stuff which is forever
        if (self.animation.frameTime is None or len(self.animation.frameTime) == 0) and self.animation.endless == True: 
            return

        # not active, no work
        if not self.isActive():
            return

        # done in advanceStep()
        if self.animation.advanceByStep: 
            return

        self.frameTimeLeft -= deltaTime
        if self.frameTimeLeft <= 0:
            # animation ended, check if we need to restart it, 
            # or take the next one
            if self.animation.endless:
                # endless, just advance
                self.frameIndex = (self.frameIndex + 1) % self.animation.frameCount
                self.frameTimeLeft = self.animation.frameTime[ self.frameIndex ]
            else:
                # check if it is the last animation, if yes stop it
                if self.frameIndex == self.animation.frameCount - 1:
                    self.setActive(False)
                    return
                else: 
                    if self.frameIndex >= len( self.animation.frameTime ): 
                        logging.error("Frameindex {} larget than frametime arr {}".format(self.frameIndex, self.animation.frameTime))
                    self.frameTimeLeft = self.animation.frameTime[ self.frameIndex ]
                    self.frameIndex = (self.frameIndex + 1) % self.animation.frameCount
    

    def draw(self, viewport):
        if not self.isActive():
            # logger.debug("Drawing nonactive sprite")
            return

        pos = self.getLocation()
        if self.frameIndex >= len(self.animation.arr): 
            raise Exception("Trying to access frameIndex {} on array with len {}, actual len{}"
                .format(self.frameIndex, self.animation.frameCount, len(self.animation.arr)))

        color = self.parentSprite.currentColor
        if self.animation.frameColors is not None: 
            color = self.animation.frameColors[ self.frameIndex ]

        # Note: For performance reason, replace enumerate with a while loop
        y = 0
        while y < len(self.animation.arr[ self.frameIndex ]):
        #for (y, rows) in enumerate(self.animation.arr[ self.frameIndex ]):
            x = 0
            while x < len(self.animation.arr[ self.frameIndex ][y]):
            # for (x, column) in enumerate(rows):
                column = self.animation.arr[ self.frameIndex ][y][x]
                if column is not '':
                    viewport.addstr(
                        pos.y + y,
                        pos.x + x,
                        column, 
                        color)

                x += 1
            y += 1


    def getCurrentFrameCopy(self): 
        return self.animation.arr[self.frameIndex].copy()


    def getAnimationTime(self) -> float:
        """Return sum of all animation times in current sprite"""
        n = 0.0
        for time in self.animation.frameTime: 
            n += time
        return n        