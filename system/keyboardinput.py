import curses

from utilities.timer import Timer
from config import Config

from system.renderable import Renderable


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
            #ent, () self.world.esperWorld.components_for_entity(self.world.player, Velocity).x = -3
            #for ent, (renderable, tPlayer) in self.world.get_components(Renderable, tPlayer):
            playerRenderable = self.world.esperWorld.component_for_entity(self.world.player, Renderable)
            player = playerRenderable.r

            player.characterStatus.handleKeyPress(time=self.world.getGameTime())


            if key == ord(' '):
                player.brain.pop()
                player.brain.push('attack')
                player.characterAttack.attack()

            if key == ord('1'):
                player.characterAttack.switchWeaponByKey('1')

            if key == ord('2'):
                player.characterAttack.switchWeaponByKey('2')

            if key == ord('3'):
                player.characterAttack.switchWeaponByKey('3')

            if key == ord('4'):
                player.characterAttack.switchWeaponByKey('4')

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
                    player.move(x=-1, y=0)
                    return True

                elif key == curses.KEY_RIGHT: 
                    player.move(x=1, y=0)
                    return True

                elif key == curses.KEY_UP:
                    player.move(x=0, y=-1)
                    return True

                elif key == curses.KEY_DOWN: 
                    player.move(x=0, y=1)
                    return True


    def advance(self, deltaTime):
        self.movementTimer.advance(deltaTime)