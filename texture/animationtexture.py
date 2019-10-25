import logging

from texture.texture import Texture
from texture.animation import Animation
from common.direction import Direction

logger = logging.getLogger(__name__)


class AnimationTexture(Texture):
    # abstract class
    def __init__(self, type, name='', setbg=False):
        super(AnimationTexture, self).__init__(type=type, name=name)
        self.setbg = setbg
        self.animation :Animation = None
        self.frameChanged = False
        self.init()


    def init(self):
        super().init()
        self.setActive(True)
        self.resetAnimation()


    def resetAnimation(self):
        """Start animation from the beginning"""
        self.frameIndex = 0
        self.frameTimeLeft = 0.0

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

        # also advance texture object
        super().advance(deltaTime)

        # no need to advance stuff which is forever
        if ((self.animation.frameTime is None or len(self.animation.frameTime) == 0)
                and self.animation.endless is True):
            return

        # not active, no work
        if not self.isActive():
            return

        # reset frame status
        self.setFrameChanged(False)

        # done in advanceStep()
        if self.animation.advanceByStep:
            return

        self.frameTimeLeft -= deltaTime
        if self.frameTimeLeft <= 0:
            # animation ended, check if we need to restart it,
            # or take the next one
            if self.animation.endless:
                # endless, just advance
                self.nextFrame()
            else:
                # check if it is the last animation, if yes stop it
                if self.frameIndex == self.animation.frameCount - 1:
                    self.setActive(False)
                else:
                    # set next frame in animation
                    if self.frameIndex >= len(self.animation.frameTime):
                        logger.error("Frameidx {} larget than frametime arr {}".format(
                            self.frameIndex, self.animation.frameTime))
                    self.nextFrame()


    def nextFrame(self):
        self.frameIndex = (self.frameIndex + 1) % self.animation.frameCount
        self.frameTimeLeft = self.animation.frameTime[self.frameIndex]
        self.setFrameChanged(True)


    def setFrameChanged(self, frameChanged):
        self.frameChanged = frameChanged


    def isFrameChanged(self):
        return self.frameChanged


    def draw(self, viewport, pos):
        if not self.isActive():
            # logger.debug("Drawing nonactive sprite")
            return

        if self.animation is None:
            m = "Animation {}: Trying to access animation which does not exist"
            raise Exception(m.format(self.name))

        if self.frameIndex >= len(self.animation.arr):
            m = "Animation {}: Trying to access frameId {} on arr with len {}, actual len {}"
            raise Exception(m.format(
                self.name,
                self.frameIndex,
                self.animation.frameCount,
                len(self.animation.arr)))

        if self.overwriteColor is not None:
            color = self.overwriteColor
        else:
            color = self.animation.frameColors[self.frameIndex]

        # Note: For performance reason, replace enumerate with a while loop
        currentFrame = self.getCurrentFrame()
        y = 0
        while y < len(currentFrame):
            x = 0
            while x < len(currentFrame[y]):
                column = currentFrame[y][x]
                if column != '':
                    viewport.addstr(
                        pos.y + y,
                        pos.x + x,
                        column,
                        color=color[0],
                        attr=color[1],
                        setbg=self.setbg)

                x += 1
            y += 1


    def getCurrentFrame(self):
        return self.animation.arr[self.frameIndex]


    def getCurrentFrameCopy(self):
        return self.animation.arr[self.frameIndex].copy()


    def getAnimationTime(self) -> float:
        """Return sum of all animation times in current sprite"""
        n = 0.0
        if self.animation.frameTime is None:
            logger.error("{}: Texture {} does not have frametime".format(
                self.name, self.animation))
        for time in self.animation.frameTime:
            n += time
        return n
