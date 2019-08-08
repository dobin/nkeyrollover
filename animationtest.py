#!/usr/bin/env python

import unittest
import time
import sys

from entities.characterattack import CharacterAttack
from entities.entity import Entity
from entities.entitytype import EntityType
from entities.player.player import Player
from entities.enemy.enemy import Enemy
from config import Config
from director import Director
from entities.direction import Direction
from sprite.charactersprite import CharacterSprite
from texture.characteranimationtype import CharacterAnimationType
from utilities.timer import Timer
from sprite.particle import Particle

import logging
#import tests.mockcurses as curses
import curses


class FakeWorld(object): 
    def __init__(self, win): 
        self.win = win
        self.worldEntity = Entity(win=win, parentEntity=None, entityType=EntityType.world)
        self.player = Player(win, self.worldEntity, None, self)
        self.director = Director(win, self) # real director

    def getPlayer(self):
        return self.player



def testPlayAnimation():
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

    args = 'particle'

    sprites = []

    n = 0
    if args == 'all':
        for animationType in CharacterAnimationType:
            characterSprite = CharacterSprite(
                parentEntity=world.worldEntity, 
                characterAnimationType=animationType,
                direction=Direction.right)

            characterSprite.setLocation(2 + (n * 5), 1)
            characterSprite.setActive(True)

            sprites.append(characterSprite)

            n += 1

    if args == 'particle':
        p = Particle(x=20, y=20, life=40, angle=10, speed=0.2, active=True)
        sprites.append(p)


    stepTimer = Timer(0.5)
    while True:
        win.erase()
        stepTimer.advance(0.01)

        # enemy.draw()
        for sprite in sprites:
            sprite.draw(win)
            sprite.advance(0.01)
            
        if stepTimer.timeIsUp():
            for sprite in sprites:
                sprite.advanceStep()
            stepTimer.reset()

        key = win.getch()
        if key != -1:
            if key == 27: # esc
                break

            if key == ord('r'): 
                for sprite in sprites: 
                    sprite.resetAnimation()
                    sprite.setActive(True)

        win.refresh()
        time.sleep(0.01)

    # Clean up before exiting
    curses.nocbreak()
    win.keypad(0)
    curses.echo()
    curses.endwin()


if __name__ == '__main__':
    testPlayAnimation()