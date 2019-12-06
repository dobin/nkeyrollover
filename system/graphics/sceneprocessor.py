import logging
from enum import Enum
import esper

from messaging import messaging, MessageType
from config import Config
import system.gamelogic.ai
import system.graphics.renderable
from utilities.timer import Timer
from directmessaging import directMessaging, DirectMessageType
from utilities.entityfinder import EntityFinder
from texture.phenomena.phenomenatype import PhenomenaType
from common.coordinates import Coordinates
from common.direction import Direction

logger = logging.getLogger(__name__)


class State(Enum):
    pushToNextScene = 0
    pushToEnemies = 1
    brawl = 2

    gameover = 3
    start = 4


class SceneProcessor(esper.Processor):
    def __init__(self, viewport, sceneManager):
        super().__init__()
        self.viewport = viewport
        self.sceneManager = sceneManager
        self.xCenter = Config.columns / 2 - 5
        self.state = State.start
        self.screenMoveTimer = Timer(0.1)
        self.lastKnownPlayerPos = None
        self.gameoverTimer = Timer(3.0, active=False)  # show gameover for this long


    def setState(self, state):
        logging.debug("Set to state: {}".format(state))
        self.state = state


    def process(self, dt):
        self.screenMoveTimer.advance(dt)
        self.gameoverTimer.advance(dt)

        for message in messaging.getByType(MessageType.Gameover):
            self.gameoverTimer.reset()
            self.gameoverTimer.start()
            self.setState(State.gameover)
            messaging.add(
                type=MessageType.EmitPhenomenaTexture,
                data={
                    'phenomenaTextureType': PhenomenaType.gameover,
                    'location': Coordinates(10, 10),
                    'staticLocation': True,
                    'direction': Direction.right,
                    'physics': False,
                }
            )

        if self.state is State.gameover:
            for message in messaging.getByType(MessageType.PlayerKeypress):
                if self.gameoverTimer.timeIsUp():
                    messaging.add(
                        type=MessageType.ClearRenderables,
                        data={}
                    )

                    self.setState(State.start)
        elif self.state is State.start:
            self.sceneManager.restartScene()
            self.setState(State.brawl)


        for message in messaging.getByType(MessageType.EntityDying):
            # if no enemies are alive, we want to go to the next akt
            if self.numEnemiesAlive() == 0:
                self.screenMoveTimer.start()

                if self.state is not State.gameover:
                    self.setState(State.pushToNextScene)
            break

        for message in messaging.getByType(MessageType.PlayerLocation):
            self.lastKnownPlayerPos = message.data

            if self.state is State.pushToNextScene:
                # if suddenly enemies appear, let the player free
                if self.numEnemiesVisible() > 0:
                    self.setState(State.brawl)

            if self.state is State.brawl:
                if (self.numEnemiesVisible() == 0
                        and not self.enemiesLeftOfChar(self.lastKnownPlayerPos.x)):
                    self.screenMoveTimer.start()
                    self.setState(State.pushToEnemies)

            if self.state is State.pushToEnemies:
                if self.numEnemiesVisible() > 0:
                    self.setState(State.brawl)

            playerScreenCoords = self.viewport.getScreenCoords(
                message.data)

            # adjust viewport on move
            if self.state is State.pushToNextScene:
                # screen follows player
                # player is left side of screen (screen pushes player right)
                if playerScreenCoords.x != 10:
                    distance = int(playerScreenCoords.x - 10)
                    if distance < 0:
                        self.adjustViewport(-1)
                        self.screenMoveTimer.reset()
                    elif distance > 0:
                        self.adjustViewport(1)
                        self.screenMoveTimer.reset()

            elif self.state is State.pushToEnemies:
                # screen follows player
                # player is middle of the screen
                if playerScreenCoords.x != self.xCenter:
                    distance = int(playerScreenCoords.x - self.xCenter)
                    if distance < 0:
                        self.adjustViewport(-1)
                        self.screenMoveTimer.reset()
                    elif distance > 0:
                        self.adjustViewport(1)
                        self.screenMoveTimer.reset()

            elif self.state is State.brawl:
                if not self.enemiesLeftOfChar(self.lastKnownPlayerPos.x):
                    # player can move freely
                    # coming close to left/right of the screen will move it
                    if playerScreenCoords.x >= Config.moveBorderRight:
                        distance = playerScreenCoords.x - Config.moveBorderRight
                        self.adjustViewport(distance)
                    if playerScreenCoords.x <= Config.moveBorderLeft:
                        distance = playerScreenCoords.x - Config.moveBorderLeft
                        self.adjustViewport(distance)
            # /adjust viewport on move

            # let the scene decide if we need more enemies
            self.sceneManager.currentScene.handlePosition(
                message.data,
                self.viewport.getx(),
                self.numEnemiesAlive())

        for message in messaging.getByType(MessageType.PlayerKeypress):
            key = message.data['key']
            self.sceneManager.handlePlayerKeyPress(key)

            if key == ord('k'):
                logger.info("Scene: Kill All Enemies")
                self.killAllEnemies()

            if key == ord('n'):
                logger.info("Scene: Go to next part")
                self.killAllEnemies()
                enemyCell = self.sceneManager.currentScene.getNextEnemy()

                playerEntity = EntityFinder.findPlayer(self.world)
                meGroupId = self.world.component_for_entity(
                    playerEntity, system.groupid.GroupId)
                renderable = self.world.component_for_entity(
                    playerEntity, system.graphics.renderable.Renderable)

                distX = enemyCell.spawnX - renderable.coordinates.x

                directMessaging.add(
                    groupId = meGroupId.getId(),
                    type = DirectMessageType.movePlayer,
                    data = {
                        'x': distX,
                        'y': 0,
                        'dontChangeDirection': False,
                        'whenMoved': None,
                    },
                )

        # move screen animation
        if self.screenMoveTimer.timeIsUp() and self.lastKnownPlayerPos is not None:
            playerScreenCoords = self.viewport.getScreenCoords(
                self.lastKnownPlayerPos)

            if self.state is State.pushToNextScene:
                # screen follows player
                # player is left side of screen (screen pushes player right)
                if playerScreenCoords.x != 10:
                    distance = int(playerScreenCoords.x - 10)
                    if distance < 0:
                        self.adjustViewport(-1)
                        self.screenMoveTimer.reset()
                    elif distance > 0:
                        self.adjustViewport(1)
                        self.screenMoveTimer.reset()

                else:
                    self.screenMoveTimer.stop()

            elif self.state is State.pushToEnemies:
                # screen follows player
                # player is middle of the screen
                if playerScreenCoords.x != self.xCenter:
                    distance = int(playerScreenCoords.x - self.xCenter)
                    if distance < 0:
                        self.adjustViewport(-1)
                        self.screenMoveTimer.reset()
                    elif distance > 0:
                        self.adjustViewport(1)
                        self.screenMoveTimer.reset()
                else:
                    self.screenMoveTimer.stop()


        self.sceneManager.advance(dt)


    def adjustViewport(self, xoff):
        viewportChanged = self.viewport.adjustViewport(xoff)
        if viewportChanged:
            messaging.add(
                type = MessageType.ScreenMove,
                data = {
                    'x': xoff,
                },
            )


    def killAllEnemies(self):
        for _, ai in self.world.get_component(system.gamelogic.ai.Ai):
            ai.brain.pop()
            ai.brain.push('dead')


    def numEnemiesAlive(self) -> int:
        count = 0
        for _, ai in self.world.get_component(system.gamelogic.ai.Ai):
            if ai.brain.state.name != 'dead' and ai.brain.state.name != 'dying':
                count += 1

        return count


    def numEnemiesVisible(self) -> int:
        count = 0
        for _, (ai, renderable) in self.world.get_components(
                system.gamelogic.ai.Ai, system.graphics.renderable.Renderable):
            if (ai.brain.state.name != 'dead' and ai.brain.state.name != 'dying'
                    and renderable.coordinates.x > self.viewport.getx()
                    and renderable.coordinates.x < self.viewport.getRightX()):
                count += 1

        return count


    def enemiesLeftOfChar(self, playerX):
        for _, (ai, renderable) in self.world.get_components(
                system.gamelogic.ai.Ai, system.graphics.renderable.Renderable):
            if (ai.brain.state.name != 'dead' and ai.brain.state.name != 'dying'
                    and renderable.coordinates.x < playerX):
                return True

        return False
