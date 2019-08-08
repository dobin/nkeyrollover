from config import Config
import sys

class MockWin(object): 
    def __init__(self, rows, columns):
        self.space = 10
        self.initialRows = rows
        self.initialColumns = columns
        self.width = columns + 10 + 10
        self.height = rows + 10 + 10
        self.win = [[ '' ] * self.width for i in range(self.height)] # https://snakify.org/en/lessons/two_dimensional_lists_arrays/


    def addstr(self, y, x, string, color=None):
        for i, ch in enumerate(string): 
            self.addChInternal(y, x+i, ch, color)
        print("addStr")
    

    def getCh(self): 
        print("GetCh")


    def border(self): 
        y = self.space
        while y <= self.initialRows + self.space:

            x = self.space
            while x <= self.initialColumns + self.space: 
                self.win[y][x] = '.'

                x += 1
            y+= 1

        pass


    def addCh(self, y, x, char, color=None): 
        self.addChInternal(y, x, char, color)


    def addChInternal(self, y, x, char, color=None): 
        self.win[ y+10 ][ x + 10] = char


    def getInternalPosFor(self, x, y):
        pos = {
            'x': x+10, 
            'y': y+10
        }
        return pos

    def draw(self): 
        print("Draw")

    def refresh(self): 
        print("Refresh")
        self.internalPrint()

    def internalPrint(self):
        print("")
        for xArr in self.win: 
            print("")
            for char in xArr:
                if char is '': 
                    sys.stdout.write(' ')
                else: 
                    sys.stdout.write(char)


    def keypad(self, n): 
        pass

    def nodelay(self, n): 
        pass

    def clear(self): 
        print("Clear")


    # used by hasttr() to check if unit test is being run
    def isUnitTest(self): 
        pass


#class MockCurses(object):
    
def color_pair(self, n): 
    return n

def initscr(self): 
    pass

def noecho(self): 
    pass

def cbreak(self): 
    pass