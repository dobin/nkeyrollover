import curses
import timeit
import time

curses.initscr()
win = curses.newwin(25, 80)
curses.noecho()
curses.cbreak()
win.keypad(1)
curses.curs_set(0)
win.nodelay(1) # make getch() nonblocking
curses.start_color()
curses.init_pair(1, curses.COLOR_GREEN, 0)

win.clear()
win.border()

current_milli_time = lambda: int(round(time.time() * 1000))

t1 = current_milli_time()
n = 0
while n < 1000000:
    win.addstr(1, 1, 'x') # 29, 180
    # win.addch(1, 1, 'x') # 25, 171
    n += 1
t2 = current_milli_time()


# Clean up before exiting
curses.nocbreak()
win.keypad(0)
curses.echo()
curses.endwin()

t = t2 - t1

print("Time: " + str(t))