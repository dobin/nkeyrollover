#!/usr/bin/env python

import curses, random, time
import logging

from entities.player.player import Player
from scene.scene import Scene
from entities.action import Action
from director import Director
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
        if Config.devMode:
            logging.basicConfig(
                filename='app.log', 
                filemode='a', 
                level=logging.DEBUG,
                format='%(asctime)s %(levelname)07s %(name)s: %(message)s')
        else: 
            logging.basicConfig(
                filename='app.log', 
                filemode='a', 
                level=logging.INFO,
                format='%(asctime)s %(levelname)07s %(name)s: %(message)s')
        logging.info("-----------------Start------------------------")

        # Create a new Curses window
        #curses.initScr()
        self.win = curses.newwin(Config.rows, Config.columns)
        curses.noecho()
        curses.cbreak()
        self.win.keypad(1) 
        curses.curs_set(0)    

        # Initialize color pairs
        curses.start_color()    
        curses.init_pair(1, curses.COLOR_GREEN, 0)
        curses.init_pair(2, curses.COLOR_BLUE, 0)
        curses.init_pair(3, curses.COLOR_RED, 0)
        curses.init_pair(4, curses.COLOR_YELLOW, 0)
        curses.init_pair(5, curses.COLOR_MAGENTA, 0)
        curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_BLACK)

        # Game variables
        speed = 1

        self.scene = Scene(self.win)
        #scene.title()

        self.win.clear()
        self.win.border()
        self.win.nodelay(1) # make getch() nonblocking

        self.world = World(win=self.win)

        self.startTime = current_milli_time()
        self.currentTime = self.startTime

    def loop(self): 
        n = 0
        targetFrameTime = 1.0 / Config.fps
        deltaTime = targetFrameTime # we try to keep it...
        timeStart = 0
        timeEnd = 0
        workTime = 0
        while True:
            timeStart = time.time()
            #logging.debug("Iteration")
            self.win.erase()
            self.win.border()

            #self.director.drawEnemies()
            #self.director.advanceEnemies(deltaTime)
            self.drawStatusbar(n)

            #self.player.draw()
            #self.player.advance(deltaTime)

            self.world.draw()
            self.world.advance(deltaTime)

            # has to be after draw, as getch() does a refresh
            # https://stackoverflow.com/questions/19748685/curses-library-why-does-getch-clear-my-screen
            self.world.player.getInput()
            #win.refresh()

            #self.collisionDetection()
            #self.director.worldUpdate()

            timeEnd = time.time()
            workTime = timeEnd - timeStart
            if workTime > targetFrameTime:
                logging.warn("Could keep FPS!")

            time.sleep(targetFrameTime - workTime)
            n = n + 1

        # Clean up before exiting
        curses.nocbreak()
        self.win.keypad(0)
        curses.echo()
        curses.endwin()


    def drawStatusbar(self, n):
        fps = 0
        if n > 100: 
            fps = 1000 * (float)(n) / (float)(current_milli_time() - self.startTime)

        s = "Health: " + str(self.world.player.characterStatus.health)
        s += "    Mana: " + str(self.world.player.characterStatus.mana)
        s += "    Points: " + str(self.world.player.characterStatus.points)
        s += "    FPS: %.0f" % (fps)
        self.win.addstr(1, 2, s, curses.color_pair(6))

        self.win.border()

        # TODO we dont use self.statusBar atm for flickering reasons
        #self.statusBarWin.erase()
        #self.statusbarWin.refresh()


    def collisionDetection(self):
        if not self.player.characterWeapon.isHitting():
            return

        # player hits enemies
        if not self.player.characterWeapon.collisionDetectionDone: 
            hitCoords = self.player.characterWeapon.getHitCoordinates()
            self.director.collisionDetection(hitCoords)
            self.player.characterWeapon.collisionDetectionDone = True
        

        # enemies hit player


def main(stdscr):
    keyrollover = Keyrollover()
    keyrollover.loop()



if __name__ == '__main__':
    curses.wrapper(main)