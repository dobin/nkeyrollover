import logging

logger = logging.getLogger(__name__)


class SceneBase(object): 
    def __init__(self, world, viewport, hasEnvironment=False):
        self.world = world
        self.viewport = viewport

        # scene data
        self.start_x = 0
        self.end_x = 0
        self.enemies = []

        # local
        self.entities = []

        # properties
        self.anyKeyFinishesScene = False
        self.name = None

        self.isShowPlayer = False
        self.isShowMap = False

        self.hasEnvironment = hasEnvironment


    def __repr__(self):
        return self.name

    def showPlayer(self):
        return self.isShowPlayer

    def showMap(self):
        return self.isShowMap


    def getStartX(self):
        return self.start_x


    def getEndX(self):
        return self.end_x


    def enter(self):
        pass


    def sceneIsFinished(self) -> bool:
        pass


    def advance(self, dt):
        pass


    def handlePosition(self, playerPosition, viewportX, numEnemiesAlive):
        pass

    def handleTime(self):
        pass

    def handleEnemyDeath(self):
        pass

    def handlePlayerKeyPress(self, key):
        pass


    def init(self):
        pass

    def leave(self):
        for entity in self.entities:
            self.removeRenderable(entity)


    def addRenderable(self, component):
        entity = self.world.create_entity()
        self.world.add_component(entity, component)
        self.entities.append(entity)
        return entity


    def removeRenderable(self, entity):
        logger.info("Remove Entity H: {}".format(entity))
        self.world.delete_entity(entity)
