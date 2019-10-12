import logging

logger = logging.getLogger(__name__)


class Apm(object):
    def __init__(self):
        self.lastKeyTime = 0

        self.time = 0
        self.count = 0


    def tick(self, time):
        self.count += 1
        timeDiff = time - self.lastKeyTime
        self.time += timeDiff
        self.lastKeyTime = time

        if self.time > 3.0:
            self.time = self.time * 0.5
            self.count = int(self.count * 0.5)


    def getApm(self):
        if self.count == 0:
            return 0

        apm :float = (1.0 / self.time) * self.count
        #apm = apm / 60
        return apm


apm = Apm()
