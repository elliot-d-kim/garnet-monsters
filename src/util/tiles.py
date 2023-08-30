"""
This file contains constants related to tile maps.
"""

TILE_COLS = {
                            #0 reserved for empty
    # grass
    (0, 0, 0):          1,           #basic wall (black)
    (100, 200, 100):    2,     #basic grass (pale green)
    (0, 100, 0):        3,         #tall grass (dark green)

    # path
    (200, 200, 200):    4,     #stone-tile (gray)

    # flower
    (160, 170, 250):    5,      #flower-tile-1
    (180, 80, 120):     6,      #flower-tile-2
    (60, 200, 200):     7,      #flower-tile-3
    (250, 120, 120):    8,      #flower-tile-4
    (250, 240, 100):    9,      #flower-tile-5
    (250, 200, 220):    10,     #flower-tile-6

    # dirt cardinal
    (220, 200, 110):    11,     #dirt-center
    (170, 150, 80):     12,     #dirt-bottom
    (250, 225, 125):    13,     #dirt-left
    (210, 200, 150):    14,     #dirt-top
    (220, 190, 60):     15,     #dirt-right


    # dirt diagonals
    (250, 220, 90):     16,      # dirt-diagonal-TR
    (250, 230, 160):    17,    # dirt-diagonal-TL
    (180, 150, 60):     18,     # dirt-diagonal-BR
    (180, 160, 110):    19,     # dirt-diagonal-BL

    # dirt corners
    (90, 80, 40):       20,     # dirt-corner-RB
    (110, 90, 20):      21,     # dirt-corner-RT
    (60, 50, 25):       22,     # dirt-corner-LB
    (50, 40, 10):       23,     # dirt-corner-LT

    # level stairs tiles
    (130, 130, 130):    24,     # level-stairs-tile

    # level
    (100, 50, 50):      25,     # level-bottom
    (210, 100, 100):    26,     # level-top
    (160, 110, 110):    27,     # level-left
    (150, 30, 30):      28,     # level-right

    # level diagonals
    (250, 200, 200):    29,     # level-diagonal-TL
    (250, 0, 0):        30,     # level-diagonal-TR
    (110, 100, 100):    31,     # level-diagonal-BL
    (100, 0, 0):        32,     # level-diagonal-BR

    # level corners
    (20, 20, 70):       33,     # level-corner-BR
    (60, 60, 90):       34,     # level-corner-BL
    (40, 40, 200):      35,     # level-corner-TR
    (150, 150, 200):    36,     # level-corner-TL
}

"""
TILES
"""
TILE_PATHS = {
    # grass
    1: "wall-1",
    2: "grass-1",
    3: "tall-grass-1",

    # path
    4: "stone-tile-1",

    # flower
    5: "flower-tile-1",
    6: "flower-tile-2",
    7: "flower-tile-3",
    8: "flower-tile-4",
    9: "flower-tile-5",
    10: "flower-tile-6",

    # dirt cardinal
    11: "dirt-center",
    12: "dirt-bottom",
    13: "dirt-top",
    14: "dirt-left",
    15: "dirt-right",

    # dirt diagonal
    16: "dirt-diagonal-TR",
    17: "dirt-diagonal-TL",
    18: "dirt-diagonal-BR",
    19: "dirt-diagonal-BL",

    # dirt corner
    20: "dirt-corner-LB",
    21: "dirt-corner-RB",
    22: "dirt-corner-LT",
    23: "dirt-corner-RT",

    # level-stairs-tile
    24: "level-stairs-tile",

    # level
    25: "level-bottom",
    26: "level-top",
    27: "level-left",
    28: "level-right",

    # level diagonals
    29: "level-diagonal-TL",
    30: "level-diagonal-TR",
    31: "level-diagonal-BL",
    32: "level-diagonal-BR",

    # level corners
    33: "level-corner-BR",
    34: "level-corner-BL",
    35: "level-corner-TR",
    36: "level-corner-TL"
}

WALL_TILES = [1, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36]

"""
ENTITIES
"""
ENT_DIMS = {
    # buildings
    "parrish-hall":         (608, 224),
    "greenhouse-green-1":   (160, 192),
    "greenhouse-green-2":   (128, 128),
    "greenhouse-blue-1":    (160, 192),
    "greenhouse-blue-2":    (128, 128),
    "greenhouse-red-2":     (128, 128),
    "greenhouse-glass":     (96, 128),

    # fences
    "fence-grass": (32, 32),
    "fence-grass-back": (32, 32),
    "fence-left": (32, 32),
    "fence-right": (32, 32),
    "fence-wall": (32, 32),

    # trees
    "oak-tree":             (64, 64),
    "short-oak-tree":       (32, 40),
    "pine-tree":            (64, 64),

    # decor
    "row-yellowFlower":     (64, 32),
    "row-blueFlower":       (64, 32),
    "wide-yellowFlower":    (32, 64),
    "flower-square":        (64, 64),
    "waterfall":            (96, 64),
    "streetLight":          (32, 64),
    "plaque":               (32, 32),
    "plant-pots":           (32, 32),
    "stump-1":              (32, 32),
    "stump-2":              (32, 32),
    "rock-1":               (32, 32),
    "rock-2":               (32, 32),
    "rock-3":               (32, 32),
}

"""
Gets a code from COLORS based on the array of length 3 passed in as color.
"""
def tileCodeFromColor(color):
    col = tuple(color)
    if col in TILE_COLS:
        return TILE_COLS[col]
    else:
        print("Warning: Unexpected color code: ", col , " in src.util.tiles.codeFromColor")
        return 0

"""
Gets the path to the asset for a given tile from the tile code.
"""
def tilePathFromColor(code):
    return "src/assets/tiles/" + TILE_PATHS[code] + ".png"

"""
Returns true if this kind of tile is a wall tile, false if it is not.
"""
def isTileWall(code):
    return code in WALL_TILES

"""
Returns the path to the entity file based on the entity name.
"""
def entityPathFromName(name):
    return "src/assets/entities/" + name + ".png"

def getEntityWidth(name):
    return ENT_DIMS[name][0]
def getEntityHeight(name):
    return ENT_DIMS[name][1]
