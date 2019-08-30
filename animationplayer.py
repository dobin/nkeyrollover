#!/usr/bin/env python

import copy
import unittest
import time
import sys
import logging
import curses
#import tests.mockcurses as curses

from entities.entity import Entity
from entities.entitytype import EntityType
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
from world.viewport import Viewport
from utilities.colorpalette import ColorPalette
from tests.fakeworld import FakeWorld


class AnimationTest(object):
    def __init__(self): 
        self.viewport = None

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
            ColorPalette.cursesInitColor()
            win.clear()
            win.border()
            # end curses
        else: 
            win = None

        self.win = win
        self.viewport = Viewport(win=win, world=None)


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
        #world = FakeWorld(self.win)
        world = FakeWorld(self.win, fakeViewPort=False, withDirector=False)
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

        p = Particle(viewport=self.viewport, x=20, y=20, life=10, 
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
            x = 15,
            y = 15,
        )
        particleEmiter.emit(loc, ParticleEffectType.cleave, direction=Direction.right)

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
                particleEmiter.emit(loc, ParticleEffectType.cleave, direction=Direction.right)

            self.win.refresh()
            time.sleep(dt) 


    def playAllParticles(self, loc, particleEmiter): 
        n = 0
        for effect in ParticleEffectType: 
            loc.x += n
            loc.y += 1
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

            n = 0
            while n < 3: 
                self.viewport.addstr(16, 10 + (n*10), str(n))
                n += 1

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
        print("Give argument: animations,particles,explosion,particle")
        sys.exit(1)

    animationTest = AnimationTest()
    animationTest.init()
    animationTest.play(sys.argv[1])
    animationTest.cleanup()