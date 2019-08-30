import curses

from utilities.timer import Timer
from config import Config
from sprite.direction import Direction
from utilities.utilities import Utility
from texture.character.characteranimationtype import CharacterAnimationType

from system.offensiveattack import OffensiveAttack

from system.renderable import Renderable
from system.gamelogic.tplayer import tPlayer

class KeyboardInput(object):
    def __init__(self, world): 
        self.world = world
        self.viewport = world.viewport
        self.movementTimer = Timer( 1.0 / Config.movementKeysPerSec, instant=True)


    def getInput(self):
        gotInput = False
        didMove = False
        key = self.viewport.win.getch()
        while key != -1:
            gotInput = True
            didMoveTmp = self.handleInput(key)
            if didMoveTmp: 
                didMove = True
            key = self.viewport.win.getch()

        # to allow diagonal movement, we allow multiple movement keys per input
        # cycle, without resetting the timer.
        if didMove: 
            self.movementTimer.reset()
        
        return gotInput


    def handleInput(self, key):
            # game related
            if key == ord('p'):
                self.world.togglePause()

            if key == 27: # esc
                self.world.quitGame()

            if key == 265: # f1
                self.world.toggleStats()

            if key == 266: # f2
                self.world.toggleShowEnemyWanderDestination()                

            # player related
            playerRenderable = self.world.esperWorld.component_for_entity(self.world.player, Renderable)
            playerAttack = self.world.esperWorld.component_for_entity(self.world.characterAttackEntity, OffensiveAttack)

            player = self.world.esperWorld.component_for_entity(self.world.player, tPlayer)

            player.characterStatus.handleKeyPress(time=self.world.getGameTime())

            if key == ord(' '):
                player.brain.pop()
                player.brain.push('attack')
                playerAttack.attack()

            if key == ord('1'):
                playerAttack.switchWeaponByKey('1')

            if key == ord('2'):
                playerAttack.switchWeaponByKey('2')

            if key == ord('3'):
                playerAttack.switchWeaponByKey('3')

            if key == ord('4'):
                playerAttack.switchWeaponByKey('4')

            if key == ord('c'):
                player.skills.doSkill('c')

            if key == ord('f'):
                player.skills.doSkill('f')

            if key == ord('g'):
                player.skills.doSkill('g')

            if key == ord('q'):
                player.skills.doSkill('q')

            if key == ord('w'):
                player.skills.doSkill('w')

            if key == ord('e'):
                player.skills.doSkill('e')

            if key == ord('r'):
                player.skills.doSkill('r')

            if self.movementTimer.timeIsUp(): 
                if key == curses.KEY_LEFT:
                    self.move(playerRenderable, player, x=-1, y=0)
                    return True

                elif key == curses.KEY_RIGHT: 
                    self.move(playerRenderable, player, x=1, y=0)
                    return True

                elif key == curses.KEY_UP:
                    self.move(playerRenderable, player, x=0, y=-1)
                    return True

                elif key == curses.KEY_DOWN: 
                    self.move(playerRenderable, player, x=0, y=1)
                    return True


    def move(self, playerRenderable, player, x=0, y=0):
        currentDirection = playerRenderable.direction
        if x < 0:
            if Utility.isPointMovable(
                playerRenderable.coordinates.x - 1, 
                playerRenderable.coordinates.y, 
                playerRenderable.texture.width, 
                playerRenderable.texture.height
            ):
                playerRenderable.coordinates.x -= 1
                playerRenderable.direction = Direction.left
                self.movePlayer(playerRenderable, player, currentDirection == playerRenderable.direction )
        elif x > 0: 
            if Utility.isPointMovable(
                playerRenderable.coordinates.x + 1, 
                playerRenderable.coordinates.y, 
                playerRenderable.texture.width, 
                playerRenderable.texture.height
            ):
                playerRenderable.coordinates.x += 1
                playerRenderable.direction = Direction.right
                self.movePlayer(playerRenderable, player, currentDirection == playerRenderable.direction )

        if y < 0:
            if Config.moveDiagonal:
                if Utility.isPointMovable(
                    playerRenderable.coordinates.x + 1, 
                    playerRenderable.coordinates.y - 1, 
                    playerRenderable.texture.width, 
                    playerRenderable.texture.height
                ):
                    playerRenderable.coordinates.y -= 1
                    playerRenderable.coordinates.x += 1
                    self.movePlayer(playerRenderable, player, currentDirection == playerRenderable.direction )
            else: 
                if Utility.isPointMovable(
                    playerRenderable.coordinates.x, 
                    playerRenderable.coordinates.y - 1, 
                    playerRenderable.texture.width, 
                    playerRenderable.texture.height
                ):
                    playerRenderable.coordinates.y -= 1
                    self.movePlayer(playerRenderable, player, currentDirection == playerRenderable.direction )
        if y > 0: 
            if Config.moveDiagonal:
                if Utility.isPointMovable(
                    playerRenderable.coordinates.x - 1, 
                    playerRenderable.coordinates.y + 1, 
                    playerRenderable.texture.width, 
                    playerRenderable.texture.height
                ):
                    playerRenderable.coordinates.y += 1
                    playerRenderable.coordinates.x -= 1
                    self.movePlayer(playerRenderable, player, currentDirection == playerRenderable.direction )
            else:
                if Utility.isPointMovable(
                    playerRenderable.coordinates.x, 
                    playerRenderable.coordinates.y + 1, 
                    playerRenderable.texture.width, 
                    playerRenderable.texture.height
                ):
                    playerRenderable.coordinates.y += 1
                    self.movePlayer(playerRenderable, player, currentDirection == playerRenderable.direction )


    def movePlayer(self, playerRenderable, player, sameDirection):
        # move window
        playerScreenCoords = self.viewport.getScreenCoords ( 
            playerRenderable.getLocation() )
        if playerScreenCoords.x >= Config.moveBorderRight:
            self.viewport.adjustViewport(1)
        if playerScreenCoords.x <= Config.moveBorderLeft:
            self.viewport.adjustViewport(-1)

        if not sameDirection:
            playerRenderable.texture.changeAnimation(
                CharacterAnimationType.walking, playerRenderable.direction)

        # walking animation
        playerRenderable.advanceStep()

        currentState = player.brain.state
        if currentState.name == 'walking': 
            # keep him walking a bit more
            currentState.setTimer(1.0)
        else: 
            player.brain.pop()
            player.brain.push('walking')


    def advance(self, deltaTime):
        self.movementTimer.advance(deltaTime)