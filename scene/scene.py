
import curses

class Scene(object):
    def __init__(self, win):
        self.win = win

    def title(self):
        # Display welcome screen and wait for key press
        self.win.clear()
        self.win.border()
        self.win.refresh()    
        
        self.win.addstr(10, 10, "Key Rollover", curses.color_pair(3))
        q = self.win.getch() # wait for key to start game