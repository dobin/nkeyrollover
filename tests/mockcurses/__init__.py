from .mockwin import MockWin

win = None

def color_pair(n):
    return n

def initscr():
    pass

def noecho():
    pass

def cbreak():
    pass


def newwin(rows, columns):
    win = MockWin(rows, columns)
    return win

def start_color():
    pass

def init_pair(n, color, i):
    pass

def curs_set(n):
    pass

COLOR_GREEN = 0
COLOR_MAGENTA = 1
COLOR_RED = 2
COLOR_YELLOW = 3
COLOR_BLUE = 4
COLOR_WHITE = 5
COLOR_BLACK = 6
COLOR_WHITE = 7
