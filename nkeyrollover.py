#!/usr/bin/env python3

import curses, time, signal, sys
import logging
import locale

from config import Config
from world.game import Game
from utilities.utilities import Utility
from system.io.keyboardinput import KeyboardInput
from utilities.colorpalette import ColorPalette


class Keyrollover(object):
    def __init__(self):
        self.win = None
        self.menuwin = None
        self.game = None
        self.currentTime = None
        self.init()


    def getTimeMs(self): 
        return int(round(time.time() * 1000))


    def init(self):
        locale.setlocale(locale.LC_ALL, '')
        Utility.setupLogger()

        if Config.devMode:
            logging.basicConfig(
                filename='app.log',
                filemode='a',
                level=logging.INFO,
                format='%(asctime)s %(levelname)-07s %(name)32s: %(message)s')
        else:
            logging.basicConfig(
                filename='app.log',
                filemode='a',
                level=logging.WARNING,
                format='%(asctime)s %(levelname)-07s %(name)32s: %(message)s')

        logger = logging.getLogger(__name__)
        logger.record("-----------------Start------------------------")

        self.menuwin = curses.newwin(3, Config.columns, 0, 0)
        self.menuwin.border()

        self.win = curses.newwin(Config.rows, Config.columns, 2, 0)
        curses.noecho()
        curses.cbreak()
        self.win.keypad(1)
        curses.curs_set(0)
        self.win.nodelay(1)  # make getch() nonblocking
        ColorPalette.cursesInitColor()

        self.win.clear()
        self.win.border()

        self.game = Game(win=self.win, menuwin=self.menuwin)
        self.keyboardInput = KeyboardInput(game=self.game)

        self.startTime = self.getTimeMs()
        self.currentTime = self.startTime
        self.workTime = 0


    def loop(self):
        n = 0
        targetFrameTime = 1.0 / Config.fps
        deltaTime = targetFrameTime  # we try to keep it...
        timeStart = 0
        timeEnd = 0
        workTime = 0
        while self.game.gameRunning:
            timeStart = time.time()
            self.win.erase()
            self.win.border()

            self.game.draw1(n)
            self.game.advance(deltaTime, n)
            self.game.draw2(n)
            self.keyboardInput.advance(deltaTime)

            # has to be after draw, as getch() does a refresh
            # https://stackoverflow.com/questions/19748685/curses-library-why-does-getch-clear-my-screen
            self.keyboardInput.getInput()

            # fps logistics
            timeEnd = time.time()
            workTime = timeEnd - timeStart
            self.workTime = workTime
            if workTime > targetFrameTime:
                logging.warning("{}: Could not keep FPS! Worktime was: {}ms".format(
                    n, self.workTime * 100.0))

            targetSleepTime = targetFrameTime - workTime
            if targetSleepTime < 0:
                logging.debug("Sleep for negative amount: " + str(targetSleepTime))
            else:
                time.sleep(targetSleepTime)
            n = n + 1

        # Clean up before exiting
        curses.nocbreak()
        self.win.keypad(0)
        curses.echo()
        curses.endwin()


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
