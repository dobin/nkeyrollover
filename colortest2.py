import asciimatics
from asciimatics.screen import Screen
import time

def demo(screen):
  screen.clear()
  while True:
    screen.print_at(
        text='Test blue green', 
        x=0, 
        y=0, 
        colour=Screen.COLOUR_WHITE, 
        attr=Screen.A_REVERSE,
        bg=Screen.COLOUR_BLACK)

    screen.print_at(
        text='Text grey background black', 
        x=0, 
        y=1, 
        colour=Screen.COLOUR_WHITE, 
        attr=Screen.A_REVERSE | Screen.A_BOLD,
        bg=Screen.COLOUR_BLACK)

    screen.move(5, 5)
    screen.draw(22, 33, char='.')

    screen.refresh()

while True:
    Screen.wrapper(demo)
    sys.exit()