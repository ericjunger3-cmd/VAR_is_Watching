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
HOME_RED = (220, 25, 55)
AWAY_YELLOW = (250, 220, 20)
SKIN = (250, 200, 160)
YELLOW = (250, 210, 60)
SKY = (150, 200, 240)
NOTE_YELLOW = (255, 225, 70)

# The shirt colours of the fans in the stadium: home fans (left half) in
# red and white, away fans (right half) in yellow and black.
HOME_FANS = [WHITE, HOME_RED, (255, 120, 120), WHITE, (235, 70, 70), HOME_RED]
AWAY_FANS = [AWAY_YELLOW, YELLOW, BLACK, AWAY_YELLOW, (255, 235, 120), YELLOW]


def fan_colour(fan_x, number):
    # The shirt colour of one fan. Fans on the left half of the room are
    # home fans, on the right half away fans. number comes from a small
    # calculation, so the crowd looks mixed but always stays the same.
    if fan_x < ROOM_WIDTH // 2:
        colours = HOME_FANS
    else:
        colours = AWAY_FANS
    return colours[number % len(colours)]


# ---------------------------------------------------------------- shared parts

def bob(tick, phase):
    # Returns 0 or 1: characters move up by one pixel half of the time,
    # which looks like breathing. tick counts the frames; phase makes not
    # everybody breathe at the same moment.
    return ((tick + phase) // 20) % 2


def float_lift(tick):
    # Returns 0, 1 or 2: how many pixels an item floats up right now, like
    # the items in Zelda or Mario. math.sin goes smoothly from -1 to 1 and
    # back, so +1 makes it 0 to 2 and the item rises and sinks slowly.
    return int(round(math.sin(tick / 15) + 1))


def draw_sparkle(canvas, x, y, tick, phase):
    # A small white star that flashes on an item for a moment every two
    # seconds (120 frames), so the eye notices the item. It grows and
    # shrinks again. phase makes not every item sparkle at the same moment.
    moment = (tick + phase) % 120
    if moment >= 12:
        return
    if moment >= 4 and moment < 8:
        size = 2      # the middle of the flash: the biggest star
    else:
        size = 1
    pygame.draw.line(canvas, WHITE, (x - size, y), (x + size, y))
    pygame.draw.line(canvas, WHITE, (x, y - size), (x, y + size))
    canvas.set_at((x, y), (255, 250, 200))


def draw_marker(canvas, x, y, tick):
    # A yellow "!" floating above something you can use, like in many
    # adventure games. (x, y) is the point just below the "!". It bounces:
    # abs() makes the sine wave always positive, like a hopping ball.
    bounce = int(abs(math.sin(tick / 10)) * 3)
    top = y - 12 - bounce
    # The stick of the "!": a dark outline, yellow inside, a light edge.
    pygame.draw.rect(canvas, OUTLINE, (x - 2, top, 5, 8))
    pygame.draw.rect(canvas, YELLOW, (x - 1, top + 1, 3, 6))
    pygame.draw.rect(canvas, (255, 245, 170), (x - 1, top + 1, 1, 6))
    # The dot of the "!".
    pygame.draw.rect(canvas, OUTLINE, (x - 2, top + 8, 5, 4))
    pygame.draw.rect(canvas, YELLOW, (x - 1, top + 9, 3, 2))


def draw_wall(canvas):
    # Cream wallpaper with soft stripes and a darker strip at the top.
    canvas.fill((246, 224, 180))
    pygame.draw.rect(canvas, (232, 205, 160), (0, 0, ROOM_WIDTH, 10))
    pygame.draw.rect(canvas, OUTLINE, (0, 10, ROOM_WIDTH, 1))
    for x in range(0, ROOM_WIDTH, 24):
        pygame.draw.rect(canvas, (240, 216, 170), (x, 11, 12, 140))
    # Less light near the ceiling and just above the panelling.
    draw_dark_band(canvas, 11, 10, 25)
    draw_dark_band(canvas, 11, 4, 25)
    draw_dark_band(canvas, 136, 11, 20)

    # Wood panelling on the lower part of the wall, with a rail on top.
    pygame.draw.rect(canvas, OUTLINE, (0, 147, ROOM_WIDTH, 1))
    pygame.draw.rect(canvas, (140, 80, 40), (0, 148, ROOM_WIDTH, 3))
    pygame.draw.rect(canvas, (175, 110, 60), (0, 148, ROOM_WIDTH, 1))
    pygame.draw.rect(canvas, (180, 110, 60), (0, 151, ROOM_WIDTH, 49))
    for x in range(0, ROOM_WIDTH, 20):
        pygame.draw.rect(canvas, (205, 135, 75), (x + 1, 152, 17, 46))   # plank
        pygame.draw.rect(canvas, (225, 160, 95), (x + 1, 152, 17, 2))    # light top
        pygame.draw.rect(canvas, (218, 150, 88), (x + 1, 152, 2, 46))    # light left side
        pygame.draw.rect(canvas, (150, 88, 48), (x + 1, 196, 17, 2))     # dark bottom
    draw_dark_band(canvas, 188, 12, 30)


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

    # Bricks. Every row is a bit taller, wider and lighter than the row
    # behind it (the same depth trick as in the other rooms), and every
    # second row is shifted by half a brick.
    y = FLOOR_Y + 7
    height = 7
    row = 0
    while y < CANVAS_HEIGHT:
        width = height * 2
        brick = (170 + row * 5, 108 + row * 5, 72 + row * 4)
        gap = darker(brick, 0.68)
        pygame.draw.rect(canvas, gap, (0, y, ROOM_WIDTH, height))
        shift = (row % 2) * (width // 2)
        for x in range(-width + shift, ROOM_WIDTH, width):
            pygame.draw.rect(canvas, brick, (x + 1, y + 1, width - 1, height - 1))
            pygame.draw.rect(canvas, (brick[0] + 25, brick[1] + 28, brick[2] + 22), (x + 1, y + 1, width - 1, 1))
            pygame.draw.rect(canvas, darker(brick, 0.85), (x + 1, y + height - 2, width - 1, 1))
        y = y + height
        height = height + 1
        row = row + 1


def draw_door(canvas, x, plaque_colour, plaque_shadow):
    # A wooden door, 40 wide and 72 high, standing on the floor,
    # with a coloured name plaque above it.
    y = FLOOR_Y - 72
    draw_shadow(canvas, x - 6, FLOOR_Y + 1, 52)

    # Door frame, with a light left edge (the light comes from the left).
    pygame.draw.rect(canvas, OUTLINE, (x - 4, y - 4, 48, 77))
    pygame.draw.rect(canvas, (120, 70, 40), (x - 3, y - 3, 46, 75))
    pygame.draw.rect(canvas, (155, 95, 55), (x - 3, y - 3, 2, 75))
    pygame.draw.rect(canvas, (155, 95, 55), (x - 3, y - 3, 46, 1))
    pygame.draw.rect(canvas, OUTLINE, (x - 1, y - 1, 42, 73))

    # The door itself: light left edge, dark right edge.
    pygame.draw.rect(canvas, (205, 130, 70), (x, y, 40, 72))
    pygame.draw.rect(canvas, (235, 165, 100), (x, y, 3, 72))
    pygame.draw.rect(canvas, (170, 100, 55), (x + 37, y, 3, 72))

    # Four panels that sit a bit deeper in the door: dark on the top and
    # left (in shadow), light on the bottom and right (catching light).
    panels = [(6, 6, 26), (22, 6, 26), (6, 38, 28), (22, 38, 28)]
    for panel_x, panel_y, panel_height in panels:
        left = x + panel_x
        top = y + panel_y
        pygame.draw.rect(canvas, (190, 118, 65), (left, top, 12, panel_height))
        pygame.draw.rect(canvas, (150, 88, 48), (left, top, 12, 1))
        pygame.draw.rect(canvas, (150, 88, 48), (left, top, 1, panel_height))
        pygame.draw.rect(canvas, (228, 158, 95), (left, top + panel_height - 1, 12, 1))
        pygame.draw.rect(canvas, (228, 158, 95), (left + 11, top, 1, panel_height))

    # Golden door knob with a shine.
    pygame.draw.rect(canvas, OUTLINE, (x + 31, y + 36, 5, 5))
    pygame.draw.rect(canvas, (255, 215, 70), (x + 32, y + 37, 3, 3))
    canvas.set_at((x + 32, y + 37), (255, 250, 200))

    # Name plaque (the text is added later, at full size), with a light top edge.
    pygame.draw.rect(canvas, OUTLINE, (x - 2, y - 20, 44, 14))
    pygame.draw.rect(canvas, plaque_shadow, (x - 1, y - 19, 42, 12))
    pygame.draw.rect(canvas, plaque_colour, (x - 1, y - 19, 42, 10))
    pygame.draw.rect(canvas, (min(255, plaque_colour[0] + 30), min(255, plaque_colour[1] + 30),
                              min(255, plaque_colour[2] + 30)), (x - 1, y - 19, 42, 1))


# ---------------------------------------------------------------- VAR Booth

def draw_window(canvas, tick):
    # A big window with sky, clouds, the stands and the pitch behind it.
    x = 10
    y = 18
    width = 196
    height = 62

    # White window frame with an outline, and a window sill below.
    pygame.draw.rect(canvas, OUTLINE, (x - 3, y - 3, width + 6, height + 6))
    pygame.draw.rect(canvas, WHITE, (x - 2, y - 2, width + 4, height + 4))
    pygame.draw.rect(canvas, OUTLINE, (x - 6, y + height + 2, width + 12, 5))
    pygame.draw.rect(canvas, (235, 230, 220), (x - 5, y + height + 3, width + 10, 3))
    pygame.draw.rect(canvas, WHITE, (x - 5, y + height + 3, width + 10, 1))

    # Sky in three shades of blue, darkest at the top.
    pygame.draw.rect(canvas, (110, 190, 250), (x, y, width, 10))
    pygame.draw.rect(canvas, (140, 210, 255), (x, y + 10, width, 10))
    pygame.draw.rect(canvas, (175, 225, 255), (x, y + 20, width, 16))

    # The clouds drift slowly to the right. set_clip makes sure nothing is
    # drawn outside the window glass; set_clip(None) turns that off again.
    canvas.set_clip((x, y, width, height))
    for start, cloud_y in [(20, 6), (120, 3), (170, 14)]:
        cloud_x = x - 30 + (start + tick // 8) % (width + 40)
        draw_cloud(canvas, cloud_x, y + cloud_y)
    canvas.set_clip(None)

    # The stands, full of fans. The colour of each fan comes from a
    # simple calculation, so the crowd looks mixed but never changes.
    pygame.draw.rect(canvas, (200, 70, 70), (x, y + 34, width, 16))
    fan_colours = [WHITE, YELLOW, (255, 120, 120), SKIN, AWAY_YELLOW]
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

    # A floodlight with a soft glow.
    glow = pygame.Surface((30, 20), pygame.SRCALPHA)
    pygame.draw.ellipse(glow, (255, 250, 210, 70), (0, 0, 30, 20))
    canvas.blit(glow, (x + 142, y - 5))
    pygame.draw.rect(canvas, (90, 90, 100), (x + 150, y + 2, 14, 6))
    pygame.draw.rect(canvas, (255, 250, 200), (x + 151, y + 3, 12, 4))

    # Reflections on the glass: two thin see-through white lines.
    shine = pygame.Surface((width, height), pygame.SRCALPHA)
    pygame.draw.line(shine, (255, 255, 255, 80), (20, height), (50, 0), 4)
    pygame.draw.line(shine, (255, 255, 255, 60), (34, height), (64, 0), 2)
    canvas.blit(shine, (x, y))

    # Two window bars.
    pygame.draw.rect(canvas, WHITE, (x + width // 3, y, 3, height))
    pygame.draw.rect(canvas, WHITE, (x + 2 * width // 3, y, 3, height))
    pygame.draw.rect(canvas, (215, 215, 225), (x + width // 3 + 2, y, 1, height))
    pygame.draw.rect(canvas, (215, 215, 225), (x + 2 * width // 3 + 2, y, 1, height))


def draw_cloud(canvas, x, y):
    # A fluffy cloud made of four white circles with a light blue bottom.
    pygame.draw.circle(canvas, WHITE, (x, y + 6), 6)
    pygame.draw.circle(canvas, WHITE, (x + 7, y + 2), 8)
    pygame.draw.circle(canvas, WHITE, (x + 16, y + 5), 6)
    pygame.draw.circle(canvas, WHITE, (x + 22, y + 7), 4)
    pygame.draw.rect(canvas, (215, 235, 255), (x - 5, y + 9, 31, 3))


def draw_monitors(canvas, tick, progress):
    # Twelve monitors in two rows of six. Eleven show a camera angle,
    # the last one is broken and has Dave's sticky note on it.
    # First a soft blue glow on the wall behind them, from all the screens.
    glow = pygame.Surface((220, 70), pygame.SRCALPHA)
    pygame.draw.ellipse(glow, (150, 200, 255, 18), (0, 0, 220, 70))
    canvas.blit(glow, (-4, 76))

    camera_number = 0
    for row in range(2):
        for column in range(6):
            x = 12 + column * 32
            y = 88 + row * 24

            if camera_number == 11:
                # The sabotaged monitor hangs crooked (see draw_crooked_monitor).
                draw_crooked_monitor(canvas, x, y, tick, progress)
            else:
                draw_monitor_frame(canvas, x, y)
                draw_camera(canvas, camera_number, x + 1, y + 1)
                # A small green power light that blinks now and then. Every
                # monitor blinks at another moment (camera_number * 13 shifts
                # the timing).
                if (tick + camera_number * 13) % 90 > 6:
                    canvas.set_at((x + 24, y + 18), (90, 230, 110))
                # A tiny shine in the top-left corner of the screen.
                canvas.set_at((x + 1, y + 1), (235, 245, 255))
            camera_number = camera_number + 1


def draw_monitor_frame(surface, x, y):
    # The frame of one monitor: light top edge, dark bottom edge.
    pygame.draw.rect(surface, OUTLINE, (x - 2, y - 2, 30, 22))
    pygame.draw.rect(surface, (90, 95, 115), (x - 1, y - 1, 28, 20))
    pygame.draw.rect(surface, (130, 135, 155), (x - 1, y - 1, 28, 1))
    pygame.draw.rect(surface, (60, 64, 80), (x - 1, y + 18, 28, 1))


def draw_crooked_monitor(canvas, x, y, tick, progress):
    # The monitor with the offside angle. Someone cut its cable (in another
    # room): it hangs crooked and its picture flickers.

    # 1. Draw the monitor on its own small see-through picture first,
    #    so we can turn the whole picture afterwards.
    picture = pygame.Surface((34, 26), pygame.SRCALPHA)
    draw_monitor_frame(picture, 4, 4)
    draw_broken_screen(picture, 5, 5, tick, progress)
    # Now and then the picture goes black for a moment (a flicker).
    # (tick * 7) % 50 < 4 is true for 4 frames out of every 50 or so.
    if (tick * 7) % 50 < 4:
        pygame.draw.rect(picture, (15, 15, 20), (5, 5, 24, 16))
    # The red power light blinks.
    if tick % 20 < 10:
        picture.set_at((28, 22), (230, 50, 50))

    # 2. Turn it 8 degrees (it hangs crooked) and put it where the
    #    monitor should be. get_rect(center=...) keeps the middle in place.
    turned = pygame.transform.rotate(picture, -8)
    middle = (x + 13, y + 9)
    canvas.blit(turned, turned.get_rect(center=middle))


def draw_sparks(canvas, x, y, tick):
    # Sparks fly out of a cut cable in short bursts: for 8 frames out of
    # every 40 there are a few yellow and white dots around the cable end.
    # random makes them jump around every frame.
    if tick % 40 >= 8:
        return
    for i in range(5):
        spark_x = x + random.randint(-5, 5)
        spark_y = y + random.randint(-3, 4)
        if random.randint(0, 1) == 0:
            colour = (255, 240, 120)
        else:
            colour = WHITE
        canvas.set_at((spark_x, spark_y), colour)


def draw_smoke(canvas, x, y, tick):
    # Three soft grey puffs of smoke rise from the cable, grow and fade out.
    # Each puff starts at another moment (puff * 30), so they never stop.
    for puff in range(3):
        age = (tick + puff * 30) % 90          # 0 to 89 frames old
        rise = age // 3                        # how far it has risen
        size = 2 + age // 15                   # it grows as it rises
        alpha = 200 - age * 2                  # and fades out
        if alpha <= 0:
            continue
        smoke = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
        pygame.draw.circle(smoke, (215, 215, 222, alpha), (size, size), size)
        # The smoke drifts a little to the left as it rises.
        canvas.blit(smoke, (x - size - age // 15, y - rise - size))


def draw_broken_screen(canvas, x, y, tick, progress):
    # The screen with the missing angle tells the player what to do:
    # 1. After the review it works again and shows the pitch.
    # 2. While you carry the USB Stick it glows green with a USB sign
    #    ("plug me in!").
    # 3. Before that it shows flickering static and a blinking red light.
    if "review" in progress["choices"]:
        draw_camera(canvas, 0, x, y)
    elif "usb" in progress["inventory"]:
        draw_usb_hint(canvas, x, y, tick)
    else:
        # TV static: random grey dots, different every frame, so it flickers.
        pygame.draw.rect(canvas, (40, 40, 48), (x, y, 24, 16))
        for i in range(60):
            dot_x = x + random.randint(0, 23)
            dot_y = y + random.randint(0, 15)
            brightness = random.randint(80, 240)
            canvas.set_at((dot_x, dot_y), (brightness, brightness, brightness))
        # A red "no signal" light that blinks: on for half a second, off
        # for half a second (30 frames each).
        if tick % 60 < 30:
            pygame.draw.rect(canvas, OUTLINE, (x + 1, y + 11, 9, 4))
            pygame.draw.rect(canvas, (230, 50, 50), (x + 2, y + 12, 7, 2))

    # Dave's sticky note with two scribbled lines.
    pygame.draw.rect(canvas, OUTLINE, (x + 12, y, 11, 11))
    pygame.draw.rect(canvas, NOTE_YELLOW, (x + 13, y + 1, 9, 9))
    pygame.draw.rect(canvas, (230, 190, 40), (x + 13, y + 8, 9, 2))
    pygame.draw.line(canvas, (150, 110, 40), (x + 14, y + 3), (x + 20, y + 3))
    pygame.draw.line(canvas, (150, 110, 40), (x + 14, y + 5), (x + 18, y + 5))


def draw_usb_hint(canvas, x, y, tick):
    # A dark green screen with a USB plug and an arrow pointing down
    # (into the computer). The green gets brighter and darker (it pulses).
    pulse = int((math.sin(tick / 8) + 1) * 40)      # 0 to 80
    pygame.draw.rect(canvas, (20, 60 + pulse // 2, 30), (x, y, 24, 16))
    green = (90, 170 + pulse, 100)
    # The plug: a metal tip on top of a body (only the left half of the
    # screen, because Dave's sticky note covers the right half).
    pygame.draw.rect(canvas, green, (x + 4, y + 2, 3, 2))       # metal tip
    pygame.draw.rect(canvas, green, (x + 3, y + 4, 5, 4))       # body
    # The arrow below the plug: a stick and a pointed end.
    pygame.draw.rect(canvas, green, (x + 5, y + 9, 1, 3))
    pygame.draw.line(canvas, green, (x + 3, y + 12), (x + 5, y + 14))
    pygame.draw.line(canvas, green, (x + 7, y + 12), (x + 5, y + 14))


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
        box(canvas, AWAY_YELLOW, x + 9, y + 10, 1, 2)
        box(canvas, HOME_RED, x + 16, y + 5, 1, 2)
        box(canvas, AWAY_YELLOW, x + 19, y + 11, 1, 2)
        box(canvas, WHITE, x + 13, y + 8, 1, 2)

    elif number == 1:
        # Spidercam from above: halfway line and centre circle.
        box(canvas, GRASS_LIGHT, x, y, 24, 16)
        box(canvas, WHITE, x, y + 8, 24, 1)
        pygame.draw.circle(canvas, WHITE, (x + 12, y + 8), 5, 1)
        canvas.set_at((x + 4, y + 3), HOME_RED)
        canvas.set_at((x + 18, y + 12), AWAY_YELLOW)
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
        box(canvas, AWAY_YELLOW, x + 3, y + 10, 18, 6)
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
        fan_colours = [WHITE, YELLOW, (255, 130, 130), SKIN, AWAY_YELLOW]
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
    # The wooden desk with drawers, a keyboard, a mug and a stack of papers.
    draw_shadow(canvas, 0, FLOOR_Y + 1, 214)
    pygame.draw.rect(canvas, OUTLINE, (4, 163, 206, 38))
    pygame.draw.rect(canvas, (215, 140, 70), (5, 164, 204, 6))     # desk top
    pygame.draw.rect(canvas, (245, 175, 100), (5, 164, 204, 2))    # light edge
    pygame.draw.rect(canvas, (170, 100, 50), (5, 170, 204, 30))    # front
    pygame.draw.rect(canvas, (150, 88, 45), (5, 170, 204, 2))      # shadow under the top
    pygame.draw.rect(canvas, (140, 80, 40), (5, 196, 204, 4))      # dark bottom

    # Two drawers that stick out a little: light top, dark bottom.
    for drawer_x in [12, 150]:
        pygame.draw.rect(canvas, OUTLINE, (drawer_x, 174, 50, 22))
        pygame.draw.rect(canvas, (190, 115, 60), (drawer_x + 1, 175, 48, 20))
        pygame.draw.rect(canvas, (215, 140, 80), (drawer_x + 1, 175, 48, 1))
        pygame.draw.rect(canvas, (160, 95, 50), (drawer_x + 1, 194, 48, 1))
        pygame.draw.rect(canvas, OUTLINE, (drawer_x + 22, 183, 6, 2))
        pygame.draw.rect(canvas, (230, 200, 150), (drawer_x + 22, 183, 6, 1))

    # Keyboard with little keys.
    pygame.draw.rect(canvas, OUTLINE, (78, 158, 52, 7))
    pygame.draw.rect(canvas, (220, 222, 235), (79, 159, 50, 5))
    pygame.draw.rect(canvas, (245, 246, 252), (79, 159, 50, 1))
    for key_x in range(81, 128, 4):
        canvas.set_at((key_x, 161), (150, 150, 170))

    # A white mug with a red stripe.
    pygame.draw.rect(canvas, OUTLINE, (150, 152, 11, 12))
    pygame.draw.rect(canvas, WHITE, (151, 153, 9, 10))
    pygame.draw.rect(canvas, (220, 222, 230), (157, 153, 3, 10))
    pygame.draw.rect(canvas, (230, 70, 70), (151, 157, 9, 3))
    pygame.draw.rect(canvas, OUTLINE, (161, 155, 3, 5))
    pygame.draw.rect(canvas, (120, 70, 40), (152, 153, 7, 1))                 # coffee

    # A messy stack of papers.
    for i in range(3):
        outlined_box(canvas, (245, 245, 238), 172 + i, 160 - i * 2, 22, 2)
    pygame.draw.rect(canvas, (170, 175, 190), (176, 155, 12, 1))

    # The office chair, seen from behind: backrest, pole and wheels.
    draw_shadow(canvas, 92, FLOOR_Y + 1, 32)
    shaded_box(canvas, (50, 52, 66), (80, 82, 100), (32, 33, 44), 96, 166, 24, 18)
    pygame.draw.rect(canvas, OUTLINE, (106, 185, 4, 9))
    pygame.draw.rect(canvas, (120, 125, 140), (107, 185, 2, 8))
    pygame.draw.rect(canvas, OUTLINE, (95, 194, 26, 3))
    for wheel_x in [95, 106, 117]:
        pygame.draw.rect(canvas, OUTLINE, (wheel_x, 196, 4, 4))


def draw_tunnel(canvas):
    # A stone archway to the pitch, with daylight at the end.
    x = 412
    stone = (140, 140, 155)
    pygame.draw.rect(canvas, OUTLINE, (x - 2, 128, 66, 73))
    pygame.draw.ellipse(canvas, OUTLINE, (x - 2, 110, 66, 40))
    pygame.draw.rect(canvas, stone, (x, 130, 62, 70))
    pygame.draw.ellipse(canvas, stone, (x, 112, 62, 36))

    # Stone blocks on the two pillars: a dark joint line every 8 pixels,
    # and a light top edge on every block.
    for block_y in range(136, 200, 8):
        for pillar_x in [x, x + 56]:
            pygame.draw.rect(canvas, (110, 110, 125), (pillar_x, block_y, 6, 1))
            pygame.draw.rect(canvas, (170, 170, 185), (pillar_x, block_y + 1, 6, 1))
    # The keystone at the top of the arch.
    outlined_box(canvas, (165, 165, 180), x + 26, 112, 10, 8)

    # The dark inside of the tunnel: darker at the edges, lighter
    # towards the daylight in the middle.
    pygame.draw.rect(canvas, (40, 44, 62), (x + 6, 136, 50, 64))
    pygame.draw.ellipse(canvas, (40, 44, 62), (x + 6, 120, 50, 32))
    pygame.draw.rect(canvas, (55, 60, 80), (x + 12, 140, 38, 60))
    pygame.draw.ellipse(canvas, (55, 60, 80), (x + 12, 128, 38, 26))

    # Light at the end: sky and grass.
    pygame.draw.rect(canvas, (180, 225, 255), (x + 18, 150, 26, 10))
    pygame.draw.rect(canvas, (255, 250, 210), (x + 18, 160, 26, 16))
    pygame.draw.rect(canvas, (120, 210, 110), (x + 14, 176, 34, 24))

    # Daylight spills out of the tunnel onto the floor.
    spill = pygame.Surface((90, 16), pygame.SRCALPHA)
    pygame.draw.polygon(spill, (255, 250, 210, 45), [(20, 0), (70, 0), (90, 16), (0, 16)])
    canvas.blit(spill, (x - 14, FLOOR_Y))


# The window, the monitors and the desk stand 58 pixels to the right of
# the left wall, so there is room for the Server Room door on the left.
BOOTH_SHIFT = 58

# The red cable of the offside camera: it goes from the crooked monitor
# down, then left along the wall and into the Server Room door.
RED_CABLE = [(236, 128), (236, 141), (40, 141)]


def draw_booth(canvas, pictures, progress, tick):
    # Draw the whole VAR Booth, from the back to the front.
    draw_wall(canvas)
    draw_floor(canvas)

    # The window, the monitors and the desk are drawn on a "subsurface":
    # a part of the canvas that starts BOOTH_SHIFT pixels to the right.
    # Everything drawn on it at x = 0 lands on the canvas at x = 58.
    shifted = canvas.subsurface((BOOTH_SHIFT, 0, ROOM_WIDTH - BOOTH_SHIFT, CANVAS_HEIGHT))
    draw_window(shifted, tick)
    draw_monitors(shifted, tick, progress)

    draw_red_cable(canvas)
    # The doors are drawn after the cable, so the cable disappears
    # behind the Server Room door.
    draw_door(canvas, 20, (230, 70, 70), (180, 45, 45))        # Server Room
    draw_door(canvas, 296, (250, 250, 250), (200, 200, 210))   # Referee's room
    draw_door(canvas, 354, (255, 210, 70), (215, 160, 40))     # Mascot room
    draw_tunnel(canvas)

    draw_desk(shifted)

    # Infantini's press pass lies behind the desk until you find it.
    # It floats up and down a little and sparkles, so you notice it.
    if "press_pass" not in progress["choices"]:
        lift = float_lift(tick)
        draw_press_pass(canvas, 82, 152 - lift)
        draw_sparkle(canvas, 95, 154 - lift, tick, 0)

    # The padlock hangs on the Mascot door until you have the whistle.
    if "whistle" not in progress["inventory"]:
        canvas.blit(pictures["padlock"], (368, 152))

    # The steward stands next to the tunnel to the pitch.
    steward = pictures["steward"]
    draw_shadow(canvas, 450, FLOOR_Y + 1, steward.get_width() + 4)
    canvas.blit(steward, (452, FLOOR_Y - steward.get_height() - bob(tick, 7)))


def draw_red_cable(canvas):
    # A thick red cable with a dark outline: first a wide dark line,
    # then a thinner red line on top, then a light line for the shine.
    pygame.draw.lines(canvas, OUTLINE, False, RED_CABLE, 5)
    pygame.draw.lines(canvas, (220, 40, 40), False, RED_CABLE, 3)
    pygame.draw.line(canvas, (255, 120, 110), (40, 140), (235, 140))
    # A white tag on the cable says which camera it belongs to
    # (the text "OFFSIDE CAM" is added later, see LABELS).
    pygame.draw.rect(canvas, OUTLINE, (190, 136, 40, 10))
    pygame.draw.rect(canvas, WHITE, (191, 137, 38, 8))


def draw_press_pass(canvas, x, y):
    # Infantini's press pass: a white card with a blue "PRESS" stripe,
    # a tiny photo (a bald head) and a few lines of text.
    pygame.draw.rect(canvas, OUTLINE, (x, y, 14, 11))
    pygame.draw.rect(canvas, WHITE, (x + 1, y + 1, 12, 9))
    pygame.draw.rect(canvas, (60, 110, 210), (x + 1, y + 1, 12, 3))
    pygame.draw.rect(canvas, (250, 200, 160), (x + 2, y + 5, 4, 4))      # the photo
    pygame.draw.line(canvas, (150, 150, 165), (x + 7, y + 6), (x + 11, y + 6))
    pygame.draw.line(canvas, (150, 150, 165), (x + 7, y + 8), (x + 10, y + 8))


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


def draw_fur_tuft(canvas, x, y):
    # A small tuft of brown fur (two light lines with a dark outline line).
    pygame.draw.line(canvas, OUTLINE, (x, y + 1), (x + 6, y - 2))
    pygame.draw.line(canvas, (190, 125, 75), (x + 1, y), (x + 6, y - 3))
    pygame.draw.line(canvas, (190, 125, 75), (x + 1, y - 1), (x + 5, y - 3))


# ---------------------------------------------------------------- floors

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
    # The floor comes before the furniture, so the shadows are drawn on top of it.
    draw_tile_floor(canvas, tick)

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
        pygame.draw.circle(canvas, AWAY_YELLOW, (x, y), 3, 1)
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
    draw_kit_cabinet(canvas, pictures, progress, tick)

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
    # Infantini's crumpled betting slip sticks out of the bin until you
    # find it. It floats up a little and sparkles, so you notice it.
    if "slip" not in progress["choices"]:
        lift = float_lift(tick)
        pygame.draw.circle(canvas, OUTLINE, (364, 174 - lift), 5)
        pygame.draw.circle(canvas, (225, 225, 215), (364, 174 - lift), 4)
        pygame.draw.circle(canvas, (250, 250, 240), (363, 173 - lift), 2)
        pygame.draw.line(canvas, (180, 180, 170), (361, 172 - lift), (366, 176 - lift))
        pygame.draw.line(canvas, (230, 60, 60), (365, 171 - lift), (362, 175 - lift))
        draw_sparkle(canvas, 367, 171 - lift, tick, 80)
    draw_ball_bag(canvas)

    draw_shower(canvas, tick)

    # The lamps shine down into the room.
    for lamp_x in [90, 230, 370]:
        draw_light_cone(canvas, lamp_x + 8, 13, FLOOR_Y, 14, 80)


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


def draw_kit_cabinet(canvas, pictures, progress, tick):
    # A small wooden cabinet with a drawer. Once the drawer is opened it
    # sticks out, and the Lucky Whistle lies in it until you take it.
    shaded_box(canvas, (190, 125, 70), (225, 160, 100), (150, 95, 55), 300, 160, 44, 40)
    if "drawer" in progress["choices"]:
        # The open drawer: the dark inside and the front pulled down a bit.
        outlined_box(canvas, (60, 40, 30), 303, 164, 38, 10)
        if "whistle" not in progress["inventory"]:
            # The whistle floats up out of the drawer and sparkles.
            lift = float_lift(tick)
            canvas.blit(pictures["whistle"], (306, 162 - lift))
            draw_sparkle(canvas, 310, 163 - lift, tick, 40)
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
    draw_mascot_wall(canvas)
    draw_wood_floor(canvas)
    draw_ceiling_lamps(canvas, [120, 330])
    draw_flag_garland(canvas)

    draw_door(canvas, 20, (255, 210, 70), (215, 160, 40))       # back to the booth

    # Framed "Employee of the Month" photo of Bernie.
    y = PHOTO_Y
    shaded_box(canvas, (250, 215, 90), (255, 240, 150), (200, 160, 40), 82, y, 40, 46)
    pygame.draw.rect(canvas, (150, 200, 240), (87, y + 5, 30, 30))
    pygame.draw.rect(canvas, (185, 220, 248), (87, y + 5, 30, 8))              # lighter sky
    pygame.draw.circle(canvas, (170, 105, 55), (95, y + 14), 3)                # ears
    pygame.draw.circle(canvas, (170, 105, 55), (109, y + 14), 3)
    pygame.draw.circle(canvas, (170, 105, 55), (102, y + 22), 9)
    pygame.draw.circle(canvas, (240, 215, 170), (102, y + 26), 5)              # muzzle
    pygame.draw.rect(canvas, OUTLINE, (100, y + 23, 4, 3))                     # nose
    pygame.draw.rect(canvas, OUTLINE, (98, y + 18, 2, 2))
    pygame.draw.rect(canvas, OUTLINE, (105, y + 18, 2, 2))
    pygame.draw.rect(canvas, HOME_RED, (87, y + 37, 30, 5))
    pygame.draw.rect(canvas, (255, 120, 110), (87, y + 37, 30, 1))

    draw_mascot_heads(canvas)
    draw_costume_rack(canvas)
    draw_ring_light(canvas, tick)
    draw_mirror_table(canvas, tick)

    # A big pot of honey with a lid, and a few drops spilled on the floor.
    draw_shadow(canvas, 452, 201, 32)
    shaded_box(canvas, (235, 170, 50), (255, 210, 100), (190, 125, 30), 456, 168, 24, 32)
    pygame.draw.polygon(canvas, OUTLINE, [(455, 168), (481, 168), (476, 160), (460, 160)])
    pygame.draw.polygon(canvas, (200, 165, 115), [(457, 167), (479, 167), (475, 161), (461, 161)])
    for drop_x, drop_y in [(446, 203), (450, 206), (441, 205), (444, 209)]:
        pygame.draw.rect(canvas, (240, 180, 50), (drop_x, drop_y, 2, 1))

    # A laundry basket full of spare fur, with a woven pattern.
    draw_shadow(canvas, 89, 201, 36)
    shaded_box(canvas, (200, 140, 80), (230, 175, 110), (160, 105, 55), 92, 180, 30, 20)
    for i in range(0, 30, 4):
        pygame.draw.rect(canvas, (170, 110, 55), (92 + i, 182, 2, 17))
    pygame.draw.rect(canvas, (230, 175, 110), (92, 189, 30, 1))
    for fur_x in [96, 104, 112, 118]:
        pygame.draw.circle(canvas, OUTLINE, (fur_x, 179), 4)
        pygame.draw.circle(canvas, (170, 105, 55), (fur_x, 179), 3)
        pygame.draw.circle(canvas, (205, 140, 85), (fur_x - 1, 178), 1)

    # The rug in front of Bernie's bench (an oval, flat on the floor).
    pygame.draw.ellipse(canvas, OUTLINE, (330, 204, 130, 22))
    pygame.draw.ellipse(canvas, (200, 90, 150), (331, 205, 128, 20))
    pygame.draw.ellipse(canvas, (240, 160, 200), (338, 207, 114, 16))
    pygame.draw.ellipse(canvas, (200, 90, 150), (360, 210, 70, 10), 1)

    # Bernie's bench, and Bernie himself.
    draw_shadow(canvas, 334, 201, 120)
    shaded_box(canvas, (215, 150, 80), (245, 185, 110), (170, 110, 60), 336, 178, 116, 6)
    for leg_x in [342, 442]:
        shaded_box(canvas, (160, 100, 55), (190, 125, 75), (120, 75, 40), leg_x, 185, 5, 15)
    draw_shadow(canvas, 360, 201, 44)
    draw_bernie(canvas, pictures, progress, tick, reveal)

    # The lamps shine down into the room.
    for lamp_x in [120, 330]:
        draw_light_cone(canvas, lamp_x + 8, 13, FLOOR_Y, 14, 90)

    # Tufts of fur on the floor.
    for tuft_x, tuft_y in [(70, FLOOR_Y + 8), (165, FLOOR_Y + 14), (262, FLOOR_Y + 9),
                                 (300, FLOOR_Y + 22), (470, FLOOR_Y + 14), (200, FLOOR_Y + 30)]:
        draw_fur_tuft(canvas, tuft_x, tuft_y)

    # Tufts of fur slowly falling through the air, swaying left and right.
    # When a tuft reaches the floor it starts again at the top.
    for start_x, offset in [(270, 0), (420, 60), (190, 120), (110, 30), (330, 90)]:
        fall = (tick // 2 + offset) % 180
        sway = ((tick // 15 + offset) % 3) - 1
        draw_fur_tuft(canvas, start_x + sway * 2, 15 + fall)


# Where things hang on the mascot room wall (moved down, so the timer
# and the pundit's speech box do not hide them).
PHOTO_Y = 56
MIRROR_Y = 66


def draw_mascot_wall(canvas):
    # Purple striped wallpaper with little diamonds, darker at the top,
    # and wooden panels below with a moulding rail.
    canvas.fill((215, 180, 230))
    for x in range(0, ROOM_WIDTH, 24):
        pygame.draw.rect(canvas, (205, 168, 222), (x, 0, 12, 140))
        # A small light diamond in the middle of every light stripe.
        for y in range(10, 140, 16):
            pygame.draw.polygon(canvas, (228, 200, 240), [(x + 18, y - 2), (x + 20, y), (x + 18, y + 2), (x + 16, y)])
    # Less light near the ceiling and just above the panels.
    draw_dark_band(canvas, 0, 14, 40)
    draw_dark_band(canvas, 0, 6, 35)
    draw_dark_band(canvas, 126, 13, 25)

    # The moulding rail on top of the panels: light top, dark bottom.
    pygame.draw.rect(canvas, OUTLINE, (0, 136, ROOM_WIDTH, 1))
    pygame.draw.rect(canvas, (185, 140, 205), (0, 137, ROOM_WIDTH, 4))
    pygame.draw.rect(canvas, (215, 180, 232), (0, 137, ROOM_WIDTH, 1))
    pygame.draw.rect(canvas, (120, 75, 140), (0, 140, ROOM_WIDTH, 1))

    # The panels: every panel has a light top and left edge and a dark
    # bottom and right edge, so it looks a little raised.
    pygame.draw.rect(canvas, (140, 92, 160), (0, 141, ROOM_WIDTH, 59))
    for x in range(0, ROOM_WIDTH, 20):
        pygame.draw.rect(canvas, (170, 120, 190), (x + 2, 145, 16, 50))
        pygame.draw.rect(canvas, (195, 150, 214), (x + 2, 145, 16, 1))
        pygame.draw.rect(canvas, (195, 150, 214), (x + 2, 145, 1, 50))
        pygame.draw.rect(canvas, (125, 80, 145), (x + 2, 194, 16, 1))
        pygame.draw.rect(canvas, (125, 80, 145), (x + 17, 145, 1, 50))
    draw_dark_band(canvas, 188, 12, 35)


def draw_wood_floor(canvas):
    # Wooden floor boards. Like the dressing room tiles, every row is a
    # bit taller and lighter than the row behind it, which gives depth.
    pygame.draw.rect(canvas, OUTLINE, (0, FLOOR_Y - 1, ROOM_WIDTH, 1))
    pygame.draw.rect(canvas, (110, 65, 120), (0, FLOOR_Y, ROOM_WIDTH, 4))      # skirting board
    pygame.draw.rect(canvas, (150, 100, 165), (0, FLOOR_Y, ROOM_WIDTH, 1))
    y = FLOOR_Y + 4
    height = 4
    row = 0
    while y < CANVAS_HEIGHT:
        wood = (150 + row * 7, 95 + row * 6, 62 + row * 4)
        light = (175 + row * 7, 118 + row * 6, 80 + row * 4)
        gap = darker(wood, 0.6)
        length = height * 14
        pygame.draw.rect(canvas, wood, (0, y, ROOM_WIDTH, height))
        pygame.draw.rect(canvas, light, (0, y, ROOM_WIDTH, 1))                # light top edge
        pygame.draw.rect(canvas, gap, (0, y + height - 1, ROOM_WIDTH, 1))     # gap between rows
        # Where one board ends and the next starts (shifted in every row).
        shift = (row * 37) % length
        for x in range(-length + shift, ROOM_WIDTH, length):
            pygame.draw.rect(canvas, gap, (x, y, 1, height))
            # A short darker line: the wood grain.
            grain_x = x + length // 3
            pygame.draw.rect(canvas, darker(wood, 0.85), (grain_x, y + height // 2, length // 4, 1))
        y = y + height
        height = height + 1
        row = row + 1


def draw_flag_garland(canvas):
    # A string of little club flags under the ceiling. The string hangs
    # lower in the middle, like a real string: the dip is biggest halfway.
    start_x = 124
    end_x = 226
    for i in range(9):
        x = start_x + i * 12
        # Halfway (i = 4) the dip is 4 * 4 = 16 ... at the ends it is 0.
        dip = (i * (8 - i)) // 4
        y = 14 + dip
        if i < 8:
            next_dip = ((i + 1) * (7 - i)) // 4
            pygame.draw.line(canvas, OUTLINE, (x, y), (x + 12, 14 + next_dip))
        if i % 2 == 0:
            colour = HOME_RED
        else:
            colour = WHITE
        pygame.draw.polygon(canvas, OUTLINE, [(x - 1, y), (x + 9, y), (x + 4, y + 10)])
        pygame.draw.polygon(canvas, colour, [(x, y + 1), (x + 7, y + 1), (x + 4, y + 8)])


def draw_bernie(canvas, pictures, progress, tick, reveal):
    # Bernie on his bench. Before you talk to him he is the bear mascot.
    # After that he is Dave: his own head on the bear body, and the
    # bear head (the mask) lies on the bench next to him.
    if "dave" not in progress["choices"]:
        bernie = pictures["bernie"]
        canvas.blit(bernie, (362, FLOOR_Y - bernie.get_height()))
        return

    body = pictures["bernie_body"]
    body_y = FLOOR_Y - body.get_height()
    canvas.blit(body, (362, body_y))
    dave = pictures["dave_head"]
    canvas.blit(dave, (362 + (body.get_width() - dave.get_width()) // 2, body_y - dave.get_height() + 4))

    # Where the mask is: during the reveal it moves in three parts
    # (lift it up, move it to the right, put it down), afterwards it lies
    # on the bench. reveal is None when there is no reveal going on.
    mask = pictures["bernie_head"]
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
    # A shelf with spare mascot heads: a lion, a bee and a spare bear.
    draw_shadow(canvas, 137, 61, 116)
    shaded_box(canvas, (190, 130, 80), (220, 160, 105), (150, 95, 55), 135, 54, 120, 5)
    # lion: a mane, a lighter face and a shine
    pygame.draw.circle(canvas, OUTLINE, (155, 42), 13)
    pygame.draw.circle(canvas, (200, 110, 30), (155, 42), 12)
    pygame.draw.circle(canvas, (230, 140, 40), (154, 41), 11)
    pygame.draw.circle(canvas, (250, 200, 90), (155, 43), 8)
    pygame.draw.circle(canvas, (255, 225, 140), (153, 41), 3)
    pygame.draw.rect(canvas, OUTLINE, (151, 40, 2, 2))
    pygame.draw.rect(canvas, OUTLINE, (157, 40, 2, 2))
    pygame.draw.rect(canvas, (150, 80, 40), (153, 45, 4, 2))
    # bee
    pygame.draw.circle(canvas, OUTLINE, (195, 44), 11)
    pygame.draw.circle(canvas, (215, 170, 30), (195, 44), 10)
    pygame.draw.circle(canvas, YELLOW, (194, 43), 9)
    pygame.draw.rect(canvas, OUTLINE, (186, 41, 18, 3))
    pygame.draw.rect(canvas, OUTLINE, (187, 47, 16, 3))
    pygame.draw.rect(canvas, (255, 240, 150), (190, 37, 3, 2))
    pygame.draw.line(canvas, OUTLINE, (191, 34), (188, 28))
    pygame.draw.line(canvas, OUTLINE, (199, 34), (202, 28))
    pygame.draw.circle(canvas, OUTLINE, (188, 28), 2)
    pygame.draw.circle(canvas, OUTLINE, (202, 28), 2)
    # spare bear head: round ears, fur, a light muzzle and a black nose
    pygame.draw.circle(canvas, OUTLINE, (227, 35), 5)
    pygame.draw.circle(canvas, OUTLINE, (243, 35), 5)
    pygame.draw.circle(canvas, (170, 105, 55), (227, 35), 4)
    pygame.draw.circle(canvas, (170, 105, 55), (243, 35), 4)
    pygame.draw.circle(canvas, OUTLINE, (235, 44), 11)
    pygame.draw.circle(canvas, (125, 75, 40), (235, 44), 10)
    pygame.draw.circle(canvas, (170, 105, 55), (234, 43), 9)
    pygame.draw.circle(canvas, (240, 215, 170), (235, 48), 5)
    pygame.draw.rect(canvas, OUTLINE, (233, 46, 5, 3))
    pygame.draw.rect(canvas, OUTLINE, (230, 41, 2, 2))
    pygame.draw.rect(canvas, OUTLINE, (239, 41, 2, 2))


def draw_costume_rack(canvas):
    # A rail with three costumes (orange lion, striped bee, brown bear)
    # and a pair of giant bear-paw slippers under it.
    draw_shadow(canvas, 128, 201, 132)
    pygame.draw.rect(canvas, OUTLINE, (132, 92, 126, 4))
    pygame.draw.rect(canvas, (220, 220, 230), (133, 93, 124, 1))
    for pole_x in [134, 253]:
        outlined_box(canvas, (200, 200, 210), pole_x, 92, 3, 108)
        pygame.draw.rect(canvas, (235, 235, 245), (pole_x, 92, 1, 108))
        outlined_box(canvas, (150, 150, 165), pole_x - 4, 197, 11, 3)        # foot
    costumes = [(145, (230, 140, 40), (250, 180, 80)),
                (180, YELLOW, (255, 235, 120)),
                (215, (170, 105, 55), (205, 140, 85))]
    for x, colour, light in costumes:
        pygame.draw.rect(canvas, OUTLINE, (x + 12, 94, 2, 6))                  # hanger
        pygame.draw.polygon(canvas, OUTLINE, [(x - 1, 99), (x + 27, 99), (x + 30, 160), (x - 4, 160)])
        pygame.draw.polygon(canvas, colour, [(x, 100), (x + 26, 100), (x + 29, 159), (x - 3, 159)])
        # Light on the left, shadow on the right, a fold in the middle.
        pygame.draw.rect(canvas, light, (x + 2, 102, 3, 54))
        pygame.draw.polygon(canvas, darker(colour, 0.78), [(x + 20, 100), (x + 26, 100), (x + 29, 159), (x + 22, 159)])
        pygame.draw.line(canvas, darker(colour, 0.85), (x + 13, 104), (x + 13, 158))
        if colour == YELLOW:
            for stripe_y in [112, 126, 140]:
                pygame.draw.rect(canvas, OUTLINE, (x - 1, stripe_y, 29, 4))
    # The slippers: brown paws with three toes each.
    for foot_x in [168, 196]:
        pygame.draw.ellipse(canvas, OUTLINE, (foot_x - 1, 189, 20, 12))
        pygame.draw.ellipse(canvas, (170, 105, 55), (foot_x, 190, 18, 10))
        pygame.draw.ellipse(canvas, (240, 215, 170), (foot_x + 3, 191, 8, 4))
        for toe in range(3):
            pygame.draw.rect(canvas, OUTLINE, (foot_x + 3 + toe * 5, 198, 1, 2))


def draw_ring_light(canvas, tick):
    # Bernie's TikTok setup: a glowing ring light with a phone, on a tripod.
    glow = pygame.Surface((60, 60), pygame.SRCALPHA)
    pygame.draw.circle(glow, (255, 255, 220, 40), (30, 30), 28)
    pygame.draw.circle(glow, (255, 255, 220, 40), (30, 30), 21)
    canvas.blit(glow, (270, 42))
    pygame.draw.circle(canvas, OUTLINE, (300, 72), 15)
    pygame.draw.circle(canvas, (255, 255, 230), (300, 72), 14)
    pygame.draw.circle(canvas, WHITE, (299, 71), 12, 2)
    pygame.draw.circle(canvas, OUTLINE, (300, 72), 9)
    pygame.draw.circle(canvas, (215, 180, 230), (300, 72), 8)
    outlined_box(canvas, (40, 40, 50), 296, 66, 8, 13)
    pygame.draw.rect(canvas, (120, 200, 255), (297, 67, 6, 10))
    pygame.draw.rect(canvas, (200, 235, 255), (297, 67, 6, 2))
    # The red "recording" dot on the phone blinks.
    if (tick // 20) % 2 == 0:
        pygame.draw.rect(canvas, (255, 60, 60), (301, 75, 2, 2))
    draw_shadow(canvas, 284, 201, 32)
    pygame.draw.rect(canvas, OUTLINE, (299, 87, 3, 90))
    pygame.draw.rect(canvas, (110, 110, 125), (300, 87, 1, 89))
    pygame.draw.line(canvas, OUTLINE, (300, 176), (288, 199), 2)
    pygame.draw.line(canvas, OUTLINE, (300, 176), (312, 199), 2)
    pygame.draw.line(canvas, OUTLINE, (300, 176), (300, 199), 2)


def draw_mirror_table(canvas, tick):
    # A make-up mirror with light bulbs all around, and a table with a
    # foam finger, a sweatband and a bottle. The bulbs twinkle: every
    # 10 frames another bulb is a bit brighter.
    y = MIRROR_Y
    shaded_box(canvas, (250, 215, 90), (255, 240, 150), (200, 160, 40), 340, y, 76, 52)
    draw_bands(canvas, [(170, 215, 240), (190, 230, 250), (205, 238, 252)], 346, y + 6, 64, 40)
    pygame.draw.line(canvas, WHITE, (352, y + 40), (366, y + 12), 3)          # reflections
    pygame.draw.line(canvas, WHITE, (362, y + 42), (376, y + 16), 1)
    bulbs = []
    for bulb_x in range(344, 416, 9):
        bulbs.append((bulb_x, y + 2))
    for bulb_y in range(y + 12, y + 50, 10):
        bulbs.append((342, bulb_y))
        bulbs.append((414, bulb_y))
    bright = (tick // 10) % len(bulbs)
    for i in range(len(bulbs)):
        bulb_x, bulb_y = bulbs[i]
        if i == bright:
            glow = pygame.Surface((12, 12), pygame.SRCALPHA)
            pygame.draw.circle(glow, (255, 250, 200, 90), (6, 6), 6)
            canvas.blit(glow, (bulb_x - 6, bulb_y - 6))
            pygame.draw.circle(canvas, WHITE, (bulb_x, bulb_y), 2)
        else:
            pygame.draw.circle(canvas, (255, 245, 190), (bulb_x, bulb_y), 2)

    # The table, with a shadow on the wall under it.
    draw_shadow(canvas, 338, y + 64, 88)
    shaded_box(canvas, (190, 130, 80), (220, 160, 105), (150, 95, 55), 336, y + 54, 84, 6)
    outlined_box(canvas, HOME_RED, 345, y + 44, 8, 10)                         # foam finger
    pygame.draw.rect(canvas, HOME_RED, (348, y + 36, 3, 8))
    pygame.draw.rect(canvas, (255, 120, 110), (345, y + 44, 2, 10))
    outlined_box(canvas, WHITE, 362, y + 47, 12, 7)                            # sweatband
    pygame.draw.rect(canvas, HOME_RED, (362, y + 50, 12, 1))
    outlined_box(canvas, (250, 165, 60), 384, y + 44, 6, 10)                   # bottle
    pygame.draw.rect(canvas, (255, 210, 130), (385, y + 45, 1, 8))


# ---------------------------------------------------------------- Server Room

def draw_server_room(canvas, progress, tick):
    # The stadium's server room: humming racks with blinking lights, a
    # technician's desk, cables under the ceiling and a raised floor with
    # cold air vents. The red cable from the booth is cut on the floor.
    draw_server_wall(canvas)
    draw_server_floor(canvas)
    draw_cable_tray(canvas)
    draw_ceiling_lamps(canvas, [150, 380])

    draw_door(canvas, 20, (230, 70, 70), (180, 45, 45))       # back to the booth
    draw_warning_sign(canvas)
    draw_air_conditioner(canvas, tick)
    draw_fire_extinguisher(canvas)
    draw_tech_desk(canvas, tick)

    # Three server racks on the right.
    for rack_x, rack_number in [(306, 0), (362, 1), (418, 2)]:
        draw_shadow(canvas, rack_x - 3, FLOOR_Y + 1, 56)
        draw_server_rack(canvas, rack_x, rack_number, tick)

    draw_floor_vent(canvas, tick)
    draw_cut_cable(canvas, progress, tick)

    # The lamps shine down into the room.
    for lamp_x in [150, 380]:
        draw_light_cone(canvas, lamp_x + 8, 13, FLOOR_Y, 14, 90)


def draw_server_wall(canvas):
    # A cool grey-blue painted wall, darker near the ceiling, with grey
    # metal panels on the lower part (like the wood panels in the booth).
    draw_bands(canvas, [(150, 165, 185), (165, 180, 198), (175, 190, 207), (182, 197, 213)],
               0, 0, ROOM_WIDTH, 148)
    pygame.draw.rect(canvas, (120, 130, 150), (0, 0, ROOM_WIDTH, 10))
    pygame.draw.rect(canvas, OUTLINE, (0, 10, ROOM_WIDTH, 1))
    # A rail on top of the panels, then the panels with a light top edge.
    pygame.draw.rect(canvas, OUTLINE, (0, 147, ROOM_WIDTH, 1))
    pygame.draw.rect(canvas, (95, 105, 125), (0, 148, ROOM_WIDTH, 3))
    pygame.draw.rect(canvas, (130, 140, 160), (0, 148, ROOM_WIDTH, 1))
    pygame.draw.rect(canvas, (110, 120, 140), (0, 151, ROOM_WIDTH, 49))
    for x in range(0, ROOM_WIDTH, 30):
        pygame.draw.rect(canvas, (128, 138, 158), (x + 1, 153, 27, 44))   # panel
        pygame.draw.rect(canvas, (150, 160, 180), (x + 1, 153, 27, 1))    # light top
        pygame.draw.rect(canvas, (95, 104, 122), (x + 1, 196, 27, 1))     # dark bottom
        canvas.set_at((x + 4, 156), (175, 182, 200))                       # screws
        canvas.set_at((x + 25, 156), (175, 182, 200))
    draw_dark_band(canvas, 11, 10, 25)
    draw_dark_band(canvas, 188, 12, 30)


def draw_server_floor(canvas):
    # A raised floor of grey square tiles. Like the other floors, every
    # row is a bit taller and lighter than the row behind it (depth).
    pygame.draw.rect(canvas, OUTLINE, (0, FLOOR_Y, ROOM_WIDTH, 1))
    y = FLOOR_Y + 1
    height = 8
    row = 0
    while y < CANVAS_HEIGHT:
        width = height * 3
        tile = (120 + row * 7, 128 + row * 7, 142 + row * 6)
        pygame.draw.rect(canvas, darker(tile, 0.7), (0, y, ROOM_WIDTH, height))
        for x in range(0, ROOM_WIDTH, width):
            pygame.draw.rect(canvas, tile, (x + 1, y + 1, width - 1, height - 1))
            pygame.draw.rect(canvas, (tile[0] + 20, tile[1] + 20, tile[2] + 18), (x + 1, y + 1, width - 1, 1))
        y = y + height
        height = height + 2
        row = row + 1


def draw_cable_tray(canvas):
    # A metal cable tray under the ceiling, full of cables. Some cables
    # hang down in loops and go into the racks.
    pygame.draw.rect(canvas, OUTLINE, (60, 17, ROOM_WIDTH - 60, 7))
    pygame.draw.rect(canvas, (150, 155, 170), (60, 18, ROOM_WIDTH - 60, 5))
    pygame.draw.rect(canvas, (185, 190, 205), (60, 18, ROOM_WIDTH - 60, 1))
    for hanger_x in range(80, ROOM_WIDTH, 60):
        pygame.draw.rect(canvas, OUTLINE, (hanger_x, 11, 2, 7))
    # Bundles of coloured cables lying in the tray.
    for i, colour in enumerate([(60, 120, 220), (240, 200, 50), (80, 190, 110)]):
        pygame.draw.line(canvas, colour, (62, 19 + i), (ROOM_WIDTH, 19 + i))
    # Cables hanging down from the tray into the tops of the racks.
    for start_x, colour in [(318, (60, 120, 220)), (334, (240, 200, 50)),
                            (378, (80, 190, 110)), (392, (60, 120, 220)), (440, (240, 200, 50))]:
        pygame.draw.line(canvas, OUTLINE, (start_x, 24), (start_x, 72), 3)
        pygame.draw.line(canvas, colour, (start_x, 24), (start_x, 72))


def draw_warning_sign(canvas):
    # A yellow warning sign with black stripes: "STAFF ONLY"
    # (the text is added later, see LABELS).
    shaded_box(canvas, (250, 215, 60), (255, 240, 130), (210, 170, 30), 78, 72, 46, 26)
    for stripe_x in range(80, 122, 6):
        pygame.draw.line(canvas, OUTLINE, (stripe_x, 92), (stripe_x + 3, 95), 2)


def draw_air_conditioner(canvas, tick):
    # A white air conditioner high on the wall (server rooms must stay
    # cold). It has a small blue display and cold air lines that wave
    # out of its bottom.
    shaded_box(canvas, (235, 238, 245), WHITE, (195, 200, 212), 168, 74, 70, 22)
    for slat_y in [88, 91]:
        pygame.draw.rect(canvas, (170, 175, 190), (172, slat_y, 62, 1))
    pygame.draw.rect(canvas, OUTLINE, (220, 77, 14, 7))
    pygame.draw.rect(canvas, (70, 160, 230), (221, 78, 12, 5))      # the display ("16C")
    # Three wavy lines of cold air under it; they move with the tick.
    for line in range(3):
        x = 182 + line * 18
        wave = (tick // 6 + line) % 3 - 1
        pygame.draw.line(canvas, (200, 230, 255), (x, 99), (x + wave, 104))
        pygame.draw.line(canvas, (200, 230, 255), (x + wave, 104), (x, 109))


def draw_fire_extinguisher(canvas):
    # A red fire extinguisher hanging on the wall next to the door.
    pygame.draw.rect(canvas, OUTLINE, (86, 160, 4, 4))                       # wall hook
    shaded_box(canvas, (220, 45, 45), (250, 100, 90), (170, 30, 30), 82, 166, 12, 28)
    pygame.draw.rect(canvas, (40, 40, 45), (84, 162, 8, 4))                  # the top
    pygame.draw.line(canvas, OUTLINE, (92, 163), (98, 170), 2)               # the hose
    pygame.draw.rect(canvas, WHITE, (84, 176, 8, 4))                         # the label


def draw_tech_desk(canvas, tick):
    # The technician's desk with two monitors, a keyboard, a mug and a
    # chair. One monitor shows a network graph; the other one is the feed
    # from the offside camera: "NO SIGNAL", blinking.
    draw_shadow(canvas, 132, FLOOR_Y + 1, 118)
    shaded_box(canvas, (95, 100, 118), (125, 130, 150), (70, 74, 90), 134, 162, 114, 6)   # top
    for leg_x in [138, 240]:
        shaded_box(canvas, (75, 80, 96), (100, 105, 122), (55, 58, 72), leg_x, 168, 5, 32)
    # A drawer unit under the desk.
    shaded_box(canvas, (85, 90, 108), (110, 115, 135), (62, 66, 80), 200, 170, 36, 30)
    pygame.draw.rect(canvas, OUTLINE, (214, 178, 8, 2))
    pygame.draw.rect(canvas, OUTLINE, (214, 190, 8, 2))

    # Monitor 1: a green network graph that moves (the line wobbles).
    draw_desk_monitor(canvas, 144)
    pygame.draw.rect(canvas, (15, 35, 25), (148, 132, 38, 22))
    points = []
    for step in range(10):
        wave = math.sin(tick / 8 + step * 0.9) * 5
        points.append((149 + step * 4, 144 + int(wave)))
    pygame.draw.lines(canvas, (90, 230, 120), False, points)

    # Monitor 2: the offside camera feed is gone. Red "NO SIGNAL" bars
    # blink (the text is drawn on top, see LABELS).
    draw_desk_monitor(canvas, 194)
    pygame.draw.rect(canvas, (40, 15, 18), (198, 132, 38, 22))
    if tick % 40 < 28:
        pygame.draw.rect(canvas, (200, 40, 40), (200, 139, 34, 8))

    # The keyboard, a mug and a messy pile of papers.
    pygame.draw.rect(canvas, OUTLINE, (160, 157, 40, 5))
    pygame.draw.rect(canvas, (210, 212, 225), (161, 158, 38, 3))
    outlined_box(canvas, (240, 240, 245), 214, 154, 7, 8)
    pygame.draw.rect(canvas, (60, 120, 220), (214, 157, 7, 2))
    for i in range(3):
        outlined_box(canvas, (245, 245, 238), 226 + i, 159 - i * 2, 16, 2)

    # The office chair, seen from behind.
    draw_shadow(canvas, 170, FLOOR_Y + 1, 30)
    shaded_box(canvas, (50, 52, 66), (80, 82, 100), (32, 33, 44), 174, 168, 22, 16)
    pygame.draw.rect(canvas, OUTLINE, (183, 185, 4, 9))
    pygame.draw.rect(canvas, OUTLINE, (173, 194, 24, 3))
    for wheel_x in [173, 183, 193]:
        pygame.draw.rect(canvas, OUTLINE, (wheel_x, 196, 4, 4))


def draw_desk_monitor(canvas, x):
    # A flat monitor on a small stand (the picture is drawn afterwards).
    shaded_box(canvas, (55, 58, 70), (85, 88, 102), (35, 37, 45), x, 128, 46, 30)
    pygame.draw.rect(canvas, OUTLINE, (x + 20, 158, 6, 4))


def draw_server_rack(canvas, x, number, tick):
    # One tall server rack: a dark cabinet full of server units. Each unit
    # has drive slots and little lights that blink at their own moment.
    shaded_box(canvas, (40, 43, 54), (70, 74, 90), (25, 27, 34), x, 74, 50, 126)
    pygame.draw.rect(canvas, (30, 32, 40), (x + 4, 78, 42, 118))             # inside
    # A small label plate on top of each rack: R1, R2, R3 (see LABELS).
    shaded_box(canvas, (220, 225, 235), WHITE, (180, 185, 200), x + 16, 66, 18, 7)

    unit_y = 80
    unit = 0
    while unit_y < 190:
        # The middle rack has a patch panel (a row of coloured plugs)
        # as its third unit: that is where the red cable goes in.
        if number == 1 and unit == 2:
            pygame.draw.rect(canvas, (70, 74, 90), (x + 5, unit_y, 40, 9))
            for plug in range(7):
                colour = [(60, 120, 220), (240, 200, 50), (80, 190, 110)][plug % 3]
                pygame.draw.rect(canvas, colour, (x + 8 + plug * 5, unit_y + 3, 3, 3))
            unit_y = unit_y + 11
            unit = unit + 1
            continue

        # A normal server: light grey front with dark drive slots.
        pygame.draw.rect(canvas, (150, 155, 170), (x + 5, unit_y, 40, 9))
        pygame.draw.rect(canvas, (185, 190, 205), (x + 5, unit_y, 40, 1))
        for slot in range(4):
            pygame.draw.rect(canvas, (90, 95, 110), (x + 8 + slot * 6, unit_y + 3, 4, 4))
        # Two lights: green (power) always on, orange (data) blinking.
        canvas.set_at((x + 36, unit_y + 4), (90, 230, 110))
        if (tick + unit * 9 + number * 17) % 24 < 12:
            canvas.set_at((x + 40, unit_y + 4), (255, 180, 60))
        unit_y = unit_y + 11
        unit = unit + 1

    # A shine on the glass door: a light diagonal line.
    pygame.draw.line(canvas, (90, 95, 115), (x + 8, 190), (x + 30, 82))


def draw_floor_vent(canvas, tick):
    # A floor tile with a vent grille under the cut cable. Cold air blows
    # up out of it (light blue lines that rise and fade) - that is the
    # wind that makes the tie flutter.
    pygame.draw.rect(canvas, OUTLINE, (236, 203, 34, 7))
    pygame.draw.rect(canvas, (90, 98, 115), (237, 204, 32, 5))
    for slit_x in range(239, 268, 3):
        pygame.draw.line(canvas, (50, 55, 68), (slit_x, 204), (slit_x, 208))
    for puff in range(4):
        age = (tick + puff * 8) % 32           # 0 to 31 frames old
        air = pygame.Surface((2, 6), pygame.SRCALPHA)
        air.fill((200, 230, 255, 140 - age * 4))
        canvas.blit(air, (240 + puff * 8, 200 - age))


def draw_cut_cable(canvas, progress, tick):
    # The red cable comes in under the door and runs along the floor.
    # Above the vent it is cut: two copper ends with sparks and smoke.
    # The second half runs on and up into the patch panel of rack R2.
    first_half = [(40, 196), (246, 196)]
    second_half = [(260, 196), (352, 196), (352, 107), (367, 107)]
    for half in [first_half, second_half]:
        pygame.draw.lines(canvas, OUTLINE, False, half, 5)
        pygame.draw.lines(canvas, (220, 40, 40), False, half, 3)
    pygame.draw.line(canvas, (255, 120, 110), (40, 195), (245, 195))       # shine
    # The copper ends.
    for end_x in [247, 258]:
        pygame.draw.rect(canvas, (230, 140, 60), (end_x, 195, 2, 3))
    draw_sparks(canvas, 252, 195, tick)
    draw_smoke(canvas, 252, 192, tick)

    # The tip of Infantini's tie is stuck in the cut, until you find it.
    # The cold air from the vent makes it flutter up and down.
    if "tie" not in progress["choices"]:
        flutter = int(math.sin(tick / 3) * 4)
        tip = [(249, 188), (249, 198), (234, 193 + flutter), (228, 189 + flutter), (234, 185 + flutter)]
        pygame.draw.polygon(canvas, OUTLINE, tip)
        inside = [(248, 189), (248, 197), (234, 192 + flutter), (230, 189 + flutter), (234, 186 + flutter)]
        pygame.draw.polygon(canvas, (55, 70, 150), inside)
        pygame.draw.line(canvas, (90, 110, 190), (247, 190), (234, 187 + flutter))   # silk shine
        # The gold initials G.I. (two small gold marks).
        pygame.draw.rect(canvas, (255, 215, 70), (238, 189 + flutter // 2, 2, 2))
        pygame.draw.rect(canvas, (255, 215, 70), (242, 189 + flutter // 2, 1, 2))
        draw_sparkle(canvas, 236, 181 + flutter, tick, 40)


# ---------------------------------------------------------------- The Pitch

# Where the people stand on the pitch (x positions on the canvas).
LINESMAN_X = 110
STRIKER_X = 196
BALL_X = 258
REFEREE_X = 296
CAPTAIN_X = 322
BUBBLE_Y = 136      # the top of the captain's "OFFSIDE!" speech bubble


def draw_pitch(canvas, pictures, ball, tick):
    # During a goal celebration the scoreboard flashes (on for 8 frames,
    # off for 8 frames ...).
    flashing = ball["celebrate"] > 0 and (ball["celebrate"] // 8) % 2 == 0
    draw_pitch_background(canvas, flashing, tick)
    draw_pitch_people(canvas, pictures, ball, tick)


def draw_title_background(canvas, pictures, tick):
    # The title screen: the empty pitch, with the VAR official on the left
    # and Bernie on the right, like decorations next to the menu.
    draw_pitch_background(canvas, False, tick, False)
    player = pictures["player"]
    canvas.blit(player, (112, FLOOR_Y - player.get_height() - bob(tick, 0)))
    # Bernie stands still with his feet on the grass, with a shadow under him.
    bernie = pictures["bernie"]
    draw_shadow(canvas, 340, FLOOR_Y + 1, bernie.get_width())
    canvas.blit(bernie, (340, FLOOR_Y - bernie.get_height()))


def draw_pitch_background(canvas, flashing, tick, scoreboard=True):
    # Everything on the pitch except the people and the ball:
    # the stadium, the boards, the grass, the tunnel, the flag and the goal.
    # scoreboard=False leaves the scoreboard out (for the title screen).
    draw_stadium(canvas, flashing, tick, scoreboard)
    draw_ad_boards(canvas, tick)
    draw_grass(canvas)

    # The tunnel back inside: stone blocks, a red top and a dark inside
    # that is even darker at the edges.
    outlined_box(canvas, (140, 140, 155), 8, 130, 64, 70)
    for block_y in range(140, 200, 8):
        for pillar_x in [8, 64]:
            pygame.draw.rect(canvas, (110, 110, 125), (pillar_x, block_y, 8, 1))
            pygame.draw.rect(canvas, (170, 170, 185), (pillar_x, block_y + 1, 8, 1))
    pygame.draw.rect(canvas, (30, 34, 48), (16, 138, 48, 62))
    pygame.draw.rect(canvas, (45, 50, 66), (22, 142, 36, 58))
    pygame.draw.rect(canvas, HOME_RED, (8, 130, 64, 6))
    pygame.draw.rect(canvas, (255, 110, 100), (8, 130, 64, 1))
    draw_shadow(canvas, 4, FLOOR_Y + 1, 72)

    # A corner flag that flutters: the tip moves up and down a little.
    flutter = (tick // 6) % 3
    draw_shadow(canvas, 86, FLOOR_Y + 2, 10)
    pygame.draw.rect(canvas, OUTLINE, (90, 176, 1, 26))
    pygame.draw.polygon(canvas, OUTLINE, [(90, 175), (102, 178 + flutter), (90, 183)])
    pygame.draw.polygon(canvas, YELLOW, [(91, 176), (100, 178 + flutter), (91, 182)])

    draw_goal(canvas, tick)


def draw_ad_boards(canvas, tick):
    # LED advertising boards along the side of the pitch. They scroll to
    # the left (1 pixel every 3 frames); % 240 starts again after 4 boards,
    # when the pattern repeats.
    boards = [(YELLOW, OUTLINE), ((70, 110, 230), WHITE), (WHITE, HOME_RED), ((90, 180, 110), WHITE)]
    scroll = (tick // 3) % 240
    canvas.set_clip((0, 148, ROOM_WIDTH, 17))
    for i in range(14):
        background, writing = boards[i % 4]
        x = i * 60 + 1 - scroll
        outlined_box(canvas, background, x, 149, 58, 15)
        pygame.draw.rect(canvas, (min(255, background[0] + 40), min(255, background[1] + 40),
                                  min(255, background[2] + 40)), (x, 149, 58, 2))      # light top
        pygame.draw.rect(canvas, darker(background, 0.75), (x, 161, 58, 3))          # dark bottom
        pygame.draw.rect(canvas, writing, (x + 11, 154, 34, 4))
        pygame.draw.rect(canvas, writing, (x + 5, 154, 4, 4))
    canvas.set_clip(None)
    pygame.draw.rect(canvas, OUTLINE, (0, 164, ROOM_WIDTH, 1))


def draw_grass(canvas):
    # The grass with mowing stripes, all the way down. Far away (at the
    # top) the grass is darker, close to you (at the bottom) it is lighter,
    # in four steps. Every stripe is made of those four bands.
    dark_stripe = [(62, 160, 66), (72, 178, 74), (80, 190, 80), (88, 200, 86)]
    light_stripe = [(80, 180, 80), (92, 198, 90), (100, 210, 95), (110, 220, 104)]
    band_tops = [165, 180, 200, 230, CANVAS_HEIGHT]
    for i in range(0, ROOM_WIDTH, 30):
        if (i // 30) % 2 == 0:
            colours = dark_stripe
        else:
            colours = light_stripe
        for band in range(4):
            top = band_tops[band]
            pygame.draw.rect(canvas, colours[band], (i, top, 30, band_tops[band + 1] - top))
    # Little light grass blades in the front, where you can see them.
    for x in range(3, ROOM_WIDTH, 7):
        blade_y = 212 + (x * 13) % 52
        pygame.draw.rect(canvas, (140, 230, 120), (x, blade_y, 1, 2))
    # The white lines: thin far away, thicker close to you.
    pygame.draw.rect(canvas, WHITE, (0, 172, ROOM_WIDTH, 1))
    pygame.draw.rect(canvas, WHITE, (0, FLOOR_Y + 2, ROOM_WIDTH, 2))


def draw_pitch_people(canvas, pictures, ball, tick):
    # The people: linesman, striker, referee and the away captain.
    # They breathe (one pixel up and down); the angry captain jumps.
    # Everyone has a shadow on the grass.
    for name, x, phase in [("linesman", LINESMAN_X, 3), ("striker", STRIKER_X, 11),
                           ("referee", REFEREE_X, 5)]:
        picture = pictures[name]
        draw_shadow(canvas, x + 2, FLOOR_Y + 1, picture.get_width() - 4)
        canvas.blit(picture, (x, FLOOR_Y - picture.get_height() - bob(tick, phase)))
    captain = pictures["captain"]
    jump = ((tick // 6) % 2) * 2
    # The shadow gets smaller when the captain jumps up.
    draw_shadow(canvas, CAPTAIN_X + 2 + jump, FLOOR_Y + 1, captain.get_width() - 4 - jump * 2)
    canvas.blit(captain, (CAPTAIN_X, FLOOR_Y - captain.get_height() - jump))

    # The linesman's flag, held up in his right hand (next to his head).
    # It flutters a little. The pole is 50 pixels long and the flag is
    # 15 x 11 pixels: yellow, with a red square top left and bottom right.
    flag_x = LINESMAN_X + 31
    flutter = (tick // 5) % 2
    pygame.draw.rect(canvas, OUTLINE, (flag_x, 140, 1, 50))
    pygame.draw.rect(canvas, OUTLINE, (flag_x, 139, 17, 13 + flutter))
    pygame.draw.rect(canvas, YELLOW, (flag_x + 1, 140, 15, 11 + flutter))
    pygame.draw.rect(canvas, HOME_RED, (flag_x + 1, 140, 7, 5))
    pygame.draw.rect(canvas, HOME_RED, (flag_x + 8, 145, 8, 6 + flutter))
    outlined_box(canvas, SKIN, flag_x - 2, 184, 4, 3)                          # his hand

    # A speech bubble over the captain ("OFFSIDE!" is added as text).
    outlined_box(canvas, WHITE, CAPTAIN_X - 14, BUBBLE_Y, 34, 12)
    pygame.draw.rect(canvas, (220, 225, 235), (CAPTAIN_X - 14, BUBBLE_Y + 10, 34, 2))
    pygame.draw.polygon(canvas, OUTLINE, [(CAPTAIN_X - 2, BUBBLE_Y + 12), (CAPTAIN_X + 2, BUBBLE_Y + 18),
                                          (CAPTAIN_X + 4, BUBBLE_Y + 12)])

    # The ball, with a little shadow. ball["x"] is where it is now.
    # While it rolls, the picture is turned in steps of 90 degrees
    # (every 6 pixels it rolls), which keeps the pixel art sharp.
    ball_x = int(ball["x"])
    turns = (ball_x // 6) % 4
    ball_picture = pygame.transform.rotate(pictures["ball"], turns * 90)
    pygame.draw.ellipse(canvas, (50, 140, 50), (ball_x, FLOOR_Y - 2, 10, 4))
    canvas.blit(ball_picture, (ball_x, FLOOR_Y - ball_picture.get_height() + 1))


def draw_stadium(canvas, celebrating, tick, scoreboard=True):
    # Sky, roof, two tiers of fans with the scoreboard, and floodlights.
    # scoreboard=False leaves the scoreboard out (for the title screen).
    draw_bands(canvas, [(100, 180, 245), (120, 195, 250), (145, 210, 255)], 0, 0, ROOM_WIDTH, 34)
    # The clouds drift slowly; % 560 brings them back on the left side.
    for start, cloud_y in [(40, 6), (250, 3), (400, 10)]:
        cloud_x = (start + tick // 10) % 560 - 40
        draw_cloud(canvas, cloud_x, cloud_y)

    # The roof.
    pygame.draw.rect(canvas, OUTLINE, (0, 33, ROOM_WIDTH, 9))
    pygame.draw.rect(canvas, (200, 205, 215), (0, 34, ROOM_WIDTH, 7))
    pygame.draw.rect(canvas, (225, 230, 240), (0, 34, ROOM_WIDTH, 1))
    for x in range(0, ROOM_WIDTH, 16):
        pygame.draw.line(canvas, (150, 155, 170), (x, 34), (x + 8, 40))

    # Upper tier: small fans, home fans on the left, away fans on the right
    # (see fan_colour).
    pygame.draw.rect(canvas, (60, 60, 80), (0, 42, ROOM_WIDTH, 50))
    for fan_y in range(44, 90, 4):
        for fan_x in range(1 + (fan_y // 4) % 2 * 2, ROOM_WIDTH, 4):
            colour = fan_colour(fan_x, fan_x * 7 + fan_y * 3)
            pygame.draw.rect(canvas, colour, (fan_x, fan_y, 2, 2))
    # The roof throws a shadow on the upper tier: darkest right under the
    # roof, fading out (three see-through bands).
    draw_dark_band(canvas, 42, 30, 50)
    draw_dark_band(canvas, 42, 18, 40)
    draw_dark_band(canvas, 42, 8, 40)

    # Phone flashes in the crowd: every 7 frames one fan takes a photo.
    # The position comes from a calculation, so it looks random.
    if tick % 7 < 2:
        flash_x = (tick * 37) % ROOM_WIDTH
        flash_y = 46 + (tick * 13) % 96
        pygame.draw.rect(canvas, WHITE, (flash_x, flash_y, 2, 2))
        pygame.draw.rect(canvas, (255, 255, 200), (flash_x - 1, flash_y + 1, 4, 1))

    # The scoreboard (the text is added later), with LED dots and a glow.
    # It stands left of the middle, so the pundit's speech box does not
    # cover it. The title screen leaves it out (the logo is there).
    if scoreboard:
        glow = pygame.Surface((120, 50), pygame.SRCALPHA)
        pygame.draw.ellipse(glow, (255, 240, 180, 30), (0, 0, 120, 50))
        canvas.blit(glow, (110, 38))
        shaded_box(canvas, (20, 20, 30), (60, 60, 75), (10, 10, 15), 120, 46, 100, 34)
        pygame.draw.rect(canvas, HOME_RED, (124, 50, 30, 10))
        pygame.draw.rect(canvas, AWAY_YELLOW, (186, 50, 30, 10))
        pygame.draw.rect(canvas, (255, 200, 40), (124, 66, 92, 10))
        if celebrating:
            pygame.draw.rect(canvas, (230, 60, 60), (124, 66, 92, 10))
        for dot_x in range(124, 216, 3):
            canvas.set_at((dot_x, 62), (60, 60, 75))                           # LED dots

    # A red banner between the tiers.
    pygame.draw.rect(canvas, OUTLINE, (0, 92, ROOM_WIDTH, 3))
    pygame.draw.rect(canvas, HOME_RED, (0, 95, ROOM_WIDTH, 7))
    pygame.draw.rect(canvas, (255, 110, 100), (0, 95, ROOM_WIDTH, 1))
    pygame.draw.rect(canvas, (180, 40, 40), (0, 101, ROOM_WIDTH, 1))
    for x in range(0, ROOM_WIDTH, 40):
        pygame.draw.rect(canvas, WHITE, (x + 6, 97, 22, 3))

    # Lower tier: bigger fans, some with their arms up.
    pygame.draw.rect(canvas, (70, 70, 95), (0, 102, ROOM_WIDTH, 46))
    for fan_y in range(105, 146, 7):
        for fan_x in range(2 + (fan_y // 7) % 2 * 4, ROOM_WIDTH, 8):
            colour = fan_colour(fan_x, fan_x * 3 + fan_y)
            pygame.draw.rect(canvas, SKIN, (fan_x + 1, fan_y, 3, 3))
            pygame.draw.rect(canvas, colour, (fan_x, fan_y + 3, 5, 3))
            pygame.draw.rect(canvas, darker(colour, 0.8), (fan_x + 3, fan_y + 3, 2, 3))
            if (fan_x + fan_y) % 3 == 0:
                # Fans with their arms up jump: half of them up, half down,
                # changing every 8 frames.
                jump = (fan_x // 8 + tick // 8) % 2
                pygame.draw.rect(canvas, SKIN, (fan_x - 1, fan_y - 2 - jump, 1, 3))
                pygame.draw.rect(canvas, SKIN, (fan_x + 5, fan_y - 2 - jump, 1, 3))

    # Fans waving scarves above their heads: the scarf moves from left to
    # right and back. Red and white on the home side, yellow and black on
    # the away side.
    for scarf_x, scarf_y in [(60, 110), (230, 124), (350, 110), (440, 131)]:
        swing = ((tick // 6 + scarf_x) % 4) - 2
        if scarf_x < ROOM_WIDTH // 2:
            first = HOME_RED
            second = WHITE
        else:
            first = AWAY_YELLOW
            second = BLACK
        for i in range(5):
            if i % 2 == 0:
                colour = first
            else:
                colour = second
            pygame.draw.rect(canvas, colour, (scarf_x + i * 2 + swing, scarf_y - 4 + abs(i - 2), 2, 2))

    # A fan waving a red and white flag.
    # The tip of the flag moves up and down to make it wave.
    wave = ((tick // 8) % 3) * 2
    pygame.draw.rect(canvas, OUTLINE, (150, 98, 1, 20))
    pygame.draw.polygon(canvas, HOME_RED, [(151, 98), (166, 99 + wave), (151, 106)])
    pygame.draw.polygon(canvas, WHITE, [(151, 102), (166, 99 + wave), (151, 106)])

    # Two floodlights, with a soft glow around them.
    for light_x in [60, 420]:
        halo = pygame.Surface((60, 34), pygame.SRCALPHA)
        pygame.draw.ellipse(halo, (255, 250, 210, 60), (0, 0, 60, 34))
        pygame.draw.ellipse(halo, (255, 250, 210, 60), (12, 6, 36, 22))
        canvas.blit(halo, (light_x - 29, -8))
        outlined_box(canvas, (90, 90, 100), light_x - 14, 2, 30, 14)
        for i in range(3):
            pygame.draw.rect(canvas, (255, 250, 200), (light_x - 12 + i * 10, 4, 8, 10))
            pygame.draw.rect(canvas, WHITE, (light_x - 12 + i * 10, 4, 8, 2))


def draw_goal(canvas, tick):
    # The goal seen from the side: a shadow, the net inside the frame,
    # the back post and ground bar (light grey, because they are further
    # away), then the white front post and crossbar.
    # It is about 1.5 times as high as a player, like a real goal.
    shadow = pygame.Surface((112, 10), pygame.SRCALPHA)
    pygame.draw.ellipse(shadow, (0, 60, 0, 70), (0, 0, 112, 10))
    canvas.blit(shadow, (384, 196))

    # The net: a light area with a grid, only between the posts.
    # The top part is a bit darker (in the shadow of the crossbar).
    pygame.draw.rect(canvas, (235, 240, 250), (393, 125, 98, 74))
    pygame.draw.rect(canvas, (215, 222, 235), (393, 125, 98, 10))
    for net_x in range(395, 491, 4):
        pygame.draw.line(canvas, (195, 200, 215), (net_x, 125), (net_x, 198))
    for net_y in range(127, 199, 4):
        pygame.draw.line(canvas, (195, 200, 215), (393, net_y), (490, net_y))

    # The back post and the bar on the ground at the back of the goal.
    outlined_box(canvas, (200, 205, 215), 490, 122, 4, 78)
    outlined_box(canvas, (200, 205, 215), 393, 197, 101, 3)

    # The white front post and the crossbar, with a grey shadow side.
    outlined_box(canvas, WHITE, 388, 120, 106, 5)
    pygame.draw.rect(canvas, (210, 215, 225), (388, 123, 106, 2))
    outlined_box(canvas, WHITE, 388, 120, 5, 80)
    pygame.draw.rect(canvas, (210, 215, 225), (391, 120, 2, 80))

    # A photographer kneeling next to the goal. Now and then the camera
    # flashes (2 frames out of every 70).
    photographer_x = 368
    draw_shadow(canvas, photographer_x - 14, FLOOR_Y + 1, 30)
    pygame.draw.rect(canvas, OUTLINE, (photographer_x, 186, 14, 14))
    pygame.draw.rect(canvas, (60, 60, 80), (photographer_x + 1, 187, 12, 13))
    pygame.draw.rect(canvas, (85, 85, 105), (photographer_x + 1, 187, 3, 13))
    pygame.draw.circle(canvas, OUTLINE, (photographer_x + 7, 182), 5)
    pygame.draw.circle(canvas, (110, 75, 50), (photographer_x + 7, 182), 4)
    outlined_box(canvas, (30, 30, 40), photographer_x - 7, 184, 9, 6)
    pygame.draw.rect(canvas, (60, 60, 70), (photographer_x - 13, 185, 7, 4))
    if tick % 70 < 2:
        flash = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.circle(flash, (255, 255, 255, 120), (15, 15), 14)
        canvas.blit(flash, (photographer_x - 28, 172))
        pygame.draw.rect(canvas, WHITE, (photographer_x - 15, 186, 3, 1))


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
    elif scene_id == "server_room":
        draw_server_room(canvas, progress, tick)
    elif scene_id == "pitch":
        draw_pitch(canvas, pictures, extras["ball"], tick)


# Text labels for each room: (text, x, y, colour, small?) in canvas positions.
# They are drawn later on the big window, so the letters stay sharp.
LABELS = {
    "booth": [
        ("SERVER", 26, 110, (255, 255, 255), False),
        ("REF", 308, 110, (60, 60, 70), False),
        ("MASCOT", 357, 110, (90, 60, 10), False),
        ("PITCH", 430, 117, (255, 255, 255), False),
        ("OFFSIDE CAM", 192, 138, (220, 40, 40), True),
    ],
    "dressing_room": [
        ("BOOTH", 28, 110, (60, 60, 70), False),
        ("TRUST THE", 296, 36, (230, 60, 60), False),
        ("PROCESS", 300, 45, (230, 60, 60), False),
    ],
    "mascot_room": [
        ("BOOTH", 28, 110, (90, 60, 10), False),
        ("EMPLOYEE", 83, 105, (120, 60, 20), True),
        ("HONEY", 457, 180, (120, 80, 30), True),
    ],
    "server_room": [
        ("BOOTH", 28, 110, (255, 255, 255), False),
        ("STAFF", 87, 75, (30, 30, 40), False),
        ("ONLY", 91, 83, (30, 30, 40), False),
        ("NO SIGNAL", 201, 140, (255, 235, 235), True),
        ("16C", 222, 77, (255, 255, 255), True),
        ("R1", 325, 67, (30, 30, 40), True),
        ("R2", 381, 67, (30, 30, 40), True),
        ("R3", 437, 67, (30, 30, 40), True),
    ],
    "pitch": [
        ("BOOTH", 25, 120, (255, 255, 255), False),
        ("FCB", 129, 50, (255, 255, 255), False),
        ("BVB", 191, 50, (30, 30, 40), False),
        ("OFFSIDE!", CAPTAIN_X - 12, BUBBLE_Y + 1, (230, 40, 40), True),
    ],
}
