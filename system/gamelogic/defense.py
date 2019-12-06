import logging

from utilities.timer import Timer

logger = logging.getLogger(__name__)


class Defense():
    def __init__(self):
        self.coordinates = None
        self.timer = Timer(1.0)
        self.isActive = False


    def advance(self, dt):
        self.timer.advance(dt)

        if self.timer.timeIsUp():
            self.isActive = False
