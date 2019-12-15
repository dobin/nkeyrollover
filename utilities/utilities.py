import logging
import math
import random

from texture.character.charactertexturetype import CharacterTextureType
from texture.character.characteranimationtype import CharacterAnimationType
from texture.animation import Animation
from common.coordinates import Coordinates, ExtCoordinates
from common.direction import Direction

logger = logging.getLogger(__name__)


class Utility(object):
    @staticmethod
    def getOffsetFor(srcRenderable, destRenderable, x, y):
        xx = srcRenderable.coordinates.x - destRenderable.coordinates.x + x
        yy = srcRenderable.coordinates.y - destRenderable.coordinates.y + y

        return xx, yy


    @staticmethod
    def diceRoll(diceStr):
        # like "1d6"
        d = int(diceStr.split('d')[1])
        return random.randint(1, d)


    @staticmethod
    def distance(coord1 :Coordinates, coord2 :Coordinates):
        res = {
            'x': 0,
            'y': 0,
            'sum': 0,
        }
        res['x'] = abs(coord1.x - coord2.x)
        res['y'] = abs(coord1.y - coord2.y)
        # res['sum'] = res['x'] + res['y']
        res['sum'] = math.sqrt(res['x'] ** 2 + res['y'] ** 2)
        return res


    @staticmethod
    def updateCoordinateListWithBase(weaponHitArea, loc, direction):
        carr = weaponHitArea.hitCd
        for c in carr:
            c.x += loc.x
            c.y += loc.y
            if direction is Direction.left:
                c.x -= weaponHitArea.width


    @staticmethod
    def getListFromTexture(frame):
        carr = []

        y = 0
        while y < len(frame):
            x = 0
            while x < len(frame[y]):
                column = frame[y][x]
                if column != '':
                    c = Coordinates(x, y)
                    carr.append(c)

                x += 1
            y += 1

        return carr


    @staticmethod
    def isPointInArea(coord1 :Coordinates, location2 :ExtCoordinates):
        if coord1.x >= location2.x and coord1.x < location2.x + location2.width and coord1.y >= location2.y and coord1.y < location2.y + location2.height:
            return True
        else:
            return False


    @staticmethod
    def getBorder(loc :Coordinates, distance :int =1, width :int =1, thicc :int =1):
        locs = []
        basex = loc.x - distance
        basey = loc.y - distance
        dd = distance * 2
        y = basey
        x = basex

        while y <= basey + dd:
            x = basex
            while x <= basex + dd:
                if y >= basey and y <= basey + dd + thicc:
                    locs.append(Coordinates(
                        x = x,
                        y = y
                    ))
                elif x >= basex and x <= basex + dd + thicc:
                    locs.append(Coordinates(
                        x = x,
                        y = y
                    ))
                x += 1
            y += 1

        return locs


    @staticmethod
    def getBorderHalf(loc :Coordinates, distance :int =1, width :int =1, partRight=True):
        locs = []
        basex = loc.x - distance
        basey = loc.y - distance
        dd = distance * 2
        y = basey
        x = basex
        while y <= basey + dd:
            x = basex
            while x <= basex + dd:
                if y == basey or y == basey + dd:
                    locs.append(Coordinates(
                        x = x,
                        y = y
                    ))
                elif x == basex or x == basex + dd:
                    locs.append(Coordinates(
                        x = x,
                        y = y
                    ))
                x += 1
            y += 1
        return locs


    @staticmethod
    def setupLogger():
        # RECORD debug level is used to record/indicate statistical relevant
        # game events
        DEBUG_LEVELV_NUM = logging.WARN + 1
        logging.addLevelName(DEBUG_LEVELV_NUM, "RECORD")

        def __record(self, message, *args, **kws):
            if self.isEnabledFor(DEBUG_LEVELV_NUM):
                # Yes, logger takes its '*args' as 'args'.
                self._log(DEBUG_LEVELV_NUM, message, args, **kws)
        logging.Logger.record = __record


    @staticmethod
    def isIdentical(coord1 :Coordinates, coord2: Coordinates) -> bool:
        if coord1.x == coord2.x and coord1.y == coord2.y:
            return True
        else:
            return False


    @staticmethod
    def checkAnimation(
        animation: Animation, animationType :CharacterAnimationType,
        characterTextureType :CharacterTextureType
    ):
        logging.debug("Load: {} {}".format(animationType, characterTextureType))
        if len(animation.arr) != animation.frameCount:
            raise Exception("Animation {} / {} invalid: frameCount={}, but array contains {}"
                .format(characterTextureType, animationType.name, animation.frameCount, len(animation.arr)))

        for a in animation.arr:
            if len(a) != animation.height:
                raise Exception("Animation {} / {} invalid: height={}, but array contains {}"
                    .format(characterTextureType, animationType.name, animation.height, len(a)))

            for line in a:
                if len(line) != animation.width:
                    raise Exception("Animation {} / {} invalid: width={}, but array contains {}"
                        .format(characterTextureType, animationType.name, animation.width, len(line)))

        if animation.advanceByStep and animation.frameTime != None:
            raise Exception("Animation {} / {} advanceByStep=True, but frameTime array given"
                .format(characterTextureType, animationType.name))

        if len(animation.frameColors) != animation.frameCount:
            raise Exception("Animation {} / {} frameColor count {} does not match frameCount {}"
                .format(characterTextureType, animationType.name, len(animation.frameColors), animation.frameCount))


    @staticmethod
    def mirrorFrames(arr):
        for a in arr:
            for line in a:
                n = 0
                while n < len(line) / 2:
                    cl = line[n]
                    cr = line[len(line) - 1 - n]

                    cl = Utility.swapChar(cl)
                    cr = Utility.swapChar(cr)

                    line[n] = cr
                    line[len(line) - 1 - n] = cl
                    n += 1


    @staticmethod
    def swapChar(char):
        if char == ')':
            return '('
        elif char == '(':
            return ')'

        elif char == '/':
            return '\\'
        elif char == '\\':
            return '/'

        elif char == '`':
            return '\''
        elif char == '\'':
            return '`'

        elif char == 'D':
            return 'Ɑ'
        elif char == 'Ɑ':
            return 'D'

        if char == '<':
            return '>'
        elif char == '>':
            return '<'

        if char == '`':
            return '´'
        elif char == '´':
            return '`'

        if char == '⌐':
            return '¬'
        elif char == '¬':
            return '⌐'

        else:
            return char
