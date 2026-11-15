# The things drawn on top of the rooms: the dialogue box, the pundit's TV
# and the close-up of Dave's sticky note.
# Boxes and pictures are drawn on the small canvas (so they look pixelated);
# the text is drawn on the big window afterwards (so it stays sharp).

import math
import pygame
import game
import sprites
import rooms
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


def draw_dialogue_box(canvas, page, faded=False):
    # The cream dialogue box, plus an orange tab for the title (if there is one).
    # faded=True draws it in greyer colours: the text has already been read.
    if faded:
        framed_box(canvas, BOX_X, BOX_Y, BOX_WIDTH, BOX_HEIGHT,
                   (225, 220, 210), (235, 232, 225), (195, 185, 170))
    else:
        framed_box(canvas, BOX_X, BOX_Y, BOX_WIDTH, BOX_HEIGHT,
                   (255, 245, 220), (255, 255, 245), (220, 190, 140))
    if page["title"] != "":
        if faded:
            framed_box(canvas, BOX_X + 8, BOX_Y - 7, 120, 16,
                       (175, 150, 135), (195, 175, 160), (150, 125, 110))
        else:
            framed_box(canvas, BOX_X + 8, BOX_Y - 7, 120, 16,
                       (230, 120, 60), (255, 160, 100), (190, 90, 40))


def draw_pundit_tv(canvas, pundit_picture, lit=False):
    # A red retro TV with two antennas, the pundit on the screen,
    # two knobs, a "live" light, and his speech box with a little tail.
    # lit=True makes the speech box and the TV light up (a new line):
    # a soft see-through yellow glow and a thick bright yellow frame.
    if lit:
        glow = pygame.Surface((SPEECH_WIDTH + 104, SPEECH_HEIGHT + 24), pygame.SRCALPHA)
        glow.fill((255, 220, 60, 90))
        canvas.blit(glow, (SPEECH_X - 10, SPEECH_Y - 10))
        pygame.draw.rect(canvas, (255, 225, 60), (SPEECH_X - 5, SPEECH_Y - 5, SPEECH_WIDTH + 10, SPEECH_HEIGHT + 10))
        pygame.draw.rect(canvas, (255, 225, 60), (TV_X - 4, TV_Y - 4, 82, 66))
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


def slot_position(index):
    # The top-left corner of inventory slot number index (0, 1, 2 ...).
    return 6 + index * 26, 6


def draw_inventory(canvas, inventory, pictures, slot_count, tick, flying_item):
    # Item slots in the top-left corner. Every item you carry is shown in
    # its own slot, in the order you picked them up. The items float gently
    # up and down (each one a little later than the one before).
    # flying_item is an item that is still flying to its slot (not drawn here).
    for i in range(slot_count):
        x, y = slot_position(i)
        framed_box(canvas, x, y, 24, 22, (90, 60, 40), (130, 90, 60), (60, 40, 25))
        pygame.draw.rect(canvas, (70, 45, 30), (x + 3, y + 3, 18, 16))
        if i < len(inventory) and inventory[i] != flying_item:
            icon = pictures[inventory[i]]
            float_up = ((tick // 15 + i * 2) % 4 == 0)
            # Put the icon in the middle of the slot (1 pixel higher when floating).
            icon_x = x + (24 - icon.get_width()) // 2
            icon_y = y + (22 - icon.get_height()) // 2 - float_up
            canvas.blit(icon, (icon_x, icon_y))


def draw_flying_item(canvas, picture, start_x, start_y, slot_index, frame, frames):
    # An item flying from where it was picked up into its slot, in an arc.
    # progress_part goes from 0.0 (start) to 1.0 (in the slot).
    progress_part = frame / frames
    slot_x, slot_y = slot_position(slot_index)
    end_x = slot_x + (24 - picture.get_width()) // 2
    end_y = slot_y + (22 - picture.get_height()) // 2
    x = start_x + (end_x - start_x) * progress_part
    y = start_y + (end_y - start_y) * progress_part
    # The arc: up to 40 pixels higher in the middle of the flight.
    y = y - 40 * 4 * progress_part * (1 - progress_part)
    canvas.blit(picture, (int(x), int(y)))


TIMER_X = 6
TIMER_Y = 32
TIMER_WIDTH = 102


def draw_timer(canvas, seconds_left, total_seconds, tick):
    # The stadium's patience: a bar under the inventory that gets shorter.
    # Green when there is plenty of time, then yellow, then red.
    # In the last 30 seconds it blinks.
    part = max(0, seconds_left) / total_seconds
    if part > 0.5:
        colour = (90, 200, 90)
    elif part > 0.2:
        colour = (240, 200, 60)
    else:
        colour = (230, 70, 60)
    framed_box(canvas, TIMER_X, TIMER_Y, TIMER_WIDTH, 16, (60, 40, 30), (90, 60, 40), (40, 25, 20))
    blink_off = seconds_left < 30 and (tick // 10) % 2 == 0
    if not blink_off:
        pygame.draw.rect(canvas, colour, (TIMER_X + 3, TIMER_Y + 10, int((TIMER_WIDTH - 6) * part), 3))


def menu_extra(option_count):
    # The dialogue box has room for 4 options. Every option more makes
    # the menu box 11 pixels taller (it grows upwards).
    return max(0, option_count - 4) * 11


def draw_menu_box(canvas, option_count):
    # The dialogue box with a wider tab for the question of a menu.
    extra = menu_extra(option_count)
    framed_box(canvas, BOX_X, BOX_Y - extra, BOX_WIDTH, BOX_HEIGHT + extra,
               (255, 245, 220), (255, 255, 245), (220, 190, 140))
    framed_box(canvas, BOX_X + 8, BOX_Y - 7 - extra, 200, 16,
               (230, 120, 60), (255, 160, 100), (190, 90, 40))


# ---------------------------------------------------------------- the VAR Review screen

# The pitch on the review monitor, seen from above. The goal line is on the
# right; every metre away from the goal line is METRE pixels to the left.
PITCH_X = 24
PITCH_Y = 50
PITCH_WIDTH = 432
PITCH_HEIGHT = 120
GOAL_LINE_X = 444
METRE = 10.5


def metres_to_x(metres):
    # Turn "metres from the goal line" into an x position on the monitor.
    return int(round(GOAL_LINE_X - metres * METRE))


def review_time(review, state):
    # The time (in seconds) of the moment the player is looking at.
    # round(..., 1) keeps it a clean number like 1.2.
    return round(state["frame"] * review["step"], 1)


def draw_review(canvas, review, state):
    # The VAR monitor: dark background, a timeline bar, the pitch from
    # above, the players and the ball at the chosen moment, and (in the
    # second step) the offside line.
    shade = pygame.Surface((canvas.get_width(), canvas.get_height()), pygame.SRCALPHA)
    shade.fill((10, 10, 20, 235))
    canvas.blit(shade, (0, 0))
    framed_box(canvas, 12, 14, 456, 186, (30, 32, 45), (60, 62, 80), (15, 15, 25))

    # The timeline bar with a marker for the current moment.
    time = review_time(review, state)
    pygame.draw.rect(canvas, (70, 72, 90), (150, 36, 300, 6))
    marker_x = 150 + int(300 * time / review["end"])
    pygame.draw.rect(canvas, OUTLINE, (marker_x - 2, 33, 5, 12))
    pygame.draw.rect(canvas, (255, 220, 90), (marker_x - 1, 34, 3, 10))

    # The pitch with mowing stripes.
    for i in range(0, PITCH_WIDTH, 24):
        if (i // 24) % 2 == 0:
            colour = (70, 160, 75)
        else:
            colour = (85, 180, 90)
        pygame.draw.rect(canvas, colour, (PITCH_X + i, PITCH_Y, 24, PITCH_HEIGHT))

    # White lines: the goal line, the penalty box (16.5 m) and the goal.
    white = (240, 240, 240)
    pygame.draw.line(canvas, white, (GOAL_LINE_X, PITCH_Y), (GOAL_LINE_X, PITCH_Y + PITCH_HEIGHT - 1))
    box_x = metres_to_x(16.5)
    pygame.draw.rect(canvas, white, (box_x, PITCH_Y + 20, GOAL_LINE_X - box_x + 1, PITCH_HEIGHT - 40), 1)
    pygame.draw.rect(canvas, white, (GOAL_LINE_X, PITCH_Y + 48, 10, 24), 1)

    tracks = review["tracks"]
    ball_x = metres_to_x(game.value_at(tracks["ball"], time, 1))
    ball_y = int(game.value_at(tracks["ball"], time, 2))

    # Until the pass, the passer's boot touches the ball (a short leg line).
    # After the pass, the ball rolls away with little speed lines behind it.
    passer_x = metres_to_x(game.value_at(tracks["passer"], time, 1))
    passer_y = int(game.value_at(tracks["passer"], time, 2))
    if time <= review["release"]:
        pygame.draw.line(canvas, (250, 200, 160), (passer_x, passer_y), (ball_x, ball_y), 2)
    else:
        for i in range(1, 4):
            pygame.draw.line(canvas, white, (ball_x - 3 - i * 4, ball_y), (ball_x - 1 - i * 4, ball_y))

    # The players: a dot with an outline for each of them.
    for player in review["players"]:
        x = metres_to_x(game.value_at(tracks[player["id"]], time, 1))
        y = int(game.value_at(tracks[player["id"]], time, 2))
        pygame.draw.circle(canvas, OUTLINE, (x, y), 7)
        pygame.draw.circle(canvas, player["colour"], (x, y), 6)

    # The ball.
    pygame.draw.circle(canvas, OUTLINE, (ball_x, ball_y), 3)
    pygame.draw.circle(canvas, white, (ball_x, ball_y), 2)

    # Second step: the offside line. state["line"] is in tenths of a metre.
    if state["step"] == "line":
        line_x = metres_to_x(state["line"] / 10)
        pygame.draw.line(canvas, (255, 70, 200), (line_x, PITCH_Y), (line_x, PITCH_Y + PITCH_HEIGHT - 1), 1)

    # The box for the instructions at the bottom.
    framed_box(canvas, BOX_X, BOX_Y, BOX_WIDTH, BOX_HEIGHT,
               (255, 245, 220), (255, 255, 245), (220, 190, 140))

    # Before the footage starts (the "rules" step): a cream panel over the
    # pitch that explains offside. Its text is written in draw_review_text.
    if state["step"] == "rules":
        framed_box(canvas, PITCH_X, PITCH_Y - 4, PITCH_WIDTH, PITCH_HEIGHT + 8,
                   (255, 245, 220), (255, 255, 245), (220, 190, 140))


def draw_ending_screen(canvas):
    # Darken everything and draw a big box for the ending.
    shade = pygame.Surface((canvas.get_width(), canvas.get_height()), pygame.SRCALPHA)
    shade.fill((10, 10, 20, 200))
    canvas.blit(shade, (0, 0))
    framed_box(canvas, 30, 24, 420, 222, (255, 245, 220), (255, 255, 245), (220, 190, 140))
    framed_box(canvas, 30, 24, 420, 40, (230, 120, 60), (255, 160, 100), (190, 90, 40))


# ---------------------------------------------------------------- title screen and yes/no box

# Where things go on the title screen (canvas positions, from the top).
ICON_Y = 6          # the VAR screen with the eye
LOGO_Y = 32         # "VAR" in big pixel letters
LOGO_SIZE = 5       # each pixel of a letter becomes a 5 x 5 square
SUBLOGO_Y = 78      # "IS WATCHING" in smaller pixel letters
MENU_Y = 116        # the first option of the menu
MENU_GAP = 19       # the distance between two options
MENU_SIZE = 2       # the menu letters: 2 x 2 squares
SHADE_END = 200     # the dark shade behind the logo fades out here

# The colours of the pixel letters, one colour per row (7 rows), from the
# top to the bottom. Light at the top and darker at the bottom makes the
# letters look shiny.
GOLD_ROWS = [(255, 240, 150), (255, 225, 90), (255, 205, 60), (250, 175, 50),
             (240, 145, 40), (230, 120, 35), (215, 100, 30)]
CREAM_ROWS = [(255, 253, 245), (255, 250, 235), (255, 246, 225), (248, 236, 210),
              (240, 226, 195), (232, 215, 180), (222, 200, 165)]


def pixel_text_width(text, size):
    # How wide a text in pixel letters is (in canvas pixels).
    # Every letter is as wide as its grid, plus 1 empty column after it;
    # a space is 3 columns wide.
    columns = 0
    for letter in text:
        if letter == " ":
            columns = columns + 3
        else:
            columns = columns + len(sprites.PIXEL_LETTERS[letter][0]) + 1
    # The last letter needs no empty column after it.
    return (columns - 1) * size


def draw_pixel_text(canvas, text, x, y, size, row_colours):
    # Draw a text in the chunky pixel letters from sprites.py.
    # Every "#" of a letter becomes a size x size square.
    # We draw the whole text three times, each time on top of the last:
    #   1. "shadow":  dark squares a bit lower (the letters look thick)
    #   2. "outline": dark squares a bit bigger (a dark edge around them)
    #   3. "colour":  the coloured squares, one colour per row
    for layer in ["shadow", "outline", "colour"]:
        left = x
        for letter in text:
            if letter == " ":
                left = left + 3 * size
                continue
            grid = sprites.PIXEL_LETTERS[letter]
            for row in range(len(grid)):
                for column in range(len(grid[row])):
                    if grid[row][column] != "#":
                        continue
                    square_x = left + column * size
                    square_y = y + row * size
                    if layer == "shadow":
                        pygame.draw.rect(canvas, OUTLINE, (square_x - 1, square_y + 1, size + 2, size + 2))
                    elif layer == "outline":
                        pygame.draw.rect(canvas, OUTLINE, (square_x - 1, square_y - 1, size + 2, size + 2))
                    else:
                        pygame.draw.rect(canvas, row_colours[row], (square_x, square_y, size, size))
            # Move to the next letter: its width plus 1 empty column.
            left = left + (len(grid[0]) + 1) * size


def draw_centred_pixel_text(canvas, text, y, size, row_colours):
    # Pixel letters in the middle of the canvas: start at half of
    # (canvas width - text width). Returns the x where the text starts.
    x = (canvas.get_width() - pixel_text_width(text, size)) // 2
    draw_pixel_text(canvas, text, x, y, size, row_colours)
    return x


def draw_title_screen(canvas, labels, selected, tick, pictures, volume):
    # The logo (the VAR screen with the eye, "VAR", "IS WATCHING") and the
    # menu in pixel letters. The chosen option is gold and has an arrow.
    # volume (0.0 to 1.0) is shown as a slider next to "VOLUME".

    # A shade that is dark at the top and fades out towards the grass,
    # so the busy crowd behind the logo gets calmer. Every row of pixels
    # gets a bit less dark (alpha 190 at the top, 0 at the grass).
    shade = pygame.Surface((canvas.get_width(), 1), pygame.SRCALPHA)
    for y in range(SHADE_END):
        alpha = 190 - 190 * y // SHADE_END
        shade.fill((15, 15, 35, alpha))
        canvas.blit(shade, (0, y))

    # The VAR screen. The pupil moves left and right slowly: math.sin goes
    # smoothly from -1 to 1 and back, so "4 * sin" goes from -4 to 4.
    screen = pictures["var_screen"]
    screen_x = (canvas.get_width() - screen.get_width()) // 2
    canvas.blit(screen, (screen_x, ICON_Y))
    look = round(4 * math.sin(tick * 0.05))
    # The middle of the eye is 15 pixels from the left and 9 from the top
    # of the picture (counting the outline).
    eye_x = screen_x + 15 + look
    eye_y = ICON_Y + 9
    pygame.draw.circle(canvas, (60, 110, 210), (eye_x, eye_y), 3)
    pygame.draw.circle(canvas, OUTLINE, (eye_x, eye_y), 2)
    canvas.set_at((eye_x - 1, eye_y - 1), (255, 255, 255))

    # The logo.
    draw_centred_pixel_text(canvas, "VAR", LOGO_Y, LOGO_SIZE, GOLD_ROWS)
    draw_centred_pixel_text(canvas, "IS WATCHING", SUBLOGO_Y, 2, CREAM_ROWS)

    # The menu: every option in the middle, the chosen one gold.
    for i in range(len(labels)):
        y = MENU_Y + i * MENU_GAP
        text = labels[i].upper()
        if text == "VOLUME":
            x = draw_volume_slider(canvas, y, volume, i == selected)
        elif i == selected:
            x = draw_centred_pixel_text(canvas, text, y, MENU_SIZE, GOLD_ROWS)
        else:
            x = draw_centred_pixel_text(canvas, text, y, MENU_SIZE, CREAM_ROWS)
        if i == selected:
            # The arrow sits left of the chosen option and moves a little
            # back and forth, like it is pointing.
            arrow = pictures["arrow"]
            nudge = round(2 * math.sin(tick * 0.2))
            canvas.blit(arrow, (x - arrow.get_width() - 6 + nudge, y + 1))


# The volume slider on the title screen: 10 blocks next to "VOLUME".
SLIDER_BLOCKS = 10
BLOCK_WIDTH = 6
BLOCK_GAP = 2


def draw_volume_slider(canvas, y, volume, chosen):
    # "VOLUME" in pixel letters, then 10 blocks: filled blocks (gold)
    # for the volume, empty blocks (dark) for the rest. Returns the x
    # where it starts (for the arrow). The whole thing is centred.
    if chosen:
        colours = GOLD_ROWS
    else:
        colours = CREAM_ROWS
    text_width = pixel_text_width("VOLUME", MENU_SIZE)
    slider_width = SLIDER_BLOCKS * (BLOCK_WIDTH + BLOCK_GAP)
    x = (canvas.get_width() - (text_width + 8 + slider_width)) // 2
    draw_pixel_text(canvas, "VOLUME", x, y, MENU_SIZE, colours)
    # round() turns e.g. 0.7 * 10 = 7.000001 into 7 blocks.
    filled = round(volume * SLIDER_BLOCKS)
    block_x = x + text_width + 8
    for i in range(SLIDER_BLOCKS):
        pygame.draw.rect(canvas, OUTLINE, (block_x - 1, y, BLOCK_WIDTH + 2, 15))
        if i < filled:
            pygame.draw.rect(canvas, colours[1], (block_x, y + 1, BLOCK_WIDTH, 6))
            pygame.draw.rect(canvas, colours[5], (block_x, y + 7, BLOCK_WIDTH, 7))
        else:
            pygame.draw.rect(canvas, (60, 60, 80), (block_x, y + 1, BLOCK_WIDTH, 13))
        block_x = block_x + BLOCK_WIDTH + BLOCK_GAP
    return x


def draw_confirm_box(canvas):
    # Darken everything and draw a small box in the middle for a yes/no question.
    shade = pygame.Surface((canvas.get_width(), canvas.get_height()), pygame.SRCALPHA)
    shade.fill((10, 10, 20, 170))
    canvas.blit(shade, (0, 0))
    framed_box(canvas, 100, 96, 280, 72, (255, 245, 220), (255, 255, 245), (220, 190, 140))


# ---------------------------------------------------------------- text (drawn on the window)

# ---------------------------------------------------------------- the studio screen
# The first screen of the game, like a little film (30 frames = 1 second):
#   1. It is dark. The four floodlights switch on one after the other.
#   2. The studio logo lights up and the crowd starts to cheer.
#   3. The three developers walk out of the players' tunnel, one after the
#      other, to their places. Each name appears like a team line-up.
#   4. "PRESS ENTER TO CONTINUE" blinks.
# Everything depends only on tick (the frame counter), so the same tick
# always gives the same picture.

STUDIO_FLOOR = 196                      # where the developers stand
STUDIO_LIGHTS = [30, 130, 350, 450]     # the x of the four floodlight masts
STUDIO_LIGHT_TICKS = [10, 20, 30, 40]   # the frame when each light goes on
STUDIO_LOGO_TICK = 52                   # the frame when the logo lights up
STUDIO_TUNNEL_X = 40                    # where the developers come out
STUDIO_DEV_X = [150, 240, 330]          # where each developer stops (240 = the middle)
# The frame when each one starts walking. Max (right) comes out first and
# Eric (left) last, so nobody has to walk past someone who is already there.
STUDIO_DEV_TICKS = [98, 82, 66]
STUDIO_WALK_SPEED = 4                   # pixels per frame
STUDIO_NAMES = ["#7 ERIC", "#10 BRIAN", "#9 MAX"]
# The frame when the last developer has arrived; then "PRESS ENTER" appears.
STUDIO_END = 0
for number in range(3):
    arrival = STUDIO_DEV_TICKS[number] + (STUDIO_DEV_X[number] - STUDIO_TUNNEL_X) // STUDIO_WALK_SPEED
    if arrival > STUDIO_END:
        STUDIO_END = arrival


def lights_on(tick):
    # How many floodlights are already on (0 to 4).
    count = 0
    for light_tick in STUDIO_LIGHT_TICKS:
        if tick >= light_tick:
            count = count + 1
    return count


def developer_x(number, tick):
    # Where developer number 0, 1 or 2 is right now, or None if he is still
    # in the tunnel. He walks to the right until he reaches his place.
    start = STUDIO_DEV_TICKS[number]
    if tick < start:
        return None
    x = STUDIO_TUNNEL_X + (tick - start) * STUDIO_WALK_SPEED
    return min(x, STUDIO_DEV_X[number])


def draw_studio_stands(canvas):
    # The stands full of fans (drawn only once, see rooms.draw_saved).
    pygame.draw.rect(canvas, (40, 42, 62), (0, 70, canvas.get_width(), 90))
    for fan_y in range(74, 156, 5):
        for fan_x in range(2 + (fan_y // 5) % 2 * 3, canvas.get_width(), 6):
            colour = rooms.fan_colour(fan_x, fan_x * 5 + fan_y)
            pygame.draw.rect(canvas, colour, (fan_x, fan_y, 3, 3))
    pygame.draw.rect(canvas, OUTLINE, (0, 158, canvas.get_width(), 2))


def draw_studio_screen(canvas, developers, tick):
    # developers holds the three pictures (already 2x bigger).
    width = canvas.get_width()

    # 1. The stadium: night sky, stands, grass with mowing stripes, tunnel.
    canvas.fill((14, 16, 34))
    rooms.draw_saved(canvas, "studio_stands", draw_studio_stands)
    for x in range(0, width, 40):
        if (x // 40) % 2 == 0:
            grass = (50, 130, 60)
        else:
            grass = (60, 145, 70)
        pygame.draw.rect(canvas, grass, (x, 160, 40, canvas.get_height() - 160))
    pygame.draw.rect(canvas, (235, 235, 235), (0, STUDIO_FLOOR + 3, width, 2))
    # The players' tunnel on the left: grey stone with a dark inside.
    pygame.draw.rect(canvas, OUTLINE, (6, 128, 66, 70))
    pygame.draw.rect(canvas, (130, 130, 145), (7, 129, 64, 69))
    pygame.draw.rect(canvas, (25, 28, 40), (15, 137, 48, 61))
    pygame.draw.rect(canvas, rooms.HOME_RED, (7, 129, 64, 6))

    # 2. The darkness: the more lights are on, the lighter the stadium.
    count = lights_on(tick)
    darkness = pygame.Surface((width, canvas.get_height()), pygame.SRCALPHA)
    darkness.fill((0, 0, 10, 215 - count * 50))
    canvas.blit(darkness, (0, 0))

    # 3. The floodlight masts. A light that is on shines down on the grass.
    for i in range(len(STUDIO_LIGHTS)):
        x = STUDIO_LIGHTS[i]
        pygame.draw.rect(canvas, (70, 70, 85), (x - 1, 22, 3, 50))           # the pole
        if i < count:
            rooms.draw_light_cone(canvas, x, 18, STUDIO_FLOOR, 16, 120)
            head = (255, 250, 210)
        else:
            head = (60, 60, 75)
        pygame.draw.rect(canvas, OUTLINE, (x - 12, 8, 25, 14))
        pygame.draw.rect(canvas, head, (x - 11, 9, 23, 12))

    # Phone flashes in the crowd once the stadium is lit.
    if count >= 2 and tick % 5 < 2:
        flash_x = (tick * 37) % width
        flash_y = 76 + (tick * 13) % 78
        pygame.draw.rect(canvas, (255, 255, 255), (flash_x, flash_y, 2, 2))

    # 4. The logo lights up: a short white flash, then gold letters.
    if tick >= STUDIO_LOGO_TICK:
        if tick < STUDIO_LOGO_TICK + 3:
            canvas.fill((255, 250, 230))
        draw_centred_pixel_text(canvas, "94TH MINUTE", 26, 4, GOLD_ROWS)
        draw_centred_pixel_text(canvas, "STUDIOS", 62, 2, CREAM_ROWS)

    # 5. The developers walk out of the tunnel. While walking they bounce,
    #    when they have arrived they only breathe slowly.
    for i in range(len(developers)):
        x = developer_x(i, tick)
        if x is None:
            continue
        picture = developers[i]
        if x < STUDIO_DEV_X[i]:
            lift = (tick // 3) % 2 * 3
        else:
            lift = rooms.bob(tick, i * 7)
        rooms.draw_shadow(canvas, x - 28, STUDIO_FLOOR + 2, 56)
        canvas.blit(picture, (x - picture.get_width() // 2, STUDIO_FLOOR - picture.get_height() - lift))

    # 6. "PRESS ENTER TO CONTINUE" blinks once everyone is there.
    if tick >= STUDIO_END and tick % 30 < 20:
        draw_centred_pixel_text(canvas, "PRESS ENTER TO CONTINUE", 238, 1, GOLD_ROWS)


def draw_studio_text(window, fonts, scale, tick):
    # The sharp text: "proudly presents" under the logo, "LINE-UP" and the
    # name of every developer who has reached his place.
    if tick >= STUDIO_LOGO_TICK:
        draw_centred_text(window, "proudly presents", fonts["small"], CREAM, 84 * scale)
    if tick >= STUDIO_DEV_TICKS[0]:
        draw_centred_text(window, "- LINE-UP -", fonts["label"], (255, 215, 90), (STUDIO_FLOOR + 10) * scale)
    for i in range(len(STUDIO_NAMES)):
        if developer_x(i, tick) == STUDIO_DEV_X[i]:
            name = fonts["label"].render(STUDIO_NAMES[i], False, CREAM)
            shadow = fonts["label"].render(STUDIO_NAMES[i], False, OUTLINE)
            x = STUDIO_DEV_X[i] * scale - name.get_width() // 2
            y = (STUDIO_FLOOR + 24) * scale
            window.blit(shadow, (x + 2, y + 2))
            window.blit(name, (x, y))


def draw_centred_text(window, text, font, colour, y):
    # Write a text in the middle of the window, with a dark shadow
    # 2 pixels lower and to the right, so it is easy to read on any background.
    picture = font.render(text, False, colour)
    shadow = font.render(text, False, OUTLINE)
    x = (window.get_width() - picture.get_width()) // 2
    window.blit(shadow, (x + 2, y + 2))
    window.blit(picture, (x, y))


def draw_title_text(window, has_save, fonts, scale):
    # The sharp text on the title screen: the line under the logo and the
    # hints at the bottom, all in the middle of the window.
    # (The logo and the menu are pixel letters, see draw_title_screen.)
    draw_centred_text(window, "A comedy mystery in the 94th minute", fonts["small"], CREAM, 98 * scale)
    if has_save:
        note = "A saved game was found: PLAY continues it."
    else:
        note = "No saved game yet: PLAY starts a new one."
    draw_centred_text(window, note, fonts["small"], CREAM, 214 * scale)
    draw_centred_text(window, "UP / DOWN: choose   ENTER: select   LEFT / RIGHT: volume   M: mute   F11: fullscreen",
                      fonts["small"], CREAM, 228 * scale)


def draw_confirm_text(window, question, fonts, scale):
    # The question of the yes/no box, and the keys to answer it.
    y = 104
    for line in wrap_text(question, fonts["text"], 260 * scale):
        window.blit(fonts["text"].render(line, False, BROWN), (110 * scale, y * scale))
        y = y + 11
    window.blit(fonts["small"].render("Y: yes        N: no", False, ORANGE), (110 * scale, 154 * scale))

def draw_menu_text(window, menu, fonts, scale):
    # The question in the tab, and the options below it. The selected
    # option gets an arrow and an orange colour.
    extra = menu_extra(len(menu["actions"]))
    question = fonts["title"].render(menu["title"].upper(), False, CREAM)
    window.blit(question, ((BOX_X + 14) * scale, (BOX_Y - 5 - extra) * scale))
    y = BOX_Y + 12 - extra
    for i in range(len(menu["actions"])):
        label = str(i + 1) + ". " + menu["actions"][i]["label"]
        if i == menu["selected"]:
            text = fonts["text"].render("> " + label, False, ORANGE)
        else:
            text = fonts["text"].render("  " + label, False, BROWN)
        window.blit(text, ((BOX_X + 8) * scale, y * scale))
        y = y + 11


def draw_review_text(window, review, state, fonts, scale):
    # The words on the VAR monitor: the header, the time, the shirt
    # numbers, and the instructions for the current step.
    header = fonts["title"].render("VAR REVIEW  -  BERNIE'S HEAD-CAM", False, CREAM)
    window.blit(header, (24 * scale, 20 * scale))
    time = review_time(review, state)
    window.blit(fonts["small"].render("TIME " + str(time) + " s", False, (255, 220, 90)),
                (24 * scale, 34 * scale))

    # The "rules" step: the offside explanation from story.json on the
    # panel, and how to start. The first line is the heading (in orange).
    if state["step"] == "rules":
        y = PITCH_Y + 4
        for i in range(len(review["rules"])):
            if i == 0:
                colour = ORANGE
            else:
                colour = BROWN
            window.blit(fonts["text"].render(review["rules"][i], False, colour), ((PITCH_X + 10) * scale, y * scale))
            y = y + 13
        lines = ["Read this first, then start the footage.",
                 "ENTER: start the footage",
                 "ESC: stop the review"]
        y = BOX_Y + 12
        for line in lines:
            window.blit(fonts["text"].render(line, False, BROWN), ((BOX_X + 10) * scale, y * scale))
            y = y + 11
        return

    # Shirt numbers on the dots, in the number colour from story.json
    # (white on red, black on yellow, so you can always read them).
    for player in review["players"]:
        x = metres_to_x(game.value_at(review["tracks"][player["id"]], time, 1))
        y = int(game.value_at(review["tracks"][player["id"]], time, 2))
        picture = fonts["small"].render(player["number"], False, player["number_colour"])
        window.blit(picture, ((x - 2) * scale, (y - 4) * scale))

    # Instructions in the box at the bottom.
    if state["step"] == "time":
        lines = ["Find the exact moment the ball leaves the passer's boot.",
                 "LEFT / RIGHT: move through the footage   ENTER: lock this moment",
                 "You only get one look.                   ESC: stop the review"]
    else:
        lines = ["Locked at " + str(time) + " s. Put the line on the 2nd-last opponent.",
                 "LEFT / RIGHT: move the line (hold to go faster)   ENTER: lock",
                 "The keeper counts. Level = onside.       ESC: back to the footage"]
    y = BOX_Y + 12
    for line in lines:
        window.blit(fonts["text"].render(line, False, BROWN), ((BOX_X + 10) * scale, y * scale))
        y = y + 11


def draw_timer_text(window, seconds_left, fonts, scale):
    # "STADIUM WAITS 6:42": minutes and seconds left.
    seconds = max(0, int(seconds_left))
    minutes = seconds // 60
    rest = seconds % 60
    # str(rest).zfill(2) adds a 0 in front of single digits: 7 -> "07".
    text = "STADIUM WAITS " + str(minutes) + ":" + str(rest).zfill(2)
    window.blit(fonts["tiny"].render(text, False, CREAM), ((TIMER_X + 4) * scale, (TIMER_Y + 2) * scale))


def draw_e_bubble(window, middle_x, top_y, tick, font):
    # The "E" bubble above things you can use, drawn directly on the big
    # window. It breathes: its size grows and shrinks a little, following
    # a sine wave (math.sin goes smoothly from -1 to 1 and back).
    size = 20 + 2 * math.sin(tick * 0.15)
    x = middle_x - size / 2
    y = top_y - size / 2
    pygame.draw.rect(window, OUTLINE, (x - 2, y - 2, size + 4, size + 4))
    pygame.draw.rect(window, (255, 252, 235), (x, y, size, size))
    pygame.draw.rect(window, OUTLINE, (middle_x - 3, y + size + 2, 6, 3))
    letter = font.render("E", False, OUTLINE)
    window.blit(letter, (middle_x - letter.get_width() / 2, top_y - letter.get_height() / 2))


def draw_ending_text(window, story, ending_id, epilogue, summary, fonts, scale):
    # The ending: its title, its text, what happens to Infantini in the
    # TV studio (the epilogue), the summary (the right call, from
    # game.ending_summary) and what the player can do now.
    ending = story["endings"][ending_id]
    window.blit(fonts["small"].render("ENDING", False, CREAM), (40 * scale, 28 * scale))
    window.blit(fonts["big"].render(ending["title"].upper(), False, CREAM), (40 * scale, 36 * scale))
    y = 70
    for line in wrap_text(ending["text"], fonts["text"], 396 * scale):
        window.blit(fonts["text"].render(line, False, BROWN), (42 * scale, y * scale))
        y = y + 10
    y = y + 6
    for line in wrap_text(epilogue, fonts["text"], 396 * scale):
        window.blit(fonts["text"].render(line, False, (120, 60, 140)), (42 * scale, y * scale))
        y = y + 10
    y = y + 8
    for text in summary:
        for line in wrap_text(text, fonts["text"], 396 * scale):
            window.blit(fonts["text"].render(line, False, (40, 120, 60)), (42 * scale, y * scale))
            y = y + 10
    hint = fonts["small"].render("N: new game        Q: quit", False, ORANGE)
    window.blit(hint, (42 * scale, 232 * scale))

def draw_dialogue_text(window, page, letters_shown, fonts, scale, faded=False):
    # Write the title and the lines of the page. Only the first
    # letters_shown letters are written, which makes the typing effect.
    # faded=True writes everything in grey (the text was already read).
    if faded:
        text_colour = (140, 130, 120)
    else:
        text_colour = BROWN
    if page["title"] != "":
        title = fonts["title"].render(page["title"].upper(), False, CREAM)
        window.blit(title, ((BOX_X + 14) * scale, (BOX_Y - 5) * scale))

    letters_left = letters_shown
    y = BOX_Y + 12
    for line in page["lines"]:
        # line[:letters_left] is the start of the line (up to letters_left letters).
        visible = line[:letters_left]
        window.blit(fonts["text"].render(visible, False, text_colour), ((BOX_X + 10) * scale, y * scale))
        letters_left = letters_left - len(line)
        if letters_left <= 0:
            break
        y = y + 11

    # When the whole page is shown, a small "SPACE >" tells the player to continue.
    if letters_shown >= letters_on_page(page) and not faded:
        hint = fonts["small"].render("SPACE >", False, ORANGE)
        window.blit(hint, ((BOX_X + BOX_WIDTH - 46) * scale, (BOX_Y + BOX_HEIGHT - 12) * scale))


def draw_pundit_text(window, pundit_line, fonts, scale):
    # The pundit's line in his speech box. It looks like "GIANNO INFANTINI: ..." or
    # "GIANNO INFANTINI (sweating): ...": the part before ": " is his name (in orange),
    # the part after it is what he says.
    position = pundit_line.index(": ")
    name = pundit_line[:position]
    said = pundit_line[position + 2:]
    window.blit(fonts["small"].render(name, False, ORANGE), ((SPEECH_X + 8) * scale, (SPEECH_Y + 5) * scale))
    lines = wrap_text(said, fonts["small"], (SPEECH_WIDTH - 16) * scale)
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
        # Safety check: if a line is too wide for the note, make it
        # smaller until it fits (smoothscale keeps handwriting smooth).
        space = (NOTE_X + NOTE_WIDTH - 10 - x) * scale
        if picture.get_width() > space:
            new_height = picture.get_height() * space // picture.get_width()
            picture = pygame.transform.smoothscale(picture, (space, new_height))
        window.blit(picture, (x * scale, y * scale))
        if i < 2:
            y = y + 28
        else:
            y = y + 15
    hint = fonts["small"].render("E: put the note back", False, CREAM)
    window.blit(hint, ((NOTE_X + 40) * scale, (NOTE_Y + NOTE_HEIGHT + 14) * scale))


# ---------------------------------------------------------------- the tutorial

# A short tour of the screen at the start of a new game (and from the pause
# menu). Every step lights up one part of the screen ("area") and explains
# it in one or two sentences. game_2d.py works out where each area is right
# now (tutorial_area). None means no area: the whole screen stays dark.
TUTORIAL_STEPS = [
    {"area": None, "title": "WELCOME, ROOKIE",
     "text": "Your first day as VAR. Here is a quick tour of the screen."},
    {"area": "pundit", "title": "INFANTINI ON TV",
     "text": "Infantini always tells you what to do next. When his box flashes, he has a new tip."},
    {"area": "items", "title": "YOUR ITEMS",
     "text": "Everything you pick up lands here."},
    {"area": "timer", "title": "STADIUM WAITS",
     "text": "The fans won't wait forever. The time only runs while you walk."},
    {"area": "player", "title": "THIS IS YOU",
     "text": "Walk with LEFT / RIGHT. A \"!\" shows where to go next. Stand there and press E."},
    {"area": "textbox", "title": "THE STORY",
     "text": "What happens is written down here. SPACE shows the next page."},
    {"area": None, "title": "YOUR GOAL",
     "text": "Find the missing camera angle and give the referee the right call: GOAL or OFFSIDE."},
]

# The size of the box that explains a step (canvas pixels).
CAPTION_WIDTH = 236
CAPTION_HEIGHT = 58


def draw_door_transition(window, door):
    # The scene change when you walk through a door: a black screen with a
    # round hole in the middle. In the first half the hole gets smaller
    # (the old room disappears), in the second half it gets bigger again
    # (the new room appears).
    # door["frames"] is how long it takes (fast for a door, slow before
    # the ending).
    width, height = window.get_size()
    half = door["frames"] // 2
    frame = door["frame"]

    # In the first half we still show the photo of the old room.
    if frame < half:
        window.blit(door["photo"], (0, 0))

    # The biggest hole: from the middle to a corner (Pythagoras), so the
    # whole screen is visible when the hole is this big.
    biggest = math.sqrt(width * width + height * height) / 2
    if frame < half:
        # Closing: from the biggest hole down to nothing.
        radius = biggest * (half - frame) / half
    else:
        # Opening: from nothing up to the biggest hole.
        radius = biggest * (frame - half) / half

    # A black sheet with a see-through circle cut out of it.
    # (0, 0, 0, 0) is "fully see-through"; draw.circle replaces the pixels.
    sheet = pygame.Surface((width, height), pygame.SRCALPHA)
    sheet.fill((0, 0, 0, 255))
    if radius > 0:
        pygame.draw.circle(sheet, (0, 0, 0, 0), (width // 2, height // 2), int(radius))
    window.blit(sheet, (0, 0))


def draw_tutorial(window, step_number, area, fonts, scale):
    # One step of the tutorial, drawn on top of everything: the screen gets
    # dark except the area (x, y, width, height in canvas pixels), which gets
    # a yellow frame, and a box next to it explains it.
    step = TUTORIAL_STEPS[step_number]
    canvas_width = window.get_width() // scale
    canvas_height = window.get_height() // scale

    # The dark layer. fill((0, 0, 0, 0), rect) makes the area see-through.
    shade = pygame.Surface(window.get_size(), pygame.SRCALPHA)
    shade.fill((10, 10, 20, 205))
    if area is not None:
        x, y, width, height = area
        shade.fill((0, 0, 0, 0), (x * scale, y * scale, width * scale, height * scale))
    window.blit(shade, (0, 0))

    # Where the box goes: in the middle when there is no area; under an
    # area in the top half of the screen, above an area in the bottom half.
    if area is None:
        box_x = (canvas_width - CAPTION_WIDTH) // 2
        box_y = (canvas_height - CAPTION_HEIGHT) // 2
    else:
        x, y, width, height = area
        pygame.draw.rect(window, (255, 215, 60), (x * scale, y * scale, width * scale, height * scale), 3)
        box_x = x + width // 2 - CAPTION_WIDTH // 2
        # max / min keep the box inside the screen.
        box_x = max(6, min(box_x, canvas_width - CAPTION_WIDTH - 6))
        if y + height // 2 < canvas_height // 2:
            box_y = y + height + 6
        else:
            box_y = y - CAPTION_HEIGHT - 6

    # The box: a dark outline with cream inside, the title, the text and
    # which keys to press (with the step number, e.g. 2/7).
    pygame.draw.rect(window, OUTLINE, (box_x * scale, box_y * scale, CAPTION_WIDTH * scale, CAPTION_HEIGHT * scale))
    pygame.draw.rect(window, (255, 245, 220), (box_x * scale + 4, box_y * scale + 4,
                                               CAPTION_WIDTH * scale - 8, CAPTION_HEIGHT * scale - 8))
    window.blit(fonts["title"].render(step["title"], False, ORANGE), ((box_x + 8) * scale, (box_y + 6) * scale))
    y = box_y + 18
    for line in wrap_text(step["text"], fonts["small"], (CAPTION_WIDTH - 16) * scale):
        window.blit(fonts["small"].render(line, False, BROWN), ((box_x + 8) * scale, y * scale))
        y = y + 8
    hint = "SPACE: next   ESC: skip   (" + str(step_number + 1) + "/" + str(len(TUTORIAL_STEPS)) + ")"
    window.blit(fonts["tiny"].render(hint, False, ORANGE), ((box_x + 8) * scale, (box_y + CAPTION_HEIGHT - 11) * scale))
