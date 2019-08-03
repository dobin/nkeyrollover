

class Timer(object): 
    def __init__(self, timerValue, instant=False, active=True): 
        self.timeLeft = 0.0
        self.timerValue = timerValue
        self.instant = instant
        self.active = active

        self.init()


    def init(self):
        if not self.instant: 
            self.timeLeft = self.timerValue
        else: 
            self.timeLeft = 0.0
        

    def setTimer(self, timerValue): 
        self.timerValue = timerValue


    def reset(self): 
        self.timeLeft = self.timerValue
        self.active = True


    def timeIsUp(self):
        if not self.active:
            return False

        if self.timeLeft <= 0.0:
            return True
        else:
            # print("{} ".format(self.timeLeft))
            return False


    def isActive(self): 
        return self.active

    def start(self): 
        pass

    def stop(self): 
        pass


    def advance(self, dt):
        if not self.active: 
            return

        if self.timeLeft > 0:
            self.timeLeft -= dt
