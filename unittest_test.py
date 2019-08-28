#!/usr/bin/env python

import unittest
import time
import logging
#import tests.mockcurses as curses
import curses

from entities.characterattack import CharacterAttack
from entities.entity import Entity
from entities.entitytype import EntityType
from entities.player.player import Player
from entities.enemy.enemy import Enemy
from config import Config
from world.director import Director
from sprite.direction import Direction
from utilities.utilities import Utility
from sprite.sprite import Sprite
from sprite.coordinates import Coordinates
from tests.fakeworld import FakeWorld

logger = logging.getLogger(__name__)


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
    world.getPlayer().setLocation( Coordinates(10, 10))
    world.getPlayer().direction = Direction.left

    enemy = Enemy(win, world.worldSprite, None, world, 'bot')
    enemy.setLocation(Coordinates(4, 10))
    world.director.enemiesAlive.append(enemy)

    logger.info("LIFE1: " + str(enemy.characterStatus.health))
    life1 = enemy.characterStatus.health
    world.getPlayer().handleInput(ord('3')) # select first weapon
    world.getPlayer().advance(0.1)
    enemy.advance(0.1)
    world.getPlayer().handleInput(ord(' ')) # fire
    logger.info("LIFE2: " + str(enemy.characterStatus.health))
    life2 = enemy.characterStatus.health
    world.getPlayer().advance(0.1)
    enemy.advance(0.1)
    life3 = enemy.characterStatus.health
    logger.info("LIFE3: " + str(enemy.characterStatus.health))

    locs = Utility.getBorderHalf(world.getPlayer().getLocationCenter(), distance=2, width=1)

    if doCurses:
        enemy.draw()
        world.getPlayer().draw()
        for loc in locs: 
            win.addstr(loc.y, loc.x, ',') 

        win.refresh()
        time.sleep(2)


if __name__ == '__main__':
    test_weaponHit()