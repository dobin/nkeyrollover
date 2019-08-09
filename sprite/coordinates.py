

class Coordinates(object): 
    def __init__(self, x :int =0, y :int =0): 
        self.x = x
        self.y = y

    def __repr__(self): 
        return "{}/{}".format(self.x, self.y)