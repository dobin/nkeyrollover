

class ObjectCache(object):
    def __init__(self, size=8):
        self.cache = []


    def addObject(self, object):
        self.cache.append(object)


    def getObject(self):
        return self.cache.pop(0)
