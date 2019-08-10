import math
import logging
import curses

from sprite.coordinates import Coordinates
from utilities.timer import Timer
from utilities.utilities import Utility

logger = logging.getLogger(__name__)


class Particle(object):
    def __init__(
        self,
        viewport =None,
        x :int =0,
        y :int =0, 
        life :int =0,
        angle :float =0, 
        speed :int =1,
        fadeout :bool =True,
        charType :int =0,
        byStep :bool =False,
        active :bool =False
    ):
        self.viewport = viewport
        self.movementTimer = Timer()
        self.init(
            x=x, y=y, life=life, angle=angle, speed=speed, fadeout=fadeout, 
            byStep=byStep, charType=charType, active=active)
        

    def init(
        self,
        x :int =0,
        y :int =0, 
        life :int =0,
        angle :float =0, 
        speed :int =1,
        fadeout :bool =True,
        byStep :bool =False,
        charType :int =0,
        active :bool =False
    ):
        self.x = x
        self.y = y
        self.life = life
        self.originalLife = life
        self.angle = angle
        self.speed = speed
        self.fadeout = fadeout
        self.byStep = byStep
        self.charType = charType

        self.angleInRadians = angle * math.pi / 180
        self.velocity = {
            'x': speed * math.cos(self.angleInRadians),
            'y': -speed * math.sin(self.angleInRadians)
        }

        self.color = None
        self.colorOpt = 0
        self.setColor()
        self.setChar()

        self.rx = 0.0
        self.ry = 0.0

        self.movementTimer.setTimer(self.speed)
        self.active = active


    def advance(self, dt):
        if self.active is False: 
            return

        if self.byStep: 
            return

        self.movementTimer.advance(dt)

        self.makeStep(dt)


    def setColor(self): 
        if self.viewport is None:
            # for simple unittests
            return

        # for unittests using MockWin
        # we always import 'curses', and dont know if we are being unittested
        # in the unittest, we use MockWin, which has method isUnitTest
        if hasattr(self.viewport, 'isUnitTest'):
            self.color = 0
            return

        self.color = curses.color_pair(7)

        if self.life > (self.originalLife / 2):
            self.colorOpt = curses.A_BOLD
        else: 
            self.colorOpt = 0


    def setChar(self): 
        if self.charType == 0: 
            if self.life > ((self.originalLife / 3) * 2):
                self.char = 'O'
            elif self.life < ((self.originalLife / 3) * 1):
                self.char = '.'
            else: 
                self.char = 'o'


    def makeStep(self, dt):
        if self.life <= 0:
            self.active = False
            return

        if self.fadeout:
            self.setColor()
        self.setChar()

        if self.speed > 0:
            xFloat = self.velocity['x'] * (dt * 100) + self.rx
            yFloat = self.velocity['y'] * (dt * 100) + self.ry

            xChange = int(round(xFloat))
            yChange = int(round(yFloat))

            # accumulate pos we could not handle yet
            changeRestX = xFloat - xChange - self.rx
            changeRestY = yFloat - yChange - self.ry 

            self.rx += changeRestX
            self.ry += changeRestY

            # change pos
            self.x += xChange
            self.y += yChange

            if False:
                print("")
                print("Real change:  X: {}  Y: {}".format(xFloat, yFloat))
                print("Round change: X: {}  Y: {}".format(xChange, yChange))
                print("Change Rest:  X: {}  Y: {}".format(changeRestX, changeRestY))
                print("New    Rest:  X: {}  Y: {}".format(self.rx, self.ry))
                print("New    Pos:   X: {}  Y: {}".format(self.x, self.y))
                print("")
                
        self.life -= 1


    def draw(self):
        self.viewport.addstr(self.y, self.x, self.char, self.color | self.colorOpt)


    def isActive(self): 
        return self.active