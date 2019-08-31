import esper
import copy
import logging

from typing import List
from sprite.coordinates import Coordinates
from entities.character import Character
from utilities.colorpalette import ColorPalette
from utilities.colortype import ColorType
from utilities.timer import Timer
from utilities.color import Color
from sprite.direction import Direction
from texture.character.characteranimationtype import CharacterAnimationType
from entities.enemy.enemyinfo import EnemyInfo

from config import Config

logger = logging.getLogger(__name__)


class Renderable():
    def __init__(
        self, texture, viewport, parent =None, coordinates =None, z =0
    ):
        self.viewport = viewport

        # coordinates
        self.coordinates = Coordinates(0, 0)
        if coordinates is not None:
            self.coordinates.x = coordinates.x
            self.coordinates.y = coordinates.y
        # For performance reason, we pre-allocate coords for use in getLocation()
        self.coordinatesRel = Coordinates(0, 0)
        self.z = z

        # texture
        self.texture = texture

        # parent
        self.parent = parent

        self.active = True
        self.rendered = True

        # color related
        self.overwriteColorTimer = Timer(0.25, active=False)
        self.overwriteColor = None

        self.direction = Direction.left
        self.name = 'none'

        ## FUCK (for enemy)
        self.enemyInfo :EnemyInfo = EnemyInfo()
        self.player = None
        self.world = None
        self.enemyMovement = None
        self.offensiveAttackEntity = None
    ## END FUCK

    def isHitBy(self, hitLocations :List[Coordinates]):
        for hitLocation in hitLocations:
            if self.collidesWithPoint(hitLocation):
                return True
        
        return False


    def __repr__(self): 
        return self.name


    def getLocation(self): 
        """Get a reference to our location.
        
        The location may depend on the parentSprite, if it is not None
        Note that we dont return a copy of the coordinates, but a reference 
        to an internal var.
        """
        if self.parent is None: 
            return self.coordinates
        else:
            parentLocation = self.parent.getLocation()

            if self.parent.direction is Direction.left:
                self.coordinatesRel.x = parentLocation.x + self.coordinates.x
                self.coordinatesRel.y = parentLocation.y + self.coordinates.y
            else: 
                self.coordinatesRel.x = parentLocation.x + (-1 * self.coordinates.x) + self.parent.texture.width - self.texture.width
                self.coordinatesRel.y = parentLocation.y + self.coordinates.y         
            return self.coordinatesRel


    def setLocation(self, coordinates :Coordinates):
        self.coordinates.x = coordinates.x
        self.coordinates.y = coordinates.y


    def getLocationCenter(self): 
        # slow, but its currently only used by rare events like skillExplosion
        loc = copy.copy(self.getLocation())
        # this will round down
        loc.x += int(self.texture.width / 2)
        loc.y += int(self.texture.height / 2)
        return loc


    def advanceStep(self):
        if not self.isActive():
            return 

        self.texture.advanceStep()


    def advance(self, deltaTime :float): 
        if not self.isActive():
            return

        self.texture.advance(deltaTime)

        # reset overwrite color
        if self.overwriteColorTimer.timeIsUp():
            self.overwriteColor = None
            self.overwriteColorTimer.stop()
        self.overwriteColorTimer.advance(deltaTime)        


    def draw(self): 
        if not self.isActive():
            return 

        if not self.isRendered():
            return

        self.texture.draw(self.viewport)


    def collidesWithPoint(self, hitCoords :Coordinates):
        if hitCoords.x >= self.coordinates.x and hitCoords.x < self.coordinates.x + self.texture.width:
            if hitCoords.y >= self.coordinates.y and hitCoords.y < self.coordinates.y + self.texture.height:
                return True

        return False


    def setOverwriteColorFor(self, time :float, color :Color):
        if self.overwriteColorTimer.isActive():
            logger.debug("Color already active on new set color")
            return 

        self.overwriteColor = color

        self.overwriteColorTimer.setTimer(time)
        self.overwriteColorTimer.reset()


    def isActive(self): 
        return self.active


    def setActive(self, active):
        self.active = active


    def isRendered(self): 
        return self.rendered
    

    def enemy_move(self, x :int =0, y :int =0):
        """Move this enemy in x/y direction, if allowed. Update direction too"""
        if x > 0:
            if self.coordinates.x < Config.columns - self.texture.width - 1:
                self.coordinates.x += 1
                
                if self.direction is not Direction.right:
                    self.direction = Direction.right
                    self.texture.changeAnimation(
                        CharacterAnimationType.walking, self.direction)  

        elif x < 0:
            if self.coordinates.x > 1:
                self.coordinates.x -= 1
                if self.direction is not Direction.left:
                    self.direction = Direction.left
                    self.texture.changeAnimation(
                        CharacterAnimationType.walking, self.direction)    

        if y > 0:
            if self.coordinates.y < Config.rows - self.texture.height - 1:
                self.coordinates.y += 1
        
        elif y < 0:
            if self.coordinates.y > 2:
                self.coordinates.y -= 1


class RenderableProcessor(esper.Processor):
    def __init__(self):
        super().__init__()

        # list of HEIGHT lists
        self.renderOrder = [[] for i in range(Config.rows + 3)]


    def process(self, dt):
        self.advance(dt)
        self.render()


    def advance(self, deltaTime):
        for ent, rend in self.world.get_component(Renderable):
            rend.advance(deltaTime)


    def render(self):
        for l in self.renderOrder: 
            l.clear()
        
        # add all elements to draw in the correct Z order
        # which is by y coordinates
        for ent, rend in self.world.get_component(Renderable):
            if rend.isActive():
                #logging.info("REND: {} {} {}".format(rend, rend.z, rend.coordinates))
                loc = rend.getLocation()
                self.renderOrder[ loc.y + rend.z ].append(rend)
            
        for l in self.renderOrder:
            for rend in l:
                rend.draw()