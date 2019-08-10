#!/usr/bin/env python

import copy
import unittest
import time
import sys
import logging
import curses
#import tests.mockcurses as curses

from entities.characterattack import CharacterAttack
from entities.entity import Entity
from entities.entitytype import EntityType
from entities.player.player import Player
from entities.enemy.enemy import Enemy
from config import Config
from world.director import Director
from sprite.direction import Direction
from texture.character.charactertexture import CharacterTexture
from texture.character.characteranimationtype import CharacterAnimationType
from utilities.timer import Timer
from sprite.particle import Particle
from world.particleemiter import ParticleEmiter
from world.particleeffecttype import ParticleEffectType
from sprite.sprite import Sprite
from sprite.coordinates import Coordinates


class FakeWorld(object): 
    def __init__(self, win): 
        self.win = win
        self.worldSprite = Sprite(win=win, parentSprite=None)
        self.player = Player(win, self.worldSprite, None, self)
        self.director = Director(win, self) # real director

    def getPlayer(self):
        return self.player


class AnimationTest(object):
    def __init__(self): 
        self.win = None

    def init(self): 
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

        self.win = win


    def cleanup(self): 
        # Clean up before exiting
        curses.nocbreak()
        self.win.keypad(0)
        curses.echo()
        curses.endwin()


    def play(self, type):
        if type == 'animations':
            self.playAllAnimations()
        elif type == 'particle':
            self.playParticle()
        elif type == 'explosion':
            self.playParticleExplosion()
        elif type == 'particles':
            self.playParticles()


    def playAllAnimations(self):
        world = FakeWorld(self.win)
        sprites = []

        n = 0
        for animationType in CharacterAnimationType:
            characterTexture = CharacterTexture(
                parentSprite=world.worldSprite, 
                characterAnimationType=animationType,
                direction=Direction.right)

            characterTexture.setLocation(2 + (n * 5), 1)
            characterTexture.setActive(True)

            sprites.append(characterTexture)

            n += 1

        stepTimer = Timer(0.5)
        while True:
            self.win.erase()
            stepTimer.advance(0.01)

            # enemy.draw()
            for sprite in sprites:
                sprite.draw(self.win)
                sprite.advance(0.01)
                
            if stepTimer.timeIsUp():
                for sprite in sprites:
                    sprite.advanceStep()
                stepTimer.reset()

            key = self.win.getch()
            if key != -1:
                if key == 27: # esc
                    break

                if key == ord('r'): 
                    for sprite in sprites: 
                        sprite.resetAnimation()
                        sprite.setActive(True)

            self.win.refresh()
            time.sleep(0.01)


    def playParticle(self): 
        sprites = []

        p = Particle(win=self.win, x=20, y=20, life=10, 
            angle=10, speed=1.2, active=True)
        sprites.append(p)

        while True:
            self.win.erase()

            # enemy.draw()
            for sprite in sprites:
                sprite.draw()
                sprite.advance(0.01)
                
            key = self.win.getch()
            if key != -1:
                if key == 27: # esc
                    break

                if key == ord('r'): 
                    p.init(x=20, y=20, life=10, 
                            angle=10, speed=1.2, active=True)

            self.win.refresh()
            time.sleep(0.01)


    def playParticleExplosion(self): 
        particleEmiter = ParticleEmiter(self.win)
        loc = Coordinates(
            x = 10,
            y = 10,
        )
        particleEmiter.emit(loc, ParticleEffectType.explosion)

        dt = 0.01
        while True:
            self.win.erase()

            particleEmiter.advance(dt)
            particleEmiter.draw()

            key = self.win.getch()
            if key != -1:
                if key == 27: # esc
                    break

            if key == ord('r'): 
                particleEmiter.emit(loc, ParticleEffectType.explosion)

            self.win.refresh()
            time.sleep(dt) 


    def playAllParticles(self, loc, particleEmiter): 
        n = 0
        for effect in ParticleEffectType: 
            loc.x += n
            particleEmiter.emit(loc, effect)
            n += 10


    def playParticles(self): 
        particleEmiter = ParticleEmiter(self.win)

        loc = Coordinates(
            x = 10,
            y = 10,
        )
        self.playAllParticles(copy.copy(loc), particleEmiter)


        dt = 0.01
        while True:
            self.win.erase()

            particleEmiter.advance(dt)
            particleEmiter.draw()

            key = self.win.getch()
            if key != -1:
                if key == 27: # esc
                    break

            if key == ord('r'): 
                self.playAllParticles(copy.copy(loc), particleEmiter)

            self.win.refresh()
            time.sleep(dt) 


if __name__ == '__main__':
    if len(sys.argv) == 1: 
        print("Give argument.")
        sys.exit(1)

    animationTest = AnimationTest()
    animationTest.init()
    animationTest.play(sys.argv[1])
    animationTest.cleanup()