

class Animation(object): 
    def __init__(self): 
        self.frameCount = 0
        self.advanceByStep = False
        self.endless = False

        self.frameTime = []
        self.arr = []

        self.width = 0
        self.height = 0