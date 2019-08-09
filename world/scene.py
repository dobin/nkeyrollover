import curses
import time
import logging 
from enum import Enum

from config import Config
from entities.entity import Entity
from entities.entitytype import EntityType
from texture.phenomena.phenomenatype import PhenomenaType
from sprite.direction import Direction
from texture.character.characteranimationtype import CharacterAnimationType
from texture.character.charactertexture import CharacterTexture
from texture.phenomena.phenomenatexture import PhenomenaTexture
from sprite.sprite import Sprite
from utilities.timer import Timer
from sprite.coordinates import Coordinates

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


    def loop(self):
        timeStart = 0
        timeEnd = 0
        workTime = 0
        n = 0         
        targetFrameTime = 1.0 / Config.fps
        deltaTime = targetFrameTime # we try to keep it...

        worldSprite = Sprite(win=self.win, parentSprite=None)
     

        entityCopter = Entity(win=self.win, parentSprite=worldSprite, entityType=EntityType.player)
        textureCopter = PhenomenaTexture(phenomenaType=PhenomenaType.roflcopter, parentSprite=entityCopter)
        entityCopter.setLocation(Coordinates(13, -5))        
        textureCopter.setActive(False)

        entityPlayer = Entity(win=self.win, parentSprite=worldSprite, entityType=EntityType.player)
        texturePlayer = CharacterTexture(characterAnimationType=CharacterAnimationType.standing, parentSprite=entityPlayer)
        texturePlayer.setActive(False)

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
                    textureCopter.setActive(True)
                    logging.debug("Scene: Go to State: Flydown")
            elif state is SceneState.flydown:
                if myTimer.timeIsUp():
                    myTimer.reset()
                    entityCopter.coordinates.y += 1

                # for next scene: Drop
                if entityCopter.coordinates.y == 8: 
                    myTimer.setTimer(0.1)
                    logging.debug("Scene: Go to State: Drop")
                    state = SceneState.drop
                    entityPlayer.coordinates.x = 24
                    entityPlayer.coordinates.y = 13
                    texturePlayer.setActive(True)                    

            elif state is SceneState.drop: 
                # for next scene: Flyup
                if myTimer.timeIsUp():
                    myTimer.reset()
                    entityCopter.coordinates.y -= 1

                if entityCopter.coordinates.y == -5:
                    state = SceneState.done

            elif state is SceneState.done: 
                logging.info("A: " + str(entityPlayer.getLocation()))
                break

            # elements
            texturePlayer.advance(deltaTime)
            texturePlayer.draw(self.win)            
            textureCopter.advance(deltaTime)
            textureCopter.draw(self.win)


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