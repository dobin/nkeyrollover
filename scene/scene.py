import curses
import time
from config import Config

from entities.entity import Entity
from entities.entitytype import EntityType
from entities.action import Action
from entities.direction import Direction
from sprite.charactersprite import CharacterSprite
from sprite.phenomenasprite import PhenomenaSprite

class Scene(object):
    def __init__(self, win):
        self.win = win

    def title(self):
        # Display welcome screen and wait for key press
        self.win.clear()
        self.win.border()
        self.win.refresh()    

        self.loop()        
        q = self.win.getch() # wait for key to start game


    def getLocation(self):
        return { 'x': 15, 'y': 5}

    def loop(self):
        timeStart = 0
        timeEnd = 0
        workTime = 0
        n = 0         
        targetFrameTime = 1.0 / Config.fps
        deltaTime = targetFrameTime # we try to keep it...

        entity = Entity(self.win, self, EntityType.player)
        sprite = PhenomenaSprite(Action.roflcopter, entity)
        sprite.isActive = True
        sprite.initSprite(Action.roflcopter, Direction.left, 0)

        while True:
            timeStart = time.time()

            self.win.addstr(5, 40, "N Key Rollover", curses.color_pair(3))
            
            #if n % 50 == 0:
            #    sprite.advanceStep()
            sprite.advance(deltaTime)
            sprite.draw(self.win)

            timeEnd = time.time()

            workTime = timeEnd - timeStart
            self.win.refresh()

            time.sleep(targetFrameTime - workTime)
            self.win.addstr(6, 40, "Adventures of ASCIIMAN", curses.color_pair(3))

            n = n + 1