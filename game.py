# VAR Is Watching - a short comedy mystery game for the terminal.
# All the story text lives in story.json. This file contains the game logic.

import json


def load_story():
    # Open story.json and turn the JSON text into a Python dictionary.
    # encoding="utf-8" makes sure special characters are read correctly.
    with open("story.json", "r", encoding="utf-8") as file:
        story = json.load(file)
    return story


def show_scene(story, scene_id):
    # Look up the scene dictionary by its id, e.g. "booth".
    scene = story["scenes"][scene_id]

    # Print the scene name, the description and the pundit's comment.
    print()
    print("=== " + scene["name"] + " ===")
    print(scene["text"])
    print()
    print(scene["pundit"])


def is_hidden(action, inventory):
    # An action that gives an item disappears once the player has that item.
    # This way the same item can never be collected twice.
    if "take_item" in action and action["take_item"] in inventory:
        return True
    return False


def get_visible_actions(scene, inventory):
    # Make a new list with only the actions the player should see right now.
    visible = []
    for action in scene["actions"]:
        if not is_hidden(action, inventory):
            visible.append(action)
    return visible


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

    # current_scene remembers where the player is (a scene id like "booth").
    current_scene = story["start_scene"]

    # inventory is a list of item ids the player carries, e.g. ["whistle"].
    inventory = []

    # The game loop: show the scene, ask for a choice, react, repeat.
    while True:
        show_scene(story, current_scene)
        scene = story["scenes"][current_scene]

        # Only the visible actions get a number in the menu.
        actions = get_visible_actions(scene, inventory)
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

        # Show the result of the action.
        print()
        print(action["text"])

        # If the action gives an item, add it (but never a second copy).
        if "take_item" in action:
            item_id = action["take_item"]
            if item_id not in inventory:
                inventory.append(item_id)

        # If the action leads somewhere, move to that scene.
        if "go_to" in action:
            current_scene = action["go_to"]


# Only start the game when this file is run directly (py game.py).
if __name__ == "__main__":
    main()
