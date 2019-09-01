import curses
import time
import logging

from config import Config
from world.world import World
from utilities.colorpalette import Color
from utilities.colorpalette import ColorPalette

logger = logging.getLogger(__name__)


# Print some chars in all possible colors 

def colorTest(): 
    logging.basicConfig(
        filename='app.log', 
        filemode='a', 
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)07s %(name)32s: %(message)s')

    curses.initscr()
    win = curses.newwin(Config.rows, Config.columns)
    curses.noecho()
    curses.cbreak()
    win.keypad(1) 
    curses.curs_set(0)    
    win.nodelay(1) # make getch() nonblocking
    ColorPalette.cursesInitColor()
    win.clear()
    win.border()

    world = World(win)

    dt = 0.01
    while True:
        win.erase()

        x = 0
        y = 1
        
        for color in Color:
            colorIdx = int(color)
            curseColor = ColorPalette.getColorByColor(color)
            # logging.info("Color: {} id {} is: {}".format(color, colorIdx, curseColor))
            # win.addstr(7, x + (colorIdx * 4), '###', curseColor )
            world.viewport.addstr(y, x + (colorIdx * 8), '###', curseColor )
            world.viewport.addstr(y+1, x + (colorIdx * 8), str(color)[6:], curseColor )

            world.viewport.addstr(y+3, x + (colorIdx * 8), '###', curseColor | curses.A_BOLD )
            world.viewport.addstr(y+4, x + (colorIdx * 8), str(color)[6:], curseColor | curses.A_BOLD )
        
        key = win.getch()
        if key == 27: # esc
            break
        # win.refresh()

        time.sleep(dt) 


if __name__ == '__main__':
    colorTest()