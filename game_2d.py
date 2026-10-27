# VAR Is Watching - the 2D pixel-art version, made with pygame.
# sprites.py holds the pixel art, rooms.py draws the rooms,
# and this file runs the game.

import pygame
import game
import sprites
import rooms
import ui
import sound

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

# The 2D game saves its progress in its own file (same format as save.json).
SAVE_FILE = "save_2d.json"

# How many frames an item needs to fly from the room into its slot.
FLY_FRAMES = 25

# How many frames Dave's reveal (taking off the mask) takes.
REVEAL_FRAMES = 60

# The room sounds that play in the background of some rooms.
ROOM_SOUNDS = {"pitch": "crowd", "dressing_room": "shower"}

# The endings that get the happy jingle (all others get the sad one).
GOOD_ENDINGS = ["var_is_watching", "justice_served", "clip_of_the_year"]



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
    if player["x"] > rooms.ROOM_WIDTH - player_width:
        player["x"] = rooms.ROOM_WIDTH - player_width

    # Count frames while walking; reset when standing still.
    if moving:
        player["walk_timer"] = player["walk_timer"] + 1
    else:
        player["walk_timer"] = 0


def player_picture(player, standing, walking):
    # Choose which picture to draw. Standing still: the front view.
    # Walking: one of the four walking frames in walking (a list).
    # The frame changes every FRAMES_PER_STEP frames:
    # (walk_timer // FRAMES_PER_STEP) counts 0, 1, 2, 3, 4 ... and
    # "% 4" turns that into 0, 1, 2, 3, 0, 1, 2, 3 ...
    if player["walk_timer"] == 0:
        return standing
    frame = (player["walk_timer"] // FRAMES_PER_STEP) % 4
    picture = walking[frame]

    # The walking pictures look to the right. Mirror them when walking left.
    # flip(picture, flip left-right?, flip up-down?)
    if player["facing_left"]:
        picture = pygame.transform.flip(picture, True, False)
    return picture


def walk_bounce(player):
    # The little bounce while walking: on the "legs passing" frames
    # (frame 1 and 3) the body is 1 pixel higher. Returns 0 or 1.
    if player["walk_timer"] == 0:
        return 0
    frame = (player["walk_timer"] // FRAMES_PER_STEP) % 4
    if frame == 1 or frame == 3:
        return 1
    return 0


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


def draw_labels(window, font, small_font, scene_id, offset):
    # Text is drawn on the big window (not the small canvas), so it stays sharp.
    # The positions are room positions: we multiply them by SCALE and
    # subtract offset (how far the camera has moved, in window pixels).
    for text, x, y, colour, small in rooms.LABELS[scene_id]:
        if small:
            label_font = small_font
        else:
            label_font = font
        # render(text, smooth edges, colour): False gives sharp pixel edges.
        picture = label_font.render(text, False, colour)
        window.blit(picture, (x * SCALE - offset, y * SCALE))


def draw_scoreboard_text(window, font, ball, offset):
    # The yellow bar of the scoreboard says "VAR CHECK", or flashes
    # "GOAL?!" while the player's goal is celebrated.
    if ball["celebrate"] > 0:
        text = "GOAL?!"
        x = 226
    else:
        text = "VAR CHECK"
        x = 210
    window.blit(font.render(text, False, (30, 20, 20)), (x * SCALE - offset, 66 * SCALE))


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
        sound.play("bonk")
        say(screen, reason, fonts)
        return

    # 2. The sticky note opens as a close-up.
    if "closeup" in action:
        sound.play("blip")
        screen["closeup"] = action["closeup"]
        return

    # 3. The VAR Review opens its own screen (see handle_review_key).
    #    "frame" is the moment in the footage (0 = 0.0 s, 12 = 1.2 s ...),
    #    "line" is where the offside line is, in tenths of a metre (300 = 30.0 m).
    if "review" in action:
        screen["review"] = {"step": "time", "frame": 0, "line": 300}
        sound.play("beep")
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
            sound.play("pickup")
            # The item flies from where it was into its slot.
            screen["flying"] = {"item": item_id, "x": action["x"], "frame": 0}

    # Remember a decision (press answer, Dave's statement ...).
    if "set_choice" in action:
        choices[action["set_choice"]] = action["value"]
        # Talking to Pombo starts Dave's reveal (taking off the mask).
        if action["set_choice"] == "dave":
            screen["reveal"] = 0
            sound.play("coo")
        # The press: cameras click. The drawer: it squeaks open.
        if action["set_choice"] == "press_answer":
            sound.play("camera")
        if action["set_choice"] == "drawer":
            sound.play("door")

    # A ruling ends the game. The ending screen appears when the text is read.
    if "ruling" in action:
        progress["ending"] = game.choose_ending(action["ruling"], choices)

    # Walk through a door into another room.
    if "go_to" in action:
        # The mascot door opens with the Lucky Whistle; all others creak.
        if action["go_to"] == "mascot_room":
            sound.play("whistle")
        else:
            sound.play("door")
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

    # The action was accepted, so save the progress right away.
    game.save_progress(progress, SAVE_FILE)


# ---------------------------------------------------------------- keys in each screen mode

def handle_dialogue_key(key, screen):
    # Space, E or Enter: show the whole page, or go to the next page.
    if key in [pygame.K_SPACE, pygame.K_e, pygame.K_RETURN]:
        page = screen["dialogue"][0]
        if screen["letters"] < ui.letters_on_page(page):
            screen["letters"] = ui.letters_on_page(page)
        else:
            screen["dialogue"].pop(0)
            # The last page stays in the box, greyed out, until a new text comes.
            if len(screen["dialogue"]) == 0:
                screen["last"] = page
            screen["letters"] = 0


def handle_menu_key(key, progress, story, screen, fonts, player, player_width):
    # Up / down chooses an option, Enter (or E / Space) confirms it,
    # the number keys choose directly, Escape closes the menu.
    menu = screen["menu"]
    count = len(menu["actions"])
    if key in [pygame.K_UP, pygame.K_w]:
        menu["selected"] = (menu["selected"] - 1) % count
        sound.play("blip")
    elif key in [pygame.K_DOWN, pygame.K_s]:
        menu["selected"] = (menu["selected"] + 1) % count
        sound.play("blip")
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
            sound.play("tick")
        elif key in [pygame.K_RIGHT, pygame.K_d] and state["frame"] < last:
            state["frame"] = state["frame"] + 1
            sound.play("tick")
        elif key in [pygame.K_RETURN, pygame.K_SPACE, pygame.K_e]:
            state["step"] = "line"
            sound.play("lock")
        elif key == pygame.K_ESCAPE:
            # Stop without deciding: nothing is remembered, try again later.
            close_review(screen)
    else:
        # The line moves to the LEFT when its distance from the goal gets
        # BIGGER, so LEFT adds 1 (0.1 m) and RIGHT subtracts 1.
        if key in [pygame.K_LEFT, pygame.K_a] and state["line"] < 400:
            state["line"] = state["line"] + 1
            sound.play("tick")
        elif key in [pygame.K_RIGHT, pygame.K_d] and state["line"] > 0:
            state["line"] = state["line"] - 1
            sound.play("tick")
        elif key == pygame.K_ESCAPE:
            state["step"] = "time"
        elif key in [pygame.K_RETURN, pygame.K_SPACE, pygame.K_e]:
            # Lock the line: the same rule as in the terminal game.
            time = ui.review_time(review, state)
            striker = game.value_at(review["tracks"]["striker"], time, 1)
            result = game.judge_offside(striker, state["line"] / 10)
            progress["choices"]["review"] = result
            game.save_progress(progress, SAVE_FILE)
            sound.play("lock")
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


# ---------------------------------------------------------------- the ball on the pitch

KICK_SPEED = 6        # how fast the ball starts rolling after a kick (pixels per frame)
FRICTION = 0.95       # every frame the ball keeps 95 % of its speed
GOAL_X = 394          # the ball is in the goal when it rolls past this x
CELEBRATION = 90      # how many frames the goal celebration lasts (3 seconds)


def new_ball():
    # The ball lies on its spot and does not move.
    # "celebrate" counts down the frames of a goal celebration (0 = none).
    return {"x": float(rooms.BALL_X), "speed": 0.0, "celebrate": 0}


def update_ball(ball, player, player_width):
    # Move the ball one frame: kicks, rolling, bouncing and goals.

    # During a goal celebration the ball waits in the net,
    # then it goes back to its spot.
    if ball["celebrate"] > 0:
        ball["celebrate"] = ball["celebrate"] - 1
        if ball["celebrate"] == 0:
            ball["x"] = float(rooms.BALL_X)
            ball["speed"] = 0.0
        return

    # A kick: the player walks into the ball.
    # The player's feet are a few pixels inside the edges of the picture.
    walking = player["walk_timer"] > 0
    feet_left = player["x"] + 6
    feet_right = player["x"] + player_width - 6
    ball_left = ball["x"]
    ball_right = ball["x"] + 7
    touching = feet_right >= ball_left and feet_left <= ball_right
    if walking and touching:
        sound.play("kick")
        if player["facing_left"]:
            ball["speed"] = -KICK_SPEED
            ball["x"] = feet_left - 8          # push it out of the player's feet
        else:
            ball["speed"] = KICK_SPEED
            ball["x"] = feet_right + 1

    # Rolling: move by the speed, then slow down a bit (friction).
    ball["x"] = ball["x"] + ball["speed"]
    ball["speed"] = ball["speed"] * FRICTION
    if abs(ball["speed"]) < 0.1:
        ball["speed"] = 0.0

    # Bounce off the left edge, losing some speed.
    if ball["x"] < 2:
        ball["x"] = 2
        ball["speed"] = -ball["speed"] * 0.6

    # GOAL! The ball stops in the net and the celebration starts.
    if ball["x"] > GOAL_X:
        ball["x"] = 466.0
        ball["speed"] = 0.0
        ball["celebrate"] = CELEBRATION
        sound.play("goal")


# ---------------------------------------------------------------- what is on screen

def box_is_open(screen):
    # True if any box is open: dialogue, close-up, menu, VAR Review,
    # pause menu or a yes/no question.
    return (len(screen["dialogue"]) > 0 or screen["closeup"] is not None
            or screen["menu"] is not None or screen["review"] is not None
            or screen["pause"] is not None or screen["confirm"] is not None)


def ending_is_showing(progress, screen):
    # The ending screen appears once the game has an ending and the last
    # text has been read (no box open any more).
    return progress["ending"] is not None and not box_is_open(screen)


# ---------------------------------------------------------------- starting a game

def make_screen(dialogue):
    # A fresh screen dictionary: nothing open except the given dialogue.
    return {
        "dialogue": dialogue,
        "letters": 0,       # how many letters of the page are typed so far
        "closeup": None,    # the lines of the sticky note while it is open
        "menu": None,       # the open menu (press answers, GOAL / OFFSIDE)
        "review": None,     # the VAR Review while it is open
        "pause": None,      # the pause menu (Escape) while it is open
        "confirm": None,    # a yes/no question while it is open
        "last": None,       # the last page read (shown greyed out)
        "flying": None,     # an item flying into its slot
        "reveal": None,     # how far Dave's reveal is (in frames)
    }


def new_game(story, fonts, player):
    # A fresh game: new progress (like game.py), saved right away, the player
    # in the middle of the booth and the booth's description on screen.
    progress = game.new_progress(story)
    progress["visited"].append(progress["scene"])
    game.save_progress(progress, SAVE_FILE)
    player["x"] = 245
    screen = make_screen(room_pages(story["scenes"][progress["scene"]], fonts))
    return progress, screen


def continue_game(story, fonts, player, progress, player_width):
    # Continue a saved game. The save file only knows the room, so the
    # player starts in front of the door back to the booth (or in the middle
    # of the booth), with a short reminder of where they are.
    scene = story["scenes"][progress["scene"]]
    if progress["scene"] == story["start_scene"]:
        player["x"] = 245
    else:
        player["x"] = arrival_x(scene, story["start_scene"], player_width)
    pages = ui.make_pages(scene["name"], "You continue where you left off.", fonts["text"], SCALE)
    return make_screen(pages)


# ---------------------------------------------------------------- pause menu and yes/no box

PAUSE_OPTIONS = ["Resume", "Volume", "Fullscreen", "Restart", "Back to the title screen"]


def fullscreen_label():
    # The text for the fullscreen option: it shows if fullscreen is on now.
    if pygame.display.is_fullscreen():
        return "Fullscreen: ON"
    return "Fullscreen: OFF"


def handle_pause_key(key, screen):
    # Up / down chooses, Enter confirms, Escape resumes the game.
    # Returns "title" when the player wants to go back to the title screen.
    pause = screen["pause"]
    choice = PAUSE_OPTIONS[pause["selected"]]
    if key in [pygame.K_UP, pygame.K_w]:
        pause["selected"] = (pause["selected"] - 1) % len(PAUSE_OPTIONS)
        sound.play("blip")
    elif key in [pygame.K_DOWN, pygame.K_s]:
        pause["selected"] = (pause["selected"] + 1) % len(PAUSE_OPTIONS)
        sound.play("blip")
    elif choice == "Volume" and key in [pygame.K_LEFT, pygame.K_a]:
        sound.change_volume(-1)
    elif choice == "Volume" and key in [pygame.K_RIGHT, pygame.K_d]:
        sound.change_volume(1)
    elif key == pygame.K_ESCAPE:
        screen["pause"] = None
    elif choice == "Volume":
        # Enter on the volume slider does nothing (use left / right).
        return None
    elif key in [pygame.K_RETURN, pygame.K_SPACE, pygame.K_e]:
        sound.play("confirm")
        if choice == "Fullscreen":
            # Switch, and keep the pause menu open (you see ON / OFF change).
            pygame.display.toggle_fullscreen()
            return None
        screen["pause"] = None
        if choice == "Restart":
            # Restarting deletes the progress, so ask first.
            screen["confirm"] = "Restart? Your current progress will be lost."
        elif choice == "Back to the title screen":
            return "title"
    return None


# ---------------------------------------------------------------- drawing

def draw_game(assets, story, progress, screen, player, nearby, moving):
    # Draw one picture of the game, in layers from the back to the front.
    window = assets["window"]
    canvas = assets["canvas"]
    overlay = assets["overlay"]
    fonts = assets["fonts"]
    player_y = assets["player_y"]
    player_width = assets["standing"].get_width()
    scene = story["scenes"][progress["scene"]]
    show_ending = ending_is_showing(progress, screen)
    ball = moving["ball"]
    tick = moving["tick"]
    # How far the camera has moved, in WINDOW pixels (not canvas pixels).
    # Because one canvas pixel is 2 window pixels, this lets the camera
    # move in smaller, smoother steps.
    offset = int(round(moving["camera"] * SCALE))

    # 1. The room and the player on the (wider) room canvas. The whole room
    #    is scaled up and placed so that the camera's part is in the window.
    extras = {"tick": tick, "ball": ball, "reveal": screen["reveal"]}
    rooms.draw_room(canvas, progress["scene"], assets["pictures"], progress, extras)
    picture = player_picture(player, assets["standing"], assets["walking"])
    canvas.blit(picture, (player["x"], player_y - walk_bounce(player)))
    big_room = pygame.transform.scale(canvas, (rooms.ROOM_WIDTH * SCALE, WINDOW_HEIGHT))
    window.blit(big_room, (-offset, 0))

    # 2. The sharp room labels and the breathing "E" bubble.
    draw_labels(window, fonts["label"], fonts["label_small"], progress["scene"], offset)
    if progress["scene"] == "pitch":
        draw_scoreboard_text(window, fonts["label"], ball, offset)
    if len(nearby) > 0:
        middle_x = (player["x"] + player_width // 2) * SCALE - offset
        ui.draw_e_bubble(window, middle_x, (player_y - 12) * SCALE, tick, fonts["bubble"])

    # 3. The boxes on the see-through overlay. fill((0, 0, 0, 0)) wipes it
    #    clean every frame (the 4th number 0 means fully transparent).
    #    The pundit's TV and the inventory are always there.
    overlay.fill((0, 0, 0, 0))
    ui.draw_pundit_tv(overlay, assets["pundit"])
    flying_item = None
    if screen["flying"] is not None:
        flying_item = screen["flying"]["item"]
    ui.draw_inventory(overlay, progress["inventory"], assets["pictures"], len(story["items"]), tick, flying_item)
    if flying_item is not None:
        slot = progress["inventory"].index(flying_item)
        ui.draw_flying_item(overlay, assets["pictures"][flying_item], screen["flying"]["x"] - offset // SCALE,
                            160, slot, screen["flying"]["frame"], FLY_FRAMES)
    ui.draw_timer(overlay, progress["seconds_left"], story["time_limit_seconds"], tick)

    # The text bar: the current page, or (greyed out) the last page read.
    menu_open = screen["menu"] is not None or screen["pause"] is not None
    full_screen = screen["closeup"] is not None or screen["review"] is not None or show_ending
    show_last = (len(screen["dialogue"]) == 0 and not menu_open and not full_screen
                 and screen["last"] is not None)
    if len(screen["dialogue"]) > 0:
        ui.draw_dialogue_box(overlay, screen["dialogue"][0])
    elif show_last:
        ui.draw_dialogue_box(overlay, screen["last"], True)
    if screen["menu"] is not None:
        ui.draw_menu_box(overlay, len(screen["menu"]["actions"]))
    if screen["pause"] is not None:
        ui.draw_menu_box(overlay, len(PAUSE_OPTIONS))
    if screen["closeup"] is not None:
        ui.draw_note_closeup(overlay)
    if screen["review"] is not None:
        ui.draw_review(overlay, story["review"], screen["review"])
    if show_ending:
        ui.draw_ending_screen(overlay)
    if screen["confirm"] is not None:
        ui.draw_confirm_box(overlay)
    window.blit(pygame.transform.scale(overlay, (WINDOW_WIDTH, WINDOW_HEIGHT)), (0, 0))

    # 4. The text inside the boxes.
    if not full_screen:
        ui.draw_timer_text(window, progress["seconds_left"], fonts, SCALE)
    if not full_screen and screen["confirm"] is None:
        # After a goal with the ball, the pundit comments on that instead.
        if progress["scene"] == "pitch" and ball["celebrate"] > 0:
            pundit_text = story["ball_goal_pundit"]
        else:
            pundit_text = game.pundit_line(story, scene, progress)
        ui.draw_pundit_text(window, pundit_text, fonts, SCALE)
    if len(screen["dialogue"]) > 0:
        ui.draw_dialogue_text(window, screen["dialogue"][0], screen["letters"], fonts, SCALE)
    elif show_last:
        ui.draw_dialogue_text(window, screen["last"], 9999, fonts, SCALE, True)
    if screen["menu"] is not None:
        ui.draw_menu_text(window, screen["menu"], fonts, SCALE)
    if screen["pause"] is not None:
        # The pause menu looks like the other menus: a title and options.
        pause_menu = {"title": "Paused", "actions": [], "selected": screen["pause"]["selected"]}
        for option in PAUSE_OPTIONS:
            if option == "Fullscreen":
                option = fullscreen_label()
            if option == "Volume":
                option = sound.volume_text()
            pause_menu["actions"].append({"label": option})
        ui.draw_menu_text(window, pause_menu, fonts, SCALE)
    if screen["closeup"] is not None:
        ui.draw_note_text(window, screen["closeup"], fonts, SCALE)
    if screen["review"] is not None:
        ui.draw_review_text(window, story["review"], screen["review"], fonts, SCALE)
    if show_ending:
        ui.draw_ending_text(window, story, progress["ending"], fonts, SCALE)
    if screen["confirm"] is not None:
        ui.draw_confirm_text(window, screen["confirm"], fonts, SCALE)


# ---------------------------------------------------------------- the title screen

def title_screen(assets, story):
    # Show the title screen until the player chooses something.
    # Returns "play", "new" or "exit".
    clock = pygame.time.Clock()
    labels = ["Play", "New Game", "Volume", "Fullscreen", "Exit"]
    selected = 0
    confirm = None      # the yes/no question, while it is open
    tick = 0    # the frame counter, for the animations
    sound.play_music("title_theme")
    sound.set_ambience(None)

    while True:
        has_save = game.load_progress(SAVE_FILE) is not None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            if event.type != pygame.KEYDOWN:
                continue

            # F11 switches between window and fullscreen, at any moment.
            if event.key == pygame.K_F11:
                pygame.display.toggle_fullscreen()
                continue
            # M mutes and unmutes all sound, at any moment.
            if event.key == pygame.K_m:
                sound.toggle_mute()
                continue

            if confirm is not None:
                # Only Y or N answer the question.
                if event.key == pygame.K_y:
                    return "new"
                if event.key in [pygame.K_n, pygame.K_ESCAPE]:
                    confirm = None
            elif event.key in [pygame.K_UP, pygame.K_w]:
                selected = (selected - 1) % len(labels)
                sound.play("blip")
            elif event.key in [pygame.K_DOWN, pygame.K_s]:
                selected = (selected + 1) % len(labels)
                sound.play("blip")
            elif labels[selected] == "Volume" and event.key in [pygame.K_LEFT, pygame.K_a]:
                sound.change_volume(-1)
            elif labels[selected] == "Volume" and event.key in [pygame.K_RIGHT, pygame.K_d]:
                sound.change_volume(1)
            elif event.key in [pygame.K_RETURN, pygame.K_SPACE, pygame.K_e]:
                choice = labels[selected]
                if choice != "Volume":
                    sound.play("confirm")
                if choice == "Play":
                    return "play"
                if choice == "Exit":
                    return "exit"
                if choice == "Fullscreen":
                    pygame.display.toggle_fullscreen()
                if choice == "New Game":
                    # A new game replaces a saved game, so ask first.
                    if has_save:
                        confirm = "Start a new game? This deletes your saved progress."
                    else:
                        return "new"

        # Draw: the pitch, the title, the buttons and (maybe) the question.
        canvas = assets["canvas"]
        overlay = assets["overlay"]
        window = assets["window"]
        tick = tick + 1
        rooms.draw_title_background(canvas, assets["pictures"], tick)
        view = canvas.subsurface((0, 0, rooms.CANVAS_WIDTH, rooms.CANVAS_HEIGHT))
        window.blit(pygame.transform.scale(view, (WINDOW_WIDTH, WINDOW_HEIGHT)), (0, 0))
        overlay.fill((0, 0, 0, 0))
        # The fullscreen option shows ON or OFF, so we change its text.
        shown = []
        for label in labels:
            if label == "Fullscreen":
                label = fullscreen_label()
            shown.append(label)
        ui.draw_title_screen(overlay, shown, selected, tick, assets["pictures"], sound.loudness())
        if confirm is not None:
            ui.draw_confirm_box(overlay)
        window.blit(pygame.transform.scale(overlay, (WINDOW_WIDTH, WINDOW_HEIGHT)), (0, 0))
        if confirm is None:
            ui.draw_title_text(window, has_save, assets["fonts"], SCALE)
        else:
            ui.draw_confirm_text(window, confirm, assets["fonts"], SCALE)
        pygame.display.flip()
        clock.tick(30)


# ---------------------------------------------------------------- playing

def play(assets, story, progress, screen, player):
    # The game loop. Returns "title" (back to the title screen) or
    # "quit" (the window was closed). The progress is saved after every
    # accepted action, so nothing is lost either way.
    clock = pygame.time.Clock()
    fonts = assets["fonts"]
    player_width = assets["standing"].get_width()
    # Everything that moves on screen but is not part of the story:
    # the frame counter (for animations), the ball (just for fun, not
    # saved) and the camera position.
    moving = {"tick": 0, "ball": new_ball(), "camera": 0.0}
    # Has the ending jingle been played? (So it plays only once.)
    jingle_played = False
    sound.play_music("game_theme")

    while True:
        scene = story["scenes"][progress["scene"]]

        # Is something open on the screen? Then the player cannot walk.
        free_to_walk = not box_is_open(screen) and not ending_is_showing(progress, screen)

        # What can the player use right here?
        nearby = []
        if free_to_walk:
            nearby = find_nearby_actions(scene, progress, player["x"], player_width)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            # KEYDOWN happens once when a key is pressed (not while held).
            if event.type != pygame.KEYDOWN:
                continue

            # F11 switches between window and fullscreen, at any moment.
            if event.key == pygame.K_F11:
                pygame.display.toggle_fullscreen()
                continue
            # M mutes and unmutes all sound, at any moment.
            if event.key == pygame.K_m:
                sound.toggle_mute()
                continue

            # Only one thing reacts to a key: whatever is open on top.
            if screen["confirm"] is not None:
                if event.key == pygame.K_y:
                    # Yes: start a fresh game (it is saved right away).
                    progress, screen = new_game(story, fonts, player)
                elif event.key in [pygame.K_n, pygame.K_ESCAPE]:
                    # No: close the question, nothing changes.
                    screen["confirm"] = None
            elif len(screen["dialogue"]) > 0:
                handle_dialogue_key(event.key, screen)
            elif screen["closeup"] is not None:
                if event.key in [pygame.K_e, pygame.K_SPACE, pygame.K_ESCAPE]:
                    screen["closeup"] = None
            elif screen["menu"] is not None:
                handle_menu_key(event.key, progress, story, screen, fonts, player, player_width)
            elif screen["review"] is not None:
                handle_review_key(event.key, progress, story, screen, fonts)
            elif screen["pause"] is not None:
                if handle_pause_key(event.key, screen) == "title":
                    # Save the time that is left before leaving.
                    game.save_progress(progress, SAVE_FILE)
                    return "title"
            elif ending_is_showing(progress, screen):
                if event.key == pygame.K_n:
                    # A new game replaces the finished game, so ask first.
                    screen["confirm"] = "Start a new game? The finished game will be deleted."
                elif event.key == pygame.K_q:
                    return "title"
            elif event.key == pygame.K_ESCAPE:
                screen["pause"] = {"selected": 0}
                sound.play("blip")
                game.save_progress(progress, SAVE_FILE)
            else:
                handle_walking_key(event.key, scene, nearby, progress, story, screen, fonts, player, player_width)

        # The keys may have changed what is open (e.g. a new game started),
        # so we check again before walking and drawing.
        free_to_walk = not box_is_open(screen) and not ending_is_showing(progress, screen)
        if not free_to_walk:
            nearby = []

        # Walking (only when nothing is open).
        if free_to_walk:
            keys = pygame.key.get_pressed()
            move_player(player, keys, player_width)
        else:
            player["walk_timer"] = 0

        # The ball rolls on the pitch.
        if progress["scene"] == "pitch":
            update_ball(moving["ball"], player, player_width)

        # The stadium is waiting: the time runs, except in the pause menu,
        # during a yes/no question and after the game has ended.
        paused = screen["pause"] is not None or screen["confirm"] is not None
        if progress["ending"] is None and not paused:
            progress["seconds_left"] = progress["seconds_left"] - 1 / 30
            if progress["seconds_left"] <= 0:
                # Time is up: close everything, the ending screen appears.
                progress["seconds_left"] = 0
                progress["ending"] = "time_up"
                screen["menu"] = None
                screen["closeup"] = None
                screen["dialogue"] = []
                if screen["review"] is not None:
                    close_review(screen)
                game.save_progress(progress, SAVE_FILE)

        # Animations: the frame counter, the flying item and Dave's reveal.
        moving["tick"] = moving["tick"] + 1

        # Sounds: the room sound (crowd, shower or nothing), the cameras
        # when they flash (the same moments as in rooms.py), and the
        # ending jingle, once, when the ending screen appears.
        sound.set_ambience(ROOM_SOUNDS.get(progress["scene"]))
        if progress["scene"] == "press_room" and moving["tick"] % 50 == 0:
            sound.play("camera")
        if progress["scene"] == "pitch" and moving["tick"] % 70 == 0:
            sound.play("camera")
        if ending_is_showing(progress, screen) and not jingle_played:
            sound.stop_music()
            if progress["ending"] in GOOD_ENDINGS:
                sound.play("jingle_good")
            else:
                sound.play("jingle_bad")
            jingle_played = True
        if progress["ending"] is None and jingle_played:
            # A new game was started after an ending: the music comes back.
            jingle_played = False
            sound.play_music("game_theme")
        if screen["flying"] is not None:
            screen["flying"]["frame"] = screen["flying"]["frame"] + 1
            if screen["flying"]["frame"] >= FLY_FRAMES:
                screen["flying"] = None
        if screen["reveal"] is not None:
            screen["reveal"] = screen["reveal"] + 1
            if screen["reveal"] >= REVEAL_FRAMES:
                screen["reveal"] = None

        # The camera follows the player exactly: it keeps the player in the
        # middle of the window, but never shows anything outside the room.
        # max(0, ...) and min(..., 20) keep it between 0 and 20 pixels.
        player_middle = player["x"] + player_width // 2
        target = player_middle - rooms.CANVAS_WIDTH // 2
        moving["camera"] = max(0, min(target, rooms.ROOM_WIDTH - rooms.CANVAS_WIDTH))

        # The typing effect: a few more letters appear every frame,
        # with a soft blip every third frame while the text is typing.
        if len(screen["dialogue"]) > 0:
            if screen["letters"] < ui.letters_on_page(screen["dialogue"][0]) and moving["tick"] % 3 == 0:
                sound.play("type")
            screen["letters"] = screen["letters"] + TYPE_SPEED

        draw_game(assets, story, progress, screen, player, nearby, moving)
        pygame.display.flip()
        clock.tick(30)


def main():
    # A small sound buffer (512) makes the sounds play without delay.
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.init()
    sound.start()
    # The game's logo in the title bar and the taskbar (set it before
    # the window opens).
    pygame.display.set_icon(pygame.image.load("icon.png"))

    # SCALED: in fullscreen, the game picture is made bigger to fill the
    # screen (with black bars if the screen has a different shape).
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SCALED)
    pygame.display.set_caption("VAR Is Watching")

    # The fonts, kept together in one dictionary.
    # "inkfree" is a handwriting font that comes with Windows.
    fonts = {
        "title": pygame.font.SysFont("consolas", 17, bold=True),
        "text": pygame.font.SysFont("consolas", 17, bold=True),
        "small": pygame.font.SysFont("consolas", 14, bold=True),
        "big": pygame.font.SysFont("consolas", 34, bold=True),
        "hand_big": pygame.font.SysFont("inkfree", 46, bold=True),
        "hand": pygame.font.SysFont("inkfree", 28, bold=True),
        "label": pygame.font.SysFont("consolas", 15, bold=True),
        "label_small": pygame.font.SysFont("consolas", 11, bold=True),
        "bubble": pygame.font.SysFont("consolas", 16, bold=True),
        "tiny": pygame.font.SysFont("consolas", 11, bold=True),
    }

    # Everything we need for drawing, kept together in one dictionary,
    # so we don't have to pass ten things to every function.
    standing = sprites.make_sprite(sprites.PLAYER)
    assets = {
        "window": window,
        # The small canvas for the rooms, and a see-through overlay for the
        # boxes, so room labels never shine through a box.
        "canvas": pygame.Surface((rooms.ROOM_WIDTH, rooms.CANVAS_HEIGHT)),
        "overlay": pygame.Surface((rooms.CANVAS_WIDTH, rooms.CANVAS_HEIGHT), pygame.SRCALPHA),
        "fonts": fonts,
        "standing": standing,
        # The four walking pictures (3/4 view), made one by one in a loop.
        "walking": [],
        "pundit": sprites.make_sprite(sprites.PUNDIT, sprites.PUNDIT_COLOURS),
        # The feet always touch the floor.
        "player_y": rooms.FLOOR_Y - standing.get_height(),
        # The characters and objects that live in the rooms. Some use the
        # same letters with their own colours (e.g. the kits).
        "pictures": {
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
            # Pombo in parts, and Dave's own face, for the reveal.
            "pombo_head": sprites.make_sprite(sprites.POMBO_HEAD),
            "pombo_body": sprites.make_sprite(sprites.POMBO_BODY),
            "dave_head": sprites.make_sprite(sprites.DAVE_HEAD),
            "lanyard": sprites.make_sprite(sprites.LANYARD),
            "slip": sprites.make_sprite(sprites.SLIP),
            # For the title screen: the VAR screen above the logo and the arrow.
            "var_screen": sprites.make_sprite(sprites.VAR_SCREEN),
            "arrow": sprites.make_sprite(sprites.ARROW),
            "player": standing,
        },
    }

    for frame in sprites.PLAYER_WALK:
        assets["walking"].append(sprites.make_sprite(frame))

    # The story from story.json, reused from the terminal game.
    story = game.load_story()

    # Everything about the player in one dictionary.
    player = {
        "x": 245,               # position from the left edge of the room
        "facing_left": False,   # which way the player looks
        "walk_timer": 0         # frames spent walking (for the animation)
    }

    # Title screen -> game -> title screen ... until the player exits.
    while True:
        choice = title_screen(assets, story)
        if choice == "exit":
            break
        saved = game.load_progress(SAVE_FILE)
        if saved is not None:
            # Older save files may miss some keys (e.g. seconds_left).
            game.add_missing_keys(saved, story)
        if choice == "play" and saved is not None:
            progress = saved
            screen = continue_game(story, fonts, player, progress, standing.get_width())
        else:
            progress, screen = new_game(story, fonts, player)
        if play(assets, story, progress, screen, player) == "quit":
            break

    pygame.quit()


# Only start the game when this file is run directly (py game_2d.py).
if __name__ == "__main__":
    main()
