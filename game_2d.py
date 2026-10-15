# VAR Is Watching - the 2D pixel-art version, made with pygame.
# sprites.py holds the pixel art, rooms.py draws the rooms,
# and this file runs the game.

import pygame
import game
import sprites
import rooms
import ui

# Everything is drawn on a small canvas and then made 2x bigger,
# so each pixel becomes a 2 x 2 block: the "chunky pixel" look.
SCALE = 2
WINDOW_WIDTH = rooms.CANVAS_WIDTH * SCALE
WINDOW_HEIGHT = rooms.CANVAS_HEIGHT * SCALE

# How many canvas pixels the player walks per frame (30 frames per second).
WALK_SPEED = 3

# How many frames each walking picture is shown before switching.
FRAMES_PER_STEP = 5

# How many letters of the dialogue appear per frame (the typing effect).
TYPE_SPEED = 2


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


def find_nearby_actions(scene, progress, player_x, player_width):
    # Find the actions the player can use right here. Usually that is one
    # action (a door, an item), but some spots have several actions at the
    # same x (the press answers, GOAL / OFFSIDE): then they become a menu.
    # get_visible_actions (from game.py) leaves out things already done.
    player_middle = player_x + player_width // 2
    actions = game.get_visible_actions(scene, progress["inventory"], progress["choices"])

    # 1. Find the first action within reach.
    spot_x = None
    for action in actions:
        # abs() turns a negative distance into a positive one.
        if "x" in action and abs(action["x"] - player_middle) <= REACH:
            spot_x = action["x"]
            break
    if spot_x is None:
        return []

    # 2. Collect every action at that same spot.
    nearby = []
    for action in actions:
        if "x" in action and action["x"] == spot_x:
            nearby.append(action)
    return nearby


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


def room_pages(scene, fonts):
    # The dialogue pages for entering a room: its name and its description.
    return ui.make_pages(scene["name"], scene["text"], fonts["text"], SCALE)


def say(screen, text, fonts):
    # Open the dialogue box with a text (split into pages).
    screen["dialogue"] = ui.make_pages("", text, fonts["text"], SCALE)
    screen["letters"] = 0


# ---------------------------------------------------------------- doing actions

def do_action(action, progress, story, screen, fonts, player, player_width):
    # Do what an action from story.json says, after the player chose it.
    # The rules are the same as in game.py; the results are shown on screen.
    inventory = progress["inventory"]
    choices = progress["choices"]

    # 1. Blocked (locked door, steward, no proof ...): show why, change nothing.
    reason = game.blocked_reason(action, inventory, choices)
    if reason is not None:
        say(screen, reason, fonts)
        return

    # 2. The sticky note opens as a close-up.
    if "closeup" in action:
        screen["closeup"] = action["closeup"]
        return

    # 3. The VAR Review opens its own screen (see handle_review_key).
    #    "frame" is the moment in the footage (0 = 0.0 s, 12 = 1.2 s ...),
    #    "line" is where the offside line is, in tenths of a metre (300 = 30.0 m).
    if "review" in action:
        screen["review"] = {"step": "time", "frame": 0, "line": 300}
        # Holding an arrow key now repeats it (after 200 ms, every 30 ms),
        # so the sliders move smoothly.
        pygame.key.set_repeat(200, 30)
        return

    # 4. Everything else shows the action's text first.
    pages = ui.make_pages("", action["text"], fonts["text"], SCALE)

    # Pick up an item (but never a second copy).
    if "take_item" in action:
        item_id = action["take_item"]
        if item_id not in inventory:
            inventory.append(item_id)

    # Remember a decision (press answer, Dave's statement ...).
    if "set_choice" in action:
        choices[action["set_choice"]] = action["value"]

    # A ruling ends the game. The ending screen appears when the text is read.
    if "ruling" in action:
        progress["ending"] = game.choose_ending(action["ruling"], choices)

    # Walk through a door into another room.
    if "go_to" in action:
        came_from = progress["scene"]
        progress["scene"] = action["go_to"]
        new_scene = story["scenes"][progress["scene"]]
        player["x"] = arrival_x(new_scene, came_from, player_width)
        # The room's description only on the first visit.
        if progress["scene"] not in progress["visited"]:
            progress["visited"].append(progress["scene"])
            pages = pages + room_pages(new_scene, fonts)

    screen["dialogue"] = pages
    screen["letters"] = 0


# ---------------------------------------------------------------- keys in each screen mode

def handle_dialogue_key(key, screen):
    # Space, E or Enter: show the whole page, or go to the next page.
    if key in [pygame.K_SPACE, pygame.K_e, pygame.K_RETURN]:
        page = screen["dialogue"][0]
        if screen["letters"] < ui.letters_on_page(page):
            screen["letters"] = ui.letters_on_page(page)
        else:
            screen["dialogue"].pop(0)
            screen["letters"] = 0


def handle_menu_key(key, progress, story, screen, fonts, player, player_width):
    # Up / down chooses an option, Enter (or E / Space) confirms it,
    # the number keys choose directly, Escape closes the menu.
    menu = screen["menu"]
    count = len(menu["actions"])
    if key in [pygame.K_UP, pygame.K_w]:
        menu["selected"] = (menu["selected"] - 1) % count
    elif key in [pygame.K_DOWN, pygame.K_s]:
        menu["selected"] = (menu["selected"] + 1) % count
    elif key == pygame.K_ESCAPE:
        screen["menu"] = None
    else:
        chosen = None
        if key in [pygame.K_RETURN, pygame.K_e, pygame.K_SPACE]:
            chosen = menu["selected"]
        number_keys = [pygame.K_1, pygame.K_2, pygame.K_3]
        for i in range(count):
            if i < len(number_keys) and key == number_keys[i]:
                chosen = i
        if chosen is not None:
            screen["menu"] = None
            do_action(menu["actions"][chosen], progress, story, screen, fonts, player, player_width)


def close_review(screen):
    # Close the review screen and switch key repeat off again
    # (set_repeat() without numbers turns it off).
    screen["review"] = None
    pygame.key.set_repeat()


def handle_review_key(key, progress, story, screen, fonts):
    # Step 1 ("time"): left / right moves through the footage, 0.1 s per
    # press; Enter locks the moment.
    # Step 2 ("line"): left / right moves the offside line, 0.1 m per press;
    # Enter locks it and the result is remembered.
    review = story["review"]
    state = screen["review"]
    if state["step"] == "time":
        # The footage has end / step + 1 moments, e.g. 3.0 / 0.1 + 1 = 31.
        last = int(round(review["end"] / review["step"]))
        if key in [pygame.K_LEFT, pygame.K_a] and state["frame"] > 0:
            state["frame"] = state["frame"] - 1
        elif key in [pygame.K_RIGHT, pygame.K_d] and state["frame"] < last:
            state["frame"] = state["frame"] + 1
        elif key in [pygame.K_RETURN, pygame.K_SPACE, pygame.K_e]:
            state["step"] = "line"
        elif key == pygame.K_ESCAPE:
            # Stop without deciding: nothing is remembered, try again later.
            close_review(screen)
    else:
        # The line moves to the LEFT when its distance from the goal gets
        # BIGGER, so LEFT adds 1 (0.1 m) and RIGHT subtracts 1.
        if key in [pygame.K_LEFT, pygame.K_a] and state["line"] < 400:
            state["line"] = state["line"] + 1
        elif key in [pygame.K_RIGHT, pygame.K_d] and state["line"] > 0:
            state["line"] = state["line"] - 1
        elif key == pygame.K_ESCAPE:
            state["step"] = "time"
        elif key in [pygame.K_RETURN, pygame.K_SPACE, pygame.K_e]:
            # Lock the line: the same rule as in the terminal game.
            time = ui.review_time(review, state)
            striker = game.value_at(review["tracks"]["striker"], time, 1)
            result = game.judge_offside(striker, state["line"] / 10)
            progress["choices"]["review"] = result
            close_review(screen)
            if result == "offside":
                say(screen, review["offside_text"], fonts)
            else:
                say(screen, review["onside_text"], fonts)


def handle_walking_key(key, scene, nearby, progress, story, screen, fonts, player, player_width):
    # While walking, E uses what is nearby: one action directly,
    # several actions at the same spot as a menu.
    if key != pygame.K_e or len(nearby) == 0:
        return

    # If every action here is blocked (e.g. the referee before the press
    # conference), just say why instead of opening a menu.
    reasons = []
    for action in nearby:
        reason = game.blocked_reason(action, progress["inventory"], progress["choices"])
        if reason is not None:
            reasons.append(reason)
    if len(reasons) == len(nearby):
        say(screen, reasons[0], fonts)
        return

    if len(nearby) == 1:
        do_action(nearby[0], progress, story, screen, fonts, player, player_width)
    else:
        screen["menu"] = {"title": scene["menu_title"], "actions": nearby, "selected": 0}


# ---------------------------------------------------------------- what is on screen

def box_is_open(screen):
    # True if any box is open: dialogue, close-up, menu or the VAR Review.
    return (len(screen["dialogue"]) > 0 or screen["closeup"] is not None
            or screen["menu"] is not None or screen["review"] is not None)


def ending_is_showing(progress, screen):
    # The ending screen appears once the game has an ending and the last
    # text has been read (no box open any more).
    return progress["ending"] is not None and not box_is_open(screen)


# ---------------------------------------------------------------- starting a game

def new_game(story, fonts, player):
    # A fresh game: new progress (like game.py), the player in the middle
    # of the booth, and the booth's description in the dialogue box.
    progress = game.new_progress(story)
    progress["visited"].append(progress["scene"])
    player["x"] = 245
    screen = {
        "dialogue": room_pages(story["scenes"][progress["scene"]], fonts),
        "letters": 0,       # how many letters of the page are typed so far
        "closeup": None,    # the lines of the sticky note while it is open
        "menu": None,       # the open menu (press answers, GOAL / OFFSIDE)
        "review": None,     # the VAR Review while it is open
    }
    return progress, screen


def main():
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("VAR Is Watching")
    clock = pygame.time.Clock()
    label_font = pygame.font.SysFont("consolas", 15, bold=True)
    small_label_font = pygame.font.SysFont("consolas", 11, bold=True)
    bubble_font = pygame.font.SysFont("consolas", 22, bold=True)

    # The fonts used by ui.py, kept together in one dictionary.
    # "inkfree" is a handwriting font that comes with Windows.
    fonts = {
        "title": pygame.font.SysFont("consolas", 17, bold=True),
        "text": pygame.font.SysFont("consolas", 17, bold=True),
        "small": pygame.font.SysFont("consolas", 14, bold=True),
        "big": pygame.font.SysFont("consolas", 34, bold=True),
        "hand_big": pygame.font.SysFont("inkfree", 46, bold=True),
        "hand": pygame.font.SysFont("inkfree", 28, bold=True),
    }

    # The story from story.json, reused from the terminal game.
    story = game.load_story()

    # The small canvas we draw the room on, and a see-through overlay for
    # the boxes, so room labels never shine through a box.
    canvas = pygame.Surface((rooms.CANVAS_WIDTH, rooms.CANVAS_HEIGHT))
    overlay = pygame.Surface((rooms.CANVAS_WIDTH, rooms.CANVAS_HEIGHT), pygame.SRCALPHA)

    # Turn the pixel grids into pictures once, at the start.
    standing = sprites.make_sprite(sprites.PLAYER)
    walking = sprites.make_sprite(sprites.PLAYER_WALK)
    player_width = standing.get_width()
    pundit_picture = sprites.make_sprite(sprites.PUNDIT)

    # The characters and objects that live in the rooms.
    # Some use the same letters with their own colours (e.g. the kits).
    pictures = {
        "pombo": sprites.make_sprite(sprites.POMBO),
        "referee": sprites.make_sprite(sprites.REFEREE, sprites.REFEREE_COLOURS),
        "striker": sprites.make_sprite(sprites.STRIKER, sprites.STRIKER_COLOURS),
        "captain": sprites.make_sprite(sprites.CAPTAIN, sprites.CAPTAIN_COLOURS),
        "linesman": sprites.make_sprite(sprites.LINESMAN, sprites.LINESMAN_COLOURS),
        "ball": sprites.make_sprite(sprites.BALL),
        "steward": sprites.make_sprite(sprites.STEWARD),
        "padlock": sprites.make_sprite(sprites.PADLOCK),
        # Item pictures: the key is the item id from story.json.
        "whistle": sprites.make_sprite(sprites.WHISTLE),
        "usb": sprites.make_sprite(sprites.USB),
        "lanyard": sprites.make_sprite(sprites.LANYARD),
        "slip": sprites.make_sprite(sprites.SLIP),
    }

    # Everything about the player in one dictionary.
    player = {
        "x": 245,               # position from the left edge of the room
        "facing_left": False,   # which way the player looks
        "walk_timer": 0         # frames spent walking (for the animation)
    }

    # The y position never changes: the feet always touch the floor.
    player_y = rooms.FLOOR_Y - standing.get_height()

    # progress: the story so far (like in game.py).
    # screen: which boxes are open right now (dialogue, close-up, menu, review).
    progress, screen = new_game(story, fonts, player)

    running = True
    while running:
        scene = story["scenes"][progress["scene"]]

        # Is something open on the screen? Then the player cannot walk.
        free_to_walk = not box_is_open(screen) and not ending_is_showing(progress, screen)

        # What can the player use right here?
        nearby = []
        if free_to_walk:
            nearby = find_nearby_actions(scene, progress, player["x"], player_width)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # KEYDOWN happens once when a key is pressed (not while held).
            if event.type != pygame.KEYDOWN:
                continue

            # Only one thing reacts to a key: whatever is open on top.
            if len(screen["dialogue"]) > 0:
                handle_dialogue_key(event.key, screen)
            elif screen["closeup"] is not None:
                if event.key in [pygame.K_e, pygame.K_SPACE, pygame.K_ESCAPE]:
                    screen["closeup"] = None
            elif screen["menu"] is not None:
                handle_menu_key(event.key, progress, story, screen, fonts, player, player_width)
            elif screen["review"] is not None:
                handle_review_key(event.key, progress, story, screen, fonts)
            elif ending_is_showing(progress, screen):
                if event.key == pygame.K_n:
                    progress, screen = new_game(story, fonts, player)
                elif event.key == pygame.K_q:
                    running = False
            else:
                handle_walking_key(event.key, scene, nearby, progress, story, screen, fonts, player, player_width)

        # The keys may have changed what is open (e.g. N starts a new game),
        # so we check again before walking and drawing.
        scene = story["scenes"][progress["scene"]]
        free_to_walk = not box_is_open(screen) and not ending_is_showing(progress, screen)
        show_ending = ending_is_showing(progress, screen)
        if not free_to_walk:
            nearby = []

        # Walking (only when nothing is open).
        if free_to_walk:
            keys = pygame.key.get_pressed()
            move_player(player, keys, player_width)
        else:
            player["walk_timer"] = 0

        # The typing effect: a few more letters appear every frame.
        if len(screen["dialogue"]) > 0:
            screen["letters"] = screen["letters"] + TYPE_SPEED

        # The picture is built in layers, from the back to the front:
        # 1. The room, the player and the E bubble on the small canvas.
        rooms.draw_room(canvas, progress["scene"], pictures, progress)
        canvas.blit(player_picture(player, standing, walking), (player["x"], player_y))
        if len(nearby) > 0:
            draw_e_bubble(canvas, player["x"], player_y, player_width)
        big_picture = pygame.transform.scale(canvas, (WINDOW_WIDTH, WINDOW_HEIGHT))
        window.blit(big_picture, (0, 0))

        # 2. The sharp room labels and the "E" in the bubble.
        draw_labels(window, label_font, small_label_font, progress["scene"])
        if len(nearby) > 0:
            letter = bubble_font.render("E", False, sprites.OUTLINE)
            letter_x = player["x"] + player_width // 2 - 3
            window.blit(letter, (letter_x * SCALE, (player_y - 17) * SCALE))

        # 3. The boxes on the see-through overlay. fill((0, 0, 0, 0)) wipes it
        #    clean every frame (the 4th number 0 means fully transparent).
        #    The pundit's TV and the inventory are always there.
        overlay.fill((0, 0, 0, 0))
        ui.draw_pundit_tv(overlay, pundit_picture)
        ui.draw_inventory(overlay, progress["inventory"], pictures, len(story["items"]))
        if len(screen["dialogue"]) > 0:
            ui.draw_dialogue_box(overlay, screen["dialogue"][0])
        if screen["menu"] is not None:
            ui.draw_menu_box(overlay)
        if screen["closeup"] is not None:
            ui.draw_note_closeup(overlay)
        if screen["review"] is not None:
            ui.draw_review(overlay, story["review"], screen["review"])
        if show_ending:
            ui.draw_ending_screen(overlay)
        big_overlay = pygame.transform.scale(overlay, (WINDOW_WIDTH, WINDOW_HEIGHT))
        window.blit(big_overlay, (0, 0))

        # 4. The text inside the boxes.
        full_screen = screen["closeup"] is not None or screen["review"] is not None or show_ending
        if not full_screen:
            ui.draw_pundit_text(window, game.pundit_line(story, scene, progress), fonts, SCALE)
        if len(screen["dialogue"]) > 0:
            ui.draw_dialogue_text(window, screen["dialogue"][0], screen["letters"], fonts, SCALE)
        if screen["menu"] is not None:
            ui.draw_menu_text(window, screen["menu"], fonts, SCALE)
        if screen["closeup"] is not None:
            ui.draw_note_text(window, screen["closeup"], fonts, SCALE)
        if screen["review"] is not None:
            ui.draw_review_text(window, story["review"], screen["review"], fonts, SCALE)
        if show_ending:
            ui.draw_ending_text(window, story, progress["ending"], fonts, SCALE)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


# Only start the game when this file is run directly (py game_2d.py).
if __name__ == "__main__":
    main()
