import logging

from utilities.timer import Timer

logger = logging.getLogger(__name__)


class TextureMinimal(object):
    def __init__(
        self,
        char :str,
        colorArr,
        timeArr,
        movementX :int =0,
        movementY :int =0,
    ):
        self.width = 1
        self.height = 1
        self.char = char
        self.movementX = movementX
        self.movementY = movementY
        self.timeArr = timeArr
        self.colorArr = colorArr

        self.idx = 0
        self.timer = Timer(self.timeArr[0])


    def advance(self, dt):
        self.timer.advance(dt)
