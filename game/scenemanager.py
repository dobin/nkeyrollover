import logging

from game.scenes.sceneplayground import ScenePlayground
from game.scenes.scene_logo import SceneLogo
from game.scenes.scene_intro import SceneIntro
from game.scenes.scene_mapblame import SceneMapBlame
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
            ScenePlayground(viewport=viewport, world=world),
            SceneLogo(viewport=viewport, world=world),
            SceneIntro(viewport=viewport, world=world),
            SceneMapBlame(viewport=viewport, world=world),
        ]

        if Config.playground:
            self.currentSceneIdx = 0
        else:
            self.currentSceneIdx = 1

        self.currentScene = self.scenes[self.currentSceneIdx]


    def initScene(self):
        if self.currentSceneIdx == 0:
            self.mapManager.loadMap('map02')
        if self.currentSceneIdx == 2:
            self.mapManager.loadMap('map02')

        self.currentScene.enter()


    def nextScene(self):
        self.currentScene.leave()
        self.currentSceneIdx += 1
        self.currentScene = self.scenes[self.currentSceneIdx]
        logger.info("Change to scene {}: {}".format(
            self.currentSceneIdx, self.currentScene))

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
