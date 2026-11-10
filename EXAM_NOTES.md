# Exam notes: VAR Is Watching

A cheat sheet for the exam: where every requirement of the Plot Twist brief
lives in the code, how to show it, and typical questions with short answers.
(The brief: "You may use AI to build; you must be able to explain and verify
what it produces." So: know these functions, not just the game.)

## The game in 30 seconds

94th minute of a cup final, 0:0. The home side scores, the away side claims
offside, and the offside camera is dead. You are a junior VAR official on your
first day. Find the footage (the mascot filmed it), check the offside line,
make the call on the pitch and answer the press. Twist: the TV expert Gianno
Infantini cut the cable because he bet on 0:0. Right call: GOAL (onside by 30 cm).

- **5 scenes:** VAR Booth (start), Referee's Dressing Room, Mascot Changing Room,
  Server Room, The Pitch
- **2 items:** Lucky Whistle (unlocks the Mascot Room), USB Stick (unlocks the VAR Review)
- **4 hidden clues** (choices, not items): press pass, betting slip, tie tip, Dave's statement
- **5 endings:** Daylight Robbery, Lucky Guess, By the Book, VAR Is Watching, The Stadium Went Home

## How the code is built

```
story.json   all content: scenes, actions, conditions, hints, endings
   |
game.py      the RULES (shared) + the terminal version
   |            load_story, new_progress, save/load, is_hidden,
   |            blocked_reason, choose_ending, value_at, judge_offside ...
   |
game_2d.py   the 2D version: game loop, keys, walking, timer, saving
ui.py        boxes and text on screen (text box, TV, review, tutorial)
rooms.py     draws the 5 rooms;  sprites.py  pixel art;  clips.py  end scenes
sound.py     sounds and music;   test_game.py  automatic tests
```

**Key idea:** the story is *data*, not code. An action in story.json is a
dictionary, e.g.

```json
{ "label": "Go to the Mascot Changing Room", "go_to": "mascot_room",
  "needs_item": "whistle", "blocked_text": "Locked. ..." }
```

The rules never say "if the player is in the booth and has the whistle".
They read keys like `needs_item`, `take_item`, `set_choice`, `go_to` and apply
the same checks to every action. Both versions use the same rules from game.py.
(The 2D version only has a few special cases for show, e.g. the whistle
sound when the Mascot Room door opens.)

**The progress** (everything that changes, = the save file), from `new_progress`:

| Key | Example | Meaning |
|---|---|---|
| `scene` | `"booth"` | where the player is |
| `inventory` | `["whistle", "usb"]` | items (list, never a duplicate) |
| `choices` | `{"drawer": "open", "ruling": "goal"}` | decisions and found clues |
| `visited` | `["booth", "pitch"]` | rooms already seen (description only once) |
| `ending` | `None` / `"by_the_book"` | set once, the game is over |
| `actions_left` / `seconds_left` | `40` / `300` | the stadium's patience (terminal / 2D) |
| `last_clue` | `"slip"` | the pundit reacts to this clue |

## Where each requirement is

### Content and constraints

| Requirement | Where / how |
|---|---|
| ~10 minutes, 5 scenes, 2 items, 2+ endings | story.json: `scenes`, `items`, `endings` |
| One ending depends on a choice or item | `choose_ending` (game.py): uses `ruling`, `review`, `press_answer` |
| Save after each accepted action | terminal: `save_progress` at the end of each loop in `play_game`; 2D: end of `do_action`, after the review, at time up, at pause |
| Rejected action leaves the save unchanged | blocked actions `continue` / `return` **before** anything is changed or saved |
| Works offline | only Python + pygame-ce, no internet, no paid service |

### Functional requirements

| | Where in the code | How to show it |
|---|---|---|
| **PT01** start and resume, confirm before replacing | terminal: `start_menu` (`n` asks `ask_yes_no`, `c` continues); 2D: `title_screen` ("Start a new game? This deletes your saved progress.") | play, quit, start again, choose continue |
| **PT02** show scene + actions, visible result | `show_scene`, `get_visible_actions`, `show_actions`; every action has a `"text"` that is shown | any action prints / shows its text |
| **PT03** inventory, item unlocks action, no duplicates | `show_inventory` (`i`); 2D: slots top left; `needs_item` in `blocked_reason`; `is_hidden` hides `take_item` once you have it | whistle opens the Mascot Room |
| **PT04** remembered decision changes later action/ending; blocked explained or hidden | `choices` dict; `choose_ending`; `blocked_text` explains, `hide_if_blocked` hides | rule OFFSIDE -> Daylight Robbery |
| **PT05** clear ending, story stops, review or restart | `show_ending` ("ENDING: ..."), `after_ending_menu` (`v` / `n` / `q`); a saved ending is shown again at start | finish, restart the app |

### Business rules

| | Where |
|---|---|
| **R1** action only when allowed; blocked = no change | `blocked_reason` returns the text or `None`; the loop changes nothing when it is not `None` |
| **R2** items only where the story puts them, once, reusable | items only come from `take_item` actions; `is_hidden` + `if item_id not in inventory`; no action ever removes an item (only loading a very old save moves its old clue items into `choices`) |
| **R3** revisited scenes remember changes | `is_hidden`: a done `set_choice` / taken `take_item` disappears (open drawer, taken whistle) |
| **R4** new game resets, every ending reachable | `new_progress` builds a fresh dict from story.json; `test_all_endings` |

### Acceptance scenarios (tests in `test_game.py`, run `py test_game.py`)

| | Our version | Test |
|---|---|---|
| **A1** locked route | Mascot Room without whistle -> "Locked..." | `test_a1_locked_route` |
| **A2** unlocked route | with whistle -> Mascot Room, whistle stays | `test_a2_unlocked_route` |
| **A3** no duplicate | "Take the Lucky Whistle" disappears | `test_a3_no_duplicate` |
| **A4** resume | save -> load gives the same scene, items, choices, actions | `test_a4_resume` |
| **A5** two outcomes | OFFSIDE -> Daylight Robbery; GOAL + review -> By the Book | `test_a5_two_outcomes`, `test_all_endings` |
| **A6** restart safely | `r` + `n` keeps everything; `r` + `y` = `new_progress` | `test_a6_restart` |

The README has step-by-step key presses for A1-A6 in both versions.

## The functions to know by heart (game.py)

- **`new_progress(story)`** - a fresh progress dictionary (see the table above).
- **`save_progress` / `load_progress`** - `json.dump` / `json.load`. A broken
  save file (empty, half written) is caught with `try` / `except` and treated
  as "nothing saved", so the game never crashes on it (`test_broken_save`).
  Old saves are updated by `update_old_save` (`test_old_save_still_works`).
- **`is_hidden(action, inventory, choices)`** - True if the action should not be
  shown: item already taken, decision already made, `hidden_after` a choice,
  or `hide_if_blocked` and blocked.
- **`blocked_reason(action, inventory, choices)`** - checks `needs_item`,
  `needs_choices`, `needs_choice`, `needs_ruling`; returns the `blocked_text`
  or `None` ("not blocked").
- **`choose_ending(choices)`** - `if`s from top to bottom, the first that fits:
  OFFSIDE -> Daylight Robbery; no review -> Lucky Guess; exposed -> VAR Is
  Watching; otherwise By the Book. (Time up is set in the game loop.)
- **`value_at(track, time, index)`** - linear interpolation: where a player is
  between two known points of the footage.
- **`judge_offside(striker, line)`** - offside if the striker is closer to the
  goal than the line; level = onside; `round(..., 2)` against float errors.
- **`find_current_hint` / `pundit_line` / `door_to_hint`** - the first hint in
  story.json that is not done; the pundit's name shows his mood (clue count);
  the door on the way to the hint's room gets the "!".

## Typical exam questions

1. **Why is the story in a JSON file?** Content and logic are separate: new
   rooms or texts need no code change, and both versions share one story.
2. **What happens when I take the whistle twice?** The take action is hidden
   (`is_hidden`), and `take_item` only appends if the item is not in the list.
3. **How do you make sure a blocked action changes nothing?** `blocked_reason`
   is checked first; if it returns a text, we show it and `continue` / `return`
   before changing or saving anything.
4. **When is the game saved?** After every accepted action (end of the loop in
   `play_game`, end of `do_action` in 2D), and when the ending is set.
5. **What if the save file is broken?** `load_progress` catches `ValueError`
   (bad JSON) and `KeyError` / `TypeError` / `AttributeError` (not a game save)
   and returns `None`, so a new game starts.
6. **Why can the ending not be changed?** `progress["ending"]` is saved; at the
   start `play_game` sees it and only shows the ending and the `v`/`n`/`q` menu.
7. **Why are the clues not items?** Design choice: they are secret. They are
   stored in `choices`; nobody sees a counter. Exposing Infantini is hidden
   until all 4 are found (`needs_choices` + `hide_if_blocked`).
8. **How does the offside check work?** Lock the moment the ball leaves the
   boot (1.2 s), put the line on the 2nd-last defender (21.5 m); the striker is
   at 21.8 m -> onside. `value_at` + `judge_offside`.
9. **What is the difference between the two versions?** Same rules and story
   (game.py, story.json). Terminal: numbers, 40 actions. 2D: pygame, walking,
   a 5-minute timer that only runs while no box is open.
10. **How do you know it works?** `test_game.py`: 17 tests with `assert`
    (A1-A6 and more), plus the step-by-step checklists in the README.
11. **What does `if __name__ == "__main__":` do?** Runs `main()` only when the
    file is started directly, not when it is imported (game_2d.py and the
    tests import game.py).
12. **Why `progress["inventory"]` and not a global variable?** Everything that
    changes is in one dictionary, so saving is one `json.dump` of it.

## Honest limits (good to say yourself)

- The 2D version saves the timer only at actions, pause and the end, so a
  crash can cost a few seconds of the timer, never an item or a choice.
- `save_progress` writes the file directly; if the computer turns off exactly
  while writing, the file can be broken. That case is caught at loading.
- The story is fixed (no editor, no random stories): on purpose, the brief
  puts a story editor out of scope.
