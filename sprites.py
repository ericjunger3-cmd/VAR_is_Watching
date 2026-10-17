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
    # headset: dark grey, grey; red light (also the red of Pombo's scarf)
    "g": (70, 72, 85), "G": (130, 135, 150), "R": (230, 55, 55),
    # black shirt: darkest, dark, light
    "k": (28, 28, 40), "b": (48, 50, 68), "B": (78, 82, 108),
    # white, light grey, yellow, light yellow, light blue ID card
    "W": (245, 245, 250), "c": (215, 220, 230), "Y": (250, 205, 50),
    "q": (255, 225, 90), "C": (210, 230, 255),
    # dark trousers, shoes and shoe shine
    "z": (20, 20, 30), "Z": (40, 42, 58), "O": (30, 25, 30), "x": (110, 115, 135),
    # pigeon: light, normal and dark grey feathers, purple and green neck,
    # orange beak, pink feet
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
STRIKER_COLOURS = {"h": (200, 150, 40), "H": (240, 200, 80), "j": (255, 235, 150),
                   "B": (235, 70, 70), "b": (190, 45, 50)}
CAPTAIN_COLOURS = {"h": (25, 20, 20), "H": (45, 35, 35), "j": (70, 60, 60),
                   "B": (80, 125, 240), "b": (50, 85, 190), "S": (205, 150, 110),
                   "s": (170, 115, 80), "t": (225, 175, 135), "p": (200, 110, 100),
                   "Q": (140, 95, 65)}
PUNDIT_COLOURS = {"h": (25, 20, 22), "H": (45, 38, 40), "j": (120, 110, 125)}
LINESMAN_COLOURS = {"h": (160, 70, 30), "H": (210, 105, 45), "j": (240, 150, 80),
                    "B": (250, 215, 60), "b": (210, 170, 30)}

# The player, standing and facing you: a junior VAR official with a
# headset (the grey band over his hair), a black polo with yellow VAR
# stripes and a VAR badge, a lanyard with an ID card, and a belt buckle.
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
# Kit colours come from STRIKER_COLOURS.
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
    "........WWWWWWWWWWWWWWWc........",
    "........WWWWWWWccWWWWWWc........",
    ".........WWWWWc..WWWWWc.........",
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

# Pombo, the club's pigeon mascot: a big costume with a head-cam,
# big sad eyes, a striped club scarf, wing feathers and pink feet.
POMBO = [
    "....................kkkk....................",
    "...................kkkkkR...................",
    "..................akGGkkkA..................",
    "...............aaaaaaaAAAAAAA...............",
    ".............aaaaaaaaaAAAAAAAAA.............",
    "...........aaaaaaaaaaaAAAAAAAAAAd...........",
    "..........AAAAAAAAAAAAAAAAAAAAAAdd..........",
    ".........AAAAeeAAAAAAAAAAAAeeAAAddd.........",
    ".........AAeeAAAAAAAAAAAAAAAAeeAddd.........",
    "........AAAEEEEAAAAAAAAAAAAAEEEEdddd........",
    "........AAEwwiiEAAAAAAAAAAAEwwiiEddd........",
    "........AAEwiiiEAAAAAAAAAAAEwiiiEddd........",
    ".......AAAEiiiiEAAAAAAAAAAAEiiiiEdddd.......",
    "........AAAEEEEAAAAAooooAAAAEEEEdddd........",
    "........AAAAAAAAAAAooooooAAAAAAAdddd........",
    "........ppAAAAAAAAAAooooAAAAAAAAddpp........",
    ".........AAAAAAAAAAAAooAAAAAAAAAddd.........",
    ".........AAAAAAAAAAAAAAAAAAAAAAAddd.........",
    "..........AAAAAAAAAAAAAAAAAAAAAAdd..........",
    "...........AAAAAAAAAAAAAAAAAAAAAd...........",
    ".............AAAAAAAAAAAAAAAAAA.............",
    "..........vvvvvvvvvvvvnnnnnnnnnnnn..........",
    "..........RWWWRRRWWWRRRWWWRRRWWWRR..........",
    "........RRWWWRRRWWWRRRWWWRRRWWWRRRWW........",
    "........RWWWRRRWWWRRRWWWRRRWWWRRRWWW........",
    "........WWWRRRWWWRRRWWWRRRWWWRRRWWWR........",
    "........WWRRRWWWRRRWWWRRRWWWRRRWWWRR........",
    "..........RRWWWRRRWWWRRRWWWRWRWWWR..........",
    "..........AAAAAAAAAAAAAAAAAWRAAAAA..........",
    ".........AAAAAAAAAAAAAAAAAARWAAAAAA.........",
    "........AAAAAAAAAAAAAAAAAAAWRAAAAAAA........",
    ".......AAAAAAAAAAAaaaaaaAAARRAAAAAAAA.......",
    "....dddAAAAAAAAAaaaaaaaaaaAAAAAAAAddAd......",
    ".....dddAAAAAAaaaaaaaaaaaaaaAAAAAAAdddd.....",
    ".....dddAAAAAaaaaaaaaaaaaaaaaAAAAAAAddd.....",
    "....dddAAAAAaaaaaaaaaaaaaaaaaaAAAAAAAddd....",
    "....dddAAAAAaaaaaaaaaaaaaaaaaaAAAAddAddd....",
    "...dddddAAAaaaaaaaaaaaaaaaaaaaaAAAAdddddd...",
    "...dddddAAAaaaaaaaaaaaaaaaaaaaaAAAAAddddd...",
    "...ddddAAAaaaaaaaaaaaaaaaaaaaaaaAAAAAdddd...",
    "...ddddAAAaaaaaaaaaaaaaaaaaaaaaaAAddAdddd...",
    "...dddddAAaaaaaaaaaaaaaaaaaaaaaaAAAdddddd...",
    "...dddddAAaaaaaaaaaaaaaaaaaaaaaaAAAAddddd...",
    "...ddddAAAaaaaaaaaaaaaaaaaaaaaaaAAAAAdddd...",
    "...ddddAAAaaaaaaaaaaaaaaaaaaaaaaAAddAdddd...",
    "....ddddAAaaaaaaaaaaaaaaaaaaaaaaAAAddddd....",
    "....ddddAAaaaaaaaaaaaaaaaaaaaaaaAAAAdddd....",
    ".....ddAAAAaaaaaaaaaaaaaaaaaaaaAAAAAAdd.....",
    "....dddAAAAaaaaaaaaaaaaaaaaaaaaAAAddAdd.....",
    ".....dddAAAAaaaaaaaaaaaaaaaaaaAAAAAddd......",
    "......ddAAAAaaaaaaaaaaaaaaaaaaAAAAAAdd......",
    "........AAAAAaaaaaaaaaaaaaaaaAAAAAAA........",
    ".........AAAAAaaaaaaaaaaaaaaAAAAAAA.........",
    "..........AAAAAAaaaaaaaaaaAAAAAAAA..........",
    "............AAAAAAaaaaaaAAAAAAAA............",
    "..............AAAAAAAAAAAAAAAA..............",
    ".................AAAAAAAAAA.................",
    "...............ff.........ff................",
    "...............ff.........ff................",
    "..............ffff.......ffff...............",
    "..............f.f.f......f.f.f..............",
    "..............ff.ff......ff.ff..............",
    "............................................",
    "............................................",
    "............................................",
    "............................................",
]

# Pombo in two parts, for Dave's reveal: the pigeon head (the mask,
# rows 0 to 20) and the body (from the neck down).
POMBO_HEAD = POMBO[:21]
POMBO_BODY = POMBO[21:]

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

# Rex Smugworth, the TV pundit (head and shoulders, shown in the TV):
# slicked-back hair, one raised eyebrow, a huge grin, a blue suit and a red tie.
PUNDIT = [
    "................................",
    "................................",
    "...........hhhhhhhhhh...........",
    "........hhhHHjjHHHHHjjhh........",
    "......hhHHjjHHHHjjHHHHjjhh......",
    ".....hHHjjHHHHjjHHHHjjHHHHh.....",
    "....hHHHHHHHHHHHHHHHHHHHHHHh....",
    "...hHHHHHHHHHHHHHHHHHHHHHHHHh...",
    "...hHHHHHHHHHHHHHHHHHHHHHHHHh...",
    "...hHHHHHHHHHHHHHHHHHHHHHHHHh...",
    "..hHHHHHHHHHHHHHHHHHHHHHHHHHHh..",
    "..hHHHHHHHHHHHHHHHHHHHHHHHHHHh..",
    "..hHSSSSSSSSSSSSSSSSSeeeSSHHHh..",
    "..hHSSSSeeeSSSSSSSSSSSSSSSSSHh..",
    "..sSSSSSeeeSSSSSSSSSSeeeSSSSSs..",
    ".ssSSSSSEEESSSSSSSSSSEEESSSSSss.",
    ".ssSSSSSEiESSSSSSSSSSEiESSSSSss.",
    "..sSSSSSSSSSSSSSSSSSSSSSSSSSSs..",
    "..sSSSSppSSSmmmmmmmmSSppSSSSSs..",
    "....sSSSSSSSmTTTTTTmSSSSSSSs....",
    ".......sSSSSSSSSmmSSSSSSs.......",
    "..........ssssssssssss..........",
    "............WWSSSSWW............",
    "............uWWllWWU............",
    ".........uuuUUWllWUUUUU.........",
    ".......uuuuUUUUllUUUUUUUU.......",
    "......uWuuuUUUUllUUUUUUUUU......",
    ".....uuWuuuUUUUllllUUUUUUUU.....",
    "....uuuuuuUUUUUllUUUUUUUUUUU....",
    "...uuuuuuuUUUUUUUUUUUUUUUUUUU...",
    "..uuuuuuuuUUUUUUUUUUUUUUUUUUUU..",
    ".uuuuuuuuuUUUUUUUUUUUUUUUUUUUUU.",
    "uuuuuuuuuUUUUUUUUUUUUUUUUUUUUUUU",
    "uuuuuuuuuUUUUUUUUUUUUUUUUUUUUUUU",
    "uuuuuuuuuUUUUUUUUUUUUUUUUUUUUUUU",
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

# The Press Lanyard: a yellow strap with a "PRESS" card (red stripe).
LANYARD = [
    ".YY......YY.",
    "..YY....YY..",
    "...YY..YY...",
    "....YYYY....",
    "...WWWWWW...",
    "...RRRRRR...",
    "...WkkkkW...",
    "...WWWWWW...",
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
