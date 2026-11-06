# The short "film scenes" at the end of the 2D game.
# Clip 1 always happens on the pitch: who celebrates and who is sad
# depends on the call (GOAL, OFFSIDE, or the coin when time ran out).
# Every clip is drawn frame by frame: "frame" counts from 0 (start) up to
# CLIP_FRAMES (the end), and every drawing uses it to move things.

import math
import pygame
import rooms
from rooms import FLOOR_Y, ROOM_WIDTH, OUTLINE, WHITE, HOME_RED, AWAY_YELLOW, SKIN, YELLOW, BLACK

# How long one clip lasts: 150 frames = 5 seconds (30 frames per second).
CLIP_FRAMES = 150

# The "camera" of the clips: it films a 320 x 180 part of the canvas,
# starting at (CLIP_LEFT, CLIP_TOP), and makes it 3 times bigger. That is
# closer than in the game (2 times), so the people look bigger, like a film.
CLIP_LEFT = 90
CLIP_TOP = 36
CLIP_WIDTH = 320
CLIP_HEIGHT = 180
CLIP_ZOOM = 3

# The colours of the confetti: red and white for the home team,
# yellow and black for the away team.
HOME_CONFETTI = [HOME_RED, WHITE, (255, 120, 120)]
AWAY_CONFETTI = [AWAY_YELLOW, BLACK, (255, 235, 120)]


def pitch_clip_name(progress):
    # Which pitch clip to show: the coin (time ran out), the away team
    # celebrating (OFFSIDE) or the home team celebrating (GOAL).
    if progress["ending"] == "time_up":
        return "pitch_time_up"
    if progress["choices"].get("ruling") == "offside":
        return "pitch_offside"
    return "pitch_goal"


# ---------------------------------------------------------------- small helpers

def ease(frame, start, end):
    # How far a movement from frame "start" to frame "end" has got:
    # 0.0 before it starts, 1.0 when it is done, and in between a number
    # that grows slower at the end (it looks like slowing down).
    if frame <= start:
        return 0.0
    if frame >= end:
        return 1.0
    part = (frame - start) / (end - start)
    return 1 - (1 - part) * (1 - part)


def stand(canvas, picture, x, lift):
    # Draw a person standing on the grass. lift moves them up (a jump);
    # the shadow gets smaller the higher they are.
    width = picture.get_width()
    shrink = min(lift, 10)
    rooms.draw_shadow(canvas, x + 2 + shrink, FLOOR_Y + 1, width - 4 - shrink * 2)
    canvas.blit(picture, (x, FLOOR_Y - picture.get_height() - lift))


def kneel(canvas, picture, x):
    # Draw a person on their knees: we only draw the top part of the
    # picture (without the lower legs), placed lower on the grass.
    height = picture.get_height() - 9
    top_part = picture.subsurface((0, 0, picture.get_width(), height))
    rooms.draw_shadow(canvas, x, FLOOR_Y + 1, picture.get_width())
    canvas.blit(top_part, (x, FLOOR_Y - height))


def slump(canvas, picture, x):
    # Draw a sad person: turned a little (head down) and 2 pixels lower.
    sad = pygame.transform.rotate(picture, -7)
    rooms.draw_shadow(canvas, x + 2, FLOOR_Y + 1, picture.get_width() - 4)
    canvas.blit(sad, (x, FLOOR_Y - sad.get_height() + 2))


def arms_up(canvas, x, head_y, width):
    # Two arms stretched up next to the head (a celebration).
    for arm_x in [x + 3, x + width - 6]:
        pygame.draw.rect(canvas, OUTLINE, (arm_x - 1, head_y - 9, 4, 14))
        pygame.draw.rect(canvas, SKIN, (arm_x, head_y - 8, 2, 12))


def hands_on_head(canvas, x, head_y, width):
    # Two hands on top of the head (shock: "how was that OFFSIDE?!").
    for hand_x in [x + 7, x + width - 11]:
        pygame.draw.rect(canvas, OUTLINE, (hand_x - 1, head_y - 2, 6, 5))
        pygame.draw.rect(canvas, SKIN, (hand_x, head_y - 1, 4, 3))


def confetti(canvas, frame, colours):
    # 80 pieces of confetti fall from the sky and sway left and right.
    # Every piece gets its own place and speed from its number (i), so
    # the confetti looks random but is the same every time.
    for i in range(80):
        x = (i * 53 + int(math.sin(frame / 10 + i) * 6)) % ROOM_WIDTH
        y = (i * 37 + frame * (2 + i % 3)) % 210
        pygame.draw.rect(canvas, colours[i % len(colours)], (x, y, 2 + i % 2, 2))


def jump_height(frame, phase):
    # A bouncing jump: up and down like a ball, between 0 and 10 pixels.
    return int(abs(math.sin(frame / 5 + phase)) * 10)


# ---------------------------------------------------------------- the clips

def draw_clip(canvas, pictures, name, frame):
    # Draw one frame of a clip on the room canvas.
    if name == "pitch_goal":
        draw_pitch_goal(canvas, pictures, frame)
    elif name == "pitch_offside":
        draw_pitch_offside(canvas, pictures, frame)
    elif name == "pitch_time_up":
        draw_pitch_time_up(canvas, pictures, frame)


def draw_pitch_goal(canvas, pictures, frame):
    # GOAL! The home striker slides on his knees with his arms up, the
    # passer jumps for joy, red and white confetti falls. The away players
    # stand there with their heads down.
    flashing = (frame // 8) % 2 == 0
    rooms.draw_pitch_background(canvas, flashing, frame)
    stand(canvas, pictures["referee"], 100, 0)

    # The away players, sad.
    slump(canvas, pictures["captain_sad"], 300)
    slump(canvas, pictures["defender_sad"], 368)

    # The passer runs in from the right, then jumps again and again.
    passer_x = int(300 - 45 * ease(frame, 0, 40))
    lift = 0
    if frame > 40:
        lift = jump_height(frame, 1)
    passer = pictures["passer"]
    stand(canvas, passer, passer_x, lift)
    arms_up(canvas, passer_x, FLOOR_Y - passer.get_height() - lift + 14, passer.get_width())

    # The striker slides on his knees from the left to the middle.
    striker = pictures["striker"]
    striker_x = int(110 + 100 * ease(frame, 0, 55))
    kneel(canvas, striker, striker_x)
    arms_up(canvas, striker_x, FLOOR_Y - striker.get_height() + 9 + 14, striker.get_width())
    # While he slides, grass flies up behind him.
    if frame < 55:
        for i in range(4):
            pygame.draw.rect(canvas, (95, 200, 80), (striker_x - 4 - i * 3, FLOOR_Y - 2 - (frame + i) % 5, 2, 2))

    confetti(canvas, frame, HOME_CONFETTI)


def draw_pitch_offside(canvas, pictures, frame):
    # OFFSIDE! The away captain and a defender run in and jump for joy,
    # yellow and black confetti falls. The home striker is on his knees
    # with his hands on his head; the passer stands there, sad.
    rooms.draw_pitch_background(canvas, False, frame)
    stand(canvas, pictures["referee"], 100, 0)

    # The home players.
    striker = pictures["striker"]
    shake = 0
    if (frame // 4) % 6 == 0:
        shake = 1                       # now and then he shakes his head
    kneel(canvas, striker, 150 + shake)
    hands_on_head(canvas, 150 + shake, FLOOR_Y - striker.get_height() + 9 + 14, striker.get_width())
    slump(canvas, pictures["passer"], 196)

    # The away players run in from the right and jump.
    for name, start_x, end_x, phase in [("captain", 430, 262, 0), ("defender", 460, 318, 2)]:
        person = pictures[name]
        x = int(start_x - (start_x - end_x) * ease(frame, 0, 45))
        lift = 0
        if frame > 45:
            lift = jump_height(frame, phase)
        stand(canvas, person, x, lift)
        arms_up(canvas, x, FLOOR_Y - person.get_height() - lift + 14, person.get_width())

    confetti(canvas, frame, AWAY_CONFETTI)


# Where the referee stands in the coin clip, and where his hand is.
COIN_REFEREE_X = 230
COIN_HAND_Y = FLOOR_Y - 20


def draw_pitch_time_up(canvas, pictures, frame):
    # Time is up: the referee flips a coin high into the air. It lands on
    # OFFSIDE (shown big in the middle). The floodlights go out one by one
    # and Bernie walks home with his sports bag.
    rooms.draw_pitch_background(canvas, False, frame)
    referee = pictures["referee"]
    stand(canvas, referee, COIN_REFEREE_X, 0)
    slump(canvas, pictures["striker"], 150)
    # The away captain jumps a little: the coin was good news for him.
    stand(canvas, pictures["captain"], 310, jump_height(frame, 0) // 2)

    # 1. The coin flies up and comes down again (frames 0 to 45).
    #    The height follows a curve: up fast, slower at the top, down again.
    #    Its width changes, so it looks like it is spinning.
    if frame < 45:
        part = frame / 45
        height = int(4 * part * (1 - part) * 110)       # 0 -> 110 -> 0
        coin_x = COIN_REFEREE_X + 28
        coin_y = COIN_HAND_Y - height
        width = 2 + int(abs(math.cos(frame / 2)) * 6)
        pygame.draw.ellipse(canvas, OUTLINE, (coin_x - width // 2 - 1, coin_y - 1, width + 2, 10))
        pygame.draw.ellipse(canvas, (255, 210, 60), (coin_x - width // 2, coin_y, width, 8))

    # 2. The result: a big coin in the middle (frames 45 to 110).
    #    The word OFFSIDE on it is added as sharp text (draw_clip_text).
    if 45 <= frame < 110:
        pygame.draw.circle(canvas, OUTLINE, (240, 128), 30)
        pygame.draw.circle(canvas, (230, 180, 40), (240, 128), 29)
        pygame.draw.circle(canvas, (255, 215, 80), (240, 128), 25)
        pygame.draw.circle(canvas, (255, 240, 160), (230, 118), 6)            # shine

    # 3. Bernie walks to the tunnel with his bag (frames 50 to 150).
    #    He bobs up and down while he walks.
    if frame > 50:
        bernie = pictures["bernie"]
        bernie_x = int(420 - 380 * ease(frame, 50, 150))
        bob = (frame // 5) % 2
        stand(canvas, bernie, bernie_x, bob)
        rooms.outlined_box(canvas, (60, 110, 210), bernie_x + 4, FLOOR_Y - 26 - bob, 14, 10)  # bag
        pygame.draw.rect(canvas, WHITE, (bernie_x + 6, FLOOR_Y - 23 - bob, 10, 2))

    # 4. The floodlights go out one by one: from frame 70, every 20 frames
    #    the whole picture gets a bit darker (a see-through dark layer).
    if frame > 70:
        steps = min(4, (frame - 70) // 20 + 1)
        dark = pygame.Surface((canvas.get_width(), canvas.get_height()), pygame.SRCALPHA)
        dark.fill((5, 5, 20, steps * 40))
        canvas.blit(dark, (0, 0))


# ---------------------------------------------------------------- the text on top

def to_window(x, y):
    # Where a point of the canvas is on the window, seen through the clip
    # camera: first move it (the camera starts at CLIP_LEFT, CLIP_TOP),
    # then make it CLIP_ZOOM times bigger.
    return ((x - CLIP_LEFT) * CLIP_ZOOM, (y - CLIP_TOP) * CLIP_ZOOM)


def draw_clip_picture(window, canvas):
    # Film the clip: cut the camera's part out of the canvas and make it
    # big enough to fill the whole window.
    part = canvas.subsurface((CLIP_LEFT, CLIP_TOP, CLIP_WIDTH, CLIP_HEIGHT))
    window.blit(pygame.transform.scale(part, window.get_size()), (0, 0))


def draw_clip_text(window, fonts, name, frame):
    # The sharp text on top of a clip: the scoreboard, the big OFFSIDE on
    # the coin, black film bars at the top and bottom with a caption, and
    # "SPACE: skip".
    scale = 2       # the film bars and the caption use the normal game size
    if name == "pitch_goal":
        score = "1 - 0"
        caption = "FULL TIME!  FCB 1 - 0 BVB"
    else:
        score = "0 - 0"
        caption = "FULL TIME!  FCB 0 - 0 BVB"
    if name == "pitch_time_up":
        caption = "TIME'S UP!  The referee lets a coin decide..."

    # The scoreboard (not in the dark coin clip after the lights go out).
    if name != "pitch_time_up" or frame < 70:
        label = fonts["text"]
        window.blit(label.render("FCB", False, WHITE), to_window(129, 50))
        window.blit(label.render(score, False, WHITE), to_window(159, 50))
        window.blit(label.render("BVB", False, (30, 30, 40)), to_window(191, 50))
        window.blit(label.render("FULL TIME", False, (30, 20, 20)), to_window(140, 67))

    # OFFSIDE on the big coin.
    if name == "pitch_time_up" and 45 <= frame < 110:
        word = fonts["title"].render("OFFSIDE", False, (120, 70, 10))
        x, y = to_window(240, 128)
        window.blit(word, (x - word.get_width() // 2, y - word.get_height() // 2))

    # Black film bars at the top and the bottom.
    width = window.get_width()
    height = window.get_height()
    bar = 16 * scale
    pygame.draw.rect(window, (0, 0, 0), (0, 0, width, bar))
    pygame.draw.rect(window, (0, 0, 0), (0, height - bar, width, bar))
    text = fonts["text"].render(caption, False, (255, 245, 220))
    window.blit(text, (16 * scale, height - bar + (bar - text.get_height()) // 2))
    skip = fonts["small"].render("SPACE: skip", False, (255, 170, 80))
    window.blit(skip, (width - skip.get_width() - 12 * scale, height - bar + (bar - skip.get_height()) // 2))
