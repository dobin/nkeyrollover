import unittest
import time
import logging
#import tests.mockcurses as curses
import curses

from entities.player.player import Player
from entities.enemy.enemy import Enemy
from config import Config
from world.director import Director
from sprite.direction import Direction
from utilities.utilities import Utility
from sprite.sprite import Sprite
from sprite.coordinates import Coordinates
from tests.fakeworld import FakeWorld
from world.world import World


def worldPlayer():
    logging.basicConfig(
        filename='app.log', 
        filemode='a', 
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)07s %(name)32s: %(message)s')

    # curses
    doCurses = True
    if doCurses:
        curses.initscr()
        win = curses.newwin(Config.rows, Config.columns)
        curses.noecho()
        curses.cbreak()
        win.keypad(1) 
        curses.curs_set(0)    
        win.nodelay(1) # make getch() nonblocking
        # Initialize color pairs
        curses.start_color()    
        curses.init_pair(1, curses.COLOR_GREEN, 0)
        curses.init_pair(2, curses.COLOR_MAGENTA, 0)
        curses.init_pair(3, curses.COLOR_RED, 0)
        curses.init_pair(4, curses.COLOR_YELLOW, 0)
        curses.init_pair(5, curses.COLOR_BLUE, 0)
        curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(7, curses.COLOR_WHITE, 0)
        win.clear()
        win.border()
        # end curses
    else: 
        win = None

    world = World(win)
    world.director.maxEnemies = 0

    while True:
        win.erase()

        world.draw()
        world.advance(0.01)

        if world.player.getInput():
            playerScreenCoords = world.viewport.getScreenCoords ( world.player.getLocation() )

            if playerScreenCoords.x == 30:
                world.viewport.x -= 1

            if playerScreenCoords.x == 20:
                world.viewport.x += 1

        time.sleep(0.01)


if __name__ == '__main__':
    worldPlayer()