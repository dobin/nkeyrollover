

class Animation(object):
    def __init__(self):
        self.frameCount = 0
        self.advanceByStep = False
        self.endless = False

        self.frameTime = None
        self.arr = []
        self.frameColors = None

        self.width = 0
        self.height = 0

        self.name = None

    def __repr__(self): 
        return str(self.name)