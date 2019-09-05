import logging
import random




class SceneBase(object): 
    def __init__(self, esperWorld, viewport): 
        self.esperWorld = esperWorld
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


    def sceneIsFinished(self) -> bool: 
        pass


    def advance(self, dt): 
        pass


    def handlePosition(self, playerPosition, viewportX):
        pass

    def handleTime(self): 
        pass

    def handleEnemyDeath(self):
        pass


    def leave(self): 
        for entity in self.entities:
            self.removeRenderable(entity)


    def addRenderable(self, sprite):
        entity = self.esperWorld.create_entity()
        self.esperWorld.add_component(entity, sprite)
        self.entities.append(entity)
        return entity


    def removeRenderable(self, entity): 
        self.esperWorld.delete_entity(entity)

