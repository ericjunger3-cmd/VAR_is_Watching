# VAR Is Watching - a short comedy mystery game for the terminal.
# All the story text lives in story.json. This file contains the game logic.

import json
import os


def load_story():
    # Open story.json and turn the JSON text into a Python dictionary.
    # encoding="utf-8" makes sure special characters are read correctly.
    with open("story.json", "r", encoding="utf-8") as file:
        story = json.load(file)
    return story


def new_progress(story):
    # Everything that changes during a game is kept in one dictionary.
    # This is exactly what gets written to save.json.
    progress = {
        "scene": story["start_scene"],   # where the player is
        "inventory": [],                 # item ids, e.g. ["whistle"]
        "choices": {},                   # decisions, e.g. {"press_answer": "goal"}
        "visited": [],                   # scene ids already seen, e.g. ["booth"]
        "ending": None                   # ending id once the game is over
    }
    return progress


def save_progress(progress):
    # Write the progress dictionary to save.json.
    # indent=2 makes the file easy to read if you open it yourself.
    with open("save.json", "w", encoding="utf-8") as file:
        json.dump(progress, file, indent=2)


def load_progress():
    # If there is no save file yet, return None ("nothing saved").
    if not os.path.exists("save.json"):
        return None
    with open("save.json", "r", encoding="utf-8") as file:
        progress = json.load(file)
    # Save files from before "visited" existed do not have it yet.
    if "visited" not in progress:
        progress["visited"] = []
    return progress


def count_clues(story, progress):
    # Count how many clues against the pundit the player has found:
    # the clue items in the inventory plus the clue choices that were made.
    count = 0
    for item_id in story["clue_items"]:
        if item_id in progress["inventory"]:
            count = count + 1
    for choice_name in story["clue_choices"]:
        if choice_name in progress["choices"]:
            count = count + 1
    return count


def pundit_line(story, scene, progress):
    # The pundit says his normal line for the scene, but the more clues
    # the player has found, the more nervous he gets.
    clues = count_clues(story, progress)
    if clues == 0:
        return scene["pundit"]
    # 1 clue -> the first nervous line (index 0), 2 clues -> index 1, ...
    return story["pundit_nervous"][clues - 1]


def show_scene(story, scene_id, first_visit, pundit_text):
    # Look up the scene dictionary by its id, e.g. "booth".
    scene = story["scenes"][scene_id]

    # Print the scene name, the description (only on the first visit)
    # and the pundit's comment.
    print()
    print("=== " + scene["name"] + " ===")
    if first_visit:
        print(scene["text"])
        print()
    print(pundit_text)


def is_hidden(action, inventory, choices):
    # An action that gives an item disappears once the player has that item.
    # This way the same item can never be collected twice.
    if "take_item" in action and action["take_item"] in inventory:
        return True
    # An answer option disappears once that question has been answered.
    # This way a decision can only be made once.
    if "set_choice" in action and action["set_choice"] in choices:
        return True
    return False


def get_visible_actions(scene, inventory, choices):
    # Make a new list with only the actions the player should see right now.
    visible = []
    for action in scene["actions"]:
        if not is_hidden(action, inventory, choices):
            visible.append(action)
    return visible


def blocked_reason(action, inventory, choices):
    # If the action needs an item the player does not have, return the
    # explanation text. Otherwise return None, which means "not blocked".
    if "needs_item" in action and action["needs_item"] not in inventory:
        return action["blocked_text"]
    # Some actions need several items: every one of them must be in the inventory.
    if "needs_items" in action:
        for item_id in action["needs_items"]:
            if item_id not in inventory:
                return action["blocked_text"]
    # Same idea for a decision the player has not made yet.
    if "needs_choice" in action and action["needs_choice"] not in choices:
        return action["blocked_text"]
    return None


def choose_ending(ruling, choices):
    # Decide the ending from the ruling and the choices made during the game.
    # The checks are read from top to bottom; the first one that fits wins.

    # The goal was legal (onside by 30 cm), so OFFSIDE is always the wrong call.
    if ruling == "offside":
        return "daylight_robbery"

    # GOAL, but without studying the footage: right, but only by luck.
    if "review" not in choices:
        return "clip_of_the_year"

    # GOAL after the review. Now the press answer decides the ending.
    # (The Pitch is locked until the press question is answered,
    # so "press_answer" is always in choices here.)
    if choices["press_answer"] == "expose":
        return "var_is_watching"
    if choices["press_answer"] == "no_comment":
        return "justice_served"
    return "right_call_wrong_mouth"


def show_ending(story, ending_id):
    # Print the ending with a clear label, so the player knows the game is over.
    ending = story["endings"][ending_id]
    print()
    print("*****************************************")
    print("ENDING: " + ending["title"])
    print("*****************************************")
    print(ending["text"])
    # Most endings also reveal what the pundit got away with.
    if ending["show_epilogue"]:
        print()
        print(story["epilogue"])


def judge_offside(frame, line_id):
    # Compare the striker with the offside line in one frame of the footage.
    # All positions are metres from the goal line, so a SMALLER number
    # means closer to the goal. If the striker is closer to the goal than
    # the line, he is offside.
    if frame["striker"] < frame[line_id]:
        return "offside"
    return "onside"


def ask_number(question, count):
    # Keep asking until the player types a number from 1 to count.
    # Returns the number the player chose.
    while True:
        answer = input(question + " ").strip()
        if answer.isdigit() and 1 <= int(answer) <= count:
            return int(answer)
        print("Please type a number from 1 to " + str(count) + ".")


def run_review(story):
    # The VAR Review in text form: choose a frame of the footage, then the
    # player to draw the offside line on. Returns "onside" or "offside".
    review = story["review"]
    print()
    print(review["intro"])

    # 1. Choose the frame.
    print()
    number = 1
    for frame in review["frames"]:
        print(str(number) + ". " + frame["name"])
        number = number + 1
    frame = review["frames"][ask_number("Which moment do you freeze?", len(review["frames"])) - 1]

    # 2. Show where everybody is in that frame.
    print()
    print(frame["text"])
    print("Distance to the goal line:")
    print("- Striker (red, number 9): " + str(frame["striker"]) + " m")
    for option in review["line_options"]:
        print("- " + option["name"] + ": " + str(frame[option["id"]]) + " m")

    # 3. Choose where to draw the offside line.
    print()
    number = 1
    for option in review["line_options"]:
        print(str(number) + ". " + option["name"])
        number = number + 1
    option = review["line_options"][ask_number("Draw the offside line at:", len(review["line_options"])) - 1]

    # 4. Show what the line says.
    result = judge_offside(frame, option["id"])
    print()
    if result == "offside":
        print(review["offside_text"])
    else:
        print(review["onside_text"])
    return result


def ask_yes_no(question):
    # Keep asking until the player types y or n.
    # Returns True for yes and False for no.
    while True:
        answer = input(question + " (y/n) ").strip().lower()
        if answer == "y":
            return True
        if answer == "n":
            return False
        print("Please type y or n.")


def start_menu(story):
    # Decide which progress to play with when the game starts.
    progress = load_progress()

    # No save file yet: simply start a new game.
    if progress is None:
        print("No saved game found. Starting a new game.")
        progress = new_progress(story)
        save_progress(progress)
        return progress

    # There is a save file: let the player choose.
    while True:
        print()
        print("n. New game")
        print("c. Continue saved game")
        choice = input("> ").strip().lower()
        if choice == "c":
            return progress
        if choice == "n":
            # Ask first, because a new game replaces the saved progress.
            if ask_yes_no("This deletes your saved progress. Are you sure?"):
                progress = new_progress(story)
                save_progress(progress)
                return progress
            # The player said no: show the menu again, nothing is changed.
        else:
            print("Please type n or c.")


def after_ending_menu(story, ending_id):
    # After an ending no story actions are possible any more.
    # The player can read the ending again, start over or quit.
    # Returns "restart" or "quit".
    while True:
        print()
        print("v. View the ending again")
        print("n. New game")
        print("q. Quit")
        choice = input("> ").strip().lower()
        if choice == "v":
            show_ending(story, ending_id)
        elif choice == "n":
            if ask_yes_no("Start a new game?"):
                return "restart"
        elif choice == "q":
            return "quit"
        else:
            print("Please type v, n or q.")


def show_actions(actions):
    # Print every action with a number in front, starting at 1.
    print()
    number = 1
    for action in actions:
        print(str(number) + ". " + action["label"])
        number = number + 1
    print("i. Inventory")
    print("r. Restart")
    print("q. Quit")


def show_inventory(story, inventory):
    # Print the names of the items the player is carrying.
    print()
    if len(inventory) == 0:
        print("Your pockets are empty.")
    else:
        print("You are carrying:")
        for item_id in inventory:
            # story["items"] turns an id like "usb" into a name like "USB Stick".
            print("- " + story["items"][item_id])


def play_game(story, progress):
    # Play one game until the player quits or wants to restart.
    # Returns "quit" or "restart".

    # If the saved game is already finished, the ending cannot change.
    if progress["ending"] is not None:
        show_ending(story, progress["ending"])
        return after_ending_menu(story, progress["ending"])

    # Short names for the inventory list and the choices dictionary.
    # They point to the same list/dictionary inside progress, so changing
    # inventory also changes progress["inventory"].
    inventory = progress["inventory"]
    choices = progress["choices"]

    # The game loop: show the scene, ask for a choice, react, repeat.
    while True:
        # The full description is only shown the first time we see a scene.
        first_visit = progress["scene"] not in progress["visited"]
        if first_visit:
            progress["visited"].append(progress["scene"])
        scene = story["scenes"][progress["scene"]]
        show_scene(story, progress["scene"], first_visit, pundit_line(story, scene, progress))

        # Only the visible actions get a number in the menu.
        actions = get_visible_actions(scene, inventory, choices)
        show_actions(actions)

        # strip() removes spaces, lower() turns "Q" into "q".
        choice = input("> ").strip().lower()

        if choice == "q":
            return "quit"

        if choice == "i":
            show_inventory(story, inventory)
            continue

        if choice == "r":
            # Only restart if the player confirms. Saying no changes nothing.
            if ask_yes_no("Restart? Your current progress will be lost."):
                return "restart"
            continue

        # isdigit() is True only if the text contains just digits, e.g. "2".
        if not choice.isdigit():
            print("Please type a number from the list.")
            continue

        number = int(choice)
        if number < 1 or number > len(actions):
            print("That number is not in the list.")
            continue

        # The list starts at index 0, but our menu starts at 1, so subtract 1.
        action = actions[number - 1]

        # A blocked action only shows the reason and changes nothing:
        # the player stays in the same scene with the same inventory.
        reason = blocked_reason(action, inventory, choices)
        if reason is not None:
            print()
            print(reason)
            continue

        # Show the result of the action.
        print()
        print(action["text"])

        # A ruling on the Pitch ends the game.
        if "ruling" in action:
            ending_id = choose_ending(action["ruling"], choices)
            # Remember and save the ending, so it cannot be changed later.
            progress["ending"] = ending_id
            save_progress(progress)
            show_ending(story, ending_id)
            return after_ending_menu(story, ending_id)

        # If the action gives an item, add it (but never a second copy).
        if "take_item" in action:
            item_id = action["take_item"]
            if item_id not in inventory:
                inventory.append(item_id)

        # If the action is a decision, remember it in the choices dictionary.
        # The VAR Review is a special decision: its value is what the
        # player's own offside line showed ("onside" or "offside").
        if "set_choice" in action:
            if "review" in action:
                choices[action["set_choice"]] = run_review(story)
            else:
                choices[action["set_choice"]] = action["value"]

        # If the action leads somewhere, move to that scene.
        if "go_to" in action:
            progress["scene"] = action["go_to"]

        # The action was accepted, so save the progress right away.
        save_progress(progress)


def main():
    story = load_story()
    print("*** " + story["title"] + " ***")

    # Ask the player: new game or continue?
    progress = start_menu(story)

    # Keep playing games until the player chooses to quit.
    while True:
        result = play_game(story, progress)
        if result == "quit":
            print("Thanks for playing!")
            break
        # The player confirmed a restart: fresh progress, saved right away.
        progress = new_progress(story)
        save_progress(progress)
        print()
        print("New game started.")


# Only start the game when this file is run directly (py game.py).
if __name__ == "__main__":
    main()
