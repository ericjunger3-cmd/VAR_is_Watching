# VAR Is Watching - the 2D pixel-art version, made with pygame.
# sprites.py holds the pixel art, rooms.py draws the rooms,
# and this file runs the game.

import pygame
import sprites
import rooms

# Everything is drawn on a small canvas and then made 2x bigger,
# so each pixel becomes a 2 x 2 block: the "chunky pixel" look.
SCALE = 2
WINDOW_WIDTH = rooms.CANVAS_WIDTH * SCALE
WINDOW_HEIGHT = rooms.CANVAS_HEIGHT * SCALE

# How many canvas pixels the player walks per frame (30 frames per second).
WALK_SPEED = 3

# How many frames each walking picture is shown before switching.
FRAMES_PER_STEP = 5


def move_player(player, keys, player_width):
    # Move the player left or right while an arrow key (or A / D) is held.
    # keys tells us which keys are pressed right now.
    moving = False
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player["x"] = player["x"] - WALK_SPEED
        player["facing_left"] = True
        moving = True
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player["x"] = player["x"] + WALK_SPEED
        player["facing_left"] = False
        moving = True

    # Stay inside the room: not past the left or right edge.
    if player["x"] < 0:
        player["x"] = 0
    if player["x"] > rooms.CANVAS_WIDTH - player_width:
        player["x"] = rooms.CANVAS_WIDTH - player_width

    # Count frames while walking; reset when standing still.
    if moving:
        player["walk_timer"] = player["walk_timer"] + 1
    else:
        player["walk_timer"] = 0


def player_picture(player, standing, walking):
    # Choose which picture to draw: standing, or the walking frame.
    # While walking, the picture switches every FRAMES_PER_STEP frames:
    # (walk_timer // FRAMES_PER_STEP) counts 0, 1, 2, 3 ... and
    # "% 2 == 1" is True for every second count.
    picture = standing
    if player["walk_timer"] > 0 and (player["walk_timer"] // FRAMES_PER_STEP) % 2 == 1:
        picture = walking

    # The pictures look to the right. Mirror them when walking left.
    # flip(picture, flip left-right?, flip up-down?)
    if player["facing_left"]:
        picture = pygame.transform.flip(picture, True, False)
    return picture


def draw_labels(window, font):
    # Text is drawn on the big window (not the small canvas), so it stays sharp.
    # The positions are canvas positions, so we multiply them by SCALE.
    labels = [
        ("REF", 250, 110, (60, 60, 70)),
        ("MASCOT", 299, 110, (90, 60, 10)),
        ("PRESS", 359, 110, (255, 255, 255)),
        ("PITCH", 430, 117, (255, 255, 255)),
    ]
    for text, x, y, colour in labels:
        # render(text, smooth edges, colour): False gives sharp pixel edges.
        picture = font.render(text, False, colour)
        window.blit(picture, (x * SCALE, y * SCALE))


def main():
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("VAR Is Watching")
    clock = pygame.time.Clock()
    label_font = pygame.font.SysFont("consolas", 15, bold=True)

    # The small canvas we draw the room on.
    canvas = pygame.Surface((rooms.CANVAS_WIDTH, rooms.CANVAS_HEIGHT))

    # Turn the player's pixel grids into pictures once, at the start.
    standing = sprites.make_sprite(sprites.PLAYER)
    walking = sprites.make_sprite(sprites.PLAYER_WALK)
    player_width = standing.get_width()

    # Everything about the player in one dictionary.
    player = {
        "x": 245,               # position from the left edge of the room
        "facing_left": False,   # which way the player looks
        "walk_timer": 0         # frames spent walking (for the animation)
    }

    # The y position never changes: the feet always touch the floor.
    player_y = rooms.FLOOR_Y - standing.get_height()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # get_pressed() tells us which keys are held down right now.
        keys = pygame.key.get_pressed()
        move_player(player, keys, player_width)

        # 1. Draw the room and the player on the small canvas.
        rooms.draw_booth(canvas)
        canvas.blit(player_picture(player, standing, walking), (player["x"], player_y))

        # 2. Scale the canvas up to the window size and show it.
        big_picture = pygame.transform.scale(canvas, (WINDOW_WIDTH, WINDOW_HEIGHT))
        window.blit(big_picture, (0, 0))

        # 3. Sharp text on top.
        draw_labels(window, label_font)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


# Only start the game when this file is run directly (py game_2d.py).
if __name__ == "__main__":
    main()
