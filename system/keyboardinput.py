import curses

from utilities.timer import Timer
from config import Config
from sprite.direction import Direction
from utilities.utilities import Utility
from texture.character.characteranimationtype import CharacterAnimationType

from system.offensiveattack import OffensiveAttack

from system.renderable import Renderable
from system.gamelogic.player import Player

from messaging import messaging, Messaging, Message, MessageType


class KeyboardInput(object):
    def __init__(self, world): 
        self.world = world
        self.viewport = world.viewport


    def getInput(self):
        gotInput = False
        key = self.viewport.win.getch()
        while key != -1:
            gotInput = True
            self.handleInput(key)
            key = self.viewport.win.getch()

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

            messaging.add(
                type=MessageType.PlayerKeypress, 
                data=key)

            # player related
            playerRenderable = self.world.esperWorld.component_for_entity(self.world.player, Renderable)
            playerAttack = self.world.esperWorld.component_for_entity(self.world.characterAttackEntity, OffensiveAttack)

            player = self.world.esperWorld.component_for_entity(self.world.player, Player)

            player.characterStatus.handleKeyPress(time=self.world.getGameTime())

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


    def advance(self, deltaTime):
        pass
