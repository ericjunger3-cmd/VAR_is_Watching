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


def show_actions(scene):
    # Print every action of the scene with a number in front, starting at 1.
    print()
    number = 1
    for action in scene["actions"]:
        print(str(number) + ". " + action["label"])
        number = number + 1
    print("q. Quit")


def main():
    story = load_story()
    print("*** " + story["title"] + " ***")

    # current_scene remembers where the player is (a scene id like "booth").
    current_scene = story["start_scene"]

    # The game loop: show the scene, ask for a choice, react, repeat.
    while True:
        show_scene(story, current_scene)
        scene = story["scenes"][current_scene]
        show_actions(scene)

        # strip() removes spaces, lower() turns "Q" into "q".
        choice = input("> ").strip().lower()

        if choice == "q":
            print("Thanks for playing!")
            break

        # isdigit() is True only if the text contains just digits, e.g. "2".
        if not choice.isdigit():
            print("Please type a number from the list.")
            continue

        number = int(choice)
        if number < 1 or number > len(scene["actions"]):
            print("That number is not in the list.")
            continue

        # The list starts at index 0, but our menu starts at 1, so subtract 1.
        action = scene["actions"][number - 1]

        # Show the result of the action and move to the new scene.
        print()
        print(action["text"])
        current_scene = action["go_to"]


# Only start the game when this file is run directly (py game.py).
if __name__ == "__main__":
    main()
