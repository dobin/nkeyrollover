

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
        self.originalDirection = None


    def getAnimationLength(self):
        n = 0

        if self.frameTime is None:
            raise Exception("Animation {}: Frametime is none (wrong call?)".format(
                self.name))

        for frameTime in self.frameTime:
            n += frameTime
        return n


    def __repr__(self):
        return str(self.name)
