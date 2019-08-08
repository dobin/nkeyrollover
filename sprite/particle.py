import math
import logging
import curses

from utilities.timer import Timer
from utilities.utilities import Utility

logger = logging.getLogger(__name__)


class Particle(object):
    def __init__(
        self,
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

        self.color = curses.color_pair(7)
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

        self.makeStep()
        #if self.movementTimer.timeIsUp():
        #    self.makeStep()
        #    self.movementTimer.reset()


    def advanceStep(self):
        if self.active is False: 
            return

        if not self.byStep: 
            return

        self.makeStep()


    def setColor(self): 
        if self.life > (self.originalLife / 2):
            self.colorOpt = curses.A_BOLD
        else: 
            self.colorOpt = 0


    def setChar(self): 
        if self.charType == 0: 
            if self.life > ((self.originalLife / 3) * 1):
                self.char = 'O'
            elif self.life > ((self.originalLife / 3) * 2):
                self.char = 'o'
            else: 
                self.char = '.'


    def makeStep(self):
        if self.life <= 0:
            self.active = False
            return

        if self.fadeout:
            self.setColor()
        self.setChar()

        xFloat = self.velocity['x'] + self.rx
        yFloat = self.velocity['y'] + self.ry

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

        #logging.info("Real change:  X: {}  Y: {}".format(xFloat, yFloat))
        #logging.info("Round change: X: {}  Y: {}".format(xChange, yChange))
        #logging.info("Change Rest:  X: {}  Y: {}".format(changeRestX, changeRestY))
        #logging.info("New    Rest:  X: {}  Y: {}".format(self.rx, self.ry))
        #logging.info("New    Pos:   X: {}  Y: {}".format(self.x, self.y))
        #logging.info("")
        self.life -= 1


    def draw(self, win):
        p = {
            'x': self.x, 
            'y': self.y,
        }
        if Utility.isPointDrawable(p):
            win.addstr(self.y, self.x, self.char, self.color | self.colorOpt)

    def isActive(self): 
        return self.active