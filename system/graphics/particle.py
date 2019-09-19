import math
import logging
import curses

from utilities.timer import Timer
from utilities.colorpalette import ColorPalette
from utilities.colortype import ColorType
from messaging import messaging, MessageType

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
        active :bool =False,
        damage :int = 0,
        damageEveryStep :bool =False,
        byPlayer :bool =True,
    ):
        self.viewport = viewport
        self.movementTimer = Timer()
        self.init(
            x=x, y=y, life=life, angle=angle, speed=speed, fadeout=fadeout,
            byStep=byStep, charType=charType, active=active,
            damage=damage,
            damageEveryStep=damageEveryStep,
            byPlayer=byPlayer)


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
        active :bool =False,
        damage :int =0,
        damageEveryStep :bool =False,
        byPlayer :bool =True,
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
        self.damage = damage
        self.damageEveryStep = damageEveryStep
        self.byPlayer = byPlayer

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


    def __repr__(self):
        # return "{}/{}  vel: {}/{}  life: {}".format(
        #     self.x, self.y, self.velocity['x'], self.velocity['y'], self.life
        # )
        return "Particle {}/{}".format(
            self.x, self.y
        )


    def advance(self, dt):
        if self.active is False:
            return

        if self.byStep:
            return

        self.movementTimer.advance(dt)

        self.makeStep(dt)


    def setColor(self):
        self.color = ColorPalette.getColorByColorType(ColorType.particle, self.viewport)

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

        if self.charType == 1:
            if self.life > ((self.originalLife / 3) * 2):
                self.char = '#'
            elif self.life < ((self.originalLife / 3) * 1):
                self.char = ':'
            else:
                self.char = '|'


    def makeStep(self, dt, adjustLife=True):
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

            if (self.damageEveryStep and self.damage > 0
                    and (xChange != 0 or yChange != 0)):
                # hitLocations = [Coordinates(self.x, self.y)]
                hitLocations = []
                hitLocations.append(self)
                messaging.add(
                    type=MessageType.AttackAt,
                    data= {
                        'hitLocations': hitLocations,
                        'damage': self.damage,
                        'byPlayer': self.byPlayer,
                    }
                )

            if False:
                print("")
                print("Real change:  X: {}  Y: {}".format(xFloat, yFloat))
                print("Round change: X: {}  Y: {}".format(xChange, yChange))
                print("Change Rest:  X: {}  Y: {}".format(changeRestX, changeRestY))
                print("New    Rest:  X: {}  Y: {}".format(self.rx, self.ry))
                print("New    Pos:   X: {}  Y: {}".format(self.x, self.y))
                print("")

        if adjustLife:
            self.life -= 1


    def draw(self):
        self.viewport.addstr(self.y, self.x, self.char, self.color | self.colorOpt)


    def isActive(self):
        return self.active
