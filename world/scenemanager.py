import logging

from world.scenes.scene0 import Scene0
from world.scenes.scene1 import Scene1
from world.scenes.scene2 import Scene2

logger = logging.getLogger(__name__)


class SceneManager(object):
    """Manages a scene in the game. 
    * Acts on player.x or viewport.x
    * Defines the viewport and its movement
    * Defines when and where enemies spawn
    * Play pre-scripted animations
    """

    def __init__(self, viewport, world, map):
        self.viewport = viewport
        self.currentScene = None
        self.map = map

        self.scenes = [
            Scene0(viewport=viewport, world=world),  # intro logo
            Scene1(viewport=viewport, world=world),  # intro animation
            Scene2(viewport=viewport, world=world),  # map
        ]
        self.currentSceneIdx = 0
        self.currentScene = self.scenes[self.currentSceneIdx]


    def initScene(self):
        self.currentScene.enter()


    def nextScene(self):
        self.currentScene.leave()
        self.currentSceneIdx += 1
        self.currentScene = self.scenes[self.currentSceneIdx]
        logger.info("Change to scene {}: {}".format(
            self.currentSceneIdx, self.currentScene))

        if self.currentSceneIdx == 2:
            logging.error("loadmap")
            self.map.loadMap('map02')
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