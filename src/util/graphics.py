"""
This file defines graphical constants. Graphics are with the origin in the top left.
"""
from pygame import Rect

#frames
FPS = 30

# size of the ribbon
RIBBON = 4

# dimensions of a given screen
SCR_WID = 160 * 2
SCR_HT = 144 * 2

# bounds of the total window, the upper screen, and the lower screen
BOUND_TOT = Rect(0, 0, 2 * RIBBON + SCR_WID, 3 * RIBBON + 2 * SCR_HT)
BOUND_UP = Rect(RIBBON, RIBBON, SCR_WID, SCR_HT)
BOUND_LOW = Rect(RIBBON, 2 * RIBBON + SCR_HT, SCR_WID, SCR_HT)

# internal bounds of an individual screen
BOUND_SCR = Rect(0, 0, SCR_WID, SCR_HT)

# fonts
FONT_4, FONT_6, FONT_8, FONT_10, FONT_12, FONT_14, FONT_16, FONT_20, FONT_24, FONT_28, FONT_32 =\
    None, None, None, None, None, None, None, None, None, None, None
