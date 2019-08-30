#!/usr/bin/env python3

import curses, random, time, signal, sys
import logging

from entities.player.player import Player
from world.scene import Scene
from config import Config
from world.world import World
from utilities.colorpalette import ColorPalette
from utilities.colortype import ColorType
from utilities.utilities import Utility

from system.gamelogic.attackable import Attackable


import locale 
current_milli_time = lambda: int(round(time.time() * 1000))


class Keyrollover(object): 
    def __init__(self): 
        self.win = None         # canvas to draw
        self.menuwin = None
        self.world = None       # the world, with all textures and units
        self.currentTime = None
        self.init()


    def init(self): 
        locale.setlocale(locale.LC_ALL, '')
        Utility.setupLogger()

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
                level=logging.INFO,
                format='%(asctime)s %(levelname)07s %(name)32s: %(message)s')

        logger = logging.getLogger(__name__)
        logger.record("-----------------Start------------------------")

        self.menuwin = curses.newwin(3, Config.columns, 0, 0)
        self.menuwin.border()

        self.win = curses.newwin(Config.rows, Config.columns, 2, 0)
        curses.noecho()
        curses.cbreak()
        self.win.keypad(1) 
        curses.curs_set(0)    
        self.win.nodelay(1) # make getch() nonblocking
        ColorPalette.cursesInitColor()

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
            # keep inputrate below half FPS (50/s by default)
            if n % 2 == 0:
                self.world.getPlayer().getInput()
            else: 
                self.win.refresh()

            # fps logistics
            timeEnd = time.time()
            workTime = timeEnd - timeStart
            self.workTime = workTime
            if workTime > targetFrameTime:
                logging.warn("Could not keep FPS! Worktime was: {}ms".format( self.workTime * 100.0))

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

        #self.menuwin.erase()
        #self.menuwin.border()
        
        s = "Health: " + str(self.world.esperWorld.component_for_entity(self.world.player, Attackable).getHealth())
        s += "  Mana: " + str(self.world.getPlayer().characterStatus.mana)
        s += "  Points: " + str(self.world.getPlayer().characterStatus.points)

        #s += "  FPS: %.0f" % (fps)
        color = ColorPalette.getColorByColorType(ColorType.menu, None)
        self.menuwin.addstr(1, 2, s, color )

        self.printSkillbar(color)
        self.menuwin.refresh()


    def printSkillbar(self, color): 
        skills = self.world.getPlayer().skills

        basex = 54
        n = 0
        for skill in skills.skillStatus: 
            if skills.isRdy(skill): 
                self.menuwin.addstr(1, basex + n, skill, curses.color_pair(9))
            else: 
                self.menuwin.addstr(1, basex + n, skill, curses.color_pair(10))

            n += 1

        weaponIdx = 62
        self.menuwin.addstr(1, 
            weaponIdx, 
            'W:' + self.world.getPlayer().characterAttack.getWeaponStr(), 
            color)

        weaponIdx = 62
        self.menuwin.addstr(1, 
            weaponIdx, 
            'APM:' + str(int(self.world.getPlayer().characterStatus.getApm().getApm() * 60)), 
            color)


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