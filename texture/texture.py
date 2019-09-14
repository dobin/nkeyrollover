import logging

from utilities.timer import Timer
from utilities.color import Color

logger = logging.getLogger(__name__)


class Texture(object):
    def __init__(self, type, width =0, height =0, name=''):
        self.type = type
        self.width :int = width
        self.height :int = height
        self.active :bool = True
        self.name = name

        # color related
        self.overwriteColorTimer = Timer(0.25, active=False)
        self.overwriteColor = None


    def init(self):
        pass


    def draw(self, viewport):
        pass


    def advance(self, deltaTime :float):
        # reset overwrite color
        if self.overwriteColorTimer.timeIsUp():
            self.overwriteColor = None
            self.overwriteColorTimer.stop()
        self.overwriteColorTimer.advance(deltaTime)


    def setOverwriteColorFor(self, time :float, color :Color):
        if self.overwriteColorTimer.isActive():
            logger.debug("{} Color already active on new set color".format(self.name))

        self.overwriteColor = color
        self.overwriteColorTimer.setTimer(time)
        self.overwriteColorTimer.reset()


    def advanceStep(self):
        pass


    def setActive(self, active :bool):
        self.active = active


    def isActive(self) -> bool:
        return self.active


    def setName(self, name :str):
        self.name = name


    def __repr__(self):
        return self.name
