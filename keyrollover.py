#!/usr/bin/env python

import curses, random, time
from player.player import Player
from enemy.enemy import Enemy
from scene.scene import Scene
import logging


ROWS = 25
COLUMNS = 80
FPS = 50



def main(stdscr):
    logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
    logging.warning('This will get logged to a file')

    # Create a new Curses window
    #curses.initScr()
    win = curses.newwin(ROWS, COLUMNS)    
    curses.noecho()
    curses.cbreak()
    win.keypad(1)
    curses.curs_set(0)    

    # Initialize color pairs
    curses.start_color()    
    curses.init_pair(1, curses.COLOR_GREEN, 0)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_WHITE)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_CYAN)    

    # Game variables
    speed = 1
    
    scene = Scene(win)
    #scene.title()
    
    win.clear()
    win.border()
    win.nodelay(1) # make getch() nonblocking

    player = Player(win)
    enemy = Enemy(win)

    n = 0
    while True: 
        win.erase()
        win.border()
        
        win.addstr(1, 75, str(n))

        enemy.draw()
        enemy.advance()

        player.draw()
        player.advance()
        # has to be after draw, as getch() does a refresh
        # https://stackoverflow.com/questions/19748685/curses-library-why-does-getch-clear-my-screen
        player.getInput()
        #win.refresh()

        time.sleep(0.02)
        n = n + 1


    # Clean up before exiting
    curses.nocbreak()
    win.keypad(0)
    curses.echo()
    curses.endwin()


if __name__ == '__main__':
    curses.wrapper(main)