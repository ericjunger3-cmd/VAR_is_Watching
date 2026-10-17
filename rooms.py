# Drawing the rooms of VAR Is Watching.
# Everything is drawn on a small 480 x 270 "canvas". The game scales the
# canvas up 2x afterwards, so every pixel here becomes a 2 x 2 block.

import math
import random
import pygame
from sprites import OUTLINE

CANVAS_WIDTH = 480
CANVAS_HEIGHT = 270

# The rooms are a bit wider than the window, so the view can slide
# after the player (camera follow).
ROOM_WIDTH = CANVAS_WIDTH + 20

# The y position of the floor: characters stand on this line.
FLOOR_Y = 200

# Colours used in the rooms, as (red, green, blue).
WHITE = (255, 255, 255)
BLACK = (30, 30, 40)
GRASS = (70, 180, 80)
GRASS_LIGHT = (95, 200, 100)
HOME_RED = (230, 60, 60)
AWAY_BLUE = (70, 110, 230)
SKIN = (250, 200, 160)
YELLOW = (250, 210, 60)
SKY = (150, 200, 240)
NOTE_YELLOW = (255, 225, 70)


# ---------------------------------------------------------------- shared parts

def bob(tick, phase):
    # Returns 0 or 1: characters move up by one pixel half of the time,
    # which looks like breathing. tick counts the frames; phase makes not
    # everybody breathe at the same moment.
    return ((tick + phase) // 20) % 2


def draw_wall(canvas):
    # Cream wallpaper with soft stripes and a darker strip at the top.
    canvas.fill((246, 224, 180))
    pygame.draw.rect(canvas, (232, 205, 160), (0, 0, ROOM_WIDTH, 10))
    pygame.draw.rect(canvas, OUTLINE, (0, 10, ROOM_WIDTH, 1))
    for x in range(0, ROOM_WIDTH, 24):
        pygame.draw.rect(canvas, (240, 216, 170), (x, 11, 12, 140))

    # Wood panelling on the lower part of the wall.
    pygame.draw.rect(canvas, OUTLINE, (0, 147, ROOM_WIDTH, 1))
    pygame.draw.rect(canvas, (140, 80, 40), (0, 148, ROOM_WIDTH, 3))
    pygame.draw.rect(canvas, (180, 110, 60), (0, 151, ROOM_WIDTH, 49))
    for x in range(0, ROOM_WIDTH, 20):
        pygame.draw.rect(canvas, (205, 135, 75), (x + 1, 152, 17, 46))   # plank
        pygame.draw.rect(canvas, (225, 160, 95), (x + 1, 152, 17, 2))    # light top
        pygame.draw.rect(canvas, (150, 88, 48), (x + 1, 196, 17, 2))     # dark bottom


def draw_floor(canvas):
    # A strip of grass on top of warm bricks, like in old 2D games.
    pygame.draw.rect(canvas, (95, 200, 80), (0, FLOOR_Y, ROOM_WIDTH, 6))
    for x in range(0, ROOM_WIDTH, 2):
        # Little grass blades of different heights (0, 1 or 2 pixels).
        blade = (x * 7) % 3
        pygame.draw.line(canvas, (95, 200, 80), (x, FLOOR_Y), (x, FLOOR_Y - 1 - blade))
        if x % 6 == 0:
            canvas.set_at((x, FLOOR_Y - 2 - blade), (160, 235, 120))
    pygame.draw.rect(canvas, (60, 150, 60), (0, FLOOR_Y + 5, ROOM_WIDTH, 2))

    # Bricks: every second row is shifted by half a brick.
    pygame.draw.rect(canvas, (165, 105, 70), (0, FLOOR_Y + 7, ROOM_WIDTH, 63))
    row = 0
    for y in range(FLOOR_Y + 7, CANVAS_HEIGHT, 12):
        if row % 2 == 0:
            shift = 0
        else:
            shift = 12
        for x in range(-24 + shift, ROOM_WIDTH, 24):
            pygame.draw.rect(canvas, (125, 75, 50), (x, y, 24, 12))      # gap
            pygame.draw.rect(canvas, (185, 122, 82), (x + 1, y + 1, 22, 10))
            pygame.draw.rect(canvas, (210, 150, 105), (x + 1, y + 1, 22, 2))
            pygame.draw.rect(canvas, (150, 95, 62), (x + 1, y + 9, 22, 2))
        row = row + 1


def draw_door(canvas, x, plaque_colour, plaque_shadow):
    # A wooden door, 40 wide and 72 high, standing on the floor,
    # with a coloured name plaque above it.
    y = FLOOR_Y - 72

    # Door frame.
    pygame.draw.rect(canvas, OUTLINE, (x - 4, y - 4, 48, 77))
    pygame.draw.rect(canvas, (120, 70, 40), (x - 3, y - 3, 46, 75))
    pygame.draw.rect(canvas, OUTLINE, (x - 1, y - 1, 42, 73))

    # The door itself: light left edge, dark right edge.
    pygame.draw.rect(canvas, (205, 130, 70), (x, y, 40, 72))
    pygame.draw.rect(canvas, (235, 165, 100), (x, y, 3, 72))
    pygame.draw.rect(canvas, (170, 100, 55), (x + 37, y, 3, 72))

    # Four panels.
    panels = [(6, 6, 26), (22, 6, 26), (6, 38, 28), (22, 38, 28)]
    for panel_x, panel_y, panel_height in panels:
        pygame.draw.rect(canvas, (170, 100, 55), (x + panel_x, y + panel_y, 12, panel_height))
        pygame.draw.rect(canvas, (190, 118, 65), (x + panel_x + 1, y + panel_y + 1, 10, panel_height - 2))

    # Golden door knob.
    pygame.draw.rect(canvas, OUTLINE, (x + 31, y + 36, 5, 5))
    pygame.draw.rect(canvas, (255, 215, 70), (x + 32, y + 37, 3, 3))

    # Name plaque (the text is added later, at full size).
    pygame.draw.rect(canvas, OUTLINE, (x - 2, y - 20, 44, 14))
    pygame.draw.rect(canvas, plaque_shadow, (x - 1, y - 19, 42, 12))
    pygame.draw.rect(canvas, plaque_colour, (x - 1, y - 19, 42, 10))


# ---------------------------------------------------------------- VAR Booth

def draw_window(canvas):
    # A big window with sky, clouds, the stands and the pitch behind it.
    x = 10
    y = 18
    width = 196
    height = 62

    # White window frame with an outline.
    pygame.draw.rect(canvas, OUTLINE, (x - 3, y - 3, width + 6, height + 6))
    pygame.draw.rect(canvas, WHITE, (x - 2, y - 2, width + 4, height + 4))

    # Sky in three shades of blue, darkest at the top.
    pygame.draw.rect(canvas, (110, 190, 250), (x, y, width, 10))
    pygame.draw.rect(canvas, (140, 210, 255), (x, y + 10, width, 10))
    pygame.draw.rect(canvas, (175, 225, 255), (x, y + 20, width, 16))

    draw_cloud(canvas, x + 20, y + 6)
    draw_cloud(canvas, x + 120, y + 3)
    draw_cloud(canvas, x + 170, y + 14)

    # The stands, full of fans. The colour of each fan comes from a
    # simple calculation, so the crowd looks mixed but never changes.
    pygame.draw.rect(canvas, (200, 70, 70), (x, y + 34, width, 16))
    fan_colours = [WHITE, YELLOW, (255, 120, 120), SKIN, AWAY_BLUE]
    for fan_y in range(y + 35, y + 49, 3):
        for fan_x in range(x + 1, x + width - 1, 3):
            colour = fan_colours[(fan_x * 3 + fan_y) % 5]
            pygame.draw.rect(canvas, colour, (fan_x, fan_y, 2, 1))

    # The pitch with light and dark mowing stripes.
    for i in range(0, width, 14):
        if (i // 14) % 2 == 0:
            colour = (80, 190, 80)
        else:
            colour = (100, 210, 95)
        pygame.draw.rect(canvas, colour, (x + i, y + 50, 14, 12))
    pygame.draw.line(canvas, WHITE, (x, y + 52), (x + width, y + 52))

    # Two window bars and a floodlight.
    pygame.draw.rect(canvas, WHITE, (x + width // 3, y, 3, height))
    pygame.draw.rect(canvas, WHITE, (x + 2 * width // 3, y, 3, height))
    pygame.draw.rect(canvas, (90, 90, 100), (x + 150, y + 2, 14, 6))
    pygame.draw.rect(canvas, (255, 250, 200), (x + 151, y + 3, 12, 4))


def draw_cloud(canvas, x, y):
    # A fluffy cloud made of four white circles with a light blue bottom.
    pygame.draw.circle(canvas, WHITE, (x, y + 6), 6)
    pygame.draw.circle(canvas, WHITE, (x + 7, y + 2), 8)
    pygame.draw.circle(canvas, WHITE, (x + 16, y + 5), 6)
    pygame.draw.circle(canvas, WHITE, (x + 22, y + 7), 4)
    pygame.draw.rect(canvas, (215, 235, 255), (x - 5, y + 9, 31, 3))


def draw_monitors(canvas):
    # Twelve monitors in two rows of six. Eleven show a camera angle,
    # the last one is broken and has Dave's sticky note on it.
    camera_number = 0
    for row in range(2):
        for column in range(6):
            x = 12 + column * 32
            y = 88 + row * 24

            # Monitor frame.
            pygame.draw.rect(canvas, OUTLINE, (x - 2, y - 2, 30, 22))
            pygame.draw.rect(canvas, (90, 95, 115), (x - 1, y - 1, 28, 20))

            if camera_number == 11:
                draw_broken_screen(canvas, x + 1, y + 1)
            else:
                draw_camera(canvas, camera_number, x + 1, y + 1)
            camera_number = camera_number + 1


def draw_broken_screen(canvas, x, y):
    # TV static: random grey dots, different every frame, so it flickers.
    pygame.draw.rect(canvas, (40, 40, 48), (x, y, 24, 16))
    for i in range(60):
        dot_x = x + random.randint(0, 23)
        dot_y = y + random.randint(0, 15)
        brightness = random.randint(80, 240)
        canvas.set_at((dot_x, dot_y), (brightness, brightness, brightness))

    # Dave's sticky note with two scribbled lines.
    pygame.draw.rect(canvas, OUTLINE, (x + 12, y, 11, 11))
    pygame.draw.rect(canvas, NOTE_YELLOW, (x + 13, y + 1, 9, 9))
    pygame.draw.rect(canvas, (230, 190, 40), (x + 13, y + 8, 9, 2))
    pygame.draw.line(canvas, (150, 110, 40), (x + 14, y + 3), (x + 20, y + 3))
    pygame.draw.line(canvas, (150, 110, 40), (x + 14, y + 5), (x + 18, y + 5))


def box(canvas, colour, x, y, width, height):
    # A shorter way to draw a filled rectangle. Used a lot by draw_camera.
    pygame.draw.rect(canvas, colour, (x, y, width, height))


def draw_camera(canvas, number, x, y):
    # Draw one camera angle on a 24 x 16 screen whose top-left corner is (x, y).
    # Every number shows a different shot of the match.

    if number == 0:
        # Main wide camera: mowing stripes, halfway line, players.
        for i in range(0, 24, 6):
            if (i // 6) % 2 == 0:
                box(canvas, GRASS, x + i, y, 6, 16)
            else:
                box(canvas, GRASS_LIGHT, x + i, y, 6, 16)
        box(canvas, WHITE, x + 12, y, 1, 16)
        box(canvas, HOME_RED, x + 5, y + 6, 1, 2)
        box(canvas, AWAY_BLUE, x + 9, y + 10, 1, 2)
        box(canvas, HOME_RED, x + 16, y + 5, 1, 2)
        box(canvas, AWAY_BLUE, x + 19, y + 11, 1, 2)
        box(canvas, WHITE, x + 13, y + 8, 1, 2)

    elif number == 1:
        # Spidercam from above: halfway line and centre circle.
        box(canvas, GRASS_LIGHT, x, y, 24, 16)
        box(canvas, WHITE, x, y + 8, 24, 1)
        pygame.draw.circle(canvas, WHITE, (x + 12, y + 8), 5, 1)
        canvas.set_at((x + 4, y + 3), HOME_RED)
        canvas.set_at((x + 18, y + 12), AWAY_BLUE)
        canvas.set_at((x + 9, y + 13), HOME_RED)

    elif number == 2:
        # Goal-line camera: the post, the net and the ball on the line.
        box(canvas, (200, 230, 255), x, y, 24, 10)
        box(canvas, GRASS, x, y + 10, 24, 6)
        for i in range(0, 10, 2):
            box(canvas, (210, 210, 220), x, y + i, 9, 1)
            box(canvas, (210, 210, 220), x + i, y, 1, 10)
        box(canvas, WHITE, x + 9, y, 2, 13)
        box(canvas, WHITE, x + 11, y + 12, 13, 1)
        box(canvas, WHITE, x + 14, y + 9, 3, 3)
        canvas.set_at((x + 15, y + 10), BLACK)

    elif number == 3:
        # Behind the goal: the keeper in yellow, seen through the net.
        box(canvas, GRASS_LIGHT, x, y, 24, 16)
        box(canvas, YELLOW, x + 10, y + 6, 4, 5)
        box(canvas, SKIN, x + 11, y + 3, 2, 3)
        box(canvas, YELLOW, x + 8, y + 6, 2, 2)
        box(canvas, YELLOW, x + 14, y + 6, 2, 2)
        for i in range(0, 24, 3):
            box(canvas, (235, 235, 245), x + i, y, 1, 16)
        for i in range(0, 16, 3):
            box(canvas, (235, 235, 245), x, y + i, 24, 1)

    elif number == 4:
        # Close-up of the home striker, number 9, smiling.
        box(canvas, (120, 90, 140), x, y, 24, 16)
        box(canvas, HOME_RED, x + 4, y + 10, 16, 6)
        box(canvas, SKIN, x + 8, y + 2, 8, 8)
        box(canvas, (90, 50, 30), x + 8, y + 1, 8, 2)
        canvas.set_at((x + 10, y + 5), BLACK)
        canvas.set_at((x + 13, y + 5), BLACK)
        box(canvas, WHITE, x + 10, y + 7, 4, 1)
        box(canvas, WHITE, x + 11, y + 11, 2, 1)
        box(canvas, WHITE, x + 12, y + 12, 1, 1)
        box(canvas, WHITE, x + 11, y + 13, 2, 1)

    elif number == 5:
        # The away captain screaming "OFFSIDE!" with his arm up.
        box(canvas, SKY, x, y, 24, 16)
        box(canvas, AWAY_BLUE, x + 3, y + 10, 18, 6)
        box(canvas, SKIN, x + 7, y + 2, 9, 8)
        box(canvas, BLACK, x + 7, y + 1, 9, 2)
        box(canvas, BLACK, x + 8, y + 3, 2, 1)
        box(canvas, BLACK, x + 13, y + 3, 2, 1)
        canvas.set_at((x + 9, y + 5), BLACK)
        canvas.set_at((x + 13, y + 5), BLACK)
        box(canvas, (120, 20, 30), x + 10, y + 6, 3, 3)
        box(canvas, SKIN, x + 19, y + 2, 2, 8)
        box(canvas, WHITE, x + 19, y, 2, 2)

    elif number == 6:
        # Crowd camera: lots of fans and a banner.
        box(canvas, (200, 70, 70), x, y, 24, 16)
        fan_colours = [WHITE, YELLOW, (255, 130, 130), SKIN, AWAY_BLUE]
        for fan_y in range(1, 12, 2):
            for fan_x in range((fan_y // 2) % 2, 24, 2):
                canvas.set_at((x + fan_x, y + fan_y), fan_colours[(fan_x * 3 + fan_y) % 5])
        box(canvas, WHITE, x + 2, y + 12, 20, 3)
        box(canvas, HOME_RED, x + 3, y + 13, 18, 1)

    elif number == 7:
        # The dugout: the manager with his hands on his head.
        box(canvas, (170, 175, 190), x, y, 24, 4)
        box(canvas, (90, 95, 110), x, y + 4, 24, 12)
        box(canvas, (40, 40, 50), x + 7, y + 8, 10, 8)
        box(canvas, SKIN, x + 9, y + 4, 6, 5)
        box(canvas, SKIN, x + 6, y + 3, 3, 2)
        box(canvas, SKIN, x + 15, y + 3, 3, 2)
        canvas.set_at((x + 10, y + 6), BLACK)
        canvas.set_at((x + 13, y + 6), BLACK)
        box(canvas, BLACK, x + 11, y + 8, 2, 1)

    elif number == 8:
        # Referee camera: hand on his earpiece, waiting for VAR.
        box(canvas, SKY, x, y, 24, 9)
        box(canvas, GRASS, x, y + 9, 24, 7)
        box(canvas, BLACK, x + 8, y + 8, 8, 8)
        box(canvas, SKIN, x + 9, y + 2, 6, 6)
        box(canvas, BLACK, x + 9, y + 1, 6, 2)
        box(canvas, SKIN, x + 16, y + 3, 2, 6)
        canvas.set_at((x + 10, y + 4), BLACK)
        canvas.set_at((x + 13, y + 4), BLACK)
        box(canvas, YELLOW, x + 15, y + 3, 1, 2)

    elif number == 9:
        # The linesman with his flag up.
        box(canvas, GRASS, x, y, 24, 16)
        box(canvas, WHITE, x, y + 13, 24, 1)
        box(canvas, YELLOW, x + 9, y + 6, 4, 6)
        box(canvas, SKIN, x + 9, y + 2, 4, 4)
        box(canvas, BLACK, x + 9, y + 12, 4, 2)
        box(canvas, SKIN, x + 13, y + 3, 1, 4)
        box(canvas, (210, 210, 210), x + 13, y, 1, 4)
        box(canvas, YELLOW, x + 14, y, 4, 3)
        box(canvas, HOME_RED, x + 14, y, 2, 1)
        box(canvas, HOME_RED, x + 16, y + 1, 2, 1)
        box(canvas, HOME_RED, x + 14, y + 2, 2, 1)

    elif number == 10:
        # Replay of the celebration, with a red "recording" light.
        box(canvas, GRASS_LIGHT, x, y, 24, 16)
        for player_x in [4, 10, 16]:
            box(canvas, HOME_RED, x + player_x, y + 8, 4, 6)
            box(canvas, SKIN, x + player_x + 1, y + 4, 2, 3)
            box(canvas, SKIN, x + player_x - 1, y + 3, 1, 4)
            box(canvas, SKIN, x + player_x + 4, y + 3, 1, 4)
        box(canvas, (230, 30, 30), x + 1, y + 1, 3, 3)


def draw_desk(canvas):
    # The wooden desk with drawers, a keyboard and a mug.
    pygame.draw.rect(canvas, OUTLINE, (4, 163, 206, 38))
    pygame.draw.rect(canvas, (215, 140, 70), (5, 164, 204, 6))     # desk top
    pygame.draw.rect(canvas, (245, 175, 100), (5, 164, 204, 2))    # light edge
    pygame.draw.rect(canvas, (170, 100, 50), (5, 170, 204, 30))    # front
    pygame.draw.rect(canvas, (140, 80, 40), (5, 196, 204, 4))      # dark bottom

    # Two drawers with handles.
    for drawer_x in [12, 150]:
        pygame.draw.rect(canvas, OUTLINE, (drawer_x, 174, 50, 22))
        pygame.draw.rect(canvas, (190, 115, 60), (drawer_x + 1, 175, 48, 20))
        pygame.draw.rect(canvas, OUTLINE, (drawer_x + 22, 183, 6, 2))

    # Keyboard with little keys.
    pygame.draw.rect(canvas, OUTLINE, (78, 158, 52, 7))
    pygame.draw.rect(canvas, (220, 222, 235), (79, 159, 50, 5))
    for key_x in range(81, 128, 4):
        canvas.set_at((key_x, 161), (150, 150, 170))

    # A white mug with a red stripe.
    pygame.draw.rect(canvas, OUTLINE, (150, 152, 11, 12))
    pygame.draw.rect(canvas, WHITE, (151, 153, 9, 10))
    pygame.draw.rect(canvas, (230, 70, 70), (151, 157, 9, 3))
    pygame.draw.rect(canvas, OUTLINE, (161, 155, 3, 5))


def draw_tunnel(canvas):
    # A stone archway to the pitch, with daylight at the end.
    x = 412
    pygame.draw.rect(canvas, OUTLINE, (x - 2, 128, 66, 73))
    pygame.draw.ellipse(canvas, OUTLINE, (x - 2, 110, 66, 40))
    pygame.draw.rect(canvas, (140, 140, 155), (x, 130, 62, 70))
    pygame.draw.ellipse(canvas, (140, 140, 155), (x, 112, 62, 36))

    # The dark inside of the tunnel.
    pygame.draw.rect(canvas, (55, 60, 80), (x + 6, 136, 50, 64))
    pygame.draw.ellipse(canvas, (55, 60, 80), (x + 6, 120, 50, 32))

    # Light at the end: sky and grass.
    pygame.draw.rect(canvas, (180, 225, 255), (x + 18, 150, 26, 10))
    pygame.draw.rect(canvas, (255, 250, 210), (x + 18, 160, 26, 16))
    pygame.draw.rect(canvas, (120, 210, 110), (x + 14, 176, 34, 24))


def draw_booth(canvas, pictures, progress, tick):
    # Draw the whole VAR Booth, from the back to the front.
    draw_wall(canvas)
    draw_window(canvas)
    draw_monitors(canvas)
    draw_desk(canvas)
    draw_door(canvas, 238, (250, 250, 250), (200, 200, 210))   # Referee's room
    draw_door(canvas, 296, (255, 210, 70), (215, 160, 40))     # Mascot room
    draw_door(canvas, 354, (110, 170, 255), (70, 120, 210))    # Press room
    draw_tunnel(canvas)
    draw_floor(canvas)

    # The yanked-out camera cable: a socket on the wall, the plug hanging down.
    pygame.draw.rect(canvas, OUTLINE, (17, 135, 10, 9))
    pygame.draw.rect(canvas, (235, 235, 240), (18, 136, 8, 7))
    canvas.set_at((20, 139), OUTLINE)
    canvas.set_at((23, 139), OUTLINE)
    pygame.draw.line(canvas, OUTLINE, (22, 144), (34, 156), 2)
    pygame.draw.rect(canvas, OUTLINE, (32, 155, 6, 6))
    pygame.draw.rect(canvas, (90, 90, 100), (33, 156, 4, 4))

    # The lanyard hangs over the back of the desk until you take it.
    if "lanyard" not in progress["inventory"]:
        pygame.draw.line(canvas, YELLOW, (24, 150), (28, 162), 2)
        pygame.draw.line(canvas, YELLOW, (36, 150), (32, 162), 2)
        pygame.draw.rect(canvas, OUTLINE, (25, 157, 11, 8))
        pygame.draw.rect(canvas, WHITE, (26, 158, 9, 6))
        pygame.draw.rect(canvas, (230, 60, 60), (26, 158, 9, 2))

    # The padlock hangs on the Mascot door until you have the whistle.
    if "whistle" not in progress["inventory"]:
        canvas.blit(pictures["padlock"], (310, 152))

    # The steward stands next to the tunnel to the pitch.
    steward = pictures["steward"]
    canvas.blit(steward, (452, FLOOR_Y - steward.get_height() - bob(tick, 7)))




# ---------------------------------------------------------------- helpers for the rooms

def outlined_box(canvas, colour, x, y, width, height):
    # A filled rectangle with a 1-pixel dark outline around it.
    pygame.draw.rect(canvas, OUTLINE, (x - 1, y - 1, width + 2, height + 2))
    pygame.draw.rect(canvas, colour, (x, y, width, height))


def shaded_box(canvas, colour, light, dark, x, y, width, height):
    # An outlined rectangle with a light top and left edge and a dark
    # bottom and right edge, so it looks a little bit 3D.
    outlined_box(canvas, colour, x, y, width, height)
    pygame.draw.rect(canvas, light, (x, y, width, 2))
    pygame.draw.rect(canvas, light, (x, y, 2, height))
    pygame.draw.rect(canvas, dark, (x, y + height - 2, width, 2))
    pygame.draw.rect(canvas, dark, (x + width - 2, y, 2, height))


def darker(colour, amount):
    # The same colour, but darker: every part (red, green, blue) is
    # multiplied by amount (e.g. 0.7 keeps 70 %). Used for shadows.
    return (int(colour[0] * amount), int(colour[1] * amount), int(colour[2] * amount))


def draw_bands(canvas, colours, x, y, width, height):
    # A "pixel art gradient": the area is cut into horizontal bands,
    # one band per colour, from the top to the bottom. Real gradients are
    # too smooth for pixel art; a few clear steps look better.
    band_height = height // len(colours)
    for i in range(len(colours)):
        top = y + i * band_height
        # The last band goes all the way down (in case it does not divide evenly).
        if i == len(colours) - 1:
            band_height = y + height - top
        pygame.draw.rect(canvas, colours[i], (x, top, width, band_height))


def draw_shadow(canvas, x, y, width):
    # A soft dark oval on the floor under a person or a piece of furniture.
    # It is see-through (alpha 70), so the floor pattern still shows.
    shadow = pygame.Surface((width, 6), pygame.SRCALPHA)
    pygame.draw.ellipse(shadow, (0, 0, 20, 70), (0, 0, width, 6))
    canvas.blit(shadow, (x, y - 3))


def draw_light_cone(canvas, x, top, bottom, top_width, bottom_width):
    # The light of a spotlight: a see-through shape that gets wider towards
    # the bottom. Two layers (a wide weak one and a narrow stronger one)
    # make the middle brighter, like real light.
    height = bottom - top
    cone = pygame.Surface((bottom_width, height), pygame.SRCALPHA)
    middle = bottom_width // 2
    pygame.draw.polygon(cone, (255, 245, 200, 22), [
        (middle - top_width // 2, 0), (middle + top_width // 2, 0),
        (bottom_width, height), (0, height)])
    pygame.draw.polygon(cone, (255, 245, 200, 26), [
        (middle - top_width // 4, 0), (middle + top_width // 4, 0),
        (middle + bottom_width // 4, height), (middle - bottom_width // 4, height)])
    canvas.blit(cone, (x - middle, top))


def draw_ceiling_lamps(canvas, lamp_positions):
    # Lamps hanging from the ceiling, each with a soft cone of light.
    # The light cone is see-through: the 4th colour number (45) is the
    # transparency, from 0 (invisible) to 255 (solid).
    for x in lamp_positions:
        pygame.draw.rect(canvas, OUTLINE, (x + 7, 0, 2, 8))
        pygame.draw.rect(canvas, OUTLINE, (x - 1, 7, 18, 7))
        pygame.draw.rect(canvas, (90, 90, 100), (x, 8, 16, 3))
        pygame.draw.rect(canvas, (255, 250, 215), (x + 1, 11, 14, 2))
        light_cone = pygame.Surface((40, 30), pygame.SRCALPHA)
        pygame.draw.polygon(light_cone, (255, 250, 210, 45), [(13, 0), (27, 0), (40, 30), (0, 30)])
        canvas.blit(light_cone, (x - 12, 13))


def draw_feather(canvas, x, y):
    # A small grey feather (two light lines with a dark outline line).
    pygame.draw.line(canvas, OUTLINE, (x, y + 1), (x + 6, y - 2))
    pygame.draw.line(canvas, (220, 225, 235), (x + 1, y), (x + 6, y - 3))
    pygame.draw.line(canvas, (220, 225, 235), (x + 1, y - 1), (x + 5, y - 3))


# ---------------------------------------------------------------- floors

def draw_carpet(canvas, colour, light, dark):
    # A wooden skirting board and a carpet with a dotted pattern.
    pygame.draw.rect(canvas, OUTLINE, (0, FLOOR_Y - 1, ROOM_WIDTH, 1))
    pygame.draw.rect(canvas, (150, 95, 55), (0, FLOOR_Y, ROOM_WIDTH, 4))
    pygame.draw.rect(canvas, (190, 130, 80), (0, FLOOR_Y, ROOM_WIDTH, 1))
    pygame.draw.rect(canvas, colour, (0, FLOOR_Y + 4, ROOM_WIDTH, CANVAS_HEIGHT - FLOOR_Y))
    pygame.draw.rect(canvas, dark, (0, FLOOR_Y + 4, ROOM_WIDTH, 2))
    for y in range(FLOOR_Y + 10, CANVAS_HEIGHT, 8):
        for x in range(4 + (y // 8) % 2 * 4, ROOM_WIDTH, 8):
            canvas.set_at((x, y), light)


# ---------------------------------------------------------------- Referee's Dressing Room

def draw_tile_floor(canvas, tick):
    # Wet white floor tiles. Every row is a bit taller (and the tiles a bit
    # wider) than the row behind it: things close to you look bigger, so
    # the floor seems to go into the screen. The front rows are lighter.
    pygame.draw.rect(canvas, OUTLINE, (0, FLOOR_Y - 1, ROOM_WIDTH, 1))
    y = FLOOR_Y
    height = 5
    row = 0
    while y < CANVAS_HEIGHT:
        width = height * 3
        # The colour gets lighter row by row (row * 7 more of each colour).
        tile = (165 + row * 7, 178 + row * 7, 195 + row * 6)
        grout = darker(tile, 0.75)
        pygame.draw.rect(canvas, grout, (0, y, ROOM_WIDTH, height))
        shift = (row % 2) * (width // 2)
        for x in range(-width + shift, ROOM_WIDTH, width):
            pygame.draw.rect(canvas, tile, (x + 1, y + 1, width - 1, height - 1))
            pygame.draw.rect(canvas, (240, 245, 250), (x + 1, y + 1, width - 1, 1))   # shine
        y = y + height
        height = height + 1
        row = row + 1

    # The puddle by the shower, with a white shine and a ripple that
    # grows (a drop falls in) and starts again: % 16 counts 0 ... 15.
    pygame.draw.ellipse(canvas, (120, 185, 230), (405, FLOOR_Y + 4, 60, 11))
    pygame.draw.ellipse(canvas, (150, 210, 245), (408, FLOOR_Y + 5, 54, 8))
    pygame.draw.line(canvas, WHITE, (415, FLOOR_Y + 7), (430, FLOOR_Y + 7))
    ripple = (tick // 3) % 16
    if ripple > 2:
        pygame.draw.ellipse(canvas, (220, 240, 255), (440 - ripple, FLOOR_Y + 9 - ripple // 4, ripple * 2, ripple // 2 + 2), 1)

    # The drain of the shower.
    pygame.draw.ellipse(canvas, OUTLINE, (432, FLOOR_Y + 1, 16, 5))
    pygame.draw.ellipse(canvas, (120, 125, 140), (433, FLOOR_Y + 2, 14, 3))


def draw_wall_tiles(canvas, top, bottom, tile, light, dark):
    # Square wall tiles (14 x 14) with dark grout lines between them.
    # Every tile has a light top and left edge and a dark bottom and
    # right edge, so it looks like it sticks out a tiny bit.
    pygame.draw.rect(canvas, darker(tile, 0.72), (0, top, ROOM_WIDTH, bottom - top))
    for y in range(top, bottom, 14):
        for x in range(0, ROOM_WIDTH, 14):
            pygame.draw.rect(canvas, tile, (x + 1, y + 1, 13, 13))
            pygame.draw.rect(canvas, light, (x + 1, y + 1, 13, 1))
            pygame.draw.rect(canvas, light, (x + 1, y + 1, 1, 13))
            pygame.draw.rect(canvas, dark, (x + 1, y + 13, 13, 1))
            pygame.draw.rect(canvas, dark, (x + 13, y + 1, 1, 13))


def draw_dark_band(canvas, y, height, alpha):
    # A see-through dark stripe across the whole room. Used near the
    # ceiling and just above the floor, where less light reaches.
    band = pygame.Surface((ROOM_WIDTH, height), pygame.SRCALPHA)
    band.fill((10, 20, 40, alpha))
    canvas.blit(band, (0, y))


def draw_dressing_room(canvas, pictures, progress, tick):
    # Tiled walls: light tiles on top, darker tiles below, a white strip between.
    draw_wall_tiles(canvas, 0, 117, (175, 225, 235), (215, 244, 250), (145, 200, 215))
    draw_wall_tiles(canvas, 121, FLOOR_Y, (95, 165, 185), (130, 192, 208), (75, 140, 160))
    pygame.draw.rect(canvas, (235, 245, 250), (0, 117, ROOM_WIDTH, 2))
    pygame.draw.rect(canvas, OUTLINE, (0, 119, ROOM_WIDTH, 2))
    # Less light near the ceiling and near the floor (two steps each).
    draw_dark_band(canvas, 7, 12, 45)
    draw_dark_band(canvas, 7, 6, 35)
    draw_dark_band(canvas, 180, 20, 30)
    draw_dark_band(canvas, 192, 8, 35)
    # The ceiling.
    pygame.draw.rect(canvas, (215, 225, 235), (0, 0, ROOM_WIDTH, 6))
    pygame.draw.rect(canvas, OUTLINE, (0, 6, ROOM_WIDTH, 1))
    draw_ceiling_lamps(canvas, [90, 230, 370])

    draw_door(canvas, 20, (250, 250, 250), (200, 200, 210))     # back to the booth
    draw_wall_clock(canvas, tick)

    # The tactics whiteboard with crosses, circles and arrows.
    shaded_box(canvas, (250, 252, 255), WHITE, (215, 220, 230), 120, 28, 70, 46)
    pygame.draw.rect(canvas, (170, 175, 190), (118, 74, 74, 3))
    pygame.draw.rect(canvas, (120, 125, 140), (118, 76, 74, 1))
    for x, y in [(132, 40), (150, 58), (170, 44)]:
        pygame.draw.line(canvas, HOME_RED, (x - 3, y - 3), (x + 3, y + 3))
        pygame.draw.line(canvas, HOME_RED, (x - 3, y + 3), (x + 3, y - 3))
    for x, y in [(140, 62), (162, 36), (178, 60)]:
        pygame.draw.circle(canvas, AWAY_BLUE, (x, y), 3, 1)
    pygame.draw.line(canvas, BLACK, (134, 44), (148, 55))
    pygame.draw.line(canvas, BLACK, (152, 56), (168, 47))
    pygame.draw.rect(canvas, HOME_RED, (176, 72, 6, 2))          # markers
    pygame.draw.rect(canvas, BLACK, (184, 72, 6, 2))

    # Coat hooks with the referee's jacket and a towel.
    pygame.draw.rect(canvas, OUTLINE, (205, 30, 60, 4))
    pygame.draw.rect(canvas, (200, 160, 110), (205, 30, 60, 3))
    pygame.draw.rect(canvas, (230, 195, 145), (205, 30, 60, 1))
    for hook_x in [212, 232, 252]:
        pygame.draw.rect(canvas, OUTLINE, (hook_x, 34, 2, 4))
    pygame.draw.polygon(canvas, OUTLINE, [(205, 37), (221, 37), (224, 78), (202, 78)])
    pygame.draw.polygon(canvas, (30, 30, 45), [(206, 38), (220, 38), (223, 77), (203, 77)])
    pygame.draw.polygon(canvas, (50, 50, 68), [(206, 38), (210, 38), (208, 77), (203, 77)])  # light side
    pygame.draw.rect(canvas, YELLOW, (212, 40, 2, 30))
    outlined_box(canvas, (240, 120, 120), 246, 38, 12, 30)
    pygame.draw.rect(canvas, (255, 160, 160), (246, 38, 3, 30))
    pygame.draw.rect(canvas, (200, 90, 90), (255, 38, 3, 30))
    pygame.draw.rect(canvas, WHITE, (246, 46, 12, 2))
    pygame.draw.rect(canvas, WHITE, (246, 58, 12, 2))

    # The poster "TRUST THE PROCESS" with a referee silhouette.
    shaded_box(canvas, (255, 250, 235), WHITE, (220, 210, 190), 290, 26, 62, 56)
    pygame.draw.rect(canvas, HOME_RED, (290, 26, 62, 6))
    pygame.draw.circle(canvas, BLACK, (321, 68), 6)
    pygame.draw.rect(canvas, BLACK, (314, 74, 14, 6))
    pygame.draw.polygon(canvas, (215, 205, 185), [(346, 26), (352, 26), (352, 32)])   # bent corner

    draw_lockers(canvas)

    # The bench with a folded towel, a water bottle and the half-eaten orange.
    draw_shadow(canvas, 136, 201, 158)
    shaded_box(canvas, (215, 150, 80), (245, 185, 110), (170, 110, 60), 140, 172, 150, 7)
    for leg_x in [148, 278]:
        shaded_box(canvas, (160, 100, 55), (190, 125, 75), (120, 75, 40), leg_x, 180, 5, 19)
    outlined_box(canvas, WHITE, 160, 164, 22, 8)
    pygame.draw.rect(canvas, (120, 200, 230), (160, 167, 22, 2))
    pygame.draw.rect(canvas, (215, 225, 235), (160, 170, 22, 2))
    outlined_box(canvas, (100, 180, 240), 200, 154, 7, 18)
    pygame.draw.rect(canvas, (180, 225, 255), (201, 156, 1, 14))               # shine
    pygame.draw.rect(canvas, HOME_RED, (200, 152, 7, 3))
    pygame.draw.circle(canvas, OUTLINE, (255, 168), 6)
    pygame.draw.circle(canvas, (250, 150, 40), (255, 168), 5)
    pygame.draw.circle(canvas, (255, 190, 90), (254, 167), 2)
    pygame.draw.rect(canvas, (255, 230, 170), (250, 162, 5, 6))                # the bite
    pygame.draw.rect(canvas, (250, 150, 40), (266, 169, 4, 2))                 # peel
    pygame.draw.rect(canvas, (250, 150, 40), (240, 170, 3, 2))

    draw_shadow(canvas, 296, 201, 52)
    draw_kit_cabinet(canvas, pictures, progress)

    # Under the bench: muddy boots and a kit bag.
    for boot_x in [175, 191]:
        draw_shadow(canvas, boot_x - 1, 201, 16)
        outlined_box(canvas, (40, 40, 45), boot_x, 191, 13, 9)
        pygame.draw.rect(canvas, (70, 70, 80), (boot_x, 191, 13, 1))
        pygame.draw.rect(canvas, (120, 80, 50), (boot_x, 196, 13, 4))         # mud
    draw_shadow(canvas, 212, 201, 46)
    outlined_box(canvas, (30, 30, 45), 215, 184, 40, 16)
    pygame.draw.rect(canvas, (55, 55, 75), (215, 184, 40, 2))
    pygame.draw.rect(canvas, HOME_RED, (215, 189, 40, 3))
    pygame.draw.rect(canvas, OUTLINE, (228, 180, 14, 4))

    # A bin with paper cups, and a net bag full of footballs.
    draw_shadow(canvas, 347, 201, 24)
    shaded_box(canvas, (120, 130, 150), (155, 165, 185), (90, 98, 115), 350, 180, 18, 20)
    outlined_box(canvas, WHITE, 352, 175, 5, 6)
    outlined_box(canvas, WHITE, 360, 177, 5, 4)
    draw_ball_bag(canvas)

    draw_shower(canvas, tick)

    # The lamps shine down into the room.
    for lamp_x in [90, 230, 370]:
        draw_light_cone(canvas, lamp_x + 8, 13, FLOOR_Y, 14, 80)

    draw_tile_floor(canvas, tick)


# Where the dressing room clock hangs (its middle).
WALL_CLOCK_X = 92
WALL_CLOCK_Y = 82


def draw_wall_clock(canvas, tick):
    # A wall clock: it is very late in the match. The red second hand
    # ticks once per second (every 30 frames) and goes round in a minute.
    pygame.draw.circle(canvas, OUTLINE, (WALL_CLOCK_X, WALL_CLOCK_Y), 13)
    pygame.draw.circle(canvas, WHITE, (WALL_CLOCK_X, WALL_CLOCK_Y), 12)
    pygame.draw.circle(canvas, (225, 230, 240), (WALL_CLOCK_X + 1, WALL_CLOCK_Y + 1), 10)
    pygame.draw.circle(canvas, WHITE, (WALL_CLOCK_X, WALL_CLOCK_Y), 9)
    pygame.draw.circle(canvas, HOME_RED, (WALL_CLOCK_X, WALL_CLOCK_Y), 12, 2)
    for mark_x, mark_y in [(WALL_CLOCK_X, WALL_CLOCK_Y - 10), (WALL_CLOCK_X + 10, WALL_CLOCK_Y), (WALL_CLOCK_X, WALL_CLOCK_Y + 10), (WALL_CLOCK_X - 10, WALL_CLOCK_Y)]:
        canvas.set_at((mark_x, mark_y), OUTLINE)
    pygame.draw.line(canvas, OUTLINE, (WALL_CLOCK_X, WALL_CLOCK_Y), (WALL_CLOCK_X, WALL_CLOCK_Y - 8), 2)
    pygame.draw.line(canvas, OUTLINE, (WALL_CLOCK_X, WALL_CLOCK_Y), (WALL_CLOCK_X + 6, WALL_CLOCK_Y + 2), 2)
    # The second hand: an angle from the seconds, then sin and cos turn the
    # angle into an end point (6 degrees per second, 0 = straight up).
    seconds = (tick // 30) % 60
    angle = math.radians(seconds * 6)
    end_x = WALL_CLOCK_X + round(9 * math.sin(angle))
    end_y = WALL_CLOCK_Y - round(9 * math.cos(angle))
    pygame.draw.line(canvas, HOME_RED, (WALL_CLOCK_X, WALL_CLOCK_Y), (end_x, end_y))
    pygame.draw.rect(canvas, OUTLINE, (WALL_CLOCK_X - 1, WALL_CLOCK_Y - 1, 2, 2))


def draw_lockers(canvas):
    # Six lockers. Number 3 is open, with a referee shirt and shin pads inside.
    y = FLOOR_Y - 78
    # A dark top on the lockers, and a shadow on the wall above them.
    draw_shadow(canvas, 110, y - 2, 192)
    for i in range(6):
        x = 116 + i * 30
        if i == 3:
            draw_open_locker(canvas, x, y)
        else:
            shaded_box(canvas, (90, 140, 210), (130, 175, 235), (60, 100, 170), x, y, 28, 78)
            # Vents: a dark slot with a light line below it (it looks cut in).
            for vent_y in range(y + 6, y + 20, 4):
                pygame.draw.rect(canvas, (45, 75, 135), (x + 7, vent_y, 14, 2))
                pygame.draw.rect(canvas, (125, 170, 230), (x + 7, vent_y + 2, 14, 1))
            pygame.draw.rect(canvas, OUTLINE, (x + 20, y + 36, 3, 10))       # handle
            pygame.draw.rect(canvas, (200, 205, 220), (x + 20, y + 36, 1, 10))
            pygame.draw.rect(canvas, WHITE, (x + 6, y + 24, 16, 6))          # name tag
            pygame.draw.rect(canvas, (150, 150, 170), (x + 8, y + 26, 10, 1))
            # A thin shine line across the metal door.
            pygame.draw.line(canvas, (125, 170, 232), (x + 5, y + 70), (x + 14, y + 52))
        if i == 1:
            pygame.draw.circle(canvas, OUTLINE, (x + 10, y + 55), 5)         # sticker
            pygame.draw.circle(canvas, YELLOW, (x + 10, y + 55), 4)
        if i == 4:
            outlined_box(canvas, HOME_RED, x + 6, y + 50, 8, 6)               # sticker
        if i == 5:
            # A small padlock on the handle.
            pygame.draw.circle(canvas, OUTLINE, (x + 21, y + 47), 3, 1)
            outlined_box(canvas, (220, 180, 60), x + 18, y + 48, 7, 6)
            canvas.set_at((x + 21, y + 50), OUTLINE)
    # The base under the lockers, and dark gaps between the doors.
    outlined_box(canvas, (40, 60, 110), 115, FLOOR_Y - 5, 181, 5)
    for i in range(1, 6):
        pygame.draw.rect(canvas, OUTLINE, (116 + i * 30 - 2, y, 2, 78))


def draw_ball_bag(canvas):
    # A net bag with three footballs, standing on the floor.
    draw_shadow(canvas, 370, 201, 22)
    for ball_x, ball_y in [(376, 194), (386, 194), (381, 186)]:
        pygame.draw.circle(canvas, OUTLINE, (ball_x, ball_y), 6)
        pygame.draw.circle(canvas, (230, 235, 245), (ball_x, ball_y), 5)
        pygame.draw.circle(canvas, WHITE, (ball_x - 1, ball_y - 1), 3)
        pygame.draw.rect(canvas, OUTLINE, (ball_x - 1, ball_y - 1, 2, 2))
    # The net: thin lines over the balls.
    for net_x in range(371, 393, 4):
        pygame.draw.line(canvas, (90, 95, 110), (net_x, 182), (net_x + 2, 200))
    pygame.draw.line(canvas, (90, 95, 110), (372, 190), (391, 190))
    pygame.draw.rect(canvas, HOME_RED, (378, 178, 6, 3))                       # the knot


def draw_open_locker(canvas, x, y):
    # An open locker: dark inside, a hanging referee shirt, yellow shin pads,
    # and the door sticking out to the right.
    outlined_box(canvas, (40, 50, 80), x, y, 28, 78)
    pygame.draw.rect(canvas, (28, 35, 60), (x, y, 28, 6))                      # dark top inside
    pygame.draw.rect(canvas, (60, 75, 110), (x + 2, y + 2, 24, 3))             # shelf
    pygame.draw.rect(canvas, OUTLINE, (x + 12, y + 8, 4, 3))                   # hanger
    pygame.draw.rect(canvas, OUTLINE, (x + 4, y + 11, 20, 30))
    pygame.draw.rect(canvas, (30, 30, 42), (x + 5, y + 12, 18, 28))
    pygame.draw.rect(canvas, (48, 48, 64), (x + 5, y + 12, 4, 28))
    pygame.draw.rect(canvas, WHITE, (x + 11, y + 12, 6, 2))
    outlined_box(canvas, YELLOW, x + 6, y + 56, 6, 12)
    outlined_box(canvas, YELLOW, x + 15, y + 56, 6, 12)
    pygame.draw.rect(canvas, (255, 240, 150), (x + 6, y + 56, 2, 12))
    pygame.draw.rect(canvas, (255, 240, 150), (x + 15, y + 56, 2, 12))
    pygame.draw.polygon(canvas, OUTLINE, [(x + 28, y - 1), (x + 40, y + 4), (x + 40, y + 74), (x + 28, y + 79)])
    pygame.draw.polygon(canvas, (110, 160, 225), [(x + 29, y + 1), (x + 39, y + 5), (x + 39, y + 73), (x + 29, y + 77)])
    pygame.draw.polygon(canvas, (140, 185, 240), [(x + 29, y + 1), (x + 32, y + 2), (x + 32, y + 76), (x + 29, y + 77)])


def draw_kit_cabinet(canvas, pictures, progress):
    # A small wooden cabinet with a drawer. Once the drawer is opened it
    # sticks out, and the Lucky Whistle lies in it until you take it.
    shaded_box(canvas, (190, 125, 70), (225, 160, 100), (150, 95, 55), 300, 160, 44, 40)
    if "drawer" in progress["choices"]:
        # The open drawer: the dark inside and the front pulled down a bit.
        outlined_box(canvas, (60, 40, 30), 303, 164, 38, 10)
        if "whistle" not in progress["inventory"]:
            canvas.blit(pictures["whistle"], (306, 162))
        shaded_box(canvas, (210, 145, 85), (240, 180, 120), (165, 105, 60), 302, 174, 40, 12)
        pygame.draw.rect(canvas, OUTLINE, (318, 179, 8, 2))
    else:
        # The closed drawer with its handle.
        shaded_box(canvas, (210, 145, 85), (240, 180, 120), (165, 105, 60), 304, 166, 36, 12)
        pygame.draw.rect(canvas, OUTLINE, (318, 171, 8, 2))
    # A second, closed drawer below.
    shaded_box(canvas, (210, 145, 85), (240, 180, 120), (165, 105, 60), 304, 186, 36, 11)


def draw_shower(canvas, tick):
    # The shower corner: tiles, a striped curtain, falling water and steam.
    outlined_box(canvas, (150, 200, 215), 392, 22, 84, 178)
    for y in range(22, 200, 12):
        for x in range(392, 476, 12):
            pygame.draw.rect(canvas, (170, 215, 230), (x + 1, y + 1, 11, 11))
            pygame.draw.rect(canvas, (200, 235, 245), (x + 1, y + 1, 11, 1))
            pygame.draw.rect(canvas, (150, 195, 212), (x + 1, y + 11, 11, 1))
    # The curtain rail with rings, and the curtain with folds: every stripe
    # has a light left edge and a dark right edge, and the stripes end at
    # different heights, so the bottom looks wavy.
    pygame.draw.rect(canvas, OUTLINE, (392, 26, 84, 2))
    pygame.draw.rect(canvas, (200, 205, 215), (392, 26, 84, 1))
    for i in range(6):
        if i % 2 == 0:
            stripe, light, dark = WHITE, WHITE, (215, 220, 230)
        else:
            stripe, light, dark = (240, 120, 120), (255, 160, 160), (200, 90, 90)
        length = 150 + (i % 2) * 2
        pygame.draw.rect(canvas, stripe, (393 + i * 5, 28, 5, length))
        pygame.draw.rect(canvas, light, (393 + i * 5, 28, 1, length))
        pygame.draw.rect(canvas, dark, (397 + i * 5, 28, 1, length))
        pygame.draw.circle(canvas, OUTLINE, (395 + i * 5, 27), 2, 1)          # ring
    pygame.draw.rect(canvas, OUTLINE, (423, 28, 1, 152))
    # The shower head and its pipe.
    pygame.draw.rect(canvas, OUTLINE, (464, 22, 3, 14))
    pygame.draw.rect(canvas, (200, 205, 215), (465, 22, 1, 13))
    outlined_box(canvas, (200, 205, 215), 448, 34, 18, 5)
    pygame.draw.rect(canvas, (235, 240, 248), (448, 34, 18, 1))
    # Falling water: every drop moves down 4 pixels per frame and starts
    # again at the top. % 150 keeps the drop between the head and the floor.
    for drop_x, offset in [(450, 0), (454, 40), (458, 85), (462, 20), (452, 110), (460, 60)]:
        drop_y = 40 + (tick * 4 + offset) % 150
        pygame.draw.rect(canvas, (90, 160, 230), (drop_x, drop_y, 1, 4))
        pygame.draw.rect(canvas, (180, 220, 250), (drop_x, drop_y, 1, 1))

    # See-through steam clouds (transparency 120 out of 255). Each cloud
    # slowly rises 60 pixels and then starts again at the bottom:
    # % 60 makes the number go 0, 1, 2 ... 59, 0, 1, 2 ...
    steam = pygame.Surface((ROOM_WIDTH, CANVAS_HEIGHT), pygame.SRCALPHA)
    clouds = [(430, 110, 14, 0), (455, 110, 12, 20), (470, 120, 10, 40), (440, 125, 13, 10), (405, 115, 9, 30)]
    for steam_x, start_y, size, offset in clouds:
        rise = (tick // 3 + offset) % 60
        pygame.draw.circle(steam, (255, 255, 255, 120), (steam_x, start_y - rise), size)
    canvas.blit(steam, (0, 0))


# ---------------------------------------------------------------- Mascot Changing Room

def draw_mascot_room(canvas, pictures, progress, tick, reveal):
    # Purple striped wallpaper with darker wooden panels below.
    canvas.fill((215, 180, 230))
    for x in range(0, ROOM_WIDTH, 24):
        pygame.draw.rect(canvas, (205, 168, 222), (x, 0, 12, FLOOR_Y))
    pygame.draw.rect(canvas, OUTLINE, (0, 139, ROOM_WIDTH, 1))
    pygame.draw.rect(canvas, (150, 100, 170), (0, 140, ROOM_WIDTH, 60))
    for x in range(0, ROOM_WIDTH, 20):
        pygame.draw.rect(canvas, (170, 120, 190), (x + 1, 142, 17, 56))
        pygame.draw.rect(canvas, (190, 145, 210), (x + 1, 142, 17, 2))
    draw_ceiling_lamps(canvas, [120, 330])

    draw_door(canvas, 20, (255, 210, 70), (215, 160, 40))       # back to the booth

    # Framed "Employee of the Month" photo of Pombo.
    shaded_box(canvas, (250, 215, 90), (255, 240, 150), (200, 160, 40), 82, 30, 40, 46)
    pygame.draw.rect(canvas, (150, 200, 240), (87, 35, 30, 30))
    pygame.draw.circle(canvas, (155, 160, 182), (102, 52), 9)
    pygame.draw.circle(canvas, (200, 205, 220), (102, 58), 7)
    pygame.draw.rect(canvas, (250, 165, 60), (100, 51, 4, 3))
    pygame.draw.rect(canvas, OUTLINE, (98, 48, 2, 2))
    pygame.draw.rect(canvas, OUTLINE, (105, 48, 2, 2))
    pygame.draw.rect(canvas, HOME_RED, (87, 67, 30, 5))

    draw_mascot_heads(canvas)
    draw_costume_rack(canvas)
    draw_ring_light(canvas)
    draw_mirror_table(canvas)

    # A bag of bird seed and a laundry basket full of feathers.
    outlined_box(canvas, (220, 190, 140), 456, 168, 24, 32)
    pygame.draw.rect(canvas, (190, 155, 100), (456, 168, 24, 4))
    outlined_box(canvas, (200, 140, 80), 92, 180, 30, 20)
    for i in range(0, 30, 4):
        pygame.draw.rect(canvas, (170, 110, 55), (92 + i, 181, 2, 19))
    for feather_x in [96, 104, 112, 118]:
        pygame.draw.circle(canvas, OUTLINE, (feather_x, 179), 4)
        pygame.draw.circle(canvas, (200, 205, 220), (feather_x, 179), 3)

    # Pombo's bench, and Pombo himself.
    shaded_box(canvas, (215, 150, 80), (245, 185, 110), (170, 110, 60), 336, 178, 116, 6)
    for leg_x in [342, 442]:
        outlined_box(canvas, (160, 100, 55), leg_x, 185, 5, 15)
    draw_pombo(canvas, pictures, progress, tick, reveal)

    draw_carpet(canvas, (130, 70, 150), (160, 100, 180), (100, 50, 120))

    # Feathers on the floor.
    for feather_x, feather_y in [(90, FLOOR_Y + 8), (165, FLOOR_Y + 14), (262, FLOOR_Y + 9),
                                 (325, FLOOR_Y + 20), (455, FLOOR_Y + 12)]:
        draw_feather(canvas, feather_x, feather_y)

    # Feathers slowly falling through the air, swaying left and right.
    # When a feather reaches the floor it starts again at the top.
    for start_x, offset in [(270, 0), (420, 60), (190, 120), (110, 30)]:
        fall = (tick // 2 + offset) % 180
        sway = ((tick // 15 + offset) % 3) - 1
        draw_feather(canvas, start_x + sway * 2, 15 + fall)


def draw_pombo(canvas, pictures, progress, tick, reveal):
    # Pombo on his bench. Before you talk to him he is the pigeon mascot.
    # After that he is Dave: his own head on the pigeon body, and the
    # pigeon head (the mask) lies on the bench next to him.
    breathe = bob(tick, 0)
    if "dave" not in progress["choices"]:
        pombo = pictures["pombo"]
        canvas.blit(pombo, (362, FLOOR_Y - pombo.get_height() - breathe))
        return

    body = pictures["pombo_body"]
    body_y = FLOOR_Y - body.get_height() - breathe
    canvas.blit(body, (362, body_y))
    dave = pictures["dave_head"]
    canvas.blit(dave, (362 + (body.get_width() - dave.get_width()) // 2, body_y - dave.get_height() + 4))

    # Where the mask is: during the reveal it moves in three parts
    # (lift it up, move it to the right, put it down), afterwards it lies
    # on the bench. reveal is None when there is no reveal going on.
    mask = pictures["pombo_head"]
    start_x = 362
    start_y = body_y - mask.get_height() + 2
    end_x = 406
    end_y = 178 - mask.get_height()
    top_y = start_y - 12
    if reveal is None or reveal >= 55:
        mask_x = end_x
        mask_y = end_y
    elif reveal < 15:
        mask_x = start_x
        mask_y = start_y + (top_y - start_y) * reveal // 15
    elif reveal < 40:
        mask_x = start_x + (end_x - start_x) * (reveal - 15) // 25
        mask_y = top_y
    else:
        mask_x = end_x
        mask_y = top_y + (end_y - top_y) * (reveal - 40) // 15
    canvas.blit(mask, (mask_x, mask_y))


def draw_mascot_heads(canvas):
    # A shelf with spare mascot heads: a lion, a bee and a spare pigeon.
    shaded_box(canvas, (190, 130, 80), (220, 160, 105), (150, 95, 55), 135, 54, 120, 5)
    # lion
    pygame.draw.circle(canvas, OUTLINE, (155, 42), 13)
    pygame.draw.circle(canvas, (230, 140, 40), (155, 42), 12)
    pygame.draw.circle(canvas, (250, 200, 90), (155, 43), 8)
    pygame.draw.rect(canvas, OUTLINE, (151, 40, 2, 2))
    pygame.draw.rect(canvas, OUTLINE, (157, 40, 2, 2))
    pygame.draw.rect(canvas, (150, 80, 40), (153, 45, 4, 2))
    # bee
    pygame.draw.circle(canvas, OUTLINE, (195, 44), 11)
    pygame.draw.circle(canvas, YELLOW, (195, 44), 10)
    pygame.draw.rect(canvas, OUTLINE, (186, 41, 18, 3))
    pygame.draw.rect(canvas, OUTLINE, (187, 47, 16, 3))
    pygame.draw.line(canvas, OUTLINE, (191, 34), (188, 28))
    pygame.draw.line(canvas, OUTLINE, (199, 34), (202, 28))
    # spare pigeon head
    pygame.draw.circle(canvas, OUTLINE, (235, 44), 11)
    pygame.draw.circle(canvas, (155, 160, 182), (235, 44), 10)
    pygame.draw.rect(canvas, (250, 165, 60), (233, 46, 5, 3))
    pygame.draw.rect(canvas, OUTLINE, (230, 41, 2, 2))
    pygame.draw.rect(canvas, OUTLINE, (239, 41, 2, 2))


def draw_costume_rack(canvas):
    # A rail with three costumes: orange lion, striped bee, grey pigeon.
    pygame.draw.rect(canvas, OUTLINE, (132, 92, 126, 4))
    outlined_box(canvas, (200, 200, 210), 134, 92, 3, 108)
    outlined_box(canvas, (200, 200, 210), 253, 92, 3, 108)
    costumes = [(145, (230, 140, 40), (250, 180, 80)),
                (180, YELLOW, (255, 235, 120)),
                (215, (155, 160, 182), (200, 205, 220))]
    for x, colour, light in costumes:
        pygame.draw.rect(canvas, OUTLINE, (x + 12, 94, 2, 6))                  # hanger
        pygame.draw.polygon(canvas, OUTLINE, [(x - 1, 99), (x + 27, 99), (x + 30, 160), (x - 4, 160)])
        pygame.draw.polygon(canvas, colour, [(x, 100), (x + 26, 100), (x + 29, 159), (x - 3, 159)])
        pygame.draw.rect(canvas, light, (x + 2, 102, 3, 54))
        if colour == YELLOW:
            for stripe_y in [112, 126, 140]:
                pygame.draw.rect(canvas, OUTLINE, (x - 1, stripe_y, 29, 4))


def draw_ring_light(canvas):
    # Pombo's TikTok setup: a ring light with a phone, on a tripod.
    pygame.draw.circle(canvas, OUTLINE, (300, 72), 15)
    pygame.draw.circle(canvas, (255, 255, 230), (300, 72), 14)
    pygame.draw.circle(canvas, OUTLINE, (300, 72), 9)
    pygame.draw.circle(canvas, (215, 180, 230), (300, 72), 8)
    outlined_box(canvas, (40, 40, 50), 296, 66, 8, 13)
    pygame.draw.rect(canvas, (120, 200, 255), (297, 67, 6, 10))
    pygame.draw.rect(canvas, OUTLINE, (299, 87, 2, 90))
    pygame.draw.line(canvas, OUTLINE, (300, 176), (288, 199), 2)
    pygame.draw.line(canvas, OUTLINE, (300, 176), (312, 199), 2)
    pygame.draw.line(canvas, OUTLINE, (300, 176), (300, 199), 2)


def draw_mirror_table(canvas):
    # A mirror with light bulbs, and a table with a foam finger,
    # a sweatband and a bottle.
    shaded_box(canvas, (250, 215, 90), (255, 240, 150), (200, 160, 40), 340, 28, 76, 66)
    pygame.draw.rect(canvas, (190, 230, 250), (346, 34, 64, 54))
    pygame.draw.line(canvas, WHITE, (352, 80), (370, 44), 3)
    pygame.draw.line(canvas, WHITE, (362, 82), (378, 50), 1)
    for bulb_x in range(344, 416, 9):
        pygame.draw.circle(canvas, (255, 255, 210), (bulb_x, 30), 2)
    shaded_box(canvas, (190, 130, 80), (220, 160, 105), (150, 95, 55), 336, 120, 84, 6)
    outlined_box(canvas, HOME_RED, 345, 110, 8, 10)                            # foam finger
    pygame.draw.rect(canvas, HOME_RED, (348, 102, 3, 8))
    outlined_box(canvas, WHITE, 362, 113, 12, 7)                               # sweatband
    pygame.draw.rect(canvas, HOME_RED, (362, 116, 12, 1))
    outlined_box(canvas, (250, 165, 60), 384, 110, 6, 10)                      # bottle


# ---------------------------------------------------------------- Press Room

def draw_reporter(canvas, x, hair, hair_light, style, shirt, shirt_light, lift):
    # A reporter seen from behind, sitting on a folding chair.
    # style is "plain", "bald", "ponytail", "cap" or "curly".
    # lift is 0 or 1: the reporter breathes (moves up by 1 pixel).
    chair = (70, 72, 88)

    # The shadow on the floor and the thin metal chair legs.
    draw_shadow(canvas, x - 3, 200, 32)
    for leg_x in [x + 1, x + 22]:
        pygame.draw.rect(canvas, OUTLINE, (leg_x - 1, 176, 4, 24))
        pygame.draw.rect(canvas, (150, 155, 170), (leg_x, 176, 2, 23))

    # Back and shoulders: light on the left, shadow on the right,
    # and a bit of neck above the collar.
    y = 150 - lift
    pygame.draw.rect(canvas, OUTLINE, (x + 1, y, 24, 22))
    pygame.draw.rect(canvas, shirt, (x + 2, y + 1, 22, 21))
    pygame.draw.rect(canvas, shirt_light, (x + 2, y + 1, 22, 3))
    pygame.draw.rect(canvas, shirt_light, (x + 2, y + 1, 3, 21))
    pygame.draw.rect(canvas, darker(shirt, 0.75), (x + 20, y + 4, 4, 18))
    pygame.draw.rect(canvas, darker(SKIN, 0.85), (x + 10, y - 1, 6, 2))

    # The backrest of the chair, in front of the reporter's back.
    shaded_box(canvas, chair, (105, 108, 125), (48, 50, 62), x, 164, 26, 12)
    pygame.draw.rect(canvas, OUTLINE, (x - 1, 176, 28, 3))

    # The back of the head: first a darker circle, then the hair circle
    # 1 pixel higher, so a dark edge stays at the bottom (the shadow).
    head_y = 141 - lift
    hair_dark = darker(hair, 0.7)
    pygame.draw.circle(canvas, OUTLINE, (x + 13, head_y), 9)
    if style == "bald":
        pygame.draw.circle(canvas, darker(SKIN, 0.85), (x + 13, head_y), 8)
        pygame.draw.circle(canvas, SKIN, (x + 13, head_y - 1), 7)
        pygame.draw.rect(canvas, (255, 235, 215), (x + 9, head_y - 6, 4, 2))     # shiny head
        pygame.draw.rect(canvas, hair, (x + 6, head_y + 1, 14, 4))
    else:
        pygame.draw.circle(canvas, hair_dark, (x + 13, head_y), 8)
        pygame.draw.circle(canvas, hair, (x + 13, head_y - 1), 7)
        pygame.draw.rect(canvas, hair_light, (x + 9, head_y - 6, 5, 2))
    if style == "ponytail":
        pygame.draw.circle(canvas, OUTLINE, (x + 13, head_y + 11), 4)
        pygame.draw.circle(canvas, hair, (x + 13, head_y + 11), 3)
        pygame.draw.rect(canvas, HOME_RED, (x + 11, head_y + 7, 5, 2))            # hair tie
    if style == "cap":
        pygame.draw.rect(canvas, OUTLINE, (x + 4, head_y - 8, 18, 7))
        pygame.draw.rect(canvas, HOME_RED, (x + 5, head_y - 7, 16, 5))
        pygame.draw.rect(canvas, (255, 110, 110), (x + 5, head_y - 7, 16, 1))
        pygame.draw.rect(canvas, (180, 40, 40), (x + 5, head_y - 3, 16, 1))
    if style == "curly":
        for dx, dy in [(-7, -3), (7, -3), (0, -8), (-5, 4), (5, 4)]:
            pygame.draw.circle(canvas, OUTLINE, (x + 13 + dx, head_y + dy), 5)
            pygame.draw.circle(canvas, hair_dark, (x + 13 + dx, head_y + dy), 4)
            pygame.draw.circle(canvas, hair, (x + 13 + dx, head_y + dy - 1), 3)

    # Ears.
    pygame.draw.rect(canvas, SKIN, (x + 3, head_y, 2, 3))
    pygame.draw.rect(canvas, SKIN, (x + 21, head_y, 2, 3))


def draw_press_room(canvas, progress, tick):
    # The back wall: dark navy, even darker towards the ceiling.
    draw_bands(canvas, [(24, 32, 64), (30, 40, 78), (36, 48, 92), (40, 54, 100)],
               0, 0, ROOM_WIDTH, FLOOR_Y)
    draw_lighting_rig(canvas)
    draw_door(canvas, 20, (110, 170, 255), (70, 120, 210))     # back to the booth
    draw_match_clock(canvas, tick)

    draw_sponsor_wall(canvas)
    draw_press_floor(canvas)
    draw_press_table(canvas)

    # The spotlights shine on the table (drawn after the wall and the
    # table, so they get brighter; the reporters stay in front).
    draw_light_cone(canvas, 300, 12, 186, 8, 90)
    draw_light_cone(canvas, 362, 12, 186, 8, 90)

    draw_tv_camera(canvas, tick)

    # Six reporters seen from behind, all different.
    reporters = [
        ((110, 70, 40), (150, 105, 70), "plain", (200, 80, 80), (230, 110, 110)),
        ((40, 30, 30), (80, 65, 65), "ponytail", (80, 120, 200), (110, 150, 230)),
        ((90, 90, 90), (130, 130, 130), "bald", (90, 160, 110), (120, 190, 140)),
        ((230, 190, 90), (255, 225, 140), "cap", (240, 240, 245), (255, 255, 255)),
        ((60, 40, 30), (100, 75, 60), "curly", (170, 110, 190), (200, 140, 220)),
        ((150, 80, 40), (190, 115, 70), "plain", (250, 190, 70), (255, 220, 110)),
    ]
    x = 84
    number = 0
    for hair, hair_light, style, shirt, shirt_light in reporters:
        lift = bob(tick, number * 7)
        draw_reporter(canvas, x, hair, hair_light, style, shirt, shirt_light, lift)
        x = x + 30
        number = number + 1

    # One reporter holds up a phone, another a camera.
    outlined_box(canvas, (30, 30, 40), 125, 118, 8, 14)
    pygame.draw.rect(canvas, (120, 200, 255), (126, 119, 6, 11))
    pygame.draw.rect(canvas, (190, 230, 255), (126, 119, 6, 2))
    pygame.draw.rect(canvas, SKIN, (127, 132, 4, 8))
    shaded_box(canvas, (50, 50, 60), (85, 85, 95), (30, 30, 38), 213, 114, 18, 12)
    pygame.draw.circle(canvas, OUTLINE, (222, 120), 5)
    pygame.draw.circle(canvas, (150, 200, 255), (222, 120), 4)
    pygame.draw.rect(canvas, WHITE, (220, 118, 2, 2))
    pygame.draw.rect(canvas, SKIN, (218, 126, 4, 10))

    # Camera flashes: every 50 frames another reporter's camera flashes
    # for 5 frames. (tick // 50) % 6 picks the reporter: 0, 1, 2 ... 5, 0 ...
    if tick % 50 < 5:
        reporter = (tick // 50) % 6
        flash_x = 84 + reporter * 30 + 13
        flash_y = 122
        flash = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.circle(flash, (255, 255, 255, 110), (20, 20), 18)
        canvas.blit(flash, (flash_x - 20, flash_y - 20))
        for dx, dy in [(-10, 0), (10, 0), (0, -10), (0, 10)]:
            pygame.draw.line(canvas, WHITE, (flash_x, flash_y), (flash_x + dx, flash_y + dy), 2)

    # A crumpled piece of paper (the betting slip) by the TV camera,
    # until you pick it up.
    if "slip" not in progress["inventory"]:
        draw_shadow(canvas, 424, 201, 13)
        pygame.draw.circle(canvas, OUTLINE, (430, 197), 5)
        pygame.draw.circle(canvas, (225, 225, 215), (430, 197), 4)
        pygame.draw.circle(canvas, (250, 250, 240), (429, 196), 2)
        pygame.draw.line(canvas, (180, 180, 170), (427, 195), (432, 199))
        pygame.draw.line(canvas, (180, 180, 170), (431, 194), (428, 198))


def draw_lighting_rig(canvas):
    # A metal beam under the ceiling with four spotlights hanging from it.
    pygame.draw.rect(canvas, OUTLINE, (0, 0, ROOM_WIDTH, 7))
    pygame.draw.rect(canvas, (90, 95, 110), (0, 1, ROOM_WIDTH, 4))
    pygame.draw.rect(canvas, (130, 135, 150), (0, 1, ROOM_WIDTH, 1))
    # Little cross struts make it look like a real lighting truss.
    for x in range(0, ROOM_WIDTH, 8):
        pygame.draw.line(canvas, (60, 63, 75), (x, 2), (x + 4, 4))
    for x in [150, 296, 358, 440]:
        pygame.draw.rect(canvas, OUTLINE, (x - 1, 5, 10, 8))
        pygame.draw.rect(canvas, (60, 62, 72), (x, 6, 8, 5))
        pygame.draw.rect(canvas, (95, 98, 110), (x, 6, 8, 1))
        pygame.draw.rect(canvas, (255, 245, 200), (x + 1, 11, 6, 2))         # the bulb


# How high the match clock hangs (below the timer, above the door).
CLOCK_Y = 74


def draw_match_clock(canvas, tick):
    # A digital clock above the door that shows the match time.
    # The two dots in the middle blink once per second (30 frames).
    shaded_box(canvas, (20, 20, 28), (55, 55, 65), (10, 10, 15), 18, CLOCK_Y, 44, 18)
    if (tick // 30) % 2 == 0:
        pygame.draw.rect(canvas, (255, 70, 60), (34, CLOCK_Y + 5, 2, 2))
        pygame.draw.rect(canvas, (255, 70, 60), (34, CLOCK_Y + 10, 2, 2))
    # A soft red glow around the clock.
    glow = pygame.Surface((56, 30), pygame.SRCALPHA)
    pygame.draw.ellipse(glow, (255, 60, 50, 25), (0, 0, 56, 30))
    canvas.blit(glow, (12, CLOCK_Y - 6))


def draw_sponsor_wall(canvas):
    # The backdrop behind the press table, like at real press conferences:
    # the same two logos repeat in a neat pattern ("step and repeat").
    # 1. The metal stands that hold it, standing on the floor.
    for stand_x in [104, 462]:
        pygame.draw.rect(canvas, OUTLINE, (stand_x - 1, 148, 5, 52))
        pygame.draw.rect(canvas, (140, 145, 160), (stand_x, 148, 3, 51))
        pygame.draw.rect(canvas, OUTLINE, (stand_x - 7, 196, 17, 4))

    # 2. The backdrop: darker at the top and bottom, lighter in the middle,
    #    with a metal frame (light top and left edge, dark bottom and right).
    pygame.draw.rect(canvas, OUTLINE, (89, 21, 388, 130))
    draw_bands(canvas, [(28, 78, 155), (32, 88, 172), (35, 96, 185), (32, 88, 172), (28, 78, 155)],
               92, 24, 382, 124)
    pygame.draw.rect(canvas, (175, 185, 205), (90, 22, 386, 2))
    pygame.draw.rect(canvas, (175, 185, 205), (90, 22, 2, 128))
    pygame.draw.rect(canvas, (95, 105, 125), (90, 148, 386, 2))
    pygame.draw.rect(canvas, (95, 105, 125), (474, 22, 2, 128))

    # 3. The logos: rows of trophies and balls, every second row moved
    #    by half a step, so they make a diagonal pattern.
    for row in range(5):
        for column in range(10):
            x = 100 + column * 38 + (row % 2) * 19
            y = 30 + row * 23
            if x > 456:
                continue
            if (row + column) % 2 == 0:
                draw_trophy_logo(canvas, x, y)
            else:
                draw_ball_logo(canvas, x, y)

    # 4. The club crest above the table, with a gold ring.
    pygame.draw.circle(canvas, OUTLINE, (330, 100), 15)
    pygame.draw.circle(canvas, (230, 180, 60), (330, 100), 14)
    pygame.draw.circle(canvas, (255, 220, 110), (329, 99), 12)
    pygame.draw.circle(canvas, WHITE, (330, 100), 11)
    pygame.draw.circle(canvas, HOME_RED, (330, 100), 8)
    pygame.draw.circle(canvas, (255, 110, 100), (328, 98), 4)
    pygame.draw.circle(canvas, WHITE, (330, 100), 3)


def draw_trophy_logo(canvas, x, y):
    # A small golden trophy with a white text line next to it.
    gold = (250, 205, 60)
    pygame.draw.rect(canvas, gold, (x + 1, y, 7, 4))          # the cup
    pygame.draw.rect(canvas, gold, (x + 2, y + 4, 5, 1))
    pygame.draw.rect(canvas, gold, (x + 4, y + 5, 1, 2))      # the stem
    pygame.draw.rect(canvas, gold, (x + 2, y + 7, 5, 1))      # the base
    canvas.set_at((x, y + 1), gold)                          # the handles
    canvas.set_at((x + 8, y + 1), gold)
    pygame.draw.rect(canvas, (255, 240, 150), (x + 2, y + 1, 1, 2))    # shine
    pygame.draw.rect(canvas, (200, 150, 30), (x + 6, y + 1, 1, 3))     # shadow
    pygame.draw.rect(canvas, (220, 230, 245), (x + 11, y + 2, 9, 2))
    pygame.draw.rect(canvas, (150, 170, 210), (x + 11, y + 5, 6, 1))


def draw_ball_logo(canvas, x, y):
    # A small white football with a text line next to it.
    pygame.draw.circle(canvas, (220, 230, 245), (x + 4, y + 4), 4)
    pygame.draw.rect(canvas, (40, 60, 110), (x + 3, y + 3, 2, 2))
    canvas.set_at((x + 1, y + 4), (40, 60, 110))
    canvas.set_at((x + 7, y + 4), (40, 60, 110))
    pygame.draw.rect(canvas, (250, 205, 60), (x + 11, y + 2, 9, 2))
    pygame.draw.rect(canvas, (150, 170, 210), (x + 11, y + 5, 6, 1))


def draw_press_floor(canvas):
    # A dark skirting board, then a carpet that gets lighter towards the
    # front (the bottom of the screen) and a red walkway to the stage.
    pygame.draw.rect(canvas, OUTLINE, (0, FLOOR_Y - 1, ROOM_WIDTH, 1))
    pygame.draw.rect(canvas, (20, 26, 52), (0, FLOOR_Y, ROOM_WIDTH, 4))
    pygame.draw.rect(canvas, (60, 72, 115), (0, FLOOR_Y, ROOM_WIDTH, 1))
    draw_bands(canvas, [(28, 42, 98), (34, 52, 115), (40, 62, 132), (46, 72, 148), (52, 82, 162)],
               0, FLOOR_Y + 4, ROOM_WIDTH, CANVAS_HEIGHT - FLOOR_Y - 4)

    # The dot pattern: the rows get further apart towards the front.
    # Things that are far away look closer together, so this gives depth.
    y = FLOOR_Y + 7
    gap = 4
    while y < CANVAS_HEIGHT:
        for x in range((y * 3) % gap, ROOM_WIDTH, gap * 2):
            canvas.set_at((x, y), (75, 105, 185))
        y = y + gap
        gap = gap + 1

    # The red walkway: narrow at the back, wide at the front (perspective),
    # with gold edges and a darker part far away.
    pygame.draw.polygon(canvas, (150, 40, 50), [(298, 204), (362, 204), (386, 270), (274, 270)])
    pygame.draw.polygon(canvas, (120, 30, 42), [(298, 204), (362, 204), (366, 215), (294, 215)])
    pygame.draw.line(canvas, (220, 175, 70), (298, 204), (274, 270), 2)
    pygame.draw.line(canvas, (220, 175, 70), (362, 204), (386, 270), 2)


def draw_press_table(canvas):
    # The stage, with the press table on it: a white tablecloth, a
    # dark blue skirt with folds and the club crest, microphones,
    # water bottles and a name card.

    # The stage (a low wooden box), with a shadow on the floor.
    draw_shadow(canvas, 244, 203, 172)
    shaded_box(canvas, (70, 75, 95), (110, 115, 135), (45, 48, 62), 250, 186, 160, 14)

    # The tablecloth on top.
    outlined_box(canvas, (230, 232, 245), 262, 146, 136, 5)
    pygame.draw.rect(canvas, WHITE, (262, 146, 136, 1))
    pygame.draw.rect(canvas, (190, 195, 215), (262, 150, 136, 1))

    # The skirt hanging down, with folds: every 8 pixels a light and a
    # dark line, like real cloth.
    outlined_box(canvas, (35, 55, 115), 264, 152, 132, 34)
    for fold_x in range(268, 394, 8):
        pygame.draw.rect(canvas, (52, 75, 142), (fold_x, 152, 1, 34))
        pygame.draw.rect(canvas, (24, 38, 85), (fold_x + 3, 152, 1, 34))
    pygame.draw.rect(canvas, (24, 38, 85), (264, 183, 132, 3))

    # The crest on the skirt.
    pygame.draw.circle(canvas, OUTLINE, (330, 168), 10)
    pygame.draw.circle(canvas, HOME_RED, (330, 168), 9)
    pygame.draw.circle(canvas, (255, 110, 100), (328, 166), 4)
    pygame.draw.circle(canvas, WHITE, (330, 168), 4)

    # Microphones of all the TV channels, with their cables.
    microphones = [(300, HOME_RED), (312, YELLOW), (322, (90, 180, 110)),
                   (334, WHITE), (346, AWAY_BLUE), (358, (240, 140, 40))]
    for mic_x, colour in microphones:
        pygame.draw.line(canvas, OUTLINE, (mic_x + 2, 145), (330, 133))
        outlined_box(canvas, (40, 40, 50), mic_x, 124, 5, 7)
        pygame.draw.rect(canvas, (110, 110, 120), (mic_x + 1, 125, 2, 2))
        outlined_box(canvas, colour, mic_x - 1, 132, 7, 5)
        pygame.draw.rect(canvas, darker(colour, 0.7), (mic_x - 1, 135, 7, 2))

    # Water bottles with a shine, and the name card.
    for bottle_x in [282, 372]:
        outlined_box(canvas, (150, 205, 245), bottle_x, 134, 6, 12)
        pygame.draw.rect(canvas, (210, 240, 255), (bottle_x + 1, 135, 1, 10))
        pygame.draw.rect(canvas, AWAY_BLUE, (bottle_x, 132, 6, 3))
    outlined_box(canvas, WHITE, 352, 139, 20, 7)
    pygame.draw.rect(canvas, (200, 205, 220), (352, 145, 20, 1))


def draw_tv_camera(canvas, tick):
    # A TV camera on a tripod, and a fluffy boom microphone over the table.
    draw_shadow(canvas, 416, 201, 42)
    for foot_x in [420, 436, 452]:
        pygame.draw.line(canvas, OUTLINE, (foot_x, 200), (436, 150), 3)
        pygame.draw.line(canvas, (120, 125, 140), (foot_x, 199), (436, 151), 1)
    shaded_box(canvas, (60, 60, 70), (95, 95, 108), (35, 35, 45), 420, 132, 34, 20)
    pygame.draw.rect(canvas, (45, 45, 55), (424, 140, 20, 2))                  # vents
    pygame.draw.rect(canvas, (45, 45, 55), (424, 144, 20, 2))
    outlined_box(canvas, (30, 30, 40), 408, 136, 12, 12)
    pygame.draw.circle(canvas, (70, 120, 200), (414, 142), 4)
    pygame.draw.circle(canvas, (150, 210, 255), (413, 141), 2)
    canvas.set_at((412, 140), WHITE)                                           # lens shine
    # The red "recording" light blinks (on for 15 frames, off for 15).
    if (tick // 15) % 2 == 0:
        pygame.draw.rect(canvas, (255, 50, 50), (448, 135, 3, 3))
    else:
        pygame.draw.rect(canvas, (110, 30, 30), (448, 135, 3, 3))
    pygame.draw.line(canvas, OUTLINE, (466, 66), (392, 98), 2)                 # boom pole
    outlined_box(canvas, (110, 110, 120), 376, 96, 18, 8)
    for i in range(0, 18, 3):
        pygame.draw.rect(canvas, (150, 150, 160), (376 + i, 96, 1, 8))


# ---------------------------------------------------------------- The Pitch

# Where the people stand on the pitch (x positions on the canvas).
LINESMAN_X = 110
STRIKER_X = 196
BALL_X = 258
REFEREE_X = 296
CAPTAIN_X = 322


def draw_pitch(canvas, pictures, ball, tick):
    # During a goal celebration the scoreboard flashes (on for 8 frames,
    # off for 8 frames ...).
    flashing = ball["celebrate"] > 0 and (ball["celebrate"] // 8) % 2 == 0
    draw_pitch_background(canvas, flashing, tick)
    draw_pitch_people(canvas, pictures, ball, tick)


def draw_title_background(canvas, pictures, tick):
    # The title screen: the empty pitch, with the VAR official on the left
    # and Pombo on the right, like decorations next to the menu.
    draw_pitch_background(canvas, False, tick)
    player = pictures["player"]
    canvas.blit(player, (112, FLOOR_Y - player.get_height() - bob(tick, 0)))
    pombo = pictures["pombo"]
    canvas.blit(pombo, (340, FLOOR_Y - pombo.get_height() - bob(tick, 10)))


def draw_pitch_background(canvas, flashing, tick):
    # Everything on the pitch except the people and the ball:
    # the stadium, the boards, the grass, the tunnel, the flag and the goal.
    draw_stadium(canvas, flashing, tick)

    # Advertising boards along the side of the pitch.
    boards = [(YELLOW, OUTLINE), ((70, 110, 230), WHITE), (WHITE, HOME_RED), ((90, 180, 110), WHITE)]
    for i in range(9):
        background, writing = boards[i % 4]
        outlined_box(canvas, background, i * 60 + 1, 149, 58, 15)
        pygame.draw.rect(canvas, writing, (i * 60 + 12, 154, 34, 4))
        pygame.draw.rect(canvas, writing, (i * 60 + 6, 154, 4, 4))

    # The grass with mowing stripes, all the way down, and the white lines.
    for i in range(0, ROOM_WIDTH, 30):
        if (i // 30) % 2 == 0:
            colour = (80, 190, 80)
        else:
            colour = (100, 210, 95)
        pygame.draw.rect(canvas, colour, (i, 165, 30, CANVAS_HEIGHT - 165))
    pygame.draw.rect(canvas, WHITE, (0, 172, ROOM_WIDTH, 1))
    pygame.draw.rect(canvas, WHITE, (0, FLOOR_Y + 2, ROOM_WIDTH, 2))

    # The tunnel back inside.
    outlined_box(canvas, (140, 140, 155), 8, 130, 64, 70)
    pygame.draw.rect(canvas, (40, 45, 60), (16, 138, 48, 62))
    pygame.draw.rect(canvas, HOME_RED, (8, 130, 64, 6))

    # A corner flag.
    pygame.draw.rect(canvas, OUTLINE, (90, 176, 1, 26))
    pygame.draw.polygon(canvas, YELLOW, [(91, 176), (100, 179), (91, 182)])

    draw_goal(canvas)


def draw_pitch_people(canvas, pictures, ball, tick):
    # The people: linesman, striker, referee and the away captain.
    # They breathe (one pixel up and down); the angry captain jumps.
    for name, x, phase in [("linesman", LINESMAN_X, 3), ("striker", STRIKER_X, 11),
                           ("referee", REFEREE_X, 5)]:
        picture = pictures[name]
        canvas.blit(picture, (x, FLOOR_Y - picture.get_height() - bob(tick, phase)))
    captain = pictures["captain"]
    jump = ((tick // 6) % 2) * 2
    canvas.blit(captain, (CAPTAIN_X, FLOOR_Y - captain.get_height() - jump))

    # The linesman's flag, held up in his hand.
    flag_x = LINESMAN_X + 27
    pygame.draw.rect(canvas, OUTLINE, (flag_x, 140, 1, 42))
    pygame.draw.rect(canvas, OUTLINE, (flag_x, 139, 11, 9))
    pygame.draw.rect(canvas, YELLOW, (flag_x + 1, 140, 9, 7))
    pygame.draw.rect(canvas, HOME_RED, (flag_x + 1, 140, 4, 3))
    pygame.draw.rect(canvas, HOME_RED, (flag_x + 5, 143, 5, 4))

    # A speech bubble over the captain ("OFFSIDE!" is added as text).
    outlined_box(canvas, WHITE, CAPTAIN_X - 14, 126, 34, 12)
    pygame.draw.polygon(canvas, OUTLINE, [(CAPTAIN_X - 2, 138), (CAPTAIN_X + 2, 144), (CAPTAIN_X + 4, 138)])

    # The ball, with a little shadow. ball["x"] is where it is now.
    # While it rolls, the picture is turned in steps of 90 degrees
    # (every 6 pixels it rolls), which keeps the pixel art sharp.
    ball_x = int(ball["x"])
    turns = (ball_x // 6) % 4
    ball_picture = pygame.transform.rotate(pictures["ball"], turns * 90)
    pygame.draw.ellipse(canvas, (50, 140, 50), (ball_x, FLOOR_Y - 2, 10, 4))
    canvas.blit(ball_picture, (ball_x, FLOOR_Y - ball_picture.get_height() + 1))


def draw_stadium(canvas, celebrating, tick):
    # Sky, roof, two tiers of fans with the scoreboard, and floodlights.
    pygame.draw.rect(canvas, (110, 190, 250), (0, 0, ROOM_WIDTH, 20))
    pygame.draw.rect(canvas, (140, 205, 255), (0, 20, ROOM_WIDTH, 14))
    draw_cloud(canvas, 40, 6)
    draw_cloud(canvas, 250, 3)

    # The roof.
    pygame.draw.rect(canvas, OUTLINE, (0, 33, ROOM_WIDTH, 9))
    pygame.draw.rect(canvas, (200, 205, 215), (0, 34, ROOM_WIDTH, 7))
    for x in range(0, ROOM_WIDTH, 16):
        pygame.draw.line(canvas, (150, 155, 170), (x, 34), (x + 8, 40))

    # Upper tier: small fans. The colour of each fan comes from a calculation,
    # so the crowd looks mixed but always the same.
    fan_colours = [WHITE, YELLOW, (255, 120, 120), SKIN, AWAY_BLUE, (235, 70, 70)]
    pygame.draw.rect(canvas, (60, 60, 80), (0, 42, ROOM_WIDTH, 50))
    for fan_y in range(44, 90, 4):
        for fan_x in range(1 + (fan_y // 4) % 2 * 2, ROOM_WIDTH, 4):
            colour = fan_colours[(fan_x * 7 + fan_y * 3) % 6]
            pygame.draw.rect(canvas, colour, (fan_x, fan_y, 2, 2))

    # The scoreboard (the text is added later).
    shaded_box(canvas, (20, 20, 30), (60, 60, 75), (10, 10, 15), 190, 46, 100, 34)
    pygame.draw.rect(canvas, HOME_RED, (194, 50, 30, 10))
    pygame.draw.rect(canvas, AWAY_BLUE, (256, 50, 30, 10))
    pygame.draw.rect(canvas, (255, 200, 40), (194, 66, 92, 10))
    if celebrating:
        pygame.draw.rect(canvas, (230, 60, 60), (194, 66, 92, 10))

    # A red banner between the tiers.
    pygame.draw.rect(canvas, OUTLINE, (0, 92, ROOM_WIDTH, 3))
    pygame.draw.rect(canvas, HOME_RED, (0, 95, ROOM_WIDTH, 7))
    for x in range(0, ROOM_WIDTH, 40):
        pygame.draw.rect(canvas, WHITE, (x + 6, 97, 22, 3))

    # Lower tier: bigger fans, some with their arms up.
    pygame.draw.rect(canvas, (70, 70, 95), (0, 102, ROOM_WIDTH, 46))
    for fan_y in range(105, 146, 7):
        for fan_x in range(2 + (fan_y // 7) % 2 * 4, ROOM_WIDTH, 8):
            colour = fan_colours[(fan_x * 3 + fan_y) % 6]
            pygame.draw.rect(canvas, SKIN, (fan_x + 1, fan_y, 3, 3))
            pygame.draw.rect(canvas, colour, (fan_x, fan_y + 3, 5, 3))
            if (fan_x + fan_y) % 3 == 0:
                # Fans with their arms up jump: half of them up, half down,
                # changing every 8 frames.
                jump = (fan_x // 8 + tick // 8) % 2
                pygame.draw.rect(canvas, SKIN, (fan_x - 1, fan_y - 2 - jump, 1, 3))
                pygame.draw.rect(canvas, SKIN, (fan_x + 5, fan_y - 2 - jump, 1, 3))

    # A fan waving a red and white flag.
    # The tip of the flag moves up and down to make it wave.
    wave = ((tick // 8) % 3) * 2
    pygame.draw.rect(canvas, OUTLINE, (150, 98, 1, 20))
    pygame.draw.polygon(canvas, HOME_RED, [(151, 98), (166, 99 + wave), (151, 106)])
    pygame.draw.polygon(canvas, WHITE, [(151, 102), (166, 99 + wave), (151, 106)])

    # Two floodlights.
    for light_x in [60, 420]:
        outlined_box(canvas, (90, 90, 100), light_x - 14, 2, 30, 14)
        for i in range(3):
            pygame.draw.rect(canvas, (255, 250, 200), (light_x - 12 + i * 10, 4, 8, 10))


def draw_goal(canvas):
    # The goal seen from the side: a shadow, the net inside the frame,
    # the back post and ground bar (light grey, because they are further
    # away), then the white front post and crossbar.
    # It is about 1.5 times as high as a player, like a real goal.
    shadow = pygame.Surface((112, 10), pygame.SRCALPHA)
    pygame.draw.ellipse(shadow, (0, 60, 0, 70), (0, 0, 112, 10))
    canvas.blit(shadow, (384, 196))

    # The net: a light area with a grid, only between the posts.
    pygame.draw.rect(canvas, (235, 240, 250), (393, 125, 98, 74))
    for net_x in range(395, 491, 4):
        pygame.draw.line(canvas, (195, 200, 215), (net_x, 125), (net_x, 198))
    for net_y in range(127, 199, 4):
        pygame.draw.line(canvas, (195, 200, 215), (393, net_y), (490, net_y))

    # The back post and the bar on the ground at the back of the goal.
    outlined_box(canvas, (200, 205, 215), 490, 122, 4, 78)
    outlined_box(canvas, (200, 205, 215), 393, 197, 101, 3)

    # The white front post and the crossbar.
    outlined_box(canvas, WHITE, 388, 120, 106, 5)
    outlined_box(canvas, WHITE, 388, 120, 5, 80)

    # A photographer kneeling next to the goal.
    for photographer_x in [368]:
        pygame.draw.rect(canvas, OUTLINE, (photographer_x, 186, 14, 14))
        pygame.draw.rect(canvas, (60, 60, 80), (photographer_x + 1, 187, 12, 13))
        pygame.draw.circle(canvas, OUTLINE, (photographer_x + 7, 182), 5)
        pygame.draw.circle(canvas, (110, 75, 50), (photographer_x + 7, 182), 4)
        outlined_box(canvas, (30, 30, 40), photographer_x - 7, 184, 9, 6)
        pygame.draw.rect(canvas, (60, 60, 70), (photographer_x - 13, 185, 7, 4))


# ---------------------------------------------------------------- choosing a room

def draw_room(canvas, scene_id, pictures, progress, extras):
    # Draw the room that belongs to a scene id from story.json.
    # pictures holds the characters and objects that live in the rooms.
    # progress is needed for things that change (padlock, whistle, slip ...).
    # extras holds what moves: "tick" (the frame counter for animations),
    # "ball" (the ball on the pitch) and "reveal" (Dave's reveal animation).
    tick = extras["tick"]
    if scene_id == "booth":
        draw_booth(canvas, pictures, progress, tick)
    elif scene_id == "dressing_room":
        draw_dressing_room(canvas, pictures, progress, tick)
    elif scene_id == "mascot_room":
        draw_mascot_room(canvas, pictures, progress, tick, extras["reveal"])
    elif scene_id == "press_room":
        draw_press_room(canvas, progress, tick)
    elif scene_id == "pitch":
        draw_pitch(canvas, pictures, extras["ball"], tick)


# Text labels for each room: (text, x, y, colour, small?) in canvas positions.
# They are drawn later on the big window, so the letters stay sharp.
LABELS = {
    "booth": [
        ("REF", 250, 110, (60, 60, 70), False),
        ("MASCOT", 299, 110, (90, 60, 10), False),
        ("PRESS", 359, 110, (255, 255, 255), False),
        ("PITCH", 430, 117, (255, 255, 255), False),
    ],
    "dressing_room": [
        ("BOOTH", 28, 110, (60, 60, 70), False),
        ("TRUST THE", 296, 36, (230, 60, 60), False),
        ("PROCESS", 300, 45, (230, 60, 60), False),
    ],
    "mascot_room": [
        ("BOOTH", 28, 110, (90, 60, 10), False),
        ("EMPLOYEE", 83, 79, (120, 60, 20), True),
        ("SEEDS", 457, 180, (120, 80, 30), True),
    ],
    "press_room": [
        ("BOOTH", 28, 110, (255, 255, 255), False),
        ("Ref. Unit", 353, 139, (40, 40, 60), True),
        ("94  00", 22, 77, (255, 70, 60), False),
    ],
    "pitch": [
        ("BOOTH", 25, 120, (255, 255, 255), False),
        ("HOME", 195, 50, (255, 255, 255), False),
        ("1 - 0", 229, 50, (255, 255, 255), False),
        ("AWAY", 258, 50, (255, 255, 255), False),
        ("OFFSIDE!", CAPTAIN_X - 12, 127, (230, 40, 40), True),
    ],
}
