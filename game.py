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


def main():
    story = load_story()
    print("*** " + story["title"] + " ***")

    # For now we only show the starting scene.
    show_scene(story, story["start_scene"])


# Only start the game when this file is run directly (py game.py).
if __name__ == "__main__":
    main()
