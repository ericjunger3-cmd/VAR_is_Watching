# VAR Is Watching

A short comedy mystery game (about 10 minutes of play), in two versions:
a **terminal version** where you type numbers, and a **2D pixel-art version**
where you walk through the stadium. Both use the same story.
Solo project for Nova SBE *Introduction to Programming*, based on the
"Plot Twist" brief.

It is the 94th minute of a cup final. The home side scores, the away side
claims offside, and the key VAR angle is missing. You are a junior VAR official
on your first day. A smug TV pundit comments on everything you do.
Find the missing footage, survive the press, and make the call.

## How to run

You need Python 3. Open a terminal in this folder.

**Terminal version** (no extra packages):

```
py game.py
```

**2D version** (needs the pygame-ce package, install it once):

```
py -m pip install pygame-ce
py game_2d.py
```

(On Mac/Linux, or if `py` does not work: use `python` or `python3` instead of `py`.)

Run the games in a real terminal window: the terminal version waits for you to
type, and the 2D version opens its own game window.

## Controls

### Terminal version

| Key | What it does |
|---|---|
| `1`, `2`, `3` ... | choose an action from the list |
| `i` | show your inventory |
| `r` | restart (asks for confirmation) |
| `q` | quit (your progress is saved) |

At the start, if a saved game exists: `n` = new game (asks for confirmation),
`c` = continue. After an ending: `v` = view the ending again, `n` = new game,
`q` = quit.

### 2D version

| Key | What it does |
|---|---|
| `←` `→` (or `A` `D`) | walk left and right |
| `E` | use what is in front of you (a door, an item, a person): an "E" bubble shows where you can |
| `E`, `Space` or `Enter` | next page of the text box (or show the whole page at once) |
| `↑` `↓` (or `W` `S`) + `Enter` | choose in a menu (you can also press `1`, `2`, `3`) |
| `Escape` | pause menu: Resume, Restart, Back to the title screen (also closes a menu or close-up) |
| `Y` / `N` | answer a yes/no question |

- **Title screen:** *Play* continues your saved game (or starts one),
  *New Game* starts again (asks first if there is a save), *Exit* closes the game.
- **Inventory:** the bar at the bottom of the screen always shows your items.
  A new item flies into its slot when you pick it up.
- **The VAR Review:** `←` `→` move through the footage in 0.1 s steps, `Enter`
  locks the moment. Then `←` `→` move the offside line in 0.1 m steps, `Enter`
  locks it. `Escape` goes back one step (from the first step it closes the
  review without deciding).
- **After an ending:** `N` = new game (asks first), `Q` = back to the title screen.
- **Timer:** the "STADIUM WAITS" clock in the top left counts down from 7 minutes. It stops in the
  pause menu and during yes/no questions.

## Files

| File | What it contains |
|---|---|
| `game.py` | the terminal game, and the game rules both versions use (saving, items, locks, endings) |
| `game_2d.py` | the 2D game: the game loop, walking, keys, timer, title screen and pause menu |
| `rooms.py` | draws the five rooms and the people in them |
| `sprites.py` | the pixel art (player, characters, items) as grids of colours |
| `ui.py` | the text box, the pundit's TV, close-ups, menus, the VAR Review screen and the inventory bar |
| `story.json` | all the story content: scenes, actions, items and endings (shared by both versions) |
| `save.json` | terminal progress; created by the game and saved after every accepted action |
| `save_2d.json` | 2D progress, same format; saved after every accepted action |

## The game at a glance

- **5 scenes:** VAR Booth (start), Referee's Dressing Room, Mascot Changing Room,
  Press Room, The Pitch.
- **4 items:** the Lucky Whistle opens the Mascot Changing Room; Pombo the pigeon
  mascot gives you the USB Stick with the missing angle; the Press Lanyard and the
  Betting Slip are clues. Items are reusable and can only be collected once.
- **The twist:** Pombo is really Dave, the missing VAR operator, and the TV pundit
  Rex Smugworth pulled the camera cable because he bet on the away team.
  Finding this out is optional.
- **The VAR Review:** plug the USB Stick into the VAR computer, find the exact
  moment the ball leaves the passer's boot (0.0 - 3.0 s in steps of 0.1 s), lock
  it, then draw the offside line (terminal: type metres; 2D: move the line).
  You only get one look.
  (The right answer: 1.2 s, line on defender number 4 at 21.5 m: onside.)
- **Remembered decisions:** your review result, Dave's statement, and your one
  answer to the press ("Clearly a goal!", "No comment", or exposing Rex, which
  needs the lanyard, the slip and Dave's statement). The referee only takes
  your call after you have spoken to the press.
- **The stadium is waiting:** you have 40 actions (terminal) or 7 minutes
  (2D version). Run out and you get a sixth ending.
- **5 endings + 1:**
  - *Daylight Robbery*: you rule OFFSIDE
  - *Clip of the Year*: GOAL without doing the review
  - *Right Call, Wrong Mouth*: GOAL after the review + "Clearly a goal!"
  - *Justice Served*: GOAL after the review + "No comment"
  - *VAR Is Watching*: GOAL after the review + you exposed Rex
  - *The Stadium Went Home*: you ran out of time

## Acceptance test checklist (A1-A6): terminal version

Start each test from a new game: delete `save.json` first, or choose `n` and then `y`
in the start menu. Type the inputs one at a time, pressing Enter after each one.

**Menu numbers.**
- **VAR Booth:** `1` Dressing Room, `2` Mascot Room, `3` Press Room, `4` Pitch,
  `5` sticky note, `6` look behind the desk, `7` plug in the USB Stick.
- **Other rooms:** item, answer and clue actions come first; "Back to the VAR Booth"
  is always the last numbered action.
- Actions you have already done disappear, so the numbers after them move up.

| Test | Inputs | Expected result |
|---|---|---|
| **A1 Locked route** | `2`, then `i` | "The door is locked..." You stay in the VAR Booth and your pockets are empty. |
| **A2 Unlocked route** | `1`, `1` (open drawer), `1` (take whistle), `1` (back), `2`, then `i` | The door opens and you are in the Mascot Changing Room. The inventory still shows the Lucky Whistle. |
| **A3 No duplicate** | `1`, `1` (open drawer), `1` (take whistle), `1` (back), `1` (Dressing Room again), then `i` | After taking it, the "Take the Lucky Whistle" action is gone, also on the second visit. The inventory shows the Lucky Whistle only once. |
| **A4 Resume** | `1`, `1`, `1`, `1`, `2`, `1` (USB), `1`, `3`, `2` (No comment), `q`. Then run `py game.py` again and type `c`, `i`, `2` (back), `4` | You continue in the Press Room without the answer options. The inventory shows both items. The Pitch is open. |
| **A5 Two outcomes** | Game 1: `3`, `1`, `2`, `4`, `1` gives **Clip of the Year**. Type `n`, `y`. Game 2: `1`, `1`, `1`, `1`, `2`, `1`, `1`, `7` (review), `1.2`, `l`, `21.5`, `3`, `2`, `2`, `4`, `1` gives **Justice Served**. Type `q`, run again, `c` | Two different endings. Reopening a finished game shows the same ending, with only `v`, `n` and `q`. |
| **A6 Restart safely** | `1`, `1` (open drawer), `1` (take whistle), then `r`, `n`, `i`. Then `r`, `y`, `i`, `3` | After `n`: you are still in the Dressing Room with the whistle. After `y`: you are back in the VAR Booth, your pockets are empty, and the Press Room shows both answers again. |

## Acceptance test checklist (A1-A6): 2D version

Start each test with **New Game** on the title screen (and `Y` if it asks),
or delete `save_2d.json` first.

**Where things are.**
- **VAR Booth**, from left to right: the desk, the VAR computer, the sticky note,
  then four doors: Dressing Room, Mascot Room, Press Room, Pitch.
- **Other rooms:** the door back to the VAR Booth is on the far left.
  You arrive in front of it.
- "Walk to X, `E`" means: walk until you stand in front of X, then press `E`.

| Test | What you do | Expected result |
|---|---|---|
| **A1 Locked route** | Walk to the Mascot Room door (2nd door), `E` | "The door is locked..." You stay in the VAR Booth and the inventory bar is empty. |
| **A2 Unlocked route** | Dressing Room door, `E`. Walk to the kit cabinet, `E` (open drawer), `E` (take whistle). Back door, `E`. Mascot Room door, `E` | The door opens and you are in the Mascot Changing Room. The Lucky Whistle is still in the inventory bar. |
| **A3 No duplicate** | Take the whistle as in A2, press `E` at the cabinet again, then leave and come back to the Dressing Room | The drawer is open and empty, and there is nothing more to take. The whistle is in the bar only once. |
| **A4 Resume** | Take the whistle, go to the Mascot Room, talk to Pombo (USB Stick), go to the Press Room and answer "No comment". `Escape`, *Back to the title screen*, close the window. Run `py game_2d.py` again and choose *Play* | You continue in the Press Room and the reporters do not ask again. The bar shows the whistle and the USB Stick. On the Pitch the referee takes your call. |
| **A5 Two outcomes** | Game 1: Press Room, answer, Pitch, referee, **GOAL** gives **Clip of the Year**. Press `N`, `Y`. Game 2: get the whistle and the USB Stick, then use the VAR computer: move to 1.2 s, `Enter`, put the line on defender number 4, `Enter`. Press Room, "No comment", Pitch, **GOAL** gives **Justice Served**. Close the window, run again, *Play* | Two different endings. Reopening a finished game shows the same ending again, with only `N` and `Q`. |
| **A6 Restart safely** | Take the whistle. `Escape`, *Restart*, `N`. Then `Escape`, *Restart*, `Y` | After `N`: you are still in the Dressing Room with the whistle. After `Y`: you are back in the VAR Booth, the bar is empty, the timer is back at 7:00, and the Press Room asks its question again. |
