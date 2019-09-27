
class ExtCoordinates(object):
    def __init__(self, x :int =0, y :int =0, width = None, height = None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def __repr__(self):
        return "{}/{} w:{} h:{}".format(self.x, self.y, self.width, self.height)


class Coordinates(object):
    def __init__(self, x :int =0, y :int =0):
        self.x = x
        self.y = y

    def __repr__(self):
        return "{}/{}".format(self.x, self.y)
