import math
import logging
from asciimatics.screen import Screen

from utilities.timer import Timer
from utilities.colorpalette import ColorPalette
from utilities.color import Color
from messaging import messaging, MessageType
from common.direction import Direction

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
        damage :int =0,
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
        color =None,
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

        self.color, self.attr = ColorPalette.getColorByColor(Color.brightmagenta)
        if color is not None:
            self.color = color[0]
            self.attr = color[1]

        self.setChar()

        self.rx = 0.0
        self.ry = 0.0

        self.movementTimer.setTimer(self.speed)
        self.active = active


    def __repr__(self):
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


    def fadeoutSetColor(self):
        if self.life > (self.originalLife / 2):
            self.attr = Screen.A_BOLD
        else:
            self.attr = Screen.A_NORMAL


    def setChar(self):
        if self.charType == 0:
            pass

        elif self.charType == 1:
            if self.life > ((self.originalLife / 3) * 2):
                self.char = 'O'
            elif self.life < ((self.originalLife / 3) * 1):
                self.char = '.'
            else:
                self.char = 'o'

        elif self.charType == 2:
            if self.life > ((self.originalLife / 3) * 2):
                self.char = '#'
            elif self.life < ((self.originalLife / 3) * 1):
                self.char = ':'
            else:
                self.char = '|'

        elif self.charType == 3:
            if self.life > ((self.originalLife / 3) * 2):
                self.char = 'O'
            elif self.life < ((self.originalLife / 3) * 1):
                self.char = '.'
            else:
                self.char = 'o'

        elif self.charType == 4:
            if self.life > ((self.originalLife / 3) * 2):
                self.char = '¦'
            elif self.life < ((self.originalLife / 3) * 1):
                self.char = '.'
            else:
                self.char = ':'

        elif self.charType == 5:
            self.char = '-'

        else:
            raise Exception("Invalid charType: {}".format(self.charType))


    def makeStep(self, dt, adjustLife=True):
        if self.life <= 0:
            self.active = False
            return

        if self.fadeout:
            self.fadeoutSetColor()
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
                        'direction': Direction.none,
                        'knockback': False,
                        'stun': False,
                        'sourceRenderable': None,
                    }
                )

            if False:
                logging.info("Real change:  X: {}  Y: {}".format(xFloat, yFloat))
                logging.info("Round change: X: {}  Y: {}".format(xChange, yChange))
                logging.info("Change Rest:  X: {}  Y: {}".format(changeRestX, changeRestY))
                logging.info("New    Rest:  X: {}  Y: {}".format(self.rx, self.ry))
                logging.info("New    Pos:   X: {}  Y: {}".format(self.x, self.y))

        if adjustLife:
            self.life -= 1


    def draw(self):
        self.viewport.addstr(
            self.y, self.x, self.char, self.color, self.attr)


    def isActive(self):
        return self.active


    def setActive(self, active):
        self.active = active
