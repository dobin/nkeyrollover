import sys


class MockWin(object):
    def __init__(self, rows, columns):
        self.space = 10
        self.initialRows = rows
        self.initialColumns = columns
        self.width = columns + 10 + 10
        self.height = rows + 10 + 10

        # https://snakify.org/en/lessons/two_dimensional_lists_arrays/
        self.win = [[''] * self.width for i in range(self.height)]


    def addstr(
        self, y, x, char, color, attr=0, bg=0, knownDrawable=False, setbg=False
    ):
        for i, ch in enumerate(char):
            self.addChInternal(y, x + i, ch, color)


    def getCh(self):
        print("GetCh")


    def border(self):
        y = self.space

        if True:
            # make border
            while y <= self.initialRows + self.space:
                x = self.space

                while x <= self.initialColumns + self.space:

                    if y == self.space or y == self.space + self.initialRows:
                        self.win[y][x] = '.'
                    elif x == self.space or x == self.space + self.initialColumns:
                        self.win[y][x] = '.'

                    x += 1

                y += 1
        else:
            # fill whole content
            while y <= self.initialRows + self.space:

                x = self.space
                while x <= self.initialColumns + self.space:
                    self.win[y][x] = '.'

                    x += 1
                y += 1


    def peek(self, x, y):
        pos = self.getInternalPosFor(x, y)
        return self.win[pos['y']][pos['x']]


    def addCh(self, y, x, char, color=None):
        self.addChInternal(y, x, char, color)


    def addChInternal(self, y, x, char, color=None):
        self.win[y + 10][x + 10] = char


    def getInternalPosFor(self, x, y):
        pos = {
            'x': x + 10,
            'y': y + 10
        }
        return pos


    def draw(self):
        self.internalPrint()


    def refresh(self):
        pass


    def internalPrint(self):
        print("")
        for xArr in self.win:
            print("")
            for char in xArr:
                if char == '':
                    sys.stdout.write(' ')
                else:
                    sys.stdout.write(char)



    def keypad(self, n):
        pass


    def nodelay(self, n):
        pass


    def clear(self):
        for y, yrow in enumerate(self.win):
            for x, _ in enumerate(yrow):
                self.win[y][x] = ''

    # used by hasttr() to check if unit test is being run
    def isUnitTest(self):
        pass



def color_pair(self, n):
    return n


def initscr(self):
    pass


def noecho(self):
    pass


def cbreak(self):
    pass
