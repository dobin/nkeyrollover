#!/usr/bin/env python3

import curses, random, time, signal, sys
import logging

from entities.player.player import Player
from world.scene import Scene
from world.director import Director
from config import Config
from world.world import World

current_milli_time = lambda: int(round(time.time() * 1000))


class Keyrollover(object): 
    def __init__(self): 
        self.win = None         # canvas to draw
        self.player = None      # the player
        self.director = None    # the enemies
        self.world = None       # the world
        self.currentTime = None

        self.init()


    def init(self): 
        DEBUG_LEVELV_NUM = logging.WARN + 1 
        logging.addLevelName(DEBUG_LEVELV_NUM, "RECORD")
        def __record(self, message, *args, **kws):
            if self.isEnabledFor(DEBUG_LEVELV_NUM):
                # Yes, logger takes its '*args' as 'args'.
                self._log(DEBUG_LEVELV_NUM, message, args, **kws) 
        logging.Logger.record = __record

        if Config.devMode:
            logging.basicConfig(
                filename='app.log', 
                filemode='a', 
                level=logging.DEBUG,
                format='%(asctime)s %(levelname)07s %(name)32s: %(message)s')
        else: 
            logging.basicConfig(
                filename='app.log', 
                filemode='a', 
                level=logging.WARN,
                format='%(asctime)s %(levelname)07s %(name)32s: %(message)s')

        logger = logging.getLogger(__name__)
        logger.record("-----------------Start------------------------")

        # Create a new Curses window
        #curses.initScr()
        self.win = curses.newwin(Config.rows, Config.columns)
        curses.noecho()
        curses.cbreak()
        self.win.keypad(1) 
        curses.curs_set(0)    
        self.win.nodelay(1) # make getch() nonblocking

        # Initialize color pairs
        curses.start_color()    
        curses.init_pair(1, curses.COLOR_GREEN, 0)
        curses.init_pair(2, curses.COLOR_MAGENTA, 0)
        curses.init_pair(3, curses.COLOR_RED, 0)
        curses.init_pair(4, curses.COLOR_YELLOW, 0)
        curses.init_pair(5, curses.COLOR_BLUE, 0)
        curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(7, curses.COLOR_WHITE, 0)

        curses.init_pair(8, curses.COLOR_WHITE, curses.COLOR_GREEN)
        curses.init_pair(9, curses.COLOR_WHITE, curses.COLOR_RED)

        self.scene = Scene(self.win)

        if not Config.devMode:
            self.scene.titleScene()
            self.scene.introScene()

        self.win.clear()
        self.win.border()

        self.world = World(win=self.win)

        self.startTime = current_milli_time()
        self.currentTime = self.startTime
        self.workTime = 0

    def loop(self): 
        n = 0
        targetFrameTime = 1.0 / Config.fps
        deltaTime = targetFrameTime # we try to keep it...
        timeStart = 0
        timeEnd = 0
        workTime = 0
        while self.world.gameRunning:
            timeStart = time.time()
            self.win.erase()
            self.win.border()

            self.drawStatusbar(n)
            self.world.draw()
            self.world.advance(deltaTime)

            # has to be after draw, as getch() does a refresh
            # https://stackoverflow.com/questions/19748685/curses-library-why-does-getch-clear-my-screen
            self.world.player.getInput()
            #win.refresh()

            # fps logistics
            timeEnd = time.time()
            workTime = timeEnd - timeStart
            self.workTime = workTime
            if workTime > targetFrameTime:
                logging.warn("Could not keep FPS!")

            targetSleepTime = targetFrameTime - workTime
            if targetSleepTime < 0:
                logging.error("Sleep for negative amount: " + str(targetSleepTime))
            else:
                time.sleep(targetSleepTime)
            n = n + 1 

        # Clean up before exiting
        curses.nocbreak()
        self.win.keypad(0)
        curses.echo()
        curses.endwin()


    def drawStatusbar(self, n):
        # fps = 0
        # if n > 100: 
        #    fps = 1000 * (float)(n) / (float)(current_milli_time() - self.startTime)
        #    #fps = self.workTime * 1000.0

        s = "Health: " + str(self.world.player.characterStatus.health)
        s += "  Mana: " + str(self.world.player.characterStatus.mana)
        s += "  Points: " + str(self.world.player.characterStatus.points)

        #s += "  FPS: %.0f" % (fps)
        self.win.addstr(1, 2, s, curses.color_pair(6) | curses.A_BOLD)

        self.printSkillbar()
        #self.win.border()

        # TODO we dont use self.statusBar atm for flickering reasons
        #self.statusBarWin.erase()
        #self.statusbarWin.refresh()


    def printSkillbar(self): 
        skills = self.world.player.skills

        basex = 54
        n = 0
        for skill in skills.skillStatus: 
            if skills.isRdy(skill): 
                self.win.addstr(1, basex + n, skill, curses.color_pair(8) | curses.A_BOLD)
            else: 
                self.win.addstr(1, basex + n, skill, curses.color_pair(9))

            n += 1

        weaponIdx = 70
        self.win.addstr(1, 
            weaponIdx, 
            'W: ' + self.world.player.characterAttack.getWeaponStr(), 
            curses.color_pair(6))


def signal_handler(sig, frame):
    # Clean up before exiting
    curses.nocbreak()
    curses.echo()
    curses.endwin()

    sys.exit(0)


def main(stdscr):
    signal.signal(signal.SIGINT, signal_handler)
    keyrollover = Keyrollover()
    keyrollover.loop()
    

if __name__ == '__main__':
    curses.wrapper(main)