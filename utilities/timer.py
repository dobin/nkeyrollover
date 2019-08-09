

class Timer(object): 
    def __init__(
        self, timerValue :float =0.0, instant :bool =False, active :bool =True
    ): 
        self.timeLeft :float = 0.0
        self.timerValue :float = timerValue
        self.instant :bool = instant
        self.active :bool = active

        self.init()


    def init(self):
        if not self.instant: 
            self.timeLeft = self.timerValue
        else: 
            self.timeLeft = 0.0
        

    def setTimer(self, timerValue: float): 
        self.timerValue = timerValue


    def reset(self): 
        self.timeLeft = self.timerValue
        self.active = True


    def timeIsUp(self) -> bool:
        if not self.active:
            return False

        if self.timeLeft <= 0.0:
            return True
        else:
            # print("{} ".format(self.timeLeft))
            return False


    def isActive(self) -> bool:
        return self.active

    def start(self): 
        self.active = True

    def stop(self): 
        self.active = False


    def advance(self, dt: float):
        if not self.active: 
            return

        if self.timeLeft > 0:
            self.timeLeft -= dt
