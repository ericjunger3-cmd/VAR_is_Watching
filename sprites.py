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
    # skin: shadow, normal, highlight, deepest shadow
    "s": (214, 150, 112), "S": (250, 200, 160), "t": (255, 228, 200), "Q": (190, 125, 95),
    # face: eye, eye shine, eye highlight, eyebrows, blush, mouth, open mouth, teeth
    "E": (35, 25, 40), "w": (255, 255, 255), "i": (150, 95, 60), "e": (60, 40, 50),
    "p": (245, 140, 140), "m": (170, 60, 70), "r": (120, 30, 40), "T": (255, 255, 240),
    # headset: dark grey, grey; red light (also the red of Bernie's shirt)
    "g": (70, 72, 85), "G": (130, 135, 150), "R": (230, 55, 55),
    # black shirt: darkest, dark, light
    "k": (28, 28, 40), "b": (48, 50, 68), "B": (78, 82, 108),
    # white, light grey, yellow, light yellow, light blue ID card
    "W": (245, 245, 250), "c": (215, 220, 230), "Y": (250, 205, 50),
    "q": (255, 225, 90), "C": (210, 230, 255),
    # dark trousers, shoes and shoe shine
    "z": (20, 20, 30), "Z": (40, 42, 58), "O": (30, 25, 30), "x": (110, 115, 135),
    # animals: light, normal and dark grey, purple and green,
    # orange, pink
    "a": (200, 205, 220), "A": (155, 160, 182), "d": (110, 115, 138),
    "v": (160, 115, 200), "n": (90, 180, 150), "o": (250, 165, 60), "f": (240, 135, 150),
    # steward: hi-vis vest, vest shadow, trousers, cap
    "V": (215, 240, 40), "y": (170, 200, 20), "N": (75, 80, 110), "M": (50, 55, 80),
    "D": (60, 110, 210), "F": (30, 70, 160),
    # pundit: slick hair, suit, tie
    "K": (35, 25, 25), "L": (80, 60, 50), "u": (40, 70, 150), "U": (70, 105, 200),
    "l": (200, 40, 50),
}

# Some characters use the same letters with different colours.
# These dictionaries say which colours change for that character.
REFEREE_COLOURS = {"h": (30, 25, 25), "H": (55, 45, 40), "j": (90, 75, 65),
                   "B": (50, 52, 62), "b": (32, 33, 42)}
# The home team plays in Bayern colours: red with white numbers.
STRIKER_COLOURS = {"h": (200, 150, 40), "H": (240, 200, 80), "j": (255, 235, 150),
                   "B": (220, 25, 55), "b": (170, 15, 45)}
# The away team plays in Dortmund colours: a yellow shirt, and black
# for the number, collar, shorts and captain's armband ("W", "c", "Y").
CAPTAIN_COLOURS = {"h": (25, 20, 20), "H": (45, 35, 35), "j": (70, 60, 60),
                   "B": (250, 220, 20), "b": (215, 180, 0), "S": (205, 150, 110),
                   "s": (170, 115, 80), "t": (225, 175, 135), "p": (200, 110, 100),
                   "Q": (140, 95, 65), "W": (35, 35, 40), "c": (20, 20, 25),
                   "Y": (35, 35, 40)}
# The police officers in the end clip (POLICE): a navy cap ("D", "F"),
# a gold badge ("R") and dark trousers ("N", "M"). The vest stays hi-vis
# yellow ("V", "y") and the checks are navy and white ("D", "W").
POLICE_COLOURS = {"D": (30, 45, 110), "F": (20, 28, 70), "R": (240, 200, 60),
                  "N": (30, 30, 45), "M": (20, 20, 30)}

# Two more players for the end clips: the home passer (red kit like the
# striker, but dark brown hair) and an away defender (yellow kit like the
# captain, but light skin and red hair).
PASSER_COLOURS = dict(STRIKER_COLOURS)
PASSER_COLOURS.update({"h": (70, 40, 25), "H": (105, 65, 40), "j": (150, 100, 60)})
DEFENDER_COLOURS = dict(CAPTAIN_COLOURS)
DEFENDER_COLOURS.update({"h": (150, 60, 30), "H": (200, 95, 45), "j": (235, 140, 80),
                         "S": (250, 200, 160), "s": (214, 150, 112), "t": (255, 228, 200),
                         "p": (245, 140, 140), "Q": (190, 125, 95)})
# The pundit wears a dark navy suit ("u", "U") and a blue silk tie ("l"),
# the same blue as the tie tip in the Server Room.
PUNDIT_COLOURS = {"h": (25, 20, 22), "H": (45, 38, 40), "j": (120, 110, 125),
                  "u": (22, 26, 48), "U": (38, 45, 80), "l": (55, 70, 150)}
# The linesman wears the same black shirt as the referee, so he does
# not look like an away (yellow) player.
LINESMAN_COLOURS = {"h": (160, 70, 30), "H": (210, 105, 45), "j": (240, 150, 80),
                    "B": (50, 52, 62), "b": (32, 33, 42)}
# The player wears a classic referee look: an all-black shirt with
# white trim instead of yellow, and black trousers.
PLAYER_COLOURS = {"b": (30, 30, 36), "B": (58, 58, 68), "k": (14, 14, 20),
                  "Y": (245, 245, 250), "q": (255, 255, 255),
                  "Z": (34, 34, 42), "z": (20, 20, 26)}

# The player, standing and facing you: a junior VAR official with a
# headset (the grey band over his hair), a polo with VAR stripes and a
# VAR badge, a lanyard with an ID card, and a belt buckle.
# The shirt colours come from PLAYER_COLOURS (black and white).
# Cute style: a big round head (more than half of the height) with big
# shiny eyes, a little curl of hair on top, a small body and short legs.
PLAYER = [
    ".................hh.............",
    "...............hhh..............",
    "...........gggGGGGggg...........",
    "........ggghHHHHHHHHhggg........",
    "......gghHHHjjjjHHHHHHHhgg......",
    ".....ghHHHjjjjHHHHHHHHHHhhg.....",
    "....ghHHHjjHHHHHHHHHHHHhHHhg....",
    "...ghHHHHHHHHHhHHHHHHHhHHHHhg...",
    "...ghHHHHHHHHhHHHHHHHhHHHHHhg...",
    "..ghHHHHHHHhHHHHHHHhHHHHHHHHhg..",
    "..ghHHHHHhHHHHHHhHHHHHHhHHHHhg..",
    "..ghHHHShHHHSHHhHHHSHHHhSHHHhg..",
    "..ghHSSSSHHSSSSHHSSSSHSSSSSHhg..",
    "..ghSSSSeeeSSSSSSSSSSeeeSSSShg..",
    ".GGgSSSSEEESSSSSSSSSSEEESSSSgGG.",
    ".GGgSSSSwEESSSSSSSSSSwEESSSSgGG.",
    ".GGgSSSSEEESSSSSSSSSSEEESSSSgGG.",
    ".GGgSSSSEiESSSSSSSSSSEiESSSSgGG.",
    ".GGgSSSppSSSSSmSSmSSSSppSSSSgGG.",
    "....ggSSSSSSSSSSmmSSSSSSSSSS....",
    ".....SgRSSSSSSSSSSSSSSSSSSs.....",
    ".......sSSSSSSSSSSSSSSSSs.......",
    "..........ssssssssssss..........",
    "..........kbYYbSSbYYbk..........",
    "......BBbbbbYbbbbbbYbbbbBB......",
    "......qBkbbbbYbbbbYbbbbkBq......",
    "......BBkbbbbbYbbYbbbbbkBB......",
    "......SSkBqqbbWWWWbbbbbkSS......",
    "......SSkBYYbbWRRWbbbbbkSS......",
    "......SskBbbbbWCCWbbbbbksS......",
    "......sskBbbbbWWWWbbbbbkss......",
    "........kkkkkkkxxkkkkkkk........",
    ".........ZZZZZZZZZZZZZZ.........",
    ".........ZZZZZz..ZZZZZz.........",
    ".........ZZZZZz..ZZZZZz.........",
    ".........ZZZZZz..ZZZZZz.........",
    ".........OOOOOO..OOOOOO.........",
    "........OxxOOOO..OOOOxxO........",
]

# The player walking to the right, turned a little towards you (3/4 view):
# the face moves to the right and you see hair on the left side.
# Four frames: right hand up + left foot behind, legs passing,
# left hand up + right foot behind, legs passing.
# When walking left, the game mirrors these pictures.
PLAYER_WALK = [
    [
        ".................hh.............",
        "...............hhh..............",
        "...........gggGGGGggg...........",
        "........ggghHHHHHHHHhggg........",
        "......gghHHHjjjjHHHHHHHhgg......",
        ".....ghHHHjjjjHHHHHHHHHHhhg.....",
        "....ghHHHjjHHHHHHHHHHHHhHHhg....",
        "...ghHHHHHHHHHhHHHHHHHhHHHHhg...",
        "...ghHHHHHHHHhHHHHHHHhHHHHHhg...",
        "..ghHHHHHHHhHHHHHHHhHHHHHHHHhg..",
        "..ghHHHHHhHHHHHHhHHHHHHhHHHHhg..",
        "..ghHHHShHHHSHHhHHHSHHHhSHHHhg..",
        "..ghhHHHSSSSHHSSSSHHSSSSHSSSh...",
        "..ghhHHSSSSeeeSSSSSSSSSSeeeSh...",
        ".GGghHHSSSSEEESSSSSSSSSSEEESs...",
        ".GGghHHSSSSwEESSSSSSSSSSwEESs...",
        ".GGghHHSSSSEEESSSSSSSSSSEEESs...",
        ".GGghHHSSSSEiESSSSSSSSSSEiESs...",
        ".GGghHHSSSppSSSSSmSSmSSSSppSs...",
        "....gghSSSSSSSSSSSSmmSSSSSSS....",
        ".....SgRSSSSSSSSSSSSSSSSSSs.....",
        ".......sSSSSSSSSSSSSSSSSs.......",
        "..........ssssssssssss..........",
        "..........kbYYbSSbYYbk..........",
        "......BBbbbbYbbbbbbYbbbbBB......",
        "......qBkbbbbYbbbbYbbbbkBq......",
        "......BBkbbbbbYbbYbbbbbkBB......",
        "......SSkBqqbbbWWWWbbbbkSSs.....",
        "......SSkBYYbbbWRRWbbbbkss......",
        ".....SS.kBbbbbbWCCWbbbbk........",
        ".....sQ.kBbbbbbWWWWbbbbk........",
        "........kkkkkkkxxkkkkkkk........",
        ".........ZZZZZZZZZZZZZZ.........",
        "........ZZZZZz....zzzzzz........",
        ".......ZZZZZz......zzzzzz.......",
        ".......ZZZZZz......zzzzzz.......",
        ".......OOOOO........OOOOOO......",
        "......OOOOOx........OOOOxO......",
    ],
    [
        ".................hh.............",
        "...............hhh..............",
        "...........gggGGGGggg...........",
        "........ggghHHHHHHHHhggg........",
        "......gghHHHjjjjHHHHHHHhgg......",
        ".....ghHHHjjjjHHHHHHHHHHhhg.....",
        "....ghHHHjjHHHHHHHHHHHHhHHhg....",
        "...ghHHHHHHHHHhHHHHHHHhHHHHhg...",
        "...ghHHHHHHHHhHHHHHHHhHHHHHhg...",
        "..ghHHHHHHHhHHHHHHHhHHHHHHHHhg..",
        "..ghHHHHHhHHHHHHhHHHHHHhHHHHhg..",
        "..ghHHHShHHHSHHhHHHSHHHhSHHHhg..",
        "..ghhHHHSSSSHHSSSSHHSSSSHSSSh...",
        "..ghhHHSSSSeeeSSSSSSSSSSeeeSh...",
        ".GGghHHSSSSEEESSSSSSSSSSEEESs...",
        ".GGghHHSSSSwEESSSSSSSSSSwEESs...",
        ".GGghHHSSSSEEESSSSSSSSSSEEESs...",
        ".GGghHHSSSSEiESSSSSSSSSSEiESs...",
        ".GGghHHSSSppSSSSSmSSmSSSSppSs...",
        "....gghSSSSSSSSSSSSmmSSSSSSS....",
        ".....SgRSSSSSSSSSSSSSSSSSSs.....",
        ".......sSSSSSSSSSSSSSSSSs.......",
        "..........ssssssssssss..........",
        "..........kbYYbSSbYYbk..........",
        "......BBbbbbYbbbbbbYbbbbBB......",
        "......qBkbbbbYbbbbYbbbbkBq......",
        "......BBkbbbbbYbbYbbbbbkBB......",
        "......SSkBqqbbbWWWWbbbbkSS......",
        "......SSkBYYbbbWRRWbbbbkSS......",
        "......sskBbbbbbWCCWbbbbkss......",
        "........kBbbbbbWWWWbbbbk........",
        "........kkkkkkkxxkkkkkkk........",
        ".........ZZZZZZZZZZZZZZ.........",
        "..........zzzzzZZZZZZ...........",
        "..........zzzzzZZZZZZ...........",
        "...........OOOOZZZZZZ...........",
        "...............OOOOOOO..........",
        "...............OOOOOxO..........",
    ],
    [
        ".................hh.............",
        "...............hhh..............",
        "...........gggGGGGggg...........",
        "........ggghHHHHHHHHhggg........",
        "......gghHHHjjjjHHHHHHHhgg......",
        ".....ghHHHjjjjHHHHHHHHHHhhg.....",
        "....ghHHHjjHHHHHHHHHHHHhHHhg....",
        "...ghHHHHHHHHHhHHHHHHHhHHHHhg...",
        "...ghHHHHHHHHhHHHHHHHhHHHHHhg...",
        "..ghHHHHHHHhHHHHHHHhHHHHHHHHhg..",
        "..ghHHHHHhHHHHHHhHHHHHHhHHHHhg..",
        "..ghHHHShHHHSHHhHHHSHHHhSHHHhg..",
        "..ghhHHHSSSSHHSSSSHHSSSSHSSSh...",
        "..ghhHHSSSSeeeSSSSSSSSSSeeeSh...",
        ".GGghHHSSSSEEESSSSSSSSSSEEESs...",
        ".GGghHHSSSSwEESSSSSSSSSSwEESs...",
        ".GGghHHSSSSEEESSSSSSSSSSEEESs...",
        ".GGghHHSSSSEiESSSSSSSSSSEiESs...",
        ".GGghHHSSSppSSSSSmSSmSSSSppSs...",
        "....gghSSSSSSSSSSSSmmSSSSSSS....",
        ".....SgRSSSSSSSSSSSSSSSSSSs.....",
        ".......sSSSSSSSSSSSSSSSSs.......",
        "..........ssssssssssss..........",
        "..........kbYYbSSbYYbk..........",
        "......BBbbbbYbbbbbbYbbbbBB......",
        "......qBkbbbbYbbbbYbbbbkBq......",
        "......BBkbbbbbYbbYbbbbbkBB......",
        ".....sSSkBqqbbbWWWWbbbbkSS......",
        "......sskBYYbbbWRRWbbbbkSS......",
        "........kBbbbbbWCCWbbbbk.SS.....",
        "........kBbbbbbWWWWbbbbk.Qs.....",
        "........kkkkkkkxxkkkkkkk........",
        ".........ZZZZZZZZZZZZZZ.........",
        "........zzzzzz....ZZZZZz........",
        ".......zzzzzz......ZZZZZz.......",
        ".......zzzzzz......ZZZZZz.......",
        ".......OOOOO........OOOOOO......",
        "......OOOOOx........OOOOxO......",
    ],
    [
        ".................hh.............",
        "...............hhh..............",
        "...........gggGGGGggg...........",
        "........ggghHHHHHHHHhggg........",
        "......gghHHHjjjjHHHHHHHhgg......",
        ".....ghHHHjjjjHHHHHHHHHHhhg.....",
        "....ghHHHjjHHHHHHHHHHHHhHHhg....",
        "...ghHHHHHHHHHhHHHHHHHhHHHHhg...",
        "...ghHHHHHHHHhHHHHHHHhHHHHHhg...",
        "..ghHHHHHHHhHHHHHHHhHHHHHHHHhg..",
        "..ghHHHHHhHHHHHHhHHHHHHhHHHHhg..",
        "..ghHHHShHHHSHHhHHHSHHHhSHHHhg..",
        "..ghhHHHSSSSHHSSSSHHSSSSHSSSh...",
        "..ghhHHSSSSeeeSSSSSSSSSSeeeSh...",
        ".GGghHHSSSSEEESSSSSSSSSSEEESs...",
        ".GGghHHSSSSwEESSSSSSSSSSwEESs...",
        ".GGghHHSSSSEEESSSSSSSSSSEEESs...",
        ".GGghHHSSSSEiESSSSSSSSSSEiESs...",
        ".GGghHHSSSppSSSSSmSSmSSSSppSs...",
        "....gghSSSSSSSSSSSSmmSSSSSSS....",
        ".....SgRSSSSSSSSSSSSSSSSSSs.....",
        ".......sSSSSSSSSSSSSSSSSs.......",
        "..........ssssssssssss..........",
        "..........kbYYbSSbYYbk..........",
        "......BBbbbbYbbbbbbYbbbbBB......",
        "......qBkbbbbYbbbbYbbbbkBq......",
        "......BBkbbbbbYbbYbbbbbkBB......",
        "......SSkBqqbbbWWWWbbbbkSS......",
        "......SSkBYYbbbWRRWbbbbkSS......",
        "......sskBbbbbbWCCWbbbbkss......",
        "........kBbbbbbWWWWbbbbk........",
        "........kkkkkkkxxkkkkkkk........",
        ".........ZZZZZZZZZZZZZZ.........",
        "..........zzzzzZZZZZZ...........",
        "..........zzzzzZZZZZZ...........",
        "...........OOOOZZZZZZ...........",
        "...............OOOOOOO..........",
        "...............OOOOOxO..........",
    ],
]

# All characters use the same cute style as the player: a big round
# head (more than half of the height), big eyes, a small body.

# The referee: black buzz cut, thick eyebrows, a moustache, a whistle
# on a cord, a badge and a yellow and red card in his pocket.
REFEREE = [
    "................................",
    "................................",
    "...........hhhhhhhhhh...........",
    "........hhhhHHHHHHHHhhhh........",
    "......hhHHHHHHHHHHHHHHHHhh......",
    ".....hHHHjHHHHHHHHHjHHHHHHh.....",
    "....hHHHHHHHHHHHHHHHHHHHHHHh....",
    "...hHHHHHHHHHHHHHHHHHHHHHHHHh...",
    "...hHHHHHHHHHHHHHHHHHHHHHHHHh...",
    "...hHHHHHHHHHHHHHHHHHHHHHHHHh...",
    "..hHHHHHHHHHHHHHHHHHHHHHHHHHHh..",
    "..hHSSSSSSSSSSSSSSSSSSSSSSSSHh..",
    "..hHSSSSSSSSSSSSSSSSSSSSSSSSHh..",
    "..hHSSSeeeeSSSSSSSSSSeeeeSSSHh..",
    "..sSSSSSEEESSSSSSSSSSEEESSSSSs..",
    ".ssSSSSSwEESSSSSSSSSSwEESSSSSss.",
    ".ssSSSSSEEESSSSSSSSSSEEESSSSSss.",
    "..sSSSSSEiESSSSSSSSSSEiESSSSSs..",
    "..sSSSSppSSShhhhhhhhSSppSSSSSs..",
    "....sSSSSSSShhSSSShhSSSSSSSs....",
    ".......sSSSSSSSSmmSSSSSSs.......",
    "..........ssssssssssss..........",
    "..........kbBBWSSWBBbk..........",
    "......BBBBBBWBBBBBBBBBbbbb......",
    "......BBBBYBBWBBBBBYRBbbbb......",
    "......SSBBBBBBccBBkkkBbbSS......",
    "......SSBBBBBBBBBBBBBBbbSS......",
    "......SSBBBBBBBBBBBBBBbbSS......",
    "......ssBBBBBBBBBBBBBBbbss......",
    "........BBBBBBBBBBBBBBbb........",
    "........kkkkkkkkkkkkkkkz........",
    "........kkkkkkkzzkkkkkkz........",
    ".........kkkkkz..kkkkkz.........",
    "..........SSSs....SSSs..........",
    "..........kkkz....kkkz..........",
    "..........kkkz....kkkz..........",
    ".........OOOOO....OOOOO.........",
    "........OxxOOO....OOOxxO........",
]

# The steward: blue cap, hi-vis vest with reflective stripes and a radio.
STEWARD = [
    "................................",
    "................................",
    "...........DDDDDDDDDD...........",
    "........DDDDDWWWDDDDDDDD........",
    ".......DDDDDDWRWDDDDDDDFF.......",
    ".....DDDDDDDWWWDDDDDDDDDFFF.....",
    "....DDDDDDDDDDDDDDDDDDDDFFFF....",
    "...DDDDDDDDDDDDDDDDDDDDDDFFFF...",
    "...FFFFFFFFFFFFFFFFFFFFFFFFFF...",
    ".FFFFFFFFFFFFFFFFFFFFFFFFFFFFFF.",
    "..sSSSSSSSSSSSSSSSSSSSSSSSSSSs..",
    "..sSSSSSSSSSSSSSSSSSSSSSSSSSSs..",
    "..sSSSSSSSSSSSSSSSSSSSSSSSSSSs..",
    "..hHSSSSeeeSSSSSSSSSSeeeSSSSHh..",
    "..sSSSSSEEESSSSSSSSSSEEESSSSSs..",
    ".ssSSSSSwEESSSSSSSSSSwEESSSSSss.",
    ".ssSSSSSEEESSSSSSSSSSEEESSSSSss.",
    "..sSSSSSEiESSSSSSSSSSEiESSSSSs..",
    "..sSSSSppSSSSSmSSmSSSSppSSSSSs..",
    "....sSSSSSSSSSSmmSSSSSSSSSSs....",
    ".......sSSSSSSSSSSSSSSSSs.......",
    "..........ssssssssssss..........",
    "...........VVVVSSVVVV...........",
    "......VVVVVVVVVVVVVVVVyyyy......",
    "......VVVVVVVVVVVVkkVVyyyy......",
    "......SSVVVVVVVVVVkGVVyySS......",
    "......SSWWWWWWWWWWWWWWWWSS......",
    "......SSVVVVVVVVVVVVVVyySS......",
    "......ssWWWWWWWWWWWWWWWWss......",
    "........VVVVVVVVVVVVVVyy........",
    "........NNNNNNNNNNNNNNMM........",
    "........NNNNNNNMMNNNNNNM........",
    ".........NNNNNM..NNNNNM.........",
    ".........NNNNNM..NNNNNM.........",
    ".........NNNNNM..NNNNNM.........",
    ".........NNNNNM..NNNNNM.........",
    ".........OOOOOO..OOOOOO.........",
    "........OxxOOOO..OOOOxxO........",
]

# The home striker: spiky blond hair, laughing (eyes closed), number 9.
# Kit colours come from STRIKER_COLOURS: red shirt, red shorts, red socks.
STRIKER = [
    "........h...hh...hh...h.........",
    "........hH.hHHh.hHHh.hHh........",
    "........HHHhHHHHHHHHhHHH........",
    ".......hHHHjjHHHHjjHHHHhh.......",
    "......hhHHHHjjjjHHHHHHHHhh......",
    ".....hHHHHjjjjHHHHHHHHHHHHh.....",
    "....hHHHHjjHHHHHHHHHHHHhHHhh....",
    "...hHHHHHHHHHHhHHHHHHHhHHHHHh...",
    "...hHHHHHHHHHhHHHHHHHhHHHHHHh...",
    "...hHHHHHHHhHHHHHHHhHHHHHHHHh...",
    "..hHHHHHHhHHHHHHhHHHHHHhHHHHHh..",
    "..hHHHSHHHSHHHSHHHHSHHHSHHHHHh..",
    "..hHHSSSHSSSSHSSSSSSHSSSHSSHHh..",
    "..hHSSSSeeeSSSSSSSSSSeeeSSSSHh..",
    "..sSSSSSSSSSSSSSSSSSSSSSSSSSSs..",
    ".ssSSSSSSESSSSSSSSSSSSESSSSSSss.",
    ".ssSSSSSESESSSSSSSSSSESESSSSSss.",
    "..sSSSSSSSSSSSSSSSSSSSSSSSSSSs..",
    "..sSSSSppSSSSmmmmmmSSSppSSSSSs..",
    "....sSSSSSSSSmTTTTmSSSSSSSSs....",
    ".......sSSSSSSSmrrmSSSSSs.......",
    "..........ssssssssssss..........",
    "..........kbBBWSSWBBbk..........",
    "......BBBBBBBBBBBBBBBBbbbb......",
    "......BBBBBBBBWWWBBBBBbbbb......",
    "......SSBBBBBBWBWBBBBBbbSS......",
    "......SSBBBBBBWWWBBBBBbbSS......",
    "......SSBBBBBBBBWBBBBBbbSS......",
    "......ssBBBBBBWWWBBBBBbbss......",
    "........BBBBBBBBBBBBBBbb........",
    "........BBBBBBBBBBBBBBBb........",
    "........BBBBBBBbbBBBBBBb........",
    ".........BBBBBb..BBBBBb.........",
    "..........SSSs....SSSs..........",
    "..........BBBb....BBBb..........",
    "..........BBBb....BBBb..........",
    ".........OOOOO....OOOOO.........",
    "........OxxOOO....OOOxxO........",
]

# The away captain: angry, shouting, fist in the air, captain's armband,
# number 4. Colours come from CAPTAIN_COLOURS.
CAPTAIN = [
    "..............................SSS.",
    ".............................SSSSs",
    "...........hhhhhhhhhh........SStSs",
    "........hhhhHHHHHHHHhhhh.....SSSss",
    "......hhHHHHHHHHHHHHHHHHhh....sss.",
    ".....hHHHjHHHHHHHHHjHHHHHHh...SSs.",
    "....hHHHHHHHHHHHHHHHHHHHHHHh..SSs.",
    "...hHHHHHHHHHHHHHHHHHHHHHHHHh.SSs.",
    "...hHHHHHHHHHHHHHHHHHHHHHHHHh.SSs.",
    "...hHHHHHHHHHHHHHHHHHHHHHHHHh.SSs.",
    "..hHHHHHHHHHHHHHHHHHHHHHHHHHH.SSs.",
    "..hHSSSSSSSSSSSSSSSSSSSSSSSSH.SSs.",
    "..hHSSSSSSSSSSSSSSSSSSSSSSSSH.SSs.",
    "..hHSSSeeeSSSSSSSSSSSSSeeeSSH.SSs.",
    "..sSSSSSSeESSSSSSSSSSEeSSSSSS.SSs.",
    ".ssSSSSSEEESSSSSSSSSSEEESSSSS.SSs.",
    ".ssSSSSSwEESSSSSSSSSSwEESSSSS.SSs.",
    "..sSSSSSEEESSSSSSSSSSEEESSSSS.BBb.",
    "..sSSSSppSSSSSmmmmSSSSppSSSSS.BBb.",
    "....sSSSSSSSSSmrrrrmSSSSSSSs..BBb.",
    ".......sSSSSSSSmrrmSSSSSs.....BBb.",
    "..........ssssssssssss....BBBBb...",
    "..........kbBBWSSWBBbk....Bbb.....",
    "......BBBBBBBBBBBBBBBBbbbb........",
    "......BBBBBBBBWBWBBBBBbbbb........",
    "......YYBBBBBBWBWBBBBBbbSS........",
    "......SSBBBBBBWWWBBBBBbbSS........",
    "......SSBBBBBBBBWBBBBBbbSS........",
    "......ssBBBBBBBBWBBBBBbbss........",
    "........BBBBBBBBBBBBBBbb..........",
    "........WWWWWWWWWWWWWWWc..........",
    "........WWWWWWWccWWWWWWc..........",
    ".........WWWWWc..WWWWWc...........",
    "..........SSSs....SSSs............",
    "..........BBBb....BBBb............",
    "..........BBBb....BBBb............",
    ".........OOOOO....OOOOO...........",
    "........OxxOOO....OOOxxO..........",
]

# The captain without his raised arm, for the sad away players in the end
# clips: in the top 23 rows everything right of column 26 (the arm) is
# made transparent, the rest of the picture stays the same.
CAPTAIN_ARM_DOWN = []
for row in CAPTAIN[:23]:
    CAPTAIN_ARM_DOWN.append(row[:26] + "." * (len(row) - 26))
CAPTAIN_ARM_DOWN = CAPTAIN_ARM_DOWN + CAPTAIN[23:]

# The linesman: curly ginger hair, freckles, a worried look.
# Kit colours come from LINESMAN_COLOURS. The flag is drawn in rooms.py.
LINESMAN = [
    "................................",
    "..........hh.hh.hh.hh...........",
    ".........hHHhhHHhhHHhh..........",
    ".......hHhjHHhHjHHhHjHHh........",
    "......hHHhHjhHHhHjhHHhHHhh......",
    ".....hHjhHHhHjhHHhHjhHHhHHh.....",
    "....hHHhHjhHHhHjhHHhHjhHHHhh....",
    "...hHjhHHhHjhHHhHjhHHhHjhHHhh...",
    "...hHHhHjhHHhHjhHHhHjhHHhHHhh...",
    "..hHjhHHhHjhHHhHjhHHhHjhHHhHhh..",
    ".hHhhHjhHHhHjhHHhHjhHHhHjhHHhHh.",
    ".hHhHhSShHSShHSShHSShHSShHShhHh.",
    ".hHhSSSSSSSSSSSSSSSSSSSSSSSShHh.",
    ".hHhSSSSSSeeSSSSSSSSeeSSSSSShHh.",
    ".hHhSSSSeSSSSSSSSSSSSSSeSSSShHh.",
    ".hHhSSSSEEESSSSSSSSSSEEESSSShHh.",
    ".ssSSSSSwEESSSSSSSSSSwEESSSSSss.",
    "..sSSSSSEiESSSSSSSSSSEiESSSSSs..",
    "..sSSQSQSSSSSSSSSSSSSSQSQSSSSs..",
    "....sSSSSSSSSSSmmSSSSSSSSSSs....",
    ".......sSSSSSSSmSSmSSSSSs.......",
    "..........ssssssssssss..........",
    "..........kbBBWSSWBBbk..........",
    "......BBBBBBBBBBBBBBBBbbbb......",
    "......BBBBBBBBBBBBBBBBbbbb......",
    "......SSBBBBBBBBBBBBBBbbSS......",
    "......SSBBBBBBBBBBBBBBbbSS......",
    "......SSBBBBBBBBBBBBBBbbSS......",
    "......ssBBBBBBBBBBBBBBbbss......",
    "........BBBBBBBBBBBBBBbb........",
    "........kkkkkkkkkkkkkkkz........",
    "........kkkkkkkzzkkkkkkz........",
    ".........kkkkkz..kkkkkz.........",
    "..........SSSs....SSSs..........",
    "..........kkkz....kkkz..........",
    "..........kkkz....kkkz..........",
    ".........OOOOO....OOOOO.........",
    "........OxxOOO....OOOxxO........",
]

# Bernie, the club's bear mascot: a big round head with teddy-bear button
# eyes, soft cheeks, a round nose and a head-cam, on a small round body in a
# red shirt with white stripes. He waves with a stubby paw.
BERNIE = [
    "...................kkkkkk...................",
    ".......AA........AAkGGkkRAA........dd.......",
    ".....AAAAAA..AAAAAAkkkkkkAAAAAA..dddddd.....",
    "....AAAAAAAAAAAAAAAAAAAAAAAAAAAAAddddddd....",
    "...AAAAffAAAaaaaaaaaaaAAAAAAAAAAAAAffdddd...",
    "...AAAffAaaaaaaaaaaaaaaaaAAAAAAAAAAAffddd...",
    "...AAAfAaaaaaaaaaaaaaaaaaaAAAAAAAAAAAfddd...",
    "...AAAAAaaaaaaaaaaaaaaaaaaAAAAAAAAAAAAddd...",
    "...AAAAAAaaaaaaaaaaaaaaaaAAAAAAAAAAAAAAdd...",
    "....AAAAAAAEEEaaaaaaaaAAAAAAAAEEEAAAAAAd....",
    "....AAAAAAEwwEEAAAAAAAAAAAAAAEwwEEAAAAAA....",
    "....AAAAAAEwwEEAAAAAAAAAAAAAAEwwEEAAAAAA....",
    "....AAAAAAEEEEEAAAAAAAAAAAAAAEEEEEAAAAAA....",
    "....AAAAAAEEEEEAAooooooooooAAEEEEEAAAAAA....",
    "....AAAAAAAEEEAAoooEEEEEEoooAAEEEAAAAAAA....",
    "....AAAAAAAAAAAoooEEwwEEEEoooAAAAAAAAAAA....",
    "....AppppAAAAAooooEEEEEEEEooooAAAAAppppA....",
    "....AppppAAAAAooooooEEEEooooooAAAAAppppd....",
    ".....AAAAAAAAAoEoooooEEoooooEoAAAAAAAAA.....",
    ".....AAAAAAAAAooEooooEEooooEooAAAAAAAAd.....",
    "......AAAAAAAAoooEEEEEEEEEEoooAAAAAAAd......",
    ".......AAAAAAAAooooooooooooooAAAAAAAd.......",
    "........AAAAAAAAooooooooooooAAAAAAAd........",
    ".........AAAAAAAAooooooooooAAAAAAdd.........",
    "...........AAAAAAAAAAAAAAAAAAAAdd...........",
    ".............AAAAAAAAAAAAAAdddd.............",
    ".............RRRRRRRRRRRRRRRRRRR.....AoA....",
    "............RRRRRRRRRRRRRRRRRRRR...oAAAAAo..",
    "............RRRRRRRRRRRRRRRRRRRRR..AAAAAAA..",
    "...........RRRRRRRRRRRRRRRRRRRRRR.AAAAoAAAA.",
    "...........WWWWWWWWWWWWWWWWWWWWWWWAAAoooAAA.",
    "..........WWWWWWWWWWWWWWWWWWWWWWWWAAoooooAA.",
    "..........RRRRRRRRRRRRRRRRRRRRRRRRRAAoooAA..",
    ".........RRRRRRRRRRRRRRRRRRRRRRRRRRAAAoAAA..",
    ".......RRRRRRRRRRRRRRRRRRRRRRRRRWWWWWAAA....",
    "......RRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR.....",
    "......RRRRRRWWWWWWWWWWWWWWWWWWWcRRRRRRR.....",
    ".....RRRRRRRRWWWWWWWWWWWWWWWWWWcRRRRRRR.....",
    "......RRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR.....",
    ".....WWWWWWWWRRRRRRRRRRRRRRRRRRRlRRRRR......",
    ".....WWAAAWWWRRRRRRRRRRRRRRRRRRRll..........",
    "......aaaAARRRRRRRRRRRRRRRRRRRRRlll.........",
    ".....AaaaAAAWWWWWWWWWWWWWWWWWWWWccc.........",
    ".....AaaaAAAWWWWWWWWWWWWWWWWWWWWccc.........",
    ".....AaaaAAARRRRRRRRRRRRRRRRRRRRll..........",
    ".....AaaaAAARRRRRRRRRRRRRRRRRRRRll..........",
    ".....AAoooAARRRRRRRRRRRRRRRRRRRlll..........",
    "......AoooARRRRRRRRRRRRRRRRRRRRlll..........",
    ".......AoA.WWWWWWWWWWWWWWWWWWWWcc...........",
    "...........WWWWWWWWWWWWWWWWWWWccc...........",
    "...........RRRRRRRRRRRRRRRRRRRlll...........",
    "............RRRRRRRRRRRRRRRRRlll............",
    ".............RRRRRRRRRRRRRRRlll.............",
    ".............ARRRRRRRRRRRRRlllA.............",
    "............AAAWWWWWWWWWWWcccAAA............",
    "............AAAAWWWWWWWWccccAAAA............",
    "............AAAAAAAA....AAAAAAAA............",
    "............AaaaAAAA....AaaaAAAA............",
    "...........AaaaaaAAAA..AaaaaaAAAA...........",
    "..........AAAaaaooAAAAAAAaaaooAAAA..........",
    "...........AAooooooAA..AAooooooAA...........",
    "............AAooooAA....AAooooAA............",
]

# Bernie's fur, muzzle, eyes and shirt shadow (same letters, other colours).
BERNIE_COLOURS = {"a": (205, 140, 85), "A": (170, 105, 55), "d": (125, 75, 40),
                  "o": (240, 215, 170), "f": (210, 175, 125), "i": (95, 140, 165),
                  "l": (190, 30, 45), "c": (225, 205, 205)}

# Bernie in two parts, for Dave's reveal: the bear head (the mask,
# rows 0 to 25) and the body (from the neck down).
BERNIE_HEAD = BERNIE[:26]
BERNIE_BODY = BERNIE[26:]

# Dave, the missing VAR operator, without his mask: messy hair, glasses,
# worried eyebrows, stubble and a nervous mouth.
DAVE_HEAD = [
    "................................",
    "...........h.hh..hh.h...........",
    "..........hHHhhhHHHHhh..........",
    "........hhhHHHHHHHHHHhhh........",
    "......hhHHHHjjjjHHHHHHHHhh......",
    ".....hHHHHjjjjHHHHHHHHHHHHh.....",
    "....hHHHHjjHHHHHHHHHHHHhHHhh....",
    "...hHHHHHHHHHHhHHHHHHHhHHHHHh...",
    "...hHHHHHHHHHhHHHHHHHhHHHHHHh...",
    "...hHHHHHHHhHHHHHHHhHHHHHHHHh...",
    "..hHHHhHHHhHHhHHHhHHHhHHHhHHHh..",
    "..hHHSHHSHHHSHHSHHHSHHSHHHSHHh..",
    "..hHSSSSHSSSSSSSHSSSSSSHSSSSHh..",
    "..hHSSSSSSeeSSSSSSSSeeSSSSSSHh..",
    "..sSSSSkkkkkSSSSSSSkkkkkSSSSSs..",
    ".ssSkkkkwEEkkkkkkkkkwEEkSSSSSss.",
    ".ssSSSSkEEEkSSSSSSSkEEEkSSSSSss.",
    "..sSSSSkkkkkSSSSSSSkkkkkSSSSSs..",
    "..sSSSSppSSSSSSSSSSSSSppSSSSSs..",
    "....sSQSQSSSSmmSmmSSSSQSQSSs....",
    ".......sSSQSQSSQSQSSQSQSs.......",
    "..........ssssssssssss..........",
]

# Gianno Infantini, the TV guest expert (head and shoulders, shown in the TV):
# a shiny bald head, friendly eyebrows, a closed-mouth smile, a dark navy
# suit, a white shirt, a small gold pin on the lapel and a dark navy tie
# that is much too short: its tip was cut off (the clue in the Server Room),
# so the white shirt shows under its straight, cut end.
PUNDIT = [
    "................................",
    "................................",
    "...........ssssssssss...........",
    "........sssSttttSSSSSsss........",
    "......ssSSStttSSSSSSSSSSss......",
    ".....sSSSSttSSSSSSSSSSSSSSs.....",
    "....sSSSSSSSSSSSSSSSSSSSSSSs....",
    "...sSSSSSSSSSSSSSSSSSSSSSSSSs...",
    "...sSSSSSSSSSSSSSSSSSSSSSSSSs...",
    "...sSSSSSSSSSSSSSSSSSSSSSSSSs...",
    "..sSSSSSSSSSSSSSSSSSSSSSSSSSSs..",
    "..sSSSSSSSSSSSSSSSSSSSSSSSSSSs..",
    "..sSSSSSSSSSSSSSSSSSSSSSSSSSSs..",
    "..sSSSSSeeeSSSSSSSSSSeeeSSSSSs..",
    "..sSSSSSSSSSSSSSSSSSSSSSSSSSSs..",
    ".ssSSSSSEEESSSSSSSSSSEEESSSSSss.",
    ".ssSSSSSEiESSSSSSSSSSEiESSSSSss.",
    "..sSSSSSSSSSSSSSSSSSSSSSSSSSSs..",
    "..sSSSSSSSSmSSSSSSSSmSSSSSSSSs..",
    "....sSSSSSSSmmmmmmmmSSSSSSSs....",
    ".......sSSSSSSSSSSSSSSSSs.......",
    "..........ssssssssssss..........",
    "............WWSSSSWW............",
    "............uWWllWWU............",
    ".........uuuUUWllWUUUUU.........",
    ".......uuuuUUUWllWUUUUUUU.......",
    "......uuuuuUUUWWWWUUUUUUUU......",
    ".....uuuuuuUUUUWWUUUUUUUUUU.....",
    "....uuuuuuUUUUUUUUUUUUYUUUUU....",
    "...uuuuuuuUUUUUUUUUUUUUUUUUUU...",
    "..uuuuuuuuUUUUUUUUUUUUUUUUUUUU..",
    ".uuuuuuuuuUUUUUUUUUUUUUUUUUUUUU.",
    "uuuuuuuuuUUUUUUUUUUUUUUUUUUUUUUU",
    "uuuuuuuuuUUUUUUUUUUUUUUUUUUUUUUU",
    "uuuuuuuuuUUUUUUUUUUUUUUUUUUUUUUU",
]

# Infantini gets more nervous with every clue the player finds (0 to 4).
# For each mood only some rows of PUNDIT change: the eyebrows, the mouth
# and the sweat drops ("C", light blue). The row number is the key.
# Mood 0: calm smile. 1: worried eyebrows, flat mouth.
# 2: wobbly mouth and sweat drops. 3: angry eyebrows, gritted teeth, more sweat.
# 4: furious, with steam coming out next to his ears.
PUNDIT_MOOD_ROWS = [
    # mood 0 (calm): nothing changes
    {
    },
    # mood 1 (nervous)
    {
        12: "..sSSSSSSSeSSSSSSSSSSeSSSSSSSs..",
        13: "..sSSSSSeeSSSSSSSSSSSSeeSSSSSs..",
        18: "..sSSSSSSSSSSSSSSSSSSSSSSSSSSs..",
        19: "....sSSSSSSSSmmmmmmSSSSSSSSs....",
    },
    # mood 2 (sweating)
    {
        8: "...sSSCSSSSSSSSSSSSSSSSSSSSSs...",
        9: "...sSSCSSSSSSSSSSSSSSSSSCSSSs...",
        10: "..sSSSSSSSSSSSSSSSSSSSSSCSSSSs..",
        12: "..sSSSSSSSeSSSSSSSSSSeSSSSSSSs..",
        13: "..sSSSSSeeSSSSSSSSSSSSeeSSSSSs..",
        18: "..sSSSSSSSSSSSmmSSmmSSSSSSSSSs..",
        19: "....sSSSSSSSmmSSmmSSSSSSSSSs....",
    },
    # mood 3 (panicking and angry)
    {
        5: ".....sSSSSttSSSSSSSSCSSSSSs.....",
        6: "....sSSSSSSSSSSSSSSSCSSSSSSs....",
        8: "...sSSCSSSSSSSSSSSSSSSSSSSSSs...",
        9: "...sSSCSSSSSSSSSSSSSSSSSCSSSs...",
        10: "..sSSSSSSSSSSSSSSSSSSSSSCSSSSs..",
        11: "..sSSSSSSSSSSSSSSSSSSSSSSSCSSs..",
        12: "..sSSSSSSSSSSSSSSSSSSSSSSSCSSs..",
        13: "..sSSSSSeSSSSSSSSSSSSSSeSSSSSs..",
        14: "..sSSSSSSeeSSSSSSSSSSeeSSSSSSs..",
        18: "..sSSSSSSSSSmmmmmmmmSSSSSSSSSs..",
        19: "....sSSSSSSSmTTTTTTmSSSSSSSs....",
    },
    # mood 4 (furious): like mood 3, plus steam ("c") puffing out
    # next to his ears and a wide open, shouting mouth.
    {
        5: ".....sSSSSttSSSSSSSSCSSSSSs.....",
        6: "....sSSSSSSSSSSSSSSSCSSSSSSs....",
        8: "...sSSCSSSSSSSSSSSSSSSSSSSSSs...",
        9: "...sSSCSSSSSSSSSSSSSSSSSCSSSs...",
        10: "c.sSSSSSSSSSSSSSSSSSSSSSCSSSSs.c",
        11: ".csSSSSSSSSSSSSSSSSSSSSSSSCSSsc.",
        12: "c.sSSSSSSSSSSSSSSSSSSSSSSSCSSs.c",
        13: "..sSSSSSeSSSSSSSSSSSSSSeSSSSSs..",
        14: "..sSSSSSSeeSSSSSSSSSSeeSSSSSSs..",
        18: "..sSSSSSSSSmmmmmmmmmmSSSSSSSSs..",
        19: "....sSSSSSSmrrrrrrrrmSSSSSSs....",
        20: ".......sSSSSmmmmmmmmSSSSs.......",
    },
]

# His skin gets redder with every mood ("S" skin, "s" shadow, "t" shine).
PUNDIT_MOOD_SKIN = [
    {},
    {"S": (250, 180, 150), "s": (214, 135, 105), "t": (255, 215, 195)},
    {"S": (245, 150, 125), "s": (205, 110, 90), "t": (255, 195, 175)},
    {"S": (235, 110, 95), "s": (190, 75, 65), "t": (250, 165, 150)},
    {"S": (220, 70, 60), "s": (170, 45, 40), "t": (240, 130, 115)},
]

# Infantini's whole body, for the end clips in the TV studio. His head
# comes from PUNDIT (rows 0 to 21, with the face of his mood), and these
# rows are his body: navy suit ("U", "u"), white shirt and the cut-off
# blue tie ("W", "l"), the gold pin ("Y"), hands ("S"), dark trousers
# ("u", "K") and black shoes ("O").
INFANTINI_BODY = [
    "...........UUWWllWWUU...........",
    "......UUUUUUUUWllWUUUUuuuu......",
    "......UUUUUUUUUWWUUUYUuuuu......",
    "......SSUUUUUUUUUUUUUUuuSS......",
    "......SSUUUUUUUUUUUUUUuuSS......",
    "......SSUUUUUUUUUUUUUUuuSS......",
    "......ssUUUUUUUUUUUUUUuuss......",
    "........UUUUUUUUUUUUUUuu........",
    "........uuuuuuuuuuuuuuKK........",
    "........uuuuuuuKKuuuuuuK........",
    ".........uuuuuK..uuuuuK.........",
    ".........uuuuuK..uuuuuK.........",
    ".........uuuuuK..uuuuuK.........",
    ".........uuuuuK..uuuuuK.........",
    ".........OOOOOO..OOOOOO.........",
    "........OxxOOOO..OOOOxxO........",
]

# A police officer for the end clip: a serious face (low, straight
# eyebrows, a small straight mouth, no rosy cheeks), a police cap with a
# blue-and-white checked band and a gold badge, a radio on the shoulder
# and a hi-vis vest with checked stripes. The word POLICE is written on
# the vest in the clip. The colours come from POLICE_COLOURS.
POLICE = [
    "................................",
    "................................",
    "...........DDDDDDDDDD...........",
    "........DDDDDWWWDDDDDDDD........",
    ".......DDDDDDWRWDDDDDDDFF.......",
    ".....DDDDDDDWWWDDDDDDDDDFFF.....",
    "....DDDDDDDDDDDDDDDDDDDDFFFF....",
    "...DDDDDDDDDDDDDDDDDDDDDDFFFF...",
    "...WDWDWDWDWDWDWDWDWDWDWDWDWD...",
    ".FFFFFFFFFFFFFFFFFFFFFFFFFFFFFF.",
    "..sSSSSSSSSSSSSSSSSSSSSSSSSSSs..",
    "..sSSSSSSSSSSSSSSSSSSSSSSSSSSs..",
    "..sSSSSSSSSSSSSSSSSSSSSSSSSSSs..",
    "..hHSSSSeeeeSSSSSSSSeeeeSSSSHh..",
    "..sSSSSSEEESSSSSSSSSSEEESSSSSs..",
    ".ssSSSSSwEESSSSSSSSSSwEESSSSSss.",
    ".ssSSSSSEEESSSSSSSSSSEEESSSSSss.",
    "..sSSSSSEiESSSSSSSSSSEiESSSSSs..",
    "..sSSSSSSSSSSSmmmmSSSSSSSSSSSs..",
    "....sSSSSSSSSSSSSSSSSSSSSSSs....",
    ".......sSSSSSSSSSSSSSSSSs.......",
    "..........ssssssssssss..........",
    "...........VVVVSSVVVV...........",
    "......VVVVVVVVVVVVVVVVyyyy......",
    "......VVVVVVVVVVVVkkVVyyyy......",
    "......SSVVVVVVVVVVkGVVyySS......",
    "......SSWDWDWDWDWDWDWDWDSS......",
    "......SSVVVVVVVVVVVVVVyySS......",
    "......ssDWDWDWDWDWDWDWDWss......",
    "........VVVVVVVVVVVVVVyy........",
    "........NNNNNNNNNNNNNNMM........",
    "........NNNNNNNMMNNNNNNM........",
    ".........NNNNNM..NNNNNM.........",
    ".........NNNNNM..NNNNNM.........",
    ".........NNNNNM..NNNNNM.........",
    ".........NNNNNM..NNNNNM.........",
    ".........OOOOOO..OOOOOO.........",
    "........OxxOOOO..OOOOxxO........",
]

# The Lucky Whistle: silver, with a red cord.
WHISTLE = [
    "..RRR...........",
    ".R...R..........",
    "R.....R.........",
    "R....cccccccc...",
    ".R..cWWWccccccxx",
    "..RcWWccccccccxx",
    "...ccccccccccx..",
    "....cccxxxxx....",
]

# The USB Stick: a silver plug, a blue body and a red light.
USB = [
    "xxxx..........",
    "ccccuuuuuuuuuu",
    "cWWcuUUUUUUUUu",
    "cWWcuUUUUUURUu",
    "ccccuuuuuuuuuu",
    "xxxx..........",
]

# The Betting Slip: white paper with scribbled lines and a red stamp.
SLIP = [
    "WWWWWWWWWWW",
    "WxxxxxxWWWW",
    "WWWWWWWWWWW",
    "WxxxxWxxxxW",
    "WWWWWWWWWWW",
    "WxxxWWWWRRW",
    "WWWWWWWWRRW",
    "WWWWWWWWWWW",
]

# The gold padlock on the Mascot Changing Room door.
PADLOCK = [
    "..xxxxx..",
    ".x.....x.",
    ".x.....x.",
    "YYYYYYYYY",
    "YqqYYYYYY",
    "YYYYkYYYY",
    "YYYYkYYYY",
    "YYYYYYYYY",
]

# The football.
BALL = [
    "..WWW..",
    ".WkWWW.",
    "WkkWWkW",
    "WWWWkkW",
    "WkWWWWW",
    ".WWkkW.",
    "..WWW..",
]

# The icon above the logo: a VAR screen with a big eye on it.
# The pupil is not in the grid: ui.py draws it, so the eye can look around.
VAR_SCREEN = [
    ".GGGGGGGGGGGGGGGGGGGGGGGGGG.",
    "GGGGGGGGGGGGGGGGGGGGGGGGGGGG",
    "GGFFFFFFFFFFFFFFFFFFFFFFFFGG",
    "GGFFFFFFFFFFFFFFFFFFFFFFFFGG",
    "GGFFFFFFFFWWWWWWWWFFFFFFFFGG",
    "GGFFFFFWWWWWWWWWWWWWWFFFFFGG",
    "GGFFFWWWWWWWWWWWWWWWWWWFFFGG",
    "GGFFWWWWWWWWWWWWWWWWWWWWFFGG",
    "GGFFWWWWWWWWWWWWWWWWWWWWFFGG",
    "GGFFFWWWWWWWWWWWWWWWWWWFFFGG",
    "GGFFFFFWWWWWWWWWWWWWWFFFFFGG",
    "GGFFFFFFFFWWWWWWWWFFFFFFFFGG",
    "GGFFFFFFFFFFFFFFFFFFFFFFFFGG",
    "GGFFFFFFFFFFFFFFFFFFFFFFFFGG",
    "GGGGGGGGGGGGGGGGGGGGGGRRGGGG",
    "GGGGGGGGGGGGGGGGGGGGGGRRGGGG",
    ".GGGGGGGGGGGGGGGGGGGGGGGGGG.",
    "...........gggggg...........",
    "...........gggggg...........",
    ".......gggggggggggggg.......",
]

# The arrow that points at the chosen option on the title screen.
ARROW = [
    "q....",
    "qq...",
    "qqq..",
    "qqqq.",
    "qqqqq",
    "YYYY.",
    "YYY..",
    "YY...",
    "Y....",
]

# Chunky pixel letters for the logo and the title menu. Every letter is
# 7 rows high; "#" is a filled pixel. ui.draw_pixel_text draws them big,
# with an outline and a shadow. Only the letters we need are here.
PIXEL_LETTERS = {
    "A": [".####.", "##..##", "##..##", "######", "##..##", "##..##", "##..##"],
    "C": [".#####", "##....", "##....", "##....", "##....", "##....", ".#####"],
    "E": ["######", "##....", "##....", "#####.", "##....", "##....", "######"],
    "F": ["######", "##....", "##....", "#####.", "##....", "##....", "##...."],
    "G": [".#####", "##....", "##....", "##.###", "##..##", "##..##", ".#####"],
    "H": ["##..##", "##..##", "##..##", "######", "##..##", "##..##", "##..##"],
    "I": ["######", "..##..", "..##..", "..##..", "..##..", "..##..", "######"],
    "L": ["##....", "##....", "##....", "##....", "##....", "##....", "######"],
    "M": ["##...##", "###.###", "#######", "##.#.##", "##...##", "##...##", "##...##"],
    "N": ["##..##", "###.##", "######", "##.###", "##..##", "##..##", "##..##"],
    "O": [".####.", "##..##", "##..##", "##..##", "##..##", "##..##", ".####."],
    "P": ["#####.", "##..##", "##..##", "#####.", "##....", "##....", "##...."],
    "R": ["#####.", "##..##", "##..##", "#####.", "##.##.", "##..##", "##..##"],
    "S": [".#####", "##....", "##....", ".####.", "....##", "....##", "#####."],
    "T": ["######", "..##..", "..##..", "..##..", "..##..", "..##..", "..##.."],
    "U": ["##..##", "##..##", "##..##", "##..##", "##..##", "##..##", ".####."],
    "V": ["##..##", "##..##", "##..##", "##..##", "##..##", ".####.", "..##.."],
    "W": ["##...##", "##...##", "##...##", "##.#.##", "#######", "###.###", "##...##"],
    "X": ["##..##", "##..##", ".####.", "..##..", ".####.", "##..##", "##..##"],
    "Y": ["##..##", "##..##", "##..##", ".####.", "..##..", "..##..", "..##.."],
    ":": ["..", "##", "##", "..", "##", "##", ".."],
}


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


def pundit_rows(mood):
    # Infantini's pixel grid for one mood (0 = calm ... 4 = furious):
    # copy his normal grid and swap in the rows that change for this mood.
    rows = list(PUNDIT)
    changes = PUNDIT_MOOD_ROWS[mood]
    for row_number in changes:
        rows[row_number] = changes[row_number]
    return rows


def pundit_colours(mood):
    # His suit colours, plus the redder skin for this mood.
    colours = dict(PUNDIT_COLOURS)
    colours.update(PUNDIT_MOOD_SKIN[mood])
    return colours


def make_pundit(mood):
    # Infantini on TV (head and shoulders) for one mood.
    return make_sprite(pundit_rows(mood), pundit_colours(mood))


def make_infantini(mood):
    # Infantini's whole body for one mood: his head (the first 22 rows of
    # the TV picture) on top of INFANTINI_BODY.
    rows = pundit_rows(mood)[:22] + INFANTINI_BODY
    return make_sprite(rows, pundit_colours(mood))


def make_sprite(rows, colour_changes=None):
    # Turn a pixel grid into a pygame picture with a dark outline around it.
    # colour_changes (optional) is a dictionary of letters that get a
    # different colour for this character, e.g. {"B": (235, 70, 70)}.

    # Start from a copy of the normal palette, then apply the changes.
    colours = dict(PALETTE)
    if colour_changes is not None:
        colours.update(colour_changes)

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
            if letter in colours:
                picture.set_at((x + 1, y + 1), colours[letter])

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
