import logging

from game.scenes.sceneplayground import ScenePlayground
from game.scenes.scene0 import Scene0
from game.scenes.scene1 import Scene1
from game.scenes.scene2 import Scene2
from config import Config

logger = logging.getLogger(__name__)


class SceneManager(object):
    """Manages a scene in the game.
    * Acts on player.x or viewport.x
    * Defines the viewport and its movement
    * Defines when and where enemies spawn
    * Play pre-scripted animations
    """

    def __init__(self, viewport, world, mapManager):
        self.viewport = viewport
        self.currentScene = None
        self.mapManager = mapManager

        self.scenes = [
            ScenePlayground(viewport=viewport, world=world),  # playground
            Scene0(viewport=viewport, world=world),  # intro logo
            Scene1(viewport=viewport, world=world),  # intro animation
            Scene2(viewport=viewport, world=world),  # map
        ]

        if Config.playground:
            self.currentSceneIdx = 0
        else:
            self.currentSceneIdx = 1

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
            self.mapManager.loadMap('map02')
        self.initScene()


    def advance(self, dt):
        self.currentScene.advance(dt)
        self.currentScene.handleTime()

        # handleEnemyDeath()

        if self.currentScene.sceneIsFinished():
            self.nextScene()


    def handlePlayerKeyPress(self, key):
        if self.currentScene.anyKeyFinishesScene:
            self.nextScene()

        self.currentScene.handlePlayerKeyPress(key)
