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

def draw_tile_floor(canvas):
    # Wet white tiles for the dressing room, with a puddle by the shower.
    pygame.draw.rect(canvas, OUTLINE, (0, FLOOR_Y - 1, CANVAS_WIDTH, 1))
    pygame.draw.rect(canvas, (150, 165, 180), (0, FLOOR_Y, CANVAS_WIDTH, CANVAS_HEIGHT - FLOOR_Y))
    row = 0
    for y in range(FLOOR_Y, CANVAS_HEIGHT, 10):
        if row % 2 == 0:
            shift = 0
        else:
            shift = 10
        for x in range(-20 + shift, CANVAS_WIDTH, 20):
            pygame.draw.rect(canvas, (215, 225, 235), (x + 1, y + 1, 19, 9))
            pygame.draw.rect(canvas, (240, 245, 250), (x + 1, y + 1, 19, 2))
        row = row + 1
    # The puddle: light blue with a white shine.
    pygame.draw.ellipse(canvas, (140, 200, 240), (405, FLOOR_Y + 4, 60, 10))
    pygame.draw.line(canvas, WHITE, (415, FLOOR_Y + 7), (430, FLOOR_Y + 7))


def draw_carpet(canvas, colour, light, dark):
    # A wooden skirting board and a carpet with a dotted pattern.
    pygame.draw.rect(canvas, OUTLINE, (0, FLOOR_Y - 1, CANVAS_WIDTH, 1))
    pygame.draw.rect(canvas, (150, 95, 55), (0, FLOOR_Y, CANVAS_WIDTH, 4))
    pygame.draw.rect(canvas, (190, 130, 80), (0, FLOOR_Y, CANVAS_WIDTH, 1))
    pygame.draw.rect(canvas, colour, (0, FLOOR_Y + 4, CANVAS_WIDTH, CANVAS_HEIGHT - FLOOR_Y))
    pygame.draw.rect(canvas, dark, (0, FLOOR_Y + 4, CANVAS_WIDTH, 2))
    for y in range(FLOOR_Y + 10, CANVAS_HEIGHT, 8):
        for x in range(4 + (y // 8) % 2 * 4, CANVAS_WIDTH, 8):
            canvas.set_at((x, y), light)


# ---------------------------------------------------------------- Referee's Dressing Room

def draw_dressing_room(canvas):
    # Tiled walls: light tiles on top, darker tiles below, a white strip between.
    canvas.fill((120, 170, 185))
    for y in range(0, FLOOR_Y, 14):
        for x in range(0, CANVAS_WIDTH, 14):
            if y >= 120:
                tile, shine = (95, 165, 185), (125, 190, 205)
            else:
                tile, shine = (175, 225, 235), (210, 242, 248)
            pygame.draw.rect(canvas, tile, (x + 1, y + 1, 13, 13))
            pygame.draw.rect(canvas, shine, (x + 1, y + 1, 13, 2))
    pygame.draw.rect(canvas, (235, 245, 250), (0, 117, CANVAS_WIDTH, 2))
    pygame.draw.rect(canvas, OUTLINE, (0, 119, CANVAS_WIDTH, 2))
    pygame.draw.rect(canvas, (215, 225, 235), (0, 0, CANVAS_WIDTH, 6))
    pygame.draw.rect(canvas, OUTLINE, (0, 6, CANVAS_WIDTH, 1))
    draw_ceiling_lamps(canvas, [90, 230, 370])

    draw_door(canvas, 20, (250, 250, 250), (200, 200, 210))     # back to the booth

    # A wall clock: it is very late in the match.
    pygame.draw.circle(canvas, OUTLINE, (95, 45), 13)
    pygame.draw.circle(canvas, WHITE, (95, 45), 12)
    pygame.draw.circle(canvas, HOME_RED, (95, 45), 12, 2)
    pygame.draw.line(canvas, OUTLINE, (95, 45), (95, 37), 2)
    pygame.draw.line(canvas, OUTLINE, (95, 45), (101, 47), 2)

    # The tactics whiteboard with crosses, circles and arrows.
    shaded_box(canvas, (250, 252, 255), WHITE, (215, 220, 230), 120, 28, 70, 46)
    pygame.draw.rect(canvas, (170, 175, 190), (118, 74, 74, 3))
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
    for hook_x in [212, 232, 252]:
        pygame.draw.rect(canvas, OUTLINE, (hook_x, 34, 2, 4))
    pygame.draw.polygon(canvas, OUTLINE, [(205, 37), (221, 37), (224, 78), (202, 78)])
    pygame.draw.polygon(canvas, (30, 30, 45), [(206, 38), (220, 38), (223, 77), (203, 77)])
    pygame.draw.rect(canvas, YELLOW, (212, 40, 2, 30))
    outlined_box(canvas, (240, 120, 120), 246, 38, 12, 30)
    pygame.draw.rect(canvas, WHITE, (246, 46, 12, 2))
    pygame.draw.rect(canvas, WHITE, (246, 58, 12, 2))

    # The poster "TRUST THE PROCESS" with a referee silhouette.
    shaded_box(canvas, (255, 250, 235), WHITE, (220, 210, 190), 290, 26, 62, 56)
    pygame.draw.rect(canvas, HOME_RED, (290, 26, 62, 6))
    pygame.draw.circle(canvas, BLACK, (321, 68), 6)
    pygame.draw.rect(canvas, BLACK, (314, 74, 14, 6))

    # Six lockers. Number 3 is open, with a referee shirt and shin pads inside.
    for i in range(6):
        x = 116 + i * 30
        y = FLOOR_Y - 78
        if i == 3:
            draw_open_locker(canvas, x, y)
        else:
            shaded_box(canvas, (90, 140, 210), (130, 175, 235), (60, 100, 170), x, y, 28, 78)
            for vent_y in range(y + 6, y + 20, 4):
                pygame.draw.rect(canvas, (60, 100, 170), (x + 7, vent_y, 14, 2))
            pygame.draw.rect(canvas, OUTLINE, (x + 20, y + 36, 3, 10))       # handle
            pygame.draw.rect(canvas, WHITE, (x + 6, y + 24, 16, 6))          # name tag
            pygame.draw.rect(canvas, (150, 150, 170), (x + 8, y + 26, 10, 1))
        if i == 1:
            pygame.draw.circle(canvas, YELLOW, (x + 10, y + 55), 4)          # sticker
        if i == 4:
            pygame.draw.rect(canvas, HOME_RED, (x + 6, y + 50, 8, 6))        # sticker

    # The bench with a folded towel, a water bottle and the half-eaten orange.
    shaded_box(canvas, (215, 150, 80), (245, 185, 110), (170, 110, 60), 140, 172, 150, 7)
    for leg_x in [148, 278]:
        outlined_box(canvas, (160, 100, 55), leg_x, 180, 5, 19)
    outlined_box(canvas, WHITE, 160, 164, 22, 8)
    pygame.draw.rect(canvas, (120, 200, 230), (160, 167, 22, 2))
    outlined_box(canvas, (100, 180, 240), 200, 154, 7, 18)
    pygame.draw.rect(canvas, HOME_RED, (200, 152, 7, 3))
    pygame.draw.circle(canvas, OUTLINE, (255, 168), 6)
    pygame.draw.circle(canvas, (250, 150, 40), (255, 168), 5)
    pygame.draw.rect(canvas, (255, 230, 170), (250, 162, 5, 6))                # the bite
    pygame.draw.rect(canvas, (250, 150, 40), (266, 169, 4, 2))                 # peel
    pygame.draw.rect(canvas, (250, 150, 40), (240, 170, 3, 2))

    # Under the bench: muddy boots and a kit bag.
    for boot_x in [175, 191]:
        outlined_box(canvas, (40, 40, 45), boot_x, 191, 13, 9)
        pygame.draw.rect(canvas, (120, 80, 50), (boot_x, 196, 13, 4))         # mud
    outlined_box(canvas, (30, 30, 45), 215, 184, 40, 16)
    pygame.draw.rect(canvas, HOME_RED, (215, 189, 40, 3))
    pygame.draw.rect(canvas, OUTLINE, (228, 180, 14, 4))

    # A bin with paper cups.
    outlined_box(canvas, (120, 130, 150), 350, 180, 18, 20)
    outlined_box(canvas, WHITE, 352, 175, 5, 6)
    outlined_box(canvas, WHITE, 360, 177, 5, 4)

    draw_shower(canvas)
    draw_tile_floor(canvas)


def draw_open_locker(canvas, x, y):
    # An open locker: dark inside, a hanging referee shirt, yellow shin pads,
    # and the door sticking out to the right.
    outlined_box(canvas, (40, 50, 80), x, y, 28, 78)
    pygame.draw.rect(canvas, (60, 75, 110), (x + 2, y + 2, 24, 3))             # shelf
    pygame.draw.rect(canvas, OUTLINE, (x + 12, y + 8, 4, 3))                   # hanger
    pygame.draw.rect(canvas, OUTLINE, (x + 4, y + 11, 20, 30))
    pygame.draw.rect(canvas, (30, 30, 42), (x + 5, y + 12, 18, 28))
    pygame.draw.rect(canvas, WHITE, (x + 11, y + 12, 6, 2))
    outlined_box(canvas, YELLOW, x + 6, y + 56, 6, 12)
    outlined_box(canvas, YELLOW, x + 15, y + 56, 6, 12)
    pygame.draw.polygon(canvas, OUTLINE, [(x + 28, y - 1), (x + 40, y + 4), (x + 40, y + 74), (x + 28, y + 79)])
    pygame.draw.polygon(canvas, (110, 160, 225), [(x + 29, y + 1), (x + 39, y + 5), (x + 39, y + 73), (x + 29, y + 77)])


def draw_shower(canvas):
    # The shower corner: tiles, a striped curtain, water drops and steam.
    outlined_box(canvas, (150, 200, 215), 392, 22, 84, 178)
    for y in range(22, 200, 12):
        for x in range(392, 476, 12):
            pygame.draw.rect(canvas, (170, 215, 230), (x + 1, y + 1, 11, 11))
    pygame.draw.rect(canvas, OUTLINE, (392, 26, 84, 2))                      # curtain rail
    for i in range(6):
        if i % 2 == 0:
            stripe = WHITE
        else:
            stripe = (240, 120, 120)
        pygame.draw.rect(canvas, stripe, (393 + i * 5, 28, 5, 150))
    pygame.draw.rect(canvas, OUTLINE, (423, 28, 1, 150))
    outlined_box(canvas, (200, 205, 215), 448, 34, 14, 5)                     # shower head
    for drop_x, drop_y in [(450, 50), (456, 62), (452, 78), (459, 92), (449, 105)]:
        pygame.draw.rect(canvas, (90, 160, 230), (drop_x, drop_y, 1, 3))

    # See-through steam clouds (transparency 120 out of 255).
    steam = pygame.Surface((CANVAS_WIDTH, CANVAS_HEIGHT), pygame.SRCALPHA)
    for steam_x, steam_y, size in [(430, 60, 14), (455, 45, 12), (470, 75, 10), (440, 95, 13), (400, 50, 9)]:
        pygame.draw.circle(steam, (255, 255, 255, 120), (steam_x, steam_y), size)
    canvas.blit(steam, (0, 0))


# ---------------------------------------------------------------- Mascot Changing Room

def draw_mascot_room(canvas, pombo_picture):
    # Purple striped wallpaper with darker wooden panels below.
    canvas.fill((215, 180, 230))
    for x in range(0, CANVAS_WIDTH, 24):
        pygame.draw.rect(canvas, (205, 168, 222), (x, 0, 12, FLOOR_Y))
    pygame.draw.rect(canvas, OUTLINE, (0, 139, CANVAS_WIDTH, 1))
    pygame.draw.rect(canvas, (150, 100, 170), (0, 140, CANVAS_WIDTH, 60))
    for x in range(0, CANVAS_WIDTH, 20):
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
    outlined_box(canvas, (220, 190, 140), 432, 168, 24, 32)
    pygame.draw.rect(canvas, (190, 155, 100), (432, 168, 24, 4))
    outlined_box(canvas, (200, 140, 80), 92, 180, 30, 20)
    for i in range(0, 30, 4):
        pygame.draw.rect(canvas, (170, 110, 55), (92 + i, 181, 2, 19))
    for feather_x in [96, 104, 112, 118]:
        pygame.draw.circle(canvas, OUTLINE, (feather_x, 179), 4)
        pygame.draw.circle(canvas, (200, 205, 220), (feather_x, 179), 3)

    # Pombo's bench, and Pombo himself.
    shaded_box(canvas, (215, 150, 80), (245, 185, 110), (170, 110, 60), 336, 178, 92, 6)
    for leg_x in [342, 418]:
        outlined_box(canvas, (160, 100, 55), leg_x, 185, 5, 15)
    canvas.blit(pombo_picture, (362, FLOOR_Y - pombo_picture.get_height()))

    draw_carpet(canvas, (130, 70, 150), (160, 100, 180), (100, 50, 120))

    # Feathers on the floor and floating in the air.
    for feather_x, feather_y in [(90, FLOOR_Y + 8), (165, FLOOR_Y + 14), (262, FLOOR_Y + 9),
                                 (325, FLOOR_Y + 20), (455, FLOOR_Y + 12),
                                 (270, 120), (420, 90), (190, 70)]:
        draw_feather(canvas, feather_x, feather_y)


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

def draw_reporter(canvas, x, hair, hair_light, style, shirt, shirt_light):
    # A reporter seen from behind, sitting on a chair.
    # style is "plain", "bald", "ponytail", "cap" or "curly".
    shaded_box(canvas, (60, 60, 75), (85, 85, 100), (40, 40, 52), x - 2, 168, 30, 32)   # chair

    # Back and shoulders.
    pygame.draw.rect(canvas, OUTLINE, (x + 1, 150, 24, 20))
    pygame.draw.rect(canvas, shirt, (x + 2, 151, 22, 19))
    pygame.draw.rect(canvas, shirt_light, (x + 2, 151, 22, 3))

    # The back of the head.
    pygame.draw.circle(canvas, OUTLINE, (x + 13, 141), 9)
    if style == "bald":
        pygame.draw.circle(canvas, SKIN, (x + 13, 141), 8)
        pygame.draw.rect(canvas, (255, 230, 205), (x + 9, 135, 4, 2))         # shiny head
        pygame.draw.rect(canvas, hair, (x + 6, 142, 14, 4))
    else:
        pygame.draw.circle(canvas, hair, (x + 13, 141), 8)
        pygame.draw.rect(canvas, hair_light, (x + 9, 135, 5, 2))
    if style == "ponytail":
        pygame.draw.circle(canvas, OUTLINE, (x + 13, 152), 4)
        pygame.draw.circle(canvas, hair, (x + 13, 152), 3)
    if style == "cap":
        pygame.draw.rect(canvas, OUTLINE, (x + 4, 133, 18, 7))
        pygame.draw.rect(canvas, HOME_RED, (x + 5, 134, 16, 5))
    if style == "curly":
        for dx, dy in [(-7, -3), (7, -3), (0, -8), (-5, 4), (5, 4)]:
            pygame.draw.circle(canvas, OUTLINE, (x + 13 + dx, 141 + dy), 5)
            pygame.draw.circle(canvas, hair, (x + 13 + dx, 141 + dy), 4)

    # Ears.
    pygame.draw.rect(canvas, SKIN, (x + 3, 141, 2, 3))
    pygame.draw.rect(canvas, SKIN, (x + 21, 141, 2, 3))


def draw_press_room(canvas):
    canvas.fill((45, 60, 110))
    draw_ceiling_lamps(canvas, [80, 200, 320, 430])
    draw_door(canvas, 20, (110, 170, 255), (70, 120, 210))     # back to the booth

    draw_sponsor_wall(canvas)
    draw_press_table(canvas)
    draw_tv_camera(canvas)

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
    for hair, hair_light, style, shirt, shirt_light in reporters:
        draw_reporter(canvas, x, hair, hair_light, style, shirt, shirt_light)
        x = x + 30

    # One reporter holds up a phone, another a camera that is flashing.
    outlined_box(canvas, (30, 30, 40), 125, 118, 8, 14)
    pygame.draw.rect(canvas, (120, 200, 255), (126, 119, 6, 11))
    pygame.draw.rect(canvas, SKIN, (127, 132, 4, 8))
    outlined_box(canvas, (50, 50, 60), 213, 114, 18, 12)
    pygame.draw.circle(canvas, (150, 200, 255), (222, 120), 4)
    pygame.draw.rect(canvas, SKIN, (218, 126, 4, 10))
    flash = pygame.Surface((40, 40), pygame.SRCALPHA)
    pygame.draw.circle(flash, (255, 255, 255, 110), (20, 20), 18)
    canvas.blit(flash, (202, 100))
    for dx, dy in [(-10, 0), (10, 0), (0, -10), (0, 10)]:
        pygame.draw.line(canvas, WHITE, (222, 120), (222 + dx, 120 + dy), 2)

    draw_carpet(canvas, (40, 70, 150), (70, 100, 180), (25, 45, 110))


def draw_sponsor_wall(canvas):
    # A blue wall covered in a repeating pattern of four kinds of logos,
    # with the red club banner in the middle.
    outlined_box(canvas, (35, 100, 190), 90, 22, 386, 128)
    for row in range(6):
        for column in range(10):
            x = 96 + column * 40 + (row % 2) * 20
            y = 28 + row * 20
            if x > 466:
                continue
            kind = (row + column) % 4
            if kind == 0:
                pygame.draw.rect(canvas, WHITE, (x, y, 16, 6))
            elif kind == 1:
                pygame.draw.circle(canvas, YELLOW, (x + 6, y + 3), 4)
                pygame.draw.rect(canvas, YELLOW, (x + 11, y + 1, 8, 3))
            elif kind == 2:
                pygame.draw.rect(canvas, (240, 110, 90), (x, y, 7, 7))
                pygame.draw.rect(canvas, WHITE, (x + 9, y + 2, 9, 3))
            else:
                pygame.draw.polygon(canvas, (120, 220, 160), [(x, y + 6), (x + 6, y), (x + 12, y + 6)])
    # The club banner with the crest.
    shaded_box(canvas, HOME_RED, (255, 120, 110), (180, 40, 40), 300, 28, 50, 62)
    pygame.draw.polygon(canvas, OUTLINE, [(300, 89), (325, 102), (350, 89)])
    pygame.draw.polygon(canvas, HOME_RED, [(302, 89), (325, 100), (348, 89)])
    pygame.draw.circle(canvas, OUTLINE, (325, 58), 13)
    pygame.draw.circle(canvas, WHITE, (325, 58), 12)
    pygame.draw.circle(canvas, HOME_RED, (325, 58), 8)
    pygame.draw.circle(canvas, WHITE, (325, 58), 3)


def draw_press_table(canvas):
    # The long press table with microphones, water bottles and a name card.
    shaded_box(canvas, (40, 60, 120), (70, 95, 160), (25, 40, 90), 270, 150, 120, 50)
    pygame.draw.rect(canvas, WHITE, (270, 150, 120, 4))
    pygame.draw.circle(canvas, OUTLINE, (330, 177), 10)
    pygame.draw.circle(canvas, HOME_RED, (330, 177), 9)
    pygame.draw.circle(canvas, WHITE, (330, 177), 4)
    microphones = [(300, HOME_RED), (312, YELLOW), (322, (90, 180, 110)),
                   (334, WHITE), (346, AWAY_BLUE), (358, (240, 140, 40))]
    for mic_x, colour in microphones:
        pygame.draw.line(canvas, OUTLINE, (mic_x + 2, 150), (330, 136))
        outlined_box(canvas, (40, 40, 50), mic_x, 128, 5, 7)
        pygame.draw.rect(canvas, (90, 90, 100), (mic_x + 1, 129, 3, 2))
        outlined_box(canvas, colour, mic_x - 1, 136, 7, 5)
    for bottle_x in [282, 372]:
        outlined_box(canvas, (180, 225, 255), bottle_x, 138, 6, 12)
        pygame.draw.rect(canvas, AWAY_BLUE, (bottle_x, 136, 6, 3))
    outlined_box(canvas, WHITE, 352, 143, 20, 7)                               # name card


def draw_tv_camera(canvas):
    # A TV camera on a tripod, and a fluffy boom microphone over the table.
    pygame.draw.line(canvas, OUTLINE, (420, 200), (436, 150), 2)
    pygame.draw.line(canvas, OUTLINE, (452, 200), (436, 150), 2)
    pygame.draw.line(canvas, OUTLINE, (436, 200), (436, 150), 2)
    shaded_box(canvas, (60, 60, 70), (90, 90, 100), (35, 35, 45), 420, 132, 34, 20)
    outlined_box(canvas, (30, 30, 40), 408, 136, 12, 12)
    pygame.draw.circle(canvas, (120, 190, 255), (414, 142), 4)
    pygame.draw.rect(canvas, (230, 40, 40), (448, 135, 3, 3))                  # "recording"
    pygame.draw.line(canvas, OUTLINE, (460, 60), (350, 110), 2)                # boom pole
    outlined_box(canvas, (110, 110, 120), 338, 108, 18, 8)
    for i in range(0, 18, 3):
        pygame.draw.rect(canvas, (150, 150, 160), (338 + i, 108, 1, 8))


# ---------------------------------------------------------------- The Pitch

# Where the people stand on the pitch (x positions on the canvas).
LINESMAN_X = 110
STRIKER_X = 196
BALL_X = 258
REFEREE_X = 296
CAPTAIN_X = 322


def draw_pitch(canvas, pictures):
    draw_stadium(canvas)

    # Advertising boards along the side of the pitch.
    boards = [(YELLOW, OUTLINE), ((70, 110, 230), WHITE), (WHITE, HOME_RED), ((90, 180, 110), WHITE)]
    for i in range(8):
        background, writing = boards[i % 4]
        outlined_box(canvas, background, i * 60 + 1, 149, 58, 15)
        pygame.draw.rect(canvas, writing, (i * 60 + 12, 154, 34, 4))
        pygame.draw.rect(canvas, writing, (i * 60 + 6, 154, 4, 4))

    # The grass with mowing stripes, all the way down, and the white lines.
    for i in range(0, CANVAS_WIDTH, 30):
        if (i // 30) % 2 == 0:
            colour = (80, 190, 80)
        else:
            colour = (100, 210, 95)
        pygame.draw.rect(canvas, colour, (i, 165, 30, CANVAS_HEIGHT - 165))
    pygame.draw.rect(canvas, WHITE, (0, 172, CANVAS_WIDTH, 1))
    pygame.draw.rect(canvas, WHITE, (0, FLOOR_Y + 2, CANVAS_WIDTH, 2))

    # The tunnel back inside.
    outlined_box(canvas, (140, 140, 155), 8, 130, 64, 70)
    pygame.draw.rect(canvas, (40, 45, 60), (16, 138, 48, 62))
    pygame.draw.rect(canvas, HOME_RED, (8, 130, 64, 6))

    # A corner flag.
    pygame.draw.rect(canvas, OUTLINE, (90, 176, 1, 26))
    pygame.draw.polygon(canvas, YELLOW, [(91, 176), (100, 179), (91, 182)])

    draw_goal(canvas)

    # The people: linesman, striker, referee and the away captain.
    for name, x in [("linesman", LINESMAN_X), ("striker", STRIKER_X),
                    ("referee", REFEREE_X), ("captain", CAPTAIN_X)]:
        picture = pictures[name]
        canvas.blit(picture, (x, FLOOR_Y - picture.get_height()))

    # The linesman's flag, held up in his hand.
    flag_x = LINESMAN_X + 26
    pygame.draw.rect(canvas, OUTLINE, (flag_x, 150, 1, 30))
    pygame.draw.rect(canvas, OUTLINE, (flag_x, 149, 11, 9))
    pygame.draw.rect(canvas, YELLOW, (flag_x + 1, 150, 9, 7))
    pygame.draw.rect(canvas, HOME_RED, (flag_x + 1, 150, 4, 3))
    pygame.draw.rect(canvas, HOME_RED, (flag_x + 5, 153, 5, 4))

    # A speech bubble over the captain ("OFFSIDE!" is added as text).
    outlined_box(canvas, WHITE, CAPTAIN_X - 8, 140, 34, 12)
    pygame.draw.polygon(canvas, OUTLINE, [(CAPTAIN_X + 4, 152), (CAPTAIN_X + 2, 158), (CAPTAIN_X + 10, 152)])

    # The ball, with a little shadow.
    ball = pictures["ball"]
    pygame.draw.ellipse(canvas, (50, 140, 50), (BALL_X, FLOOR_Y - 2, 10, 4))
    canvas.blit(ball, (BALL_X, FLOOR_Y - ball.get_height() + 1))


def draw_stadium(canvas):
    # Sky, roof, two tiers of fans with the scoreboard, and floodlights.
    pygame.draw.rect(canvas, (110, 190, 250), (0, 0, CANVAS_WIDTH, 20))
    pygame.draw.rect(canvas, (140, 205, 255), (0, 20, CANVAS_WIDTH, 14))
    draw_cloud(canvas, 40, 6)
    draw_cloud(canvas, 250, 3)

    # The roof.
    pygame.draw.rect(canvas, OUTLINE, (0, 33, CANVAS_WIDTH, 9))
    pygame.draw.rect(canvas, (200, 205, 215), (0, 34, CANVAS_WIDTH, 7))
    for x in range(0, CANVAS_WIDTH, 16):
        pygame.draw.line(canvas, (150, 155, 170), (x, 34), (x + 8, 40))

    # Upper tier: small fans. The colour of each fan comes from a calculation,
    # so the crowd looks mixed but always the same.
    fan_colours = [WHITE, YELLOW, (255, 120, 120), SKIN, AWAY_BLUE, (235, 70, 70)]
    pygame.draw.rect(canvas, (60, 60, 80), (0, 42, CANVAS_WIDTH, 50))
    for fan_y in range(44, 90, 4):
        for fan_x in range(1 + (fan_y // 4) % 2 * 2, CANVAS_WIDTH, 4):
            colour = fan_colours[(fan_x * 7 + fan_y * 3) % 6]
            pygame.draw.rect(canvas, colour, (fan_x, fan_y, 2, 2))

    # The scoreboard (the text is added later).
    shaded_box(canvas, (20, 20, 30), (60, 60, 75), (10, 10, 15), 190, 46, 100, 34)
    pygame.draw.rect(canvas, HOME_RED, (194, 50, 30, 10))
    pygame.draw.rect(canvas, AWAY_BLUE, (256, 50, 30, 10))
    pygame.draw.rect(canvas, (255, 200, 40), (194, 66, 92, 10))

    # A red banner between the tiers.
    pygame.draw.rect(canvas, OUTLINE, (0, 92, CANVAS_WIDTH, 3))
    pygame.draw.rect(canvas, HOME_RED, (0, 95, CANVAS_WIDTH, 7))
    for x in range(0, CANVAS_WIDTH, 40):
        pygame.draw.rect(canvas, WHITE, (x + 6, 97, 22, 3))

    # Lower tier: bigger fans, some with their arms up.
    pygame.draw.rect(canvas, (70, 70, 95), (0, 102, CANVAS_WIDTH, 46))
    for fan_y in range(105, 146, 7):
        for fan_x in range(2 + (fan_y // 7) % 2 * 4, CANVAS_WIDTH, 8):
            colour = fan_colours[(fan_x * 3 + fan_y) % 6]
            pygame.draw.rect(canvas, SKIN, (fan_x + 1, fan_y, 3, 3))
            pygame.draw.rect(canvas, colour, (fan_x, fan_y + 3, 5, 3))
            if (fan_x + fan_y) % 3 == 0:
                pygame.draw.rect(canvas, SKIN, (fan_x - 1, fan_y - 2, 1, 3))
                pygame.draw.rect(canvas, SKIN, (fan_x + 5, fan_y - 2, 1, 3))

    # A fan waving a red and white flag.
    pygame.draw.rect(canvas, OUTLINE, (150, 98, 1, 20))
    pygame.draw.polygon(canvas, HOME_RED, [(151, 98), (166, 101), (151, 106)])
    pygame.draw.polygon(canvas, WHITE, [(151, 102), (166, 101), (151, 106)])

    # Two floodlights.
    for light_x in [60, 420]:
        outlined_box(canvas, (90, 90, 100), light_x - 14, 2, 30, 14)
        for i in range(3):
            pygame.draw.rect(canvas, (255, 250, 200), (light_x - 12 + i * 10, 4, 8, 10))


def draw_goal(canvas):
    # The goal on the right: a shadow, the net and the white posts.
    shadow = pygame.Surface((70, 10), pygame.SRCALPHA)
    pygame.draw.ellipse(shadow, (0, 60, 0, 70), (0, 0, 70, 10))
    canvas.blit(shadow, (410, 196))
    pygame.draw.rect(canvas, (235, 240, 250), (420, 140, 55, 60))
    for net_x in range(420, 475, 4):
        pygame.draw.line(canvas, (195, 200, 215), (net_x, 140), (net_x + 6, 199))
    for net_y in range(140, 200, 4):
        pygame.draw.line(canvas, (195, 200, 215), (420, net_y), (474, net_y))
    outlined_box(canvas, WHITE, 414, 134, 62, 5)
    outlined_box(canvas, WHITE, 414, 134, 5, 66)

    # Two photographers kneeling next to the goal.
    for photographer_x in [372, 392]:
        pygame.draw.rect(canvas, OUTLINE, (photographer_x, 186, 14, 14))
        pygame.draw.rect(canvas, (60, 60, 80), (photographer_x + 1, 187, 12, 13))
        pygame.draw.circle(canvas, OUTLINE, (photographer_x + 7, 182), 5)
        pygame.draw.circle(canvas, (110, 75, 50), (photographer_x + 7, 182), 4)
        outlined_box(canvas, (30, 30, 40), photographer_x - 7, 184, 9, 6)
        pygame.draw.rect(canvas, (60, 60, 70), (photographer_x - 13, 185, 7, 4))


# ---------------------------------------------------------------- choosing a room

def draw_room(canvas, scene_id, pictures):
    # Draw the room that belongs to a scene id from story.json.
    # pictures holds the characters and objects that live in the rooms.
    if scene_id == "booth":
        draw_booth(canvas)
    elif scene_id == "dressing_room":
        draw_dressing_room(canvas)
    elif scene_id == "mascot_room":
        draw_mascot_room(canvas, pictures["pombo"])
    elif scene_id == "press_room":
        draw_press_room(canvas)
    elif scene_id == "pitch":
        draw_pitch(canvas, pictures)


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
        ("SEEDS", 433, 180, (120, 80, 30), True),
    ],
    "press_room": [
        ("BOOTH", 28, 110, (255, 255, 255), False),
        ("Ref. Unit", 353, 143, (40, 40, 60), True),
    ],
    "pitch": [
        ("BOOTH", 25, 120, (255, 255, 255), False),
        ("HOME", 195, 50, (255, 255, 255), False),
        ("1 - 0", 229, 50, (255, 255, 255), False),
        ("AWAY", 258, 50, (255, 255, 255), False),
        ("VAR CHECK", 210, 66, (30, 20, 20), False),
        ("OFFSIDE!", CAPTAIN_X - 6, 141, (230, 40, 40), True),
    ],
}
