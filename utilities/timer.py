

class Timer(object): 
    def __init__(self, timerValue, instant=False): 
        self.timeLeft = 0.0
        self.timerValue = timerValue
        self.instant = instant
        self.isActive = True

        self.init()


    def init(self):
        if not self.instant: 
            self.timeLeft = self.timerValue
        else: 
            self.timeLeft = 0.0
        
        self.isActive = True


    def setTimer(self, timerValue): 
        self.timerValue = timerValue


    def reset(self): 
        self.timeLeft = self.timerValue
        self.isActive = True


    def timeIsUp(self):
        if self.timeLeft <= 0.0:
            return True
        else:
            # print("{} ".format(self.timeLeft))
            return False


    def start(self): 
        pass

    def stop(self): 
        pass


    def advance(self, dt):
        if not self.isActive: 
            return

        if self.timeLeft > 0:
            self.timeLeft -= dt
