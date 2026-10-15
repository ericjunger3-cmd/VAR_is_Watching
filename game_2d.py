# VAR Is Watching - the 2D pixel-art version, made with pygame.
# sprites.py holds the pixel art, rooms.py draws the rooms,
# and this file runs the game.

import pygame
import game
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


# How close (in canvas pixels) the player must be to something to use it.
REACH = 14


def find_nearby_action(scene, player_x, player_width):
    # Look for an action in this scene whose "x" is close to the player.
    # Returns that action, or None if nothing is in reach.
    player_middle = player_x + player_width // 2
    for action in scene["actions"]:
        # abs() turns a negative distance into a positive one.
        if "x" in action and abs(action["x"] - player_middle) <= REACH:
            return action
    return None


def arrival_x(scene, came_from, player_width):
    # When entering a room, stand in front of the door that leads back
    # to the room we came from. Returns the new x position of the player.
    for action in scene["actions"]:
        if "go_to" in action and action["go_to"] == came_from and "x" in action:
            return action["x"] - player_width // 2
    # No matching door found: start near the left side.
    return 30


def draw_e_bubble(canvas, player_x, player_y, player_width):
    # A little white speech bubble above the player's head.
    # The letter "E" is added later on the big window.
    x = player_x + player_width // 2 - 7
    y = player_y - 18
    pygame.draw.rect(canvas, sprites.OUTLINE, (x, y, 14, 14))
    pygame.draw.rect(canvas, (255, 252, 235), (x + 1, y + 1, 12, 12))
    pygame.draw.rect(canvas, (235, 225, 195), (x + 1, y + 11, 12, 2))
    pygame.draw.rect(canvas, sprites.OUTLINE, (x + 5, y + 14, 4, 2))


def draw_labels(window, font, small_font, scene_id):
    # Text is drawn on the big window (not the small canvas), so it stays sharp.
    # The positions are canvas positions, so we multiply them by SCALE.
    for text, x, y, colour, small in rooms.LABELS[scene_id]:
        if small:
            label_font = small_font
        else:
            label_font = font
        # render(text, smooth edges, colour): False gives sharp pixel edges.
        picture = label_font.render(text, False, colour)
        window.blit(picture, (x * SCALE, y * SCALE))


def main():
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("VAR Is Watching")
    clock = pygame.time.Clock()
    label_font = pygame.font.SysFont("consolas", 15, bold=True)
    small_font = pygame.font.SysFont("consolas", 11, bold=True)
    bubble_font = pygame.font.SysFont("consolas", 22, bold=True)

    # The story from story.json, reused from the terminal game.
    story = game.load_story()
    scene_id = story["start_scene"]

    # The small canvas we draw the room on.
    canvas = pygame.Surface((rooms.CANVAS_WIDTH, rooms.CANVAS_HEIGHT))

    # Turn the pixel grids into pictures once, at the start.
    standing = sprites.make_sprite(sprites.PLAYER)
    walking = sprites.make_sprite(sprites.PLAYER_WALK)
    player_width = standing.get_width()

    # The characters and objects that live in the rooms.
    # Some use the same letters with their own colours (e.g. the kits).
    pictures = {
        "pombo": sprites.make_sprite(sprites.POMBO),
        "referee": sprites.make_sprite(sprites.REFEREE, sprites.REFEREE_COLOURS),
        "striker": sprites.make_sprite(sprites.STRIKER, sprites.STRIKER_COLOURS),
        "captain": sprites.make_sprite(sprites.CAPTAIN, sprites.CAPTAIN_COLOURS),
        "linesman": sprites.make_sprite(sprites.LINESMAN, sprites.LINESMAN_COLOURS),
        "ball": sprites.make_sprite(sprites.BALL),
    }

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
        scene = story["scenes"][scene_id]

        # Is there a door (or later: an object) right next to the player?
        nearby = find_nearby_action(scene, player["x"], player_width)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # KEYDOWN happens once when a key is pressed (not while held).
            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                if nearby is not None and "go_to" in nearby:
                    # Walk through the door. (Locked doors come in step P5.)
                    came_from = scene_id
                    scene_id = nearby["go_to"]
                    new_scene = story["scenes"][scene_id]
                    player["x"] = arrival_x(new_scene, came_from, player_width)

        # get_pressed() tells us which keys are held down right now.
        keys = pygame.key.get_pressed()
        move_player(player, keys, player_width)

        # 1. Draw the room and the player on the small canvas.
        rooms.draw_room(canvas, scene_id, pictures)
        canvas.blit(player_picture(player, standing, walking), (player["x"], player_y))
        if nearby is not None:
            draw_e_bubble(canvas, player["x"], player_y, player_width)

        # 2. Scale the canvas up to the window size and show it.
        big_picture = pygame.transform.scale(canvas, (WINDOW_WIDTH, WINDOW_HEIGHT))
        window.blit(big_picture, (0, 0))

        # 3. Sharp text on top: room labels and the "E" in the bubble.
        draw_labels(window, label_font, small_font, scene_id)
        if nearby is not None:
            letter = bubble_font.render("E", False, sprites.OUTLINE)
            letter_x = player["x"] + player_width // 2 - 3
            window.blit(letter, (letter_x * SCALE, (player_y - 17) * SCALE))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


# Only start the game when this file is run directly (py game_2d.py).
if __name__ == "__main__":
    main()
