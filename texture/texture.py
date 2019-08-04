class Texture(object): 
    def __init__(self): 
        self.width = 0
        self.height = 0
        self.frameCount = 0

        self.advanceByStep = False
        self.endless = False

        self.frameTime = []
        self.arr = []
