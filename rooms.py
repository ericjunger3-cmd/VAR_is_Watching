# Drawing the rooms of VAR Is Watching.
# Everything is drawn on a small 480 x 270 "canvas". The game scales the
# canvas up 2x afterwards, so every pixel here becomes a 2 x 2 block.

import random
import pygame
from sprites import OUTLINE

CANVAS_WIDTH = 480
CANVAS_HEIGHT = 270

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

def draw_wall(canvas):
    # Cream wallpaper with soft stripes and a darker strip at the top.
    canvas.fill((246, 224, 180))
    pygame.draw.rect(canvas, (232, 205, 160), (0, 0, CANVAS_WIDTH, 10))
    pygame.draw.rect(canvas, OUTLINE, (0, 10, CANVAS_WIDTH, 1))
    for x in range(0, CANVAS_WIDTH, 24):
        pygame.draw.rect(canvas, (240, 216, 170), (x, 11, 12, 140))

    # Wood panelling on the lower part of the wall.
    pygame.draw.rect(canvas, OUTLINE, (0, 147, CANVAS_WIDTH, 1))
    pygame.draw.rect(canvas, (140, 80, 40), (0, 148, CANVAS_WIDTH, 3))
    pygame.draw.rect(canvas, (180, 110, 60), (0, 151, CANVAS_WIDTH, 49))
    for x in range(0, CANVAS_WIDTH, 20):
        pygame.draw.rect(canvas, (205, 135, 75), (x + 1, 152, 17, 46))   # plank
        pygame.draw.rect(canvas, (225, 160, 95), (x + 1, 152, 17, 2))    # light top
        pygame.draw.rect(canvas, (150, 88, 48), (x + 1, 196, 17, 2))     # dark bottom


def draw_floor(canvas):
    # A strip of grass on top of warm bricks, like in old 2D games.
    pygame.draw.rect(canvas, (95, 200, 80), (0, FLOOR_Y, CANVAS_WIDTH, 6))
    for x in range(0, CANVAS_WIDTH, 2):
        # Little grass blades of different heights (0, 1 or 2 pixels).
        blade = (x * 7) % 3
        pygame.draw.line(canvas, (95, 200, 80), (x, FLOOR_Y), (x, FLOOR_Y - 1 - blade))
        if x % 6 == 0:
            canvas.set_at((x, FLOOR_Y - 2 - blade), (160, 235, 120))
    pygame.draw.rect(canvas, (60, 150, 60), (0, FLOOR_Y + 5, CANVAS_WIDTH, 2))

    # Bricks: every second row is shifted by half a brick.
    pygame.draw.rect(canvas, (165, 105, 70), (0, FLOOR_Y + 7, CANVAS_WIDTH, 63))
    row = 0
    for y in range(FLOOR_Y + 7, CANVAS_HEIGHT, 12):
        if row % 2 == 0:
            shift = 0
        else:
            shift = 12
        for x in range(-24 + shift, CANVAS_WIDTH, 24):
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


def draw_booth(canvas):
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
