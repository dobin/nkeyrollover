class Texture(object): 
    def __init__(self): 
        self.width = 0
        self.height = 0
        self.frameCount = 0

        self.advanceByStep = False
        self.endless = False

        self.frameTime = []
        self.arr = []


    def getAnimationTime(self) -> float:
        """Return sum of all animation times in current sprite"""
        n = 0.0
        for time in self.frameTime: 
            n += time
        return n