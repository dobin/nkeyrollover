#!/usr/bin/env python

import curses, random, time
from player.player import Player
from scene.scene import Scene
import logging
from player.action import Action
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
        logging.basicConfig(filename='app.log', filemode='w', level=logging.DEBUG,
            format='%(levelname)s %(name)s: %(message)s')

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
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_WHITE)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_CYAN)    

        # Game variables
        speed = 1

        self.scene = Scene(self.win)
        #scene.title()

        self.win.clear()
        self.win.border()
        self.win.nodelay(1) # make getch() nonblocking

        self.player = Player(win=self.win, parent=None, coordinates={ 'max_y': Config.columns, 'max_x': Config.rows })
        self.director = Director(self.win)
        self.world = World(self.win)

        self.startTime = current_milli_time()
        self.currentTime = self.startTime

    def loop(self): 
        n = 0
        while True: 
            self.win.erase()
            self.win.border()

            self.director.drawEnemies()
            self.director.advanceEnemies()
            self.drawStatusbar(n)

            self.player.draw()
            self.player.advance()

            self.world.draw()
            self.world.advance()

            # has to be after draw, as getch() does a refresh
            # https://stackoverflow.com/questions/19748685/curses-library-why-does-getch-clear-my-screen
            self.player.getInput()
            self.director.getInput(self.player.getLocation())
            #win.refresh()

            self.collisionDetection()
            self.director.worldUpdate()
            time.sleep( 1.0 / Config.fps)
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

        s = "Health: " + str(self.player.playerStatus.health)
        s += "    Mana: " + str(self.player.playerStatus.mana)
        s += "    Points: " + str(self.player.playerStatus.points)
        s += "    FPS: %.0f" % (fps)
        self.win.addstr(1, 2, s)

        self.win.border()

        # we dont use self.statusBar atm for flickering reasons
        #self.statusBarWin.erase()
        #self.statusbarWin.refresh()


    def collisionDetection(self):
        if not self.player.playerHit.isHitting():
            return

        # player hits enemies
        if not self.player.playerHit.collisionDetectionDone: 
            hitCoords = self.player.playerHit.getHitCoordinates()
            self.director.collisionDetection(hitCoords)
            self.player.playerHit.collisionDetectionDone = True
        

        # enemies hit player


def main(stdscr):
    keyrollover = Keyrollover()
    keyrollover.loop()



if __name__ == '__main__':
    curses.wrapper(main)