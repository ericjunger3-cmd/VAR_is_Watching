# The things drawn on top of the rooms: the dialogue box, the pundit's TV
# and the close-up of Dave's sticky note.
# Boxes and pictures are drawn on the small canvas (so they look pixelated);
# the text is drawn on the big window afterwards (so it stays sharp).

import pygame
from sprites import OUTLINE

# The dialogue box at the bottom of the screen (canvas positions).
BOX_X = 6
BOX_Y = 212
BOX_WIDTH = 468
BOX_HEIGHT = 54
LINES_PER_PAGE = 3

# The pundit's TV in the top-right corner, and his speech box next to it.
TV_X = 400
TV_Y = 8
SPEECH_X = 232
SPEECH_Y = 10
SPEECH_WIDTH = 160
SPEECH_HEIGHT = 50

# The sticky note close-up.
NOTE_X = 150
NOTE_Y = 40
NOTE_WIDTH = 180
NOTE_HEIGHT = 170

# Text colours.
BROWN = (90, 50, 30)
ORANGE = (210, 80, 50)
CREAM = (255, 250, 235)
INK = (40, 50, 120)


# ---------------------------------------------------------------- text helpers

def wrap_text(text, font, max_width):
    # Split a long text into lines that each fit into max_width pixels.
    # We add words one by one; when the line gets too wide, we start a new line.
    words = text.split(" ")
    lines = []
    current_line = ""
    for word in words:
        if current_line == "":
            test_line = word
        else:
            test_line = current_line + " " + word
        # font.size(...) returns (width, height) of the text in pixels.
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    if current_line != "":
        lines.append(current_line)
    return lines


def make_pages(title, text, font, scale):
    # Turn a text into pages for the dialogue box: each page is a dictionary
    # with a title and at most LINES_PER_PAGE lines.
    max_width = (BOX_WIDTH - 24) * scale
    lines = wrap_text(text, font, max_width)
    pages = []
    for start in range(0, len(lines), LINES_PER_PAGE):
        # lines[start:start + 3] takes 3 lines, starting at "start".
        page = {"title": title, "lines": lines[start:start + LINES_PER_PAGE]}
        pages.append(page)
    return pages


def letters_on_page(page):
    # Count all letters on a page (needed for the typing effect).
    total = 0
    for line in page["lines"]:
        total = total + len(line)
    return total


# ---------------------------------------------------------------- boxes (drawn on the canvas)

def framed_box(canvas, x, y, width, height, fill, light, dark):
    # A box with a dark outline, rounded corners (the corner pixels are left
    # out), a light top-left edge and a darker bottom-right edge.
    pygame.draw.rect(canvas, OUTLINE, (x + 1, y, width - 2, height))
    pygame.draw.rect(canvas, OUTLINE, (x, y + 1, width, height - 2))
    pygame.draw.rect(canvas, dark, (x + 1, y + 1, width - 2, height - 2))
    pygame.draw.rect(canvas, light, (x + 1, y + 1, width - 3, height - 3))
    pygame.draw.rect(canvas, fill, (x + 3, y + 3, width - 6, height - 6))


def draw_dialogue_box(canvas, page):
    # The cream dialogue box, plus an orange tab for the title (if there is one).
    framed_box(canvas, BOX_X, BOX_Y, BOX_WIDTH, BOX_HEIGHT,
               (255, 245, 220), (255, 255, 245), (220, 190, 140))
    if page["title"] != "":
        framed_box(canvas, BOX_X + 8, BOX_Y - 7, 120, 16,
                   (230, 120, 60), (255, 160, 100), (190, 90, 40))


def draw_pundit_tv(canvas, pundit_picture):
    # A red retro TV with two antennas, the pundit on the screen,
    # two knobs, a "live" light, and his speech box with a little tail.
    pygame.draw.line(canvas, OUTLINE, (TV_X + 26, TV_Y + 2), (TV_X + 16, TV_Y - 8), 2)
    pygame.draw.line(canvas, OUTLINE, (TV_X + 44, TV_Y + 2), (TV_X + 56, TV_Y - 8), 2)
    framed_box(canvas, TV_X, TV_Y, 74, 58, (230, 80, 70), (255, 130, 110), (180, 50, 50))

    # The screen.
    pygame.draw.rect(canvas, OUTLINE, (TV_X + 5, TV_Y + 5, 50, 46))
    pygame.draw.rect(canvas, (120, 200, 255), (TV_X + 6, TV_Y + 6, 48, 44))
    pygame.draw.rect(canvas, (160, 220, 255), (TV_X + 6, TV_Y + 6, 48, 10))

    # The pundit in the middle of the screen, standing on its bottom edge.
    pundit_x = TV_X + 6 + (48 - pundit_picture.get_width()) // 2
    pundit_y = TV_Y + 50 - pundit_picture.get_height()
    canvas.blit(pundit_picture, (pundit_x, pundit_y))

    # Knobs and the red "live" light.
    for knob_y, colour in [(TV_Y + 10, (255, 220, 80)), (TV_Y + 20, (80, 200, 120))]:
        pygame.draw.rect(canvas, OUTLINE, (TV_X + 59, knob_y, 9, 7))
        pygame.draw.rect(canvas, colour, (TV_X + 60, knob_y + 1, 7, 5))
    pygame.draw.rect(canvas, (250, 60, 60), (TV_X + 60, TV_Y + 44, 7, 4))

    # Speech box with a tail pointing at the TV.
    framed_box(canvas, SPEECH_X, SPEECH_Y, SPEECH_WIDTH, SPEECH_HEIGHT,
               (255, 245, 220), (255, 255, 245), (220, 190, 140))
    tail_x = SPEECH_X + SPEECH_WIDTH - 1
    pygame.draw.polygon(canvas, OUTLINE, [(tail_x, 26), (tail_x + 9, 30), (tail_x, 34)])
    pygame.draw.polygon(canvas, (255, 245, 220), [(tail_x - 2, 27), (tail_x + 6, 30), (tail_x - 2, 33)])


def draw_note_closeup(canvas):
    # Darken the room, then draw a big sticky note in the middle.
    # The 4th number (170) is how see-through the dark layer is.
    shade = pygame.Surface((canvas.get_width(), canvas.get_height()), pygame.SRCALPHA)
    shade.fill((20, 10, 30, 170))
    canvas.blit(shade, (0, 0))

    x = NOTE_X
    y = NOTE_Y
    pygame.draw.rect(canvas, (20, 10, 30), (x + 6, y + 6, NOTE_WIDTH, NOTE_HEIGHT))   # shadow
    pygame.draw.rect(canvas, OUTLINE, (x - 1, y - 1, NOTE_WIDTH + 2, NOTE_HEIGHT + 2))
    pygame.draw.rect(canvas, (255, 230, 90), (x, y, NOTE_WIDTH, NOTE_HEIGHT))
    pygame.draw.rect(canvas, (255, 242, 150), (x, y, NOTE_WIDTH, 6))                  # light top
    pygame.draw.rect(canvas, (235, 200, 60), (x, y + NOTE_HEIGHT - 10, NOTE_WIDTH, 10))

    # The curled bottom-right corner.
    right = x + NOTE_WIDTH
    bottom = y + NOTE_HEIGHT
    pygame.draw.polygon(canvas, (215, 175, 45), [(right, bottom - 22), (right - 22, bottom), (right, bottom)])
    pygame.draw.polygon(canvas, (250, 215, 80), [(right - 22, bottom), (right, bottom - 22), (right - 18, bottom - 18)])

    # A piece of tape on top.
    pygame.draw.rect(canvas, OUTLINE, (x + 64, y - 9, 52, 18))
    pygame.draw.rect(canvas, (235, 235, 225), (x + 65, y - 8, 50, 16))
    pygame.draw.rect(canvas, (250, 250, 245), (x + 65, y - 8, 50, 4))

    # A little smiley doodle.
    pygame.draw.circle(canvas, (150, 90, 40), (x + 28, y + 148), 10, 1)
    canvas.set_at((x + 25, y + 145), (150, 90, 40))
    canvas.set_at((x + 31, y + 145), (150, 90, 40))
    pygame.draw.line(canvas, (150, 90, 40), (x + 24, y + 151), (x + 32, y + 151))


# ---------------------------------------------------------------- text (drawn on the window)

def draw_dialogue_text(window, page, letters_shown, fonts, scale):
    # Write the title and the lines of the page. Only the first
    # letters_shown letters are written, which makes the typing effect.
    if page["title"] != "":
        title = fonts["title"].render(page["title"].upper(), False, CREAM)
        window.blit(title, ((BOX_X + 14) * scale, (BOX_Y - 5) * scale))

    letters_left = letters_shown
    y = BOX_Y + 12
    for line in page["lines"]:
        # line[:letters_left] is the start of the line (up to letters_left letters).
        visible = line[:letters_left]
        window.blit(fonts["text"].render(visible, False, BROWN), ((BOX_X + 10) * scale, y * scale))
        letters_left = letters_left - len(line)
        if letters_left <= 0:
            break
        y = y + 11

    # When the whole page is shown, a small "SPACE >" tells the player to continue.
    if letters_shown >= letters_on_page(page):
        hint = fonts["small"].render("SPACE >", False, ORANGE)
        window.blit(hint, ((BOX_X + BOX_WIDTH - 46) * scale, (BOX_Y + BOX_HEIGHT - 12) * scale))


def draw_pundit_text(window, pundit_line, fonts, scale):
    # The pundit's line in his speech box. story.json writes it as
    # "PUNDIT: ...", so we cut off the first 8 letters ("PUNDIT: ").
    if pundit_line.startswith("PUNDIT: "):
        pundit_line = pundit_line[8:]
    window.blit(fonts["small"].render("PUNDIT", False, ORANGE), ((SPEECH_X + 8) * scale, (SPEECH_Y + 5) * scale))
    lines = wrap_text(pundit_line, fonts["small"], (SPEECH_WIDTH - 16) * scale)
    y = SPEECH_Y + 14
    for line in lines[:4]:
        window.blit(fonts["small"].render(line, False, BROWN), ((SPEECH_X + 8) * scale, y * scale))
        y = y + 8


def draw_note_text(window, lines, fonts, scale):
    # Dave's handwriting on the sticky note. The first two lines are big.
    y = NOTE_Y + 20
    for i in range(len(lines)):
        if i < 2:
            font = fonts["hand_big"]
        else:
            font = fonts["hand"]
        picture = font.render(lines[i], True, INK)
        # Line 2 ("- Dave") is moved to the right, like a signature.
        if i == 1:
            x = NOTE_X + 90
        else:
            x = NOTE_X + 14
        window.blit(picture, (x * scale, y * scale))
        if i < 2:
            y = y + 28
        else:
            y = y + 15
    hint = fonts["small"].render("E: put the note back", False, CREAM)
    window.blit(hint, ((NOTE_X + 40) * scale, (NOTE_Y + NOTE_HEIGHT + 14) * scale))
