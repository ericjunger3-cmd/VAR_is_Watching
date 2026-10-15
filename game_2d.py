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

    # Turn the player's pixel grid into a picture once, at the start.
    player_picture = sprites.make_sprite(sprites.PLAYER)

    # Where the player stands. The y position is chosen so the feet
    # touch the floor: floor line minus the height of the picture.
    player_x = 245
    player_y = rooms.FLOOR_Y - player_picture.get_height()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 1. Draw the room and the player on the small canvas.
        rooms.draw_booth(canvas)
        canvas.blit(player_picture, (player_x, player_y))

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
