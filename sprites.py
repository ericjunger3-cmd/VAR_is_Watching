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
REFEREE_COLOURS = {"h": (30, 25, 25), "H": (55, 45, 40), "j": (90, 75, 65)}
STRIKER_COLOURS = {"h": (200, 150, 40), "H": (240, 200, 80), "j": (255, 235, 150),
                   "B": (235, 70, 70), "b": (190, 45, 50)}
CAPTAIN_COLOURS = {"h": (25, 20, 20), "H": (45, 35, 35), "j": (70, 60, 60),
                   "B": (80, 125, 240), "b": (50, 85, 190),
                   "S": (205, 150, 110), "s": (170, 115, 80), "t": (225, 175, 135),
                   "p": (200, 110, 100)}
LINESMAN_COLOURS = {"h": (160, 70, 30), "H": (210, 105, 45), "j": (240, 150, 80),
                    "B": (250, 215, 60), "b": (210, 170, 30),
                    "W": (30, 30, 40), "c": (60, 60, 70)}

# The player: a junior VAR official with a headset, lanyard and VAR patches.
PLAYER = [
    ".........hhhhhhhh.........",
    ".......hhHHHHHHHHhh.......",
    ".....hhHHHjjjHHHHHHhh.....",
    "....hHHHjjjHHHHHHHHHHh....",
    "...hHHHjjHHHHHHHHHHHHHh...",
    "...hHHHHHHHHHHHHHHHHHHh...",
    "..hHHHHHHHHHHHHHHHHHHHHh..",
    "..hHHHhHHHHHhHHHHHHhHHHh..",
    "..hHHSShHHHSSShHHHSSSHHh..",
    "..GhSSSSSSSSSSSSSSSSSSShh.",
    ".GgGSSSSSSSSSSSSSSSSSSSSh.",
    ".GgGSSSeeeSSSSSSSeeeSSSSs.",
    ".GgGSSSSSSSSSSSSSSSSSSSSs.",
    ".GgGSSSEEESSSSSSSEEESSSSs.",
    ".GgGSSSwEESSSSSSSwEESSSSs.",
    ".GgGSSSEEESSSSSSSEEESSSSs.",
    ".GgGSSSEiESSSSSSSEiESSSSs.",
    "..gSSSSSSSSSSSSSSSSSSSSSs.",
    "..gSSppSSSSSsSSSSSSppSSSs.",
    "..gSSSSSSSSmSSSmSSSSSSSSs.",
    "..g.sSSSSSSSmmmSSSSSSSSs..",
    "..gGGsSSSSSSSSSSSSSSSss...",
    "....R.sssSSSSSSSSSss......",
    "........ssssssssss........",
    ".......kbbWWWWWWbbk.......",
    "......kbBBBWWqqWWBBBbk....",
    ".....kbBBBBBBYYBBBBBBbk...",
    "....kbBBBBBBBYYBBBBBBBbk..",
    "....bBYYBBBBBYYBBBBBYYBb..",
    "....SbBBBBBBCCCCBBBBBBbS..",
    "...SSbBBBBBBCCCCBBBBBBbSS.",
    "...sSbBBBBBBCCCCBBBBBBbSs.",
    "....s.bbbbbbbbbbbbbbbb.s..",
    "......ZZZZZZZZZZZZZZZZ....",
    "......ZZZZZZZz.zZZZZZZ....",
    ".......ZZZZZz...zZZZZZ....",
    ".......ZZZZZz...zZZZZZ....",
    "......OOOOOOO..OOOOOOO....",
    "......OxxOOOO..OxxOOOO....",
]

# The referee: moustache, whistle, and a yellow and red card in his pocket.
REFEREE = [
    "..........................",
    "..........................",
    "........hhhhhhhhhh........",
    "......hhHHHHHHHHHHhh......",
    ".....hHHHjjjHHHHHHHHh.....",
    "....hHHHjjHHHHHHHHHHHh....",
    "...hHHHHHHHHHHHHHHHHHHh...",
    "...hHHHHHHHHHHHHHHHHHHh...",
    "...hHSSSSSSSSSSSSSSSSHh...",
    "...hSSSSSSSSSSSSSSSSSSShh.",
    "...hSSSSSSSSSSSSSSSSSSSSh.",
    "...SSSSeeeSSSSSSSeeeSSSSs.",
    "...SSSSSSSSSSSSSSSSSSSSSs.",
    "...SSSSEEESSSSSSSEEESSSSs.",
    "...SSSSwEESSSSSSSwEESSSSs.",
    "...SSSSEEESSSSSSSEEESSSSs.",
    "...SSSSEiESSSSSSSEiESSSSs.",
    "...SSSSSSSSSSSSSSSSSSSSSs.",
    "...SSppSSSSSsSSSSSSppSSSs.",
    "...SSSSSShhhhhhhhhSSSSSSs.",
    "....sSSSSSSSmmmSSSSSSSSs..",
    ".....sSSSSSSSSSSSSSSSss...",
    "......sssSSSSSSSSSss......",
    "........ssssssssss........",
    ".......kbbWWWWWWbbk.......",
    "......kbBBBBcWBBBBBbk.....",
    ".....kbBBBBBBcBBBBBBbk....",
    "....kbBBBBBBBWWBBYlBBbk...",
    "....bBBBBBBBBWWBBYlBBBb...",
    "....SbBBBBBBBBBBBBBBBbS...",
    "...SSbBBBBBBBBBBBBBBBbSS..",
    "...sSbBBBBBBBBBBBBBBBbSs..",
    "....s.bbbbbbbbbbbbbbbb.s..",
    "......kkkkkkkkkkkkkkkk....",
    "......kkkkkkkk.kkkkkkk....",
    ".......SSSSSs...SSSSSs....",
    ".......kkkkkk...kkkkkk....",
    "......OOOOOOO..OOOOOOO....",
    "......OxxOOOO..OxxOOOO....",
]

# The steward: blue cap, hi-vis vest with reflective stripes and a radio.
STEWARD = [
    "..........................",
    "........FFFFFFFFFF........",
    "......FFDDDDDDDDDDFF......",
    ".....FDDDDWWDDDDDDDDF.....",
    "....FDDDDWWDDDDDDDDDDF....",
    "....FDDDDDDDDDDDDDDDDF....",
    "...FFFFFFFFFFFFFFFFFFFFFFF",
    "...hHHHHHHHHHHHHHHHHHH....",
    "...hSSSSSSSSSSSSSSSSSSh...",
    "...hSSSSSSSSSSSSSSSSSSShh.",
    "...hSSSSSSSSSSSSSSSSSSSSh.",
    "...SSSSeeeSSSSSSSeeeSSSSs.",
    "...SSSSSSSSSSSSSSSSSSSSSs.",
    "...SSSSEEESSSSSSSEEESSSSs.",
    "...SSSSwEESSSSSSSwEESSSSs.",
    "...SSSSEEESSSSSSSEEESSSSs.",
    "...SSSSEiESSSSSSSEiESSSSs.",
    "...SSSSSSSSSSSSSSSSSSSSSs.",
    "...SSppSSSSSsSSSSSSppSSSs.",
    "...SSSSSSSSmSSSmSSSSSSSSs.",
    "....sSSSSSSSmmmSSSSSSSSs..",
    ".....sSSSSSSSSSSSSSSSss...",
    "......sssSSSSSSSSSss......",
    "........ssssssssss........",
    ".......FDDVVVVVVDDF.......",
    "......FDVVVVVWWVVVVDF.....",
    ".....FDVVVVVVVVVVVVVVDF...",
    "....FDWWWWWWWWWWWWWWWWDF..",
    "....DDVVVVVVVVVVVVVVVVDD..",
    "....SDVVVVVVVVVVVVVkkVDS..",
    "...SSDVVVVVVVVVVVVVkkVDSS.",
    "...sSDWWWWWWWWWWWWWWWWDSs.",
    "....s.yyyyyyyyyyyyyyyy.s..",
    "......NNNNNNNNNNNNNNNN....",
    "......NNNNNNNM.MNNNNNN....",
    ".......NNNNNM...MNNNNN....",
    ".......NNNNNM...MNNNNN....",
    "......OOOOOOO..OOOOOOO....",
    "......OxxOOOO..OxxOOOO....",
]

# The home striker with spiky hair. Kit colours come from HOME_KIT.
STRIKER = [
    ".....h....h.....h....h....",
    ".....hh..hHh...hHh..hh....",
    "....hHHhhHjHhhhHjHhhHh....",
    "....hHHHHjjHHHHjjHHHHh....",
    "...hHHHjjHHHHHHHHHHHHHh...",
    "...hHHHHHHHHHHHHHHHHHHh...",
    "..hHHHHHHHHHHHHHHHHHHHHh..",
    "..hHHHHHhHHHHHHHhHHHHHHh..",
    "..hHSSSSSSHHSSSSSSSSHHHh..",
    "...hSSSSSSSSSSSSSSSSSSShh.",
    "...hSSSSSSSSSSSSSSSSSSSSh.",
    "...SSSSeeeSSSSSSSeeeSSSSs.",
    "...SSSSSSSSSSSSSSSSSSSSSs.",
    "...SSSSEEESSSSSSSEEESSSSs.",
    "...SSSSwEESSSSSSSwEESSSSs.",
    "...SSSSEEESSSSSSSEEESSSSs.",
    "...SSSSEiESSSSSSSEiESSSSs.",
    "...SSSSSSSSSSSSSSSSSSSSSs.",
    "...SSppSSSSSsSSSSSSppSSSs.",
    "...SSSSSSSSmSSSmSSSSSSSSs.",
    "....sSSSSSSSmmmSSSSSSSSs..",
    ".....sSSSSSSSSSSSSSSSss...",
    "......sssSSSSSSSSSss......",
    "........ssssssssss........",
    ".......BBBWWWWWWBBB.......",
    "......BBBBBWWWWBBBBBb.....",
    ".....BBBBBBBBBBBBBBBBb....",
    "....BBBBBBBBWWWBBBBBBBb...",
    "....BBBBBBBBBBWBBBBBBBb...",
    "....SBBBBBBBBWWBBBBBBbS...",
    "...SSBBBBBBBBWBBBBBBBbSS..",
    "...sSBBBBBBBBWWWBBBBBbSs..",
    "....s.bbbbbbbbbbbbbbbb.s..",
    "......WWWWWWWWWWWWWWWW....",
    "......WWWWWWWc.cWWWWWW....",
    ".......SSSSSs...SSSSSs....",
    ".......BBBBBb...BBBBBb....",
    "......OOOOOOO..OOOOOOO....",
    "......OxxOOOO..OxxOOOO....",
]

# The away captain: angry, arm raised, captain's armband. Colours from AWAY_KIT.
CAPTAIN = [
    "..............................",
    ".........................SSSS.",
    "........hhhhhhhhhh.......SSSSs",
    "......hhHHHHHHHHHHhh.....SSSSs",
    ".....hHHHjjjHHHHHHHHh.....Ss..",
    "....hHHHjjHHHHHHHHHHHh....Ss..",
    "...hHHHHHHHHHHHHHHHHHHh...Ss..",
    "...hHHHHHHHHHHHHHHHHHHh...Ss..",
    "...hHSSSSSSSSSSSSSSSSHh...Ss..",
    "...hSSSSSSSSSSSSSSSSSSShh.Ss..",
    "...hSSSSSSSSSSSSSSSSSSSSh.Ss..",
    "...SSSeeSSSSSSSSSSeeSSSSs.Ss..",
    "...SSSSSeeSSSSSSeeSSSSSSs.Ss..",
    "...SSSSEEESSSSSSSEEESSSSs.Ss..",
    "...SSSSwEESSSSSSSwEESSSSs.Ss..",
    "...SSSSEEESSSSSSSEEESSSSs.Ss..",
    "...SSSSEiESSSSSSSEiESSSSs.Ss..",
    "...SSSSSSSSSSSSSSSSSSSSSs.Ss..",
    "...SSppSSSSSsSSSSSSppSSSs.Ss..",
    "...SSSSSSSSrrrrSSSSSSSSSs.Ss..",
    "....sSSSSSSrrrrSSSSSSSSs..Ss..",
    ".....sSSSSSSrrSSSSSSSss..BBb..",
    "......sssSSSSSSSSSss.....BBb..",
    "........ssssssssss.......BBb..",
    ".......BBBWWWWWWBBB......BBb..",
    "......BBBBBWWWWBBBBBb....BBb..",
    ".....BBBBBBBBBBBBBBBBb...BBb..",
    "....BBBBBBBBWWWBBBBBBBBBBBb...",
    "....BYYBBBBBBBWBBBBBBBBBBb....",
    "....SBBBBBBBBWWBBBBBBbBb......",
    "...SSBBBBBBBBWBBBBBBBbb.......",
    "...sSBBBBBBBBWWWBBBBBbb.......",
    "....s.bbbbbbbbbbbbbbbb.s......",
    "......WWWWWWWWWWWWWWWW........",
    "......WWWWWWWc.cWWWWWW........",
    ".......SSSSSs...SSSSSs........",
    ".......BBBBBb...BBBBBb........",
    "......OOOOOOO..OOOOOOO........",
    "......OxxOOOO..OxxOOOO........",
]

# The linesman. Kit colours come from LINESMAN_KIT.
LINESMAN = [
    ".........hhhhhhhh.........",
    ".......hhHHHHHHHHhh.......",
    ".....hhHHHjjjHHHHHHhh.....",
    "....hHHHjjjHHHHHHHHHHh....",
    "...hHHHjjHHHHHHHHHHHHHh...",
    "...hHHHHHHHHHHHHHHHHHHh...",
    "..hHHHHHHHHHHHHHHHHHHHHh..",
    "..hHHHhHHHHHhHHHHHHhHHHh..",
    "..hHHSShHHHSSShHHHSSSHHh..",
    "...hSSSSSSSSSSSSSSSSSSShh.",
    "...hSSSSSSSSSSSSSSSSSSSSh.",
    "...SSSSeeeSSSSSSSeeeSSSSs.",
    "...SSSSSSSSSSSSSSSSSSSSSs.",
    "...SSSSEEESSSSSSSEEESSSSs.",
    "...SSSSwEESSSSSSSwEESSSSs.",
    "...SSSSEEESSSSSSSEEESSSSs.",
    "...SSSSEiESSSSSSSEiESSSSs.",
    "...SSSSSSSSSSSSSSSSSSSSSs.",
    "...SSppSSSSSsSSSSSSppSSSs.",
    "...SSSSSSSSmSSSmSSSSSSSSs.",
    "....sSSSSSSSmmmSSSSSSSSs..",
    ".....sSSSSSSSSSSSSSSSss...",
    "......sssSSSSSSSSSss......",
    "........ssssssssss........",
    ".......BBBWWWWWWBBB.......",
    "......BBBBBWWWWBBBBBb.....",
    ".....BBBBBBBBBBBBBBBBb....",
    "....BBBBBBBBWWWBBBBBBBb...",
    "....BBBBBBBBBBWBBBBBBBb...",
    "....SBBBBBBBBWWBBBBBBbS...",
    "...SSBBBBBBBBWBBBBBBBbSS..",
    "...sSBBBBBBBBWWWBBBBBbSs..",
    "....s.bbbbbbbbbbbbbbbb.s..",
    "......WWWWWWWWWWWWWWWW....",
    "......WWWWWWWc.cWWWWWW....",
    ".......SSSSSs...SSSSSs....",
    ".......BBBBBb...BBBBBb....",
    "......OOOOOOO..OOOOOOO....",
    "......OxxOOOO..OxxOOOO....",
]

# Pombo, the club's pigeon mascot: head-cam, sad eyes and a club scarf.
POMBO = [
    "................kkkkkR..............",
    "................kkkkkk..............",
    "..............aaaaaaaaaa............",
    "...........aaaAAAAAAAAAAaaa.........",
    ".........aaAAAAAAAAAAAAAAAAaa.......",
    "........aAAAAAAAAAAAAAAAAAAAAa......",
    ".......aAAAAAAAAAAAAAAAAAAAAAAa.....",
    "......aAAAAAAAAAAAAAAAAAAAAAAAAa....",
    "......AAAAAkkkAAAAAAAAAAkkkAAAAA....",
    ".....AAAAkkkAAAAAAAAAAAAAAkkkAAAA...",
    ".....AAAAAAAAAAAAAAAAAAAAAAAAAAAA...",
    ".....AAAAAEEEEAAAAAAAAAAEEEEAAAAA...",
    ".....AAAAEwwEEEAAAAAAAAEwwEEEAAAA...",
    ".....AAAAEwEEEEAAAAAAAAEwEEEEAAAA...",
    ".....AAAAEEEEEEAAAAAAAAEEEEEEAAAA...",
    ".....AAAAAEEEEAAAAAAAAAAEEEEAAAAA...",
    ".....AAApAAAAAAAAooooAAAAAAAApAAA...",
    ".....AAAAAAAAAAAoooooooAAAAAAAAAA...",
    "......AAAAAAAAAAAoooooAAAAAAAAAA....",
    ".......AAAAAAAAAAAAAAAAAAAAAAAA.....",
    "........RRWWRRWWRRWWRRWWRRWWRR......",
    ".......RRWWRRWWRRWWRRWWRRWWRRWW.....",
    "........vvvvvvnnnnnnRRWWnnnnn.......",
    ".......dvvvvvvvnnnnnRWWRnnnnnd......",
    "......dAAAAAAAAAAAAAWWRRAAAAAAd.....",
    ".....dAAAaaaaaaaaaaaRRWWaaAAAAAd....",
    "....ddAAaaaaaaaaaaaaaaaaaaaAAAAdd...",
    "...dddAaaaaaaaaaaaaaaaaaaaaaAAAddd..",
    "..ddddAaaaaaaaaaaaaaaaaaaaaaaAAdddd.",
    "..ddddAaaaaaaaaaaaaaaaaaaaaaaAAdddd.",
    "..dddAAaaaaaaaaaaaaaaaaaaaaaaAAAddd.",
    "...ddAAaaaaaaaaaaaaaaaaaaaaaaAAAdd..",
    "....dAAAaaaaaaaaaaaaaaaaaaaaAAAAd...",
    "....dAAAAaaaaaaaaaaaaaaaaaaAAAAAd...",
    ".....dAAAAaaaaaaaaaaaaaaaaAAAAAd....",
    "......dAAAAAAAAAAAAAAAAAAAAAAAd.....",
    ".......ddAAAAAAAAAAAAAAAAAAAdd......",
    ".........ddddddddddddddddddd........",
    "............ff..........ff..........",
    "............ff..........ff..........",
    "...........fff.........fff..........",
    "..........fffff.......fffff.........",
    ".........ff.f.ff.....ff.f.ff........",
]

# The TV pundit (head and shoulders, shown inside the TV).
PUNDIT = [
    "........KKKKKKKKKKKK........",
    "......KKLLLLLLLLLLLLKK......",
    ".....KLLLwwwLLLLLLLLLLK.....",
    "....KLLLwwLLLLLLLLLLLLLK....",
    "....KLLLLLLLLLLLLLLLLLLK....",
    "....KLLSSSSSSSSSSSSSSLLK....",
    "....KSSSSSSSSSSSSSSSSSSK....",
    "....SSSKKKKSSSSSSSKKKKSS....",
    "....SSSSSSSSSSSSSSSSSSSS....",
    "....SSSEEEESSSSSSEEEESSs....",
    "....SSSwEEESSSSSSwEEESSs....",
    "...sSSSSSSSSSSsSSSSSSSSSs...",
    "...sSpSSSSSSSSsSSSSSSSpSs...",
    "....SSSrTTTTTTTTTTTTrSSs....",
    "....SSSSrTTTTTTTTTTrSSSs....",
    ".....sSSSrrrrrrrrrrSSSs.....",
    "......sSSSSSSSSSSSSSss......",
    "........ssssssssssss........",
    "......uuuuuWWWlWWWuuuuu.....",
    "....uuUUUUUUWWllWUUUUUUuu...",
    "...uUUUWWUUUUWllWUUUUUUUUu..",
    "..uUUUUWWUUUUWllWUUUUUUUUUu.",
    "..uUUUUUUUUUUUllUUUUUUUUUUu.",
]
# The walking frame: the same body (the first 33 rows of PLAYER),
# but the legs are wide apart in a big step.
# PLAYER[:33] means "rows 0 up to (not including) row 33".
PLAYER_WALK = PLAYER[:33] + [
    "......ZZZZZZZZZZZZZZZZ....",
    ".....ZZZZZZz....zZZZZZZ...",
    "....ZZZZZz.......zZZZZZ...",
    "...ZZZZz..........zZZZZZ..",
    "..OOOOOO..........OOOOOOO.",
    "..OxxOOO..........OxxOOOO.",
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
