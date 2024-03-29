#!/usr/bin/env python3.7

from asciimatics.screen import Screen
import time
import signal
import sys
import logging
import locale
import yaml

from config import Config
from game.game import Game
from utilities.utilities import Utility
from system.io.keyboardinput import KeyboardInput

fpsOverrun = []
frameCount = 0


class Keyrollover(object):
    def __init__(self, screen):
        self.win = screen
        self.menuwin = None
        self.game = None
        self.init()


    def init(self):
        locale.setlocale(locale.LC_ALL, '')
        Utility.setupLogger()
        self.loadConfig()

        if Config.devMode:
            logging.basicConfig(
                filename='nkeyrollover.log',
                filemode='a',
                level=logging.INFO,
                format='%(asctime)s %(levelname)-07s %(name)32s: %(message)s')
        else:
            logging.basicConfig(
                filename='nkeyrollover.log',
                filemode='a',
                level=logging.INFO,
                format='%(asctime)s %(levelname)-07s %(name)32s: %(message)s')

        logger = logging.getLogger(__name__)
        logger.record("-----------------Start------------------------")

        self.game = Game(win=self.win, menuwin=self.menuwin)
        self.keyboardInput = KeyboardInput(
            game=self.game,
            viewport=self.game.viewport)


    def loadConfig(self):
        with open("nkeyrollover.yaml", 'r') as stream:
            try:
                d = yaml.safe_load(stream)
                if 'isdevmode' in d:
                    Config.devMode = d['isdevmode']
            except yaml.YAMLError as exc:
                logging.error(exc)


    def loop(self):
        global frameCount
        global fpsOverrun

        n = 0
        targetFrameTime = 1.0 / Config.fps  # we try to keep it...
        timeStart = 0
        timeEnd = 0
        workTime = 0

        while self.game.gameRunning:
            timeStart = time.time()

            self.game.draw1(n)
            self.game.advance(targetFrameTime, n)
            self.game.draw2(n)

            self.keyboardInput.getInput()
            self.win.refresh()

            # fps logistics
            timeEnd = time.time()
            workTime = timeEnd - timeStart
            if workTime > targetFrameTime:
                logging.warning("{}: Could not keep FPS! Worktime was: {}ms".format(
                    n, workTime * 100.0))
                fpsOverrun.append(workTime * 100.0)

            targetSleepTime = targetFrameTime - workTime
            if targetSleepTime < 0:
                logging.debug("Sleep for negative amount: " + str(targetSleepTime))
            else:
                time.sleep(targetSleepTime)
            n = n + 1
            frameCount = n


def evaluateFpsOverrun():
    logging.info("Frm: {}".format(frameCount))
    percent = (len(fpsOverrun) / frameCount) * 100
    logging.info("Cnt: {} ({}%)".format(len(fpsOverrun), percent))
    #logging.info("All: {}".format(fpsOverrun))
    if len(fpsOverrun) > 0:
        logging.info("Max: {}".format(max(fpsOverrun)))


def signal_handler(sig, frame):
    evaluateFpsOverrun()
    sys.exit(0)


def main(screen):
    signal.signal(signal.SIGINT, signal_handler)
    keyrollover = Keyrollover(screen)
    keyrollover.loop()


if __name__ == '__main__':
    Screen.wrapper(main, unicode_aware=True)
