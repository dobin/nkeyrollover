#!/usr/bin/env python

import curses, random, time
from player.player import Player
from enemy.enemy import Enemy
from scene.scene import Scene
import logging
from player.action import Action


ROWS = 25
COLUMNS = 80
FPS = 50

class Keyrollover(object): 
    def __init__(self): 
        logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
        logging.warning('This will get logged to a file')

        # Create a new Curses window
        #curses.initScr()
        self.win = curses.newwin(ROWS, COLUMNS)
        curses.noecho()
        curses.cbreak()
        self.win.keypad(1)
        curses.curs_set(0)    

        self.statusBarWin = curses.newwin(3, COLUMNS, 0, 0)

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

        self.player = Player(self.win)
        self.enemy = Enemy(self.win)

        self.statusBarWin.border()

    def loop(self): 
        n = 0
        while True: 
            self.win.erase()
            self.win.border()

            self.enemy.draw()
            self.enemy.advance()

            self.player.draw()
            self.player.advance()
            # has to be after draw, as getch() does a refresh
            # https://stackoverflow.com/questions/19748685/curses-library-why-does-getch-clear-my-screen
            self.player.getInput()
            #win.refresh()

            self.collisionDetection()
            self.drawStatusbar(n)
            time.sleep(0.02)
            n = n + 1

        # Clean up before exiting
        curses.nocbreak()
        self.win.keypad(0)
        curses.echo()
        curses.endwin()

    def drawStatusbar(self, n):
        s = "Health: " + str(self.player.playerStatus.health)
        s += "    Mana: " + str(self.player.playerStatus.mana)
        s += "    Points: " + str(self.player.playerStatus.points)
        
        self.statusBarWin.addstr(1, 2, s)
        self.statusBarWin.addstr(1, 73, str(n))
        self.statusBarWin.refresh()


    def collisionDetection(self):
        if not self.player.playerHit.isHitting():
            return

        hitCoords = self.player.playerHit.getHitCoordinates()

        if self.enemy.collidesWithPoint(hitCoords):
            self.enemy.getHit(50)


def main(stdscr):
    keyrollover = Keyrollover()
    keyrollover.loop()



if __name__ == '__main__':
    curses.wrapper(main)