# Tests for VAR Is Watching.
# They check the acceptance scenarios A1-A6 from the Plot Twist brief
# (and a few more rules) with the functions from game.py.
# Run them with:  py test_game.py   (Mac: python3 test_game.py)
# Every test uses "assert": if the check is False, the test fails.

import os
import game

# A separate save file, so the tests never touch your real save.json.
TEST_SAVE = "test_save.json"


def find_action(story, scene_id, label_start):
    # Find an action in a scene by the start of its label,
    # e.g. "Go to the Mascot" in the booth.
    for action in story["scenes"][scene_id]["actions"]:
        if action["label"].startswith(label_start):
            return action
    return None


def test_a1_locked_route(story):
    # A1: without the Lucky Whistle, the Mascot Changing Room is locked.
    # A blocked action only shows a reason, so the scene and the
    # inventory stay the same.
    progress = game.new_progress(story)
    door = find_action(story, "booth", "Go to the Mascot")
    reason = game.blocked_reason(door, progress["inventory"], progress["choices"])
    assert reason is not None
    assert progress["scene"] == "booth"
    assert progress["inventory"] == []


def test_a2_unlocked_route(story):
    # A2: with the whistle, the door opens, leads to the Mascot Changing
    # Room, and the whistle stays in the inventory (items are reusable).
    progress = game.new_progress(story)
    progress["inventory"].append("whistle")
    door = find_action(story, "booth", "Go to the Mascot")
    assert game.blocked_reason(door, progress["inventory"], progress["choices"]) is None
    assert door["go_to"] == "mascot_room"
    assert "whistle" in progress["inventory"]


def test_a3_no_duplicate(story):
    # A3: once the whistle is in the inventory, the "take" action is
    # hidden, so it can never be collected a second time.
    progress = game.new_progress(story)
    progress["choices"]["drawer"] = "open"
    take = find_action(story, "dressing_room", "Take the Lucky Whistle")
    assert not game.is_hidden(take, progress["inventory"], progress["choices"])
    progress["inventory"].append("whistle")
    assert game.is_hidden(take, progress["inventory"], progress["choices"])
    assert progress["inventory"].count("whistle") == 1


def test_a4_resume(story):
    # A4: after getting an item and making a choice, saving and loading
    # gives back the same scene, item, choice and available actions.
    progress = game.new_progress(story)
    progress["scene"] = "mascot_room"
    progress["inventory"].append("whistle")
    progress["choices"]["dave"] = "talked"
    game.save_progress(progress, TEST_SAVE)
    loaded = game.load_progress(TEST_SAVE)
    os.remove(TEST_SAVE)
    assert loaded["scene"] == "mascot_room"
    assert loaded["inventory"] == ["whistle"]
    assert loaded["choices"]["dave"] == "talked"
    scene = story["scenes"]["mascot_room"]
    before = game.get_visible_actions(scene, progress["inventory"], progress["choices"])
    after = game.get_visible_actions(scene, loaded["inventory"], loaded["choices"])
    assert before == after


def test_a5_two_outcomes(story):
    # A5: two different paths reach two different endings, and a saved
    # ending stays the same after loading.
    bad = game.choose_ending("offside", {"press_answer": "goal"})
    good = game.choose_ending("goal", {"review": "onside", "press_answer": "no_comment"})
    assert bad == "daylight_robbery"
    assert good == "justice_served"
    progress = game.new_progress(story)
    progress["ending"] = good
    game.save_progress(progress, TEST_SAVE)
    loaded = game.load_progress(TEST_SAVE)
    os.remove(TEST_SAVE)
    assert loaded["ending"] == "justice_served"


def test_a6_restart(story):
    # A6: a new game starts in the opening scene with an empty inventory
    # and no decisions.
    progress = game.new_progress(story)
    assert progress["scene"] == story["start_scene"]
    assert progress["inventory"] == []
    assert progress["choices"] == {}
    assert progress["ending"] is None


def test_offside_rule(story):
    # The VAR Review: at 1.2 s the striker is at 21.8 m and the 2nd-last
    # defender at 21.5 m, so the right line gives ONSIDE (by 30 cm).
    # Level counts as onside.
    tracks = story["review"]["tracks"]
    striker = game.value_at(tracks["striker"], 1.2, 1)
    defender = game.value_at(tracks["deep_defender"], 1.2, 1)
    assert round(striker, 1) == 21.8
    assert round(defender, 1) == 21.5
    assert game.judge_offside(striker, defender) == "onside"
    assert game.judge_offside(21.8, 21.8) == "onside"
    assert game.judge_offside(21.8, 21.9) == "offside"


def test_expose_needs_all_clues(story):
    # The option to expose Infantini stays hidden until the player has the lanyard,
    # the betting slip AND Dave's statement. Clues are choices, not items.
    expose = find_action(story, "press_room", "Say: 'Gianno Infantini")
    assert game.is_hidden(expose, [], {"lanyard": "found", "slip": "found"})
    assert game.is_hidden(expose, [], {"lanyard": "found", "dave": "talked"})
    assert not game.is_hidden(expose, [], {"lanyard": "found", "slip": "found", "dave": "talked"})


def test_clues_are_not_items(story):
    # Finding a clue never puts it in the inventory, and an old save that
    # still has a clue as an item is converted when it is loaded.
    assert "lanyard" not in story["items"]
    assert "slip" not in story["items"]
    progress = game.new_progress(story)
    progress["inventory"] = ["whistle", "lanyard"]
    game.save_progress(progress, TEST_SAVE)
    loaded = game.load_progress(TEST_SAVE)
    os.remove(TEST_SAVE)
    assert loaded["inventory"] == ["whistle"]
    assert loaded["choices"]["lanyard"] == "found"


def test_pundit_hints(story):
    # The pundit's hint changes with the progress, and he gets more
    # nervous with every clue.
    progress = game.new_progress(story)
    first = game.current_hint(story, progress)
    progress["inventory"].append("whistle")
    assert game.current_hint(story, progress) != first
    assert game.pundit_line(story, progress).startswith("GIANNO INFANTINI: ")
    progress["choices"]["lanyard"] = "found"
    assert game.pundit_line(story, progress).startswith("GIANNO INFANTINI (nervous): ")


def test_door_to_hint(story):
    # The "!" door: from the booth the door to the hint's room, from any
    # other room the door back to the booth, and none in the hint's room.
    progress = game.new_progress(story)
    assert game.door_to_hint(story, progress)["go_to"] == "dressing_room"
    progress["scene"] = "dressing_room"
    assert game.door_to_hint(story, progress) is None
    progress["inventory"].append("whistle")
    assert game.door_to_hint(story, progress)["go_to"] == "booth"
    progress["scene"] = "booth"
    assert game.door_to_hint(story, progress)["go_to"] == "mascot_room"


def test_ending_summary(story):
    # Every ending explains the result: the truth and a tip.
    progress = game.new_progress(story)
    for ending_id in story["endings"]:
        progress["ending"] = ending_id
        summary = game.ending_summary(story, progress)
        assert len(summary) == 2
        assert summary[0] == story["truth"]
        assert summary[1] == story["endings"][ending_id]["tip"]


def run_all_tests():
    story = game.load_story()
    tests = [test_a1_locked_route, test_a2_unlocked_route, test_a3_no_duplicate,
             test_a4_resume, test_a5_two_outcomes, test_a6_restart,
             test_offside_rule, test_expose_needs_all_clues, test_clues_are_not_items,
             test_pundit_hints, test_door_to_hint, test_ending_summary]
    failed = 0
    for test in tests:
        # try / except: if an assert fails, we count it and keep going.
        # test.__name__ is the name of the function, e.g. "test_a1_locked_route".
        try:
            test(story)
            print("PASS  " + test.__name__)
        except AssertionError:
            print("FAIL  " + test.__name__)
            failed = failed + 1
    print()
    print(str(len(tests) - failed) + " of " + str(len(tests)) + " tests passed.")


# Only run the tests when this file is run directly.
if __name__ == "__main__":
    run_all_tests()
