import logging

from game.scenes.sceneplayground import ScenePlayground
from game.scenes.scene_logo import SceneLogo
from game.scenes.scene_intro import SceneIntro
from game.scenes.scene_mapblame import SceneMapBlame
from config import Config
from messaging import messaging, MessageType

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
        self.initAllScenes()

        self.currentSceneIdx = None
        self.currentScene = None

        if Config.playground:
            self.setScene(0)
        elif Config.devMode:
            self.setScene(1)
        else:
            self.setScene(1)


    def initAllScenes(self):
        for scene in self.scenes:
            scene.init()


    def setScene(self, idx):
        self.currentSceneIdx = idx
        self.currentScene = self.scenes[self.currentSceneIdx]

        if self.currentSceneIdx == 0:
            self.mapManager.loadMap('map02')
        if self.currentSceneIdx == 2:
            self.mapManager.loadMap('map02')


    def startScene(self):
        self.viewport.reset()
        self.currentScene.enter()

        if self.currentScene.hasEnvironment:
            # Environment is current listing for screenmove messages, which
            # are only in maps (not intro etc.)
            messaging.add(
                type = MessageType.ScreenMove,
                data = {
                    'x': 0,
                },
            )


    def nextScene(self):
        logger.info("Change to scene {}: {}".format(
            self.currentSceneIdx, self.currentScene))

        self.currentScene.leave()
        self.setScene(self.currentSceneIdx + 1)
        self.startScene()


    def restartScene(self):
        self.currentScene.leave()
        self.currentScene.init()
        self.startScene()

        if self.currentScene.isShowPlayer:
            messaging.add(
                type=MessageType.GameStart,
                data={}
            )


    def advance(self, dt):
        self.currentScene.advance(dt)
        self.currentScene.handleTime()

        if self.currentScene.sceneIsFinished():
            self.nextScene()


    def handlePlayerKeyPress(self, key):
        if self.currentScene.anyKeyFinishesScene:
            self.nextScene()

        self.currentScene.handlePlayerKeyPress(key)
