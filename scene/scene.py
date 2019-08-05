import curses
import time
import logging 
from enum import Enum

from config import Config
from entities.entity import Entity
from entities.entitytype import EntityType
from texture.phenomenatype import PhenomenaType
from entities.direction import Direction
from texture.characteranimationtype import CharacterAnimationType
from sprite.charactersprite import CharacterSprite
from sprite.phenomenasprite import PhenomenaSprite
from utilities.timer import Timer

logger = logging.getLogger(__name__)

class SceneState(Enum): 
    wait1 = 0       # wait 1s
    flydown = 1     # fly heli down
    drop = 2        # drop asciiman
    flyup = 3       # fly up
    done = 4        # start the game


class Scene(object):
    def __init__(self, win):
        self.win = win

    def title(self):
        self.win.clear()
        self.win.border()
        self.win.refresh()    

        self.loop()


    def getLocation(self):
        return { 'x': 15, 'y': -5}


    def loop(self):
        timeStart = 0
        timeEnd = 0
        workTime = 0
        n = 0         
        targetFrameTime = 1.0 / Config.fps
        deltaTime = targetFrameTime # we try to keep it...

        entityCopter = Entity(win=self.win, parentEntity=self, entityType=EntityType.player)
        spriteCopter = PhenomenaSprite(phenomenaType=PhenomenaType.roflcopter, parentEntity=entityCopter)
        spriteCopter.setActive(False)

        entityPlayer = Entity(win=self.win, parentEntity=self, entityType=EntityType.player)
        spritePlayer = CharacterSprite(characterAnimationType=CharacterAnimationType.standing, parentEntity=entityPlayer)
        spritePlayer.setActive(False)

        myTimer = Timer(0.5)
        state = SceneState.wait1
        logging.debug("To State: Wait1")

        while True:
            timeStart = time.time()
            self.win.erase()
            self.win.border()

            # static
            self.win.addstr(5, 40, "N Key Rollover", curses.color_pair(3))
            self.win.addstr(6, 40, "Adventures of ASCIIMAN", curses.color_pair(3))

            # state
            if state is SceneState.wait1:
                # for next scene: Flydown
                if myTimer.timeIsUp():
                    state = SceneState.flydown
                    myTimer.setTimer(0.1)
                    spriteCopter.setActive(True)
                    logging.debug("To State: Flydown")
            elif state is SceneState.flydown:
                if myTimer.timeIsUp():
                    myTimer.reset()
                    entityCopter.offsetY += 1

                # for next scene: Drop
                if entityCopter.offsetY == 12: 
                    myTimer.setTimer(0.1)
                    logging.debug("To State: Drop")
                    state = SceneState.drop
                    entityPlayer.offsetY = 18
                    entityPlayer.offsetX = 8
                    spritePlayer.setActive(True)                    

            elif state is SceneState.drop: 
                # for next scene: Flyup
                if myTimer.timeIsUp():
                    myTimer.reset()
                    entityCopter.offsetY -= 1

                if entityCopter.offsetY == -5:
                    state = SceneState.done

            elif state is SceneState.done: 
                logging.info("A: " + str(entityPlayer.getLocation()))
                break

            # elements
            spritePlayer.advance(deltaTime)
            spritePlayer.draw(self.win)            
            spriteCopter.advance(deltaTime)
            spriteCopter.draw(self.win)


            # input
            key = self.win.getch()
            if key != -1:
                break

            # advance
            myTimer.advance(deltaTime)

            timeEnd = time.time()
            workTime = timeEnd - timeStart
            time.sleep(targetFrameTime - workTime)

            n = n + 1