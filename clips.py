# The short "film scenes" at the end of the 2D game.
# Clip 1 always happens on the pitch: who celebrates and who is sad
# depends on the call (GOAL, OFFSIDE, or the coin when time ran out).
# Clip 2 always happens in Infantini's TV studio: he is arrested, his bet
# wins, or his bet is lost.
# Every clip is drawn frame by frame: "frame" counts from 0 (start) up to
# CLIP_FRAMES (the end), and every drawing uses it to move things.

import math
import random
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
    elif name == "studio_wins":
        draw_studio_wins(canvas, pictures, frame)
    elif name == "studio_loses":
        draw_studio_loses(canvas, pictures, frame)
    elif name == "studio_arrested":
        draw_studio_arrested(canvas, pictures, frame)


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


# ---------------------------------------------------------------- the TV studio clips

# Clip 2 always happens in Infantini's TV studio. What happens there
# depends on game.studio_outcome: "arrested", "wins" or "loses".

# In the studio everybody is drawn 2 times bigger (a close-up).
STUDIO_SIZE = 2
# Where Infantini stands (his middle).
STUDIO_MIDDLE = 250


def final_score(progress):
    # The final score: 0 - 0 if the goal was taken away (OFFSIDE, or the
    # coin when time ran out), otherwise 1 - 0.
    if progress["ending"] == "time_up" or progress["choices"].get("ruling") == "offside":
        return "0 - 0"
    return "1 - 0"


def bigger(picture):
    # The same picture, STUDIO_SIZE times bigger. scale keeps the pixels sharp.
    width = picture.get_width() * STUDIO_SIZE
    height = picture.get_height() * STUDIO_SIZE
    return pygame.transform.scale(picture, (width, height))


def person_top(picture):
    # The y position of the top of a (bigger) person standing on the floor.
    return FLOOR_Y - picture.get_height()


def draw_studio(canvas, frame):
    # The TV studio: a dark blue wall, two spotlights, a big screen with
    # the score, an "ON AIR" light, a shiny floor and a small presenter's
    # desk on the left.
    rooms.draw_bands(canvas, [(20, 25, 55), (28, 34, 70), (36, 44, 86), (44, 54, 100)],
                     0, 0, ROOM_WIDTH, FLOOR_Y)
    # Thin light stripes on the wall.
    for stripe_x in range(100, 420, 40):
        pygame.draw.rect(canvas, (60, 72, 125), (stripe_x, 36, 2, 164))
    # The big screen (the score and the show's name are added as text).
    rooms.shaded_box(canvas, (15, 18, 30), (60, 64, 80), (8, 8, 15), 150, 48, 200, 72)
    pygame.draw.rect(canvas, (25, 55, 120), (154, 52, 192, 52))
    pygame.draw.rect(canvas, (200, 40, 50), (154, 104, 192, 12))
    # The "ON AIR" light: it blinks.
    if (frame // 15) % 2 == 0:
        on_air = (230, 40, 40)
    else:
        on_air = (120, 30, 30)
    rooms.outlined_box(canvas, on_air, 360, 44, 40, 12)

    # The shiny studio floor: dark blue with light stripes (reflections).
    pygame.draw.rect(canvas, OUTLINE, (0, FLOOR_Y, ROOM_WIDTH, 1))
    pygame.draw.rect(canvas, (30, 36, 70), (0, FLOOR_Y + 1, ROOM_WIDTH, 70))
    for shine_x in range(100, 420, 60):
        pygame.draw.line(canvas, (60, 70, 120), (shine_x, FLOOR_Y + 3), (shine_x + 20, FLOOR_Y + 14))

    # The small presenter's desk on the left, with the show's round logo.
    rooms.draw_shadow(canvas, 96, FLOOR_Y + 1, 86)
    rooms.shaded_box(canvas, (200, 205, 220), (235, 238, 245), (160, 165, 180), 98, 146, 82, 6)
    rooms.shaded_box(canvas, (40, 60, 130), (60, 85, 165), (28, 42, 95), 102, 152, 74, 48)
    pygame.draw.rect(canvas, (200, 40, 50), (102, 162, 74, 3))
    pygame.draw.circle(canvas, OUTLINE, (139, 182), 10)
    pygame.draw.circle(canvas, (255, 215, 70), (139, 182), 9)
    pygame.draw.circle(canvas, (40, 60, 130), (139, 182), 5)

    # Two spotlights shine down from the ceiling.
    for lamp_x in [210, 330]:
        rooms.outlined_box(canvas, (70, 70, 80), lamp_x - 6, 36, 12, 6)
        rooms.draw_light_cone(canvas, lamp_x, 42, FLOOR_Y, 10, 110)


def draw_infantini(canvas, pictures, mood, x, turn):
    # Infantini standing in the studio, his whole body, 2 times bigger.
    # mood is his face (0 = calm ... 4 = furious). turn tilts him (his head
    # hangs down when he is taken away). Returns the top of his picture.
    picture = bigger(pictures["infantini"][mood])
    top = person_top(picture)
    rooms.draw_shadow(canvas, x - 26, FLOOR_Y + 1, 52)
    if turn != 0:
        picture = pygame.transform.rotate(picture, turn)
    canvas.blit(picture, (x - picture.get_width() // 2, FLOOR_Y - picture.get_height()))
    return top


def draw_hand(canvas, x, y):
    # A hand (a small skin-coloured box with an outline).
    rooms.outlined_box(canvas, SKIN, x, y, 8, 7)
    pygame.draw.rect(canvas, (214, 150, 112), (x, y + 5, 8, 2))


def draw_slip(canvas, x, y, size):
    # The betting slip: white paper with lines and a red stamp.
    # size is its width (it gets smaller when it is crumpled).
    height = size + size // 3
    rooms.outlined_box(canvas, WHITE, x, y, size, height)
    if size > 8:
        pygame.draw.line(canvas, (150, 150, 165), (x + 2, y + 3), (x + size - 3, y + 3))
        pygame.draw.line(canvas, (150, 150, 165), (x + 2, y + 6), (x + size - 5, y + 6))
        pygame.draw.rect(canvas, (220, 50, 50), (x + size - 6, y + height - 5, 4, 3))


# Where Infantini's right hand hangs (on our right), and where his mouth
# is, measured from the top of his (bigger) picture.
HAND_FROM_MIDDLE = 18
HAND_FROM_TOP = 52
MOUTH_FROM_TOP = 37


def draw_studio_wins(canvas, pictures, frame):
    # His bet wins (0:0): he smiles, lifts the betting slip to his mouth
    # and kisses it. Little hearts float up and banknotes rain down.
    draw_studio(canvas, frame)
    top = draw_infantini(canvas, pictures, 0, STUDIO_MIDDLE, 0)

    # The hand with the slip goes up to his mouth (frames 0 to 35),
    # then waves it left and right.
    rise = ease(frame, 0, 35)
    hand_x = int(STUDIO_MIDDLE + HAND_FROM_MIDDLE - 14 * rise)
    hand_y = int(top + HAND_FROM_TOP - (HAND_FROM_TOP - MOUTH_FROM_TOP) * rise)
    if frame > 70:
        hand_x = hand_x + int(math.sin(frame / 4) * 10)
    draw_slip(canvas, hand_x - 2, hand_y - 14, 14)
    draw_hand(canvas, hand_x, hand_y)

    # The kiss: pink hearts float up from the slip (frames 35 to 75).
    if 35 < frame < 75:
        for i in range(3):
            rise_up = (frame - 35 + i * 12) % 40
            heart_x = STUDIO_MIDDLE + 6 + i * 9 + int(math.sin(frame / 5 + i) * 3)
            heart_y = top + 20 - rise_up
            pygame.draw.rect(canvas, (255, 120, 160), (heart_x, heart_y, 2, 2))
            pygame.draw.rect(canvas, (255, 120, 160), (heart_x + 3, heart_y, 2, 2))
            pygame.draw.rect(canvas, (255, 120, 160), (heart_x + 1, heart_y + 2, 3, 2))

    # Banknotes rain down from frame 40 (green notes with a dark middle).
    if frame > 40:
        for i in range(24):
            x = 100 + (i * 41) % 300 + int(math.sin(frame / 8 + i) * 5)
            y = 36 + ((frame - 40) * (2 + i % 2) + i * 23) % 180
            rooms.outlined_box(canvas, (110, 200, 110), x, y, 8, 4)
            pygame.draw.rect(canvas, (60, 140, 70), (x + 3, y + 1, 2, 2))


def draw_studio_loses(canvas, pictures, frame):
    # His bet is lost (1:0): he stares at the betting slip, his face turns
    # furious, he crumples the slip into a ball and throws it away.
    # Steam comes out next to his head.
    draw_studio(canvas, frame)
    if frame < 35:
        mood = 2
    else:
        mood = 4
    top = draw_infantini(canvas, pictures, mood, STUDIO_MIDDLE, 0)

    # He holds the slip up in front of him. It gets smaller (crumpled)
    # from frame 35 to 70.
    hand_x = STUDIO_MIDDLE + HAND_FROM_MIDDLE
    hand_y = top + HAND_FROM_TOP - 8
    if frame < 70:
        size = int(14 - 9 * ease(frame, 35, 70))
        draw_slip(canvas, hand_x - 2, hand_y - size, size)
        draw_hand(canvas, hand_x, hand_y)
    else:
        # Then the paper ball flies away to the right in a curve.
        part = ease(frame, 70, 100)
        ball_x = int(hand_x + 130 * part)
        ball_y = int(hand_y - 10 - 60 * math.sin(part * math.pi))
        if frame < 100:
            pygame.draw.circle(canvas, OUTLINE, (ball_x, ball_y), 4)
            pygame.draw.circle(canvas, (230, 230, 220), (ball_x, ball_y), 3)
        draw_hand(canvas, hand_x, hand_y)

    # Steam: white puffs rise next to his head while he is furious.
    if frame >= 35:
        for side in [-1, 1]:
            for puff in range(3):
                age = (frame + puff * 10) % 30
                puff_x = STUDIO_MIDDLE + side * (34 + age // 3)
                puff_y = top + 26 - age
                steam = pygame.Surface((8, 8), pygame.SRCALPHA)
                pygame.draw.circle(steam, (240, 240, 250, 200 - age * 6), (4, 4), 2 + age // 10)
                canvas.blit(steam, (puff_x - 4, puff_y - 4))


def police_positions(frame):
    # Where the two police officers stand (their middles) and how far
    # everybody has walked to the left. Used for the pictures and for the
    # word POLICE on their vests, so both always match.
    away = int(330 * ease(frame, 65, 115))
    left_x = int(60 + 120 * ease(frame, 0, 45)) - away
    right_x = int(440 - 120 * ease(frame, 0, 45)) - away
    return left_x, right_x, away


def draw_studio_arrested(canvas, pictures, frame):
    # He is arrested: two police officers walk in from both sides, the
    # handcuffs click, and they lead him away with his head down.
    # Then the picture turns to TV static: SIGNAL LOST.
    police = bigger(pictures["police"])
    draw_studio(canvas, frame)
    left_x, right_x, away = police_positions(frame)

    # The officers bob a little while they walk.
    walk = 0
    if frame < 45 or frame > 65:
        walk = (frame // 5) % 2 * 2
    for x in [left_x, right_x]:
        rooms.draw_shadow(canvas, x - 26, FLOOR_Y + 1, 52)
        canvas.blit(police, (x - police.get_width() // 2, person_top(police) - walk))

    # Infantini: furious, and from frame 60 his head hangs down.
    turn = 0
    if frame > 60:
        turn = -10
    top = draw_infantini(canvas, pictures, 4, STUDIO_MIDDLE - away, turn)

    # The handcuffs (from frame 45): two grey rings with a short chain,
    # on his hands in front of him.
    if frame >= 45:
        cuffs_x = STUDIO_MIDDLE - 8 - away
        cuffs_y = top + HAND_FROM_TOP
        for ring_x in [cuffs_x, cuffs_x + 16]:
            pygame.draw.circle(canvas, OUTLINE, (ring_x, cuffs_y), 5)
            pygame.draw.circle(canvas, (190, 195, 210), (ring_x, cuffs_y), 4)
            pygame.draw.circle(canvas, OUTLINE, (ring_x, cuffs_y), 2)
        pygame.draw.line(canvas, (150, 155, 170), (cuffs_x + 5, cuffs_y), (cuffs_x + 11, cuffs_y), 2)

    # TV static from frame 115: grey blocks in random brightness,
    # different every frame (so it flickers).
    if frame >= 115:
        for block_y in range(CLIP_TOP, CLIP_TOP + CLIP_HEIGHT, 4):
            for block_x in range(CLIP_LEFT, CLIP_LEFT + CLIP_WIDTH, 4):
                grey = random.randint(30, 220)
                pygame.draw.rect(canvas, (grey, grey, grey), (block_x, block_y, 4, 4))


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


def draw_clip_text(window, fonts, name, frame, score):
    # The sharp text on top of a clip: the scoreboard (pitch) or the big
    # studio screen, black film bars at the top and bottom with a caption,
    # and "SPACE: skip". score is the final score, e.g. "1 - 0".
    scale = 2       # the film bars and the caption use the normal game size
    if name.startswith("studio"):
        draw_studio_text(window, fonts, name, frame, score)
        return
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


# What the caption says in each studio clip.
STUDIO_CAPTIONS = {
    "studio_wins": "MEANWHILE, IN THE TV STUDIO...  his bet on 0:0 wins.",
    "studio_loses": "MEANWHILE, IN THE TV STUDIO...  his 500 are gone.",
    "studio_arrested": "MEANWHILE, IN THE TV STUDIO...  POLICE!",
}


def draw_studio_text(window, fonts, name, frame, score):
    # The text in the studio clips: the score and the show's name on the
    # big screen, "ON AIR", "CLICK!" for the handcuffs and "SIGNAL LOST"
    # for the static at the end. Then the film bars with the caption.
    static = name == "studio_arrested" and frame >= 115
    if not static:
        big = fonts["title"]
        screen_text = big.render("FCB " + score + " BVB", False, WHITE)
        x, y = to_window(250, 56)
        window.blit(screen_text, (x - screen_text.get_width() // 2, y))
        # The show's name on the red banner.
        show = fonts["small"].render("INFANTINI'S VERDICT", False, WHITE)
        x, y = to_window(250, 105)
        window.blit(show, (x - show.get_width() // 2, y + 2))
        window.blit(fonts["small"].render("ON AIR", False, WHITE), to_window(364, 46))
    if name == "studio_arrested" and not static:
        left_x, right_x, away = police_positions(frame)
        police_word = fonts["small"].render("POLICE", False, (20, 30, 80))
        for x in [left_x, right_x]:
            word_x, word_y = to_window(x, FLOOR_Y - 76 + 45)
            window.blit(police_word, (word_x - police_word.get_width() // 2, word_y))
    if name == "studio_arrested" and 45 <= frame < 70:
        click = fonts["big"].render("CLICK!", False, (255, 235, 120))
        x, y = to_window(250, 70)
        window.blit(click, (x - click.get_width() // 2, y))
    if static:
        lost = fonts["big"].render("[SIGNAL LOST]", False, WHITE)
        x = window.get_width() // 2 - lost.get_width() // 2
        y = window.get_height() // 2 - lost.get_height() // 2
        pygame.draw.rect(window, (0, 0, 0), (x - 12, y - 6, lost.get_width() + 24, lost.get_height() + 12))
        window.blit(lost, (x, y))

    # The film bars and the caption.
    scale = 2
    width = window.get_width()
    height = window.get_height()
    bar = 16 * scale
    pygame.draw.rect(window, (0, 0, 0), (0, 0, width, bar))
    pygame.draw.rect(window, (0, 0, 0), (0, height - bar, width, bar))
    caption = fonts["text"].render(STUDIO_CAPTIONS[name], False, (255, 245, 220))
    window.blit(caption, (16 * scale, height - bar + (bar - caption.get_height()) // 2))
    skip = fonts["small"].render("SPACE: skip", False, (255, 170, 80))
    window.blit(skip, (width - skip.get_width() - 12 * scale, height - bar + (bar - skip.get_height()) // 2))
