#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

import curses
import locale

locale.setlocale(locale.LC_ALL, '')


curses.initscr()

win = curses.newwin(10, 10, 0, 0)
curses.noecho()
curses.cbreak()
win.keypad(1)
curses.curs_set(0)
win.nodelay(1)  # make getch() nonblocking

curses.start_color()
curses.init_pair(1, curses.COLOR_GREEN, 0)
curses.init_pair(2, curses.COLOR_MAGENTA, 0)

b = '░'  # 0x2591
bb = 0x2591
print("A: " + b)

win.addstr(0, 0, 'A', curses.color_pair(1))
win.addstr(0, 1, 'B', curses.color_pair(2))
win.addstr(0, 2, b, curses.color_pair(2))


ch = win.inch(0, 0)
chcolor = ch & curses.A_COLOR
print("CH0: " + hex(ch) + " Color: " + hex(chcolor))
ch0 = ch

ch = win.inch(0, 1)
chcolor = ch & curses.A_COLOR
print("CH2: " + hex(ch) + " Color: " + hex(chcolor))
ch1 = ch

ch = win.inch(0, 2)
chcolor = ch & curses.A_COLOR
chcolor = ch & 0xA00
print("CH3: " + hex(ch) + " Color: " + hex(chcolor))
ch2 = ch


c0 = ch0 & curses.A_CHARTEXT
c2 = ch2 & curses.A_CHARTEXT
print("0: " + hex(c0))
print("2: " + hex(c2))

print("X0: " + hex(ch0) + " + " + hex(ch0 - 0x41))
print("X2: " + hex(ch2) + " + " + hex(ch2 - bb))


n = (ch2 - 0x2500) & curses.A_COLOR
print("N: " + hex(n))

