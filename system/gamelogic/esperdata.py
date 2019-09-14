

class EsperData(object):
    def __init__(self, world, entity, name):
        self.world = world
        self.entity = entity
        self.name = name


    def __repr__(self):
        return self.name
