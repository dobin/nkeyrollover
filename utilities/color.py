from enum import IntEnum


class Color(IntEnum):
    brightwhite = 1     # 255 255 255
    white = 2           # 229 229 229
    grey = 3            # 077 077 077
    black = 4           # 000 000 000

    brightblue = 5      # 000 000 255
    blue = 6            # 000 000 205
    brightcyan = 7      # 000 255 255
    cyan = 8            # 000 205 205

    brightyellow = 9    # 255 255 000
    yellow = 10         # 205 205 000

    brightred = 11      # 255 000 000
    red = 12            # 205 000 000
    brightmagenta = 13  # 255 000 255
    magenta = 14        # 205 000 205

    brightgreen = 15    # 000 255 000
    green = 16          # 000 205 000
