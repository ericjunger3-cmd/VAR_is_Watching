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
    return progress


def show_scene(story, scene_id):
    # Look up the scene dictionary by its id, e.g. "booth".
    scene = story["scenes"][scene_id]

    # Print the scene name, the description and the pundit's comment.
    print()
    print("=== " + scene["name"] + " ===")
    print(scene["text"])
    print()
    print(scene["pundit"])


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
    # Same idea for a decision the player has not made yet.
    if "needs_choice" in action and action["needs_choice"] not in choices:
        return action["blocked_text"]
    return None


def choose_ending(ruling, inventory, choices):
    # Decide the ending from the ruling, the inventory and the press answer.
    # Returns the id of an ending, or None if the ruling is refused.

    # Without the USB Stick there is no evidence: either ruling goes viral.
    if "usb" not in inventory:
        return "clip_of_the_year"

    # With the USB Stick the footage shows it was a goal,
    # so ruling offside is refused.
    if ruling == "offside":
        return None

    # The ruling is GOAL. Now the press answer decides the ending.
    # (The Pitch is locked until the press question is answered,
    # so "press_answer" is always in choices here.)
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


def after_ending_menu(story, ending_id):
    # After an ending no story actions are possible any more.
    # The player can only read the ending again or quit.
    while True:
        print()
        print("v. View the ending again")
        print("q. Quit")
        choice = input("> ").strip().lower()
        if choice == "v":
            show_ending(story, ending_id)
        elif choice == "q":
            print("Thanks for playing!")
            break
        else:
            print("Please type v or q.")


def show_actions(actions):
    # Print every action with a number in front, starting at 1.
    print()
    number = 1
    for action in actions:
        print(str(number) + ". " + action["label"])
        number = number + 1
    print("i. Inventory")
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


def main():
    story = load_story()
    print("*** " + story["title"] + " ***")

    # Continue the saved game if there is one, otherwise start a new one.
    # (Step 8 will ask the player first.)
    progress = load_progress()
    if progress is None:
        progress = new_progress(story)

    # If the saved game is already finished, the ending cannot change.
    if progress["ending"] is not None:
        show_ending(story, progress["ending"])
        after_ending_menu(story, progress["ending"])
        return

    # Short names for the inventory list and the choices dictionary.
    # They point to the same list/dictionary inside progress, so changing
    # inventory also changes progress["inventory"].
    inventory = progress["inventory"]
    choices = progress["choices"]

    # The game loop: show the scene, ask for a choice, react, repeat.
    while True:
        show_scene(story, progress["scene"])
        scene = story["scenes"][progress["scene"]]

        # Only the visible actions get a number in the menu.
        actions = get_visible_actions(scene, inventory, choices)
        show_actions(actions)

        # strip() removes spaces, lower() turns "Q" into "q".
        choice = input("> ").strip().lower()

        if choice == "q":
            print("Thanks for playing!")
            break

        if choice == "i":
            show_inventory(story, inventory)
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

        # A ruling on the Pitch can end the game.
        if "ruling" in action:
            ending_id = choose_ending(action["ruling"], inventory, choices)
            if ending_id is None:
                # The ruling was refused: show why and change nothing.
                print()
                print(action["wrong_call_text"])
                continue
            # Remember and save the ending, so it cannot be changed later.
            progress["ending"] = ending_id
            save_progress(progress)
            show_ending(story, ending_id)
            after_ending_menu(story, ending_id)
            break

        # Show the result of the action.
        print()
        print(action["text"])

        # If the action gives an item, add it (but never a second copy).
        if "take_item" in action:
            item_id = action["take_item"]
            if item_id not in inventory:
                inventory.append(item_id)

        # If the action is a decision, remember it in the choices dictionary.
        if "set_choice" in action:
            choices[action["set_choice"]] = action["value"]

        # If the action leads somewhere, move to that scene.
        if "go_to" in action:
            progress["scene"] = action["go_to"]

        # The action was accepted, so save the progress right away.
        save_progress(progress)


# Only start the game when this file is run directly (py game.py).
if __name__ == "__main__":
    main()
