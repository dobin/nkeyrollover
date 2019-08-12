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
from world.viewport import Viewport

logger = logging.getLogger(__name__)


class IntroSceneState(Enum):
    wait1 = 1       # wait 1s
    flydown = 2     # fly heli down
    drop = 3        # drop asciiman
    flyup = 4       # fly up
    done = 5        # start the game

            

class Scene(object):
    """Play predefined scripts on the screen"""

    def __init__(self, win):
        self.win = win
        self.viewport = Viewport(win=win, world=None)


    def titleScene(self):
        targetFrameTime = 1.0 / Config.fps
        deltaTime = targetFrameTime # we try to keep it..
        
        worldSprite = Sprite(viewport=self.viewport, parentSprite=None)

        entityIntro = Entity(viewport=self.viewport, parentSprite=worldSprite, entityType=EntityType.player)
        textureIntro = PhenomenaTexture(phenomenaType=PhenomenaType.intro, parentSprite=entityIntro)
        entityIntro.setLocation(Coordinates(2, 5))
        textureIntro.setActive(True)

        # entityIntro.setColor( curses.color_pair(10) )

        myTimer = Timer(3)
            
        while True:
            self.win.erase()
            #self.win.border()

            if myTimer.timeIsUp(): 
                break

            self.win.addstr(24, 75,  Config.version, curses.color_pair(1))
            # advance
            myTimer.advance(deltaTime)
            textureIntro.advance(deltaTime)
            textureIntro.draw(self.viewport)

            # input
            key = self.win.getch()
            if key != -1:
                break

            time.sleep(targetFrameTime)


    def introScene(self):
        self.win.clear()
        self.win.border()
        self.win.refresh()    

        timeStart = 0
        timeEnd = 0
        workTime = 0
        n = 0         
        targetFrameTime = 1.0 / Config.fps
        deltaTime = targetFrameTime # we try to keep it...

        worldSprite = Sprite(viewport=self.viewport, parentSprite=None)

        entityCopter = Entity(viewport=self.viewport, parentSprite=worldSprite, entityType=EntityType.player)
        textureCopter = PhenomenaTexture(phenomenaType=PhenomenaType.roflcopter, parentSprite=entityCopter)
        entityCopter.setLocation(Coordinates(13, -5))        
        textureCopter.setActive(False)

        entityPlayer = Entity(viewport=self.viewport, parentSprite=worldSprite, entityType=EntityType.player)
        texturePlayer = CharacterTexture(characterAnimationType=CharacterAnimationType.standing, parentSprite=entityPlayer)
        texturePlayer.setActive(False)

        myTimer = Timer(0.5)
        state = IntroSceneState.wait1

        while True:
            timeStart = time.time()
            self.win.erase()
            self.win.border()

            # static
            if state is IntroSceneState.wait1 or state is IntroSceneState.flydown or state is IntroSceneState.drop or state is IntroSceneState.flyup:
                self.win.addstr(5, 40,  "N Key Rollover", curses.color_pair(3))
                self.win.addstr(6, 40,  "Adventures of ASCIIMAN", curses.color_pair(3))
                self.win.addstr(8, 40,  "Select attack: 1 2 3 4", curses.color_pair(4))
                self.win.addstr(9, 40,  "Attack       : space", curses.color_pair(4))
                self.win.addstr(10, 40, "Skills       : q w e r", curses.color_pair(4))
                self.win.addstr(11, 40, "Heal, Port   : f g", curses.color_pair(4))

            # state
            if state is IntroSceneState.wait1:
                # for next scene: Flydown
                if myTimer.timeIsUp():
                    state = IntroSceneState.flydown
                    myTimer.setTimer(0.1)
                    textureCopter.setActive(True)
                    logger.debug("Scene: Go to State: Flydown")
            elif state is IntroSceneState.flydown:
                if myTimer.timeIsUp():
                    myTimer.reset()
                    entityCopter.coordinates.y += 1

                # for next scene: Drop
                if entityCopter.coordinates.y == 8: 
                    myTimer.setTimer(0.1)
                    logger.debug("Scene: Go to State: Drop")
                    state = IntroSceneState.drop
                    entityPlayer.coordinates.x = 24
                    entityPlayer.coordinates.y = 13
                    texturePlayer.setActive(True)                    

            elif state is IntroSceneState.drop: 
                # for next scene: Flyup
                if myTimer.timeIsUp():
                    myTimer.reset()
                    entityCopter.coordinates.y -= 1

                if entityCopter.coordinates.y == -5:
                    state = IntroSceneState.done

            elif state is IntroSceneState.done: 
                break

            # elements
            texturePlayer.advance(deltaTime)
            texturePlayer.draw(self.viewport)            
            textureCopter.advance(deltaTime)
            textureCopter.draw(self.viewport)

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