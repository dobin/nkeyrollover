import logging

logger = logging.getLogger(__name__)


class Timer(object):
    def __init__(
        self, timerValue :float =0.0, instant :bool =False, active :bool =True
    ):
        self.timeLeft :float = 0.0
        self.timerValue :float = timerValue
        self.instant :bool = instant
        self.active :bool = active

        self.rearm :bool = False
        self.init()


    def init(self):
        if not self.instant:
            self.timeLeft = self.timerValue
        else:
            self.timeLeft = 0.0


    def setTimer(self, timerValue: float):
        self.timerValue = timerValue
        self.init()


    def reset(self):
        self.timeLeft = self.timerValue
        self.active = True


    def timeIsUp(self) -> bool:
        # time cant be up if we dont count it / we are disabled
        if not self.active:
            return False

        if self.timeLeft <= 0.0:
            return True
        else:
            return False


    def isActive(self) -> bool:
        return self.active

    def setActive(self, active):
        self.active = active


    def start(self):
        self.timeLeft = self.timerValue
        self.active = True


    def stop(self):
        self.active = False


    def getTimeLeft(self):
        return self.timeLeft


    def advance(self, dt: float):
        if not self.active:
            return

        if self.timeLeft > 0:
            self.timeLeft -= dt
