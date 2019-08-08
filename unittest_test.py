#!/usr/bin/env python

import unittest
import time
import logging

from entities.characterattack import CharacterAttack
from entities.entity import Entity
from entities.entitytype import EntityType
from entities.player.player import Player
from entities.enemy.enemy import Enemy
from config import Config
from director import Director
from entities.direction import Direction
import tests.mockcurses as curses
from utilities.utilities import Utility

class FakeWorld(object): 
    def __init__(self, win): 
        self.win = win
        self.worldEntity = Entity(win=win, parentEntity=None, entityType=EntityType.world)
        self.player = Player(win, self.worldEntity, None, self)
        self.director = Director(win, self) # real director

    def getPlayer(self):
        return self.player




def test_weaponHit():
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

    world = FakeWorld(win)
    world.player.setLocation(10, 10)
    world.player.direction = Direction.left

    enemy = Enemy(win, world.worldEntity, None, world, 'bot')
    enemy.setLocation(4, 10)
    world.director.enemiesAlive.append(enemy)

    logging.info("LIFE1: " + str(enemy.characterStatus.health))
    life1 = enemy.characterStatus.health
    world.player.handleInput(ord('3')) # select first weapon
    world.player.advance(0.1)
    enemy.advance(0.1)
    world.player.handleInput(ord(' ')) # fire
    logging.info("LIFE2: " + str(enemy.characterStatus.health))
    life2 = enemy.characterStatus.health
    world.player.advance(0.1)
    enemy.advance(0.1)
    life3 = enemy.characterStatus.health
    logging.info("LIFE3: " + str(enemy.characterStatus.health))

    locs = Utility.getBorder(world.player.getLocationCenter(), distance=2, width=1)

    if doCurses:
        enemy.draw()
        world.player.draw()
        for loc in locs: 
            win.addstr(loc['y'], loc['x'], ',') 

        win.refresh()
        time.sleep(2)




if __name__ == '__main__':
    test_weaponHit()