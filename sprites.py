# Pixel art for VAR Is Watching.
# Every character is drawn as a "pixel grid": a list of text rows where
# each letter stands for one colour and "." means transparent (nothing).

import pygame

# The dark colour used for all outlines.
OUTLINE = (45, 28, 40)

# Which colour each letter means, as (red, green, blue).
PALETTE = {
    # hair: dark, normal, light
    "h": (92, 52, 30), "H": (140, 82, 44), "j": (190, 125, 70),
    # skin: shadow, normal, highlight
    "s": (214, 150, 112), "S": (250, 200, 160), "t": (255, 228, 200),
    # face: eye, eye shine, blush, mouth
    "E": (35, 25, 40), "w": (255, 255, 255), "p": (245, 140, 140), "m": (170, 60, 70),
    # headset: dark grey, grey
    "g": (70, 72, 85), "G": (130, 135, 150),
    # black referee shirt: darkest, dark, light
    "k": (28, 28, 40), "b": (48, 50, 68), "B": (78, 82, 108),
    # white collar, yellow lanyard, light blue ID card
    "W": (245, 245, 250), "Y": (250, 205, 50), "C": (210, 230, 255),
    # shoes
    "O": (30, 25, 30),
}

# The player: a junior VAR official with a headset and a lanyard.
PLAYER = [
    "......hhhhhhhh......",
    "....hhHHHHHHHHhh....",
    "...hHHjjjHHHHHHHh...",
    "..hHHjjHHHHHHHHHHh..",
    "..hHHHHHHHHHHHHHHh..",
    "..hHHSSSHHHSSSSHHh..",
    ".GgHSSSSSSSSSSSSSSh.",
    ".GgSStSSSSSSSSStSSs.",
    ".GgSSwESSSSSSwESSSs.",
    ".GgSSEESSSSSSEESSSs.",
    ".GgSSEESSSSSSEESSSs.",
    "..gSpSSSSSSSSSSSpSs.",
    "..gSSSSSSmmmSSSSSSs.",
    "..ggsSSSSSSSSSSSSs..",
    "....gGsssSSSSSsss...",
    "......ssssssssss....",
    "......bbWWWWWWbb....",
    ".....bBBBWYYWBBBb...",
    "....bBBBBBYYBBBBBb..",
    "...SbBBBBBYYBBBBBbS.",
    "...SSbBBBCCCCBBBbSS.",
    "...sSbBBBCCCCBBBbSs.",
    "....sbbbbbbbbbbbbs..",
    ".....kkkkkkkkkkkk...",
    ".....kkkkk..kkkkk...",
    "......SSs....SSs....",
    "......bbb....bbb....",
    ".....OOOO...OOOO....",
]

# The walking frame: the same body (the first 23 rows of PLAYER),
# but the back leg pushes off the floor and the front foot is lifted.
# PLAYER[:23] means "rows 0 up to (not including) row 23".
PLAYER_WALK = PLAYER[:23] + [
    ".....kkkkkkkkkkkk...",
    "....kkkkk...kkkkkk..",
    "...SSs.......SSSOOO.",
    "..bbb........bbOOO..",
    ".OOOO...............",
]


def has_coloured_neighbour(surface, x, y):
    # Check the 4 pixels around (x, y): left, right, above and below.
    # Returns True if at least one of them is coloured (not transparent).
    width = surface.get_width()
    height = surface.get_height()
    neighbours = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
    for nx, ny in neighbours:
        # Skip positions outside the picture.
        if nx < 0 or ny < 0 or nx >= width or ny >= height:
            continue
        # get_at gives (red, green, blue, alpha); alpha 0 means transparent.
        if surface.get_at((nx, ny))[3] > 0:
            return True
    return False


def make_sprite(rows):
    # Turn a pixel grid into a pygame picture with a dark outline around it.

    # The picture is 2 pixels wider and taller than the grid,
    # so there is room for the outline on every side.
    grid_width = 0
    for row in rows:
        if len(row) > grid_width:
            grid_width = len(row)
    width = grid_width + 2
    height = len(rows) + 2

    # SRCALPHA makes a picture that can have transparent pixels.
    picture = pygame.Surface((width, height), pygame.SRCALPHA)

    # 1. Colour one pixel for every letter in the grid.
    for y in range(len(rows)):
        row = rows[y]
        for x in range(len(row)):
            letter = row[x]
            if letter in PALETTE:
                picture.set_at((x + 1, y + 1), PALETTE[letter])

    # 2. Add the outline: every empty pixel next to a coloured pixel
    #    becomes dark. We look at a copy, so new outline pixels
    #    do not create even more outline pixels.
    original = picture.copy()
    for y in range(height):
        for x in range(width):
            is_empty = original.get_at((x, y))[3] == 0
            if is_empty and has_coloured_neighbour(original, x, y):
                picture.set_at((x, y), OUTLINE)

    return picture
