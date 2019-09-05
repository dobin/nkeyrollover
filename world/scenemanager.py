import logging

from world.scenes.scene0 import Scene0
from world.scenes.scene1 import Scene1
from world.scenes.scene2 import Scene2
from messaging import messaging, MessageType

logger = logging.getLogger(__name__)


class SceneManager(object):
    """Manages a scene in the game. 
    
    * Acts on player.x or viewport.x
    * Defines the viewport and its movement
    * Defines when and where enemies spawn
    * Play pre-scripted animations
    """

    def __init__(self, viewport, esperWorld):
        self.viewport = viewport
        self.currentScene = None

        self.scenes = [
            Scene0(viewport=viewport, esperWorld=esperWorld), # intro logo
            Scene1(viewport=viewport, esperWorld=esperWorld), # intro animation
            Scene2(viewport=viewport, esperWorld=esperWorld), # map
        ]
        self.currentSceneIdx = 0
        self.currentScene = self.scenes[self.currentSceneIdx]


    def initScene(self): 
        self.currentScene.enter()


    def nextScene(self):
        self.currentScene.leave()
        self.currentSceneIdx += 1
        self.currentScene = self.scenes[self.currentSceneIdx]
        logger.info("Change to scene {}: {}".format(self.currentSceneIdx, self.currentScene))
        self.initScene()


    def advance(self, dt): 
        self.currentScene.advance(dt)
        self.currentScene.handleTime()

        # handleEnemyDeath()

        if self.currentScene.sceneIsFinished():
            self.nextScene()


    def handlePosition(self, playerPosition, viewportX):
        self.currentScene.handlePosition(playerPosition, viewportX)


    def handlePlayerKeyPress(self): 
        if self.currentScene.anyKeyFinishesScene:
            self.nextScene()