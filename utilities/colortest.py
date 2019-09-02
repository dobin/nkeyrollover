import curses

def colornum(fg, bg):
    B = 1 << 7
    bbb = (7 & bg) << 4
    ffff = 7 & fg

    return (B | bbb | ffff)


def curs_color(fg):
    a = 7 & fg

    if a == 0:
        return curses.COLOR_BLACK
    if a == 1:
        return curses.COLOR_BLUE
    if a == 2:
        return curses.COLOR_GREEN
    if a == 3:
        return curses.COLOR_CYAN
    if a == 4:
        return curses.COLOR_RED
    if a == 5:
        return curses.COLOR_MAGENTA
    if a == 6:
        return curses.COLOR_YELLOW
    if a == 7:
        return curses.COLOR_WHITE

