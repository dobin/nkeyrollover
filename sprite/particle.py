import math
import logging
import curses

from utilities.timer import Timer


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
        byStep :bool =False,
        active :bool =False
    ):
        self.movementTimer = Timer()
        self.init(x=x, y=y, life=life, angle=angle, speed=speed, fadeout=fadeout, byStep=byStep, active=active)
        

    def init(
        self,
        x :int =0,
        y :int =0, 
        life :int =0,
        angle :float =0, 
        speed :int =1,
        fadeout :bool =True,
        byStep :bool =False,
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

        self.angleInRadians = angle * math.pi / 180
        self.velocity = {
            'x': speed * math.cos(self.angleInRadians),
            'y': -speed * math.sin(self.angleInRadians)
        }

        self.color = curses.color_pair(7)
        self.colorOpt = 0
        self.setColor()

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

        if self.movementTimer.timeIsUp():
            self.makeStep()
            self.movementTimer.reset()


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

    def makeStep(self):
        if self.life <= 0: 
            self.active = False
            return


        if self.fadeout:
            self.setColor()


        xFloat = self.velocity['x'] + self.rx
        yFloat = self.velocity['y'] + self.ry

        xChange = int(round(xFloat))
        yChange = int(round(yFloat))

        # change pos
        self.x += xChange
        self.y += yChange

        # accumulate pos we could not handle yet
        changeRestX = xFloat - xChange - self.rx
        changeRestY = yFloat - yChange - self.ry 

        self.rx += changeRestX
        self.ry += changeRestY

        #logging.info("Real change:  X: {}  Y: {}".format(xFloat, yFloat))
        #logging.info("Round change: X: {}  Y: {}".format(xChange, yChange))

        #logging.info("Change Rest:  X: {}  Y: {}".format(changeRestX, changeRestY))
        #logging.info("New    Rest:  X: {}  Y: {}".format(self.rx, self.ry))
        #logging.info("")
        self.life -= 1


    def draw(self, win): 
        win.addstr(self.y, self.x, 'O', self.color | self.colorOpt)