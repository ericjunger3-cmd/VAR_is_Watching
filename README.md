# VAR Is Watching

A short comedy mystery game (about 10 minutes of play), in two versions:
a **terminal version** where you type numbers, and a **2D pixel-art version**
where you walk through the stadium. Both use the same story.
Team project for Nova SBE *Introduction to Programming*. It started as a solo
project from the "Plot Twist" brief and was extended by the team.

**Play it in the browser:** https://ericjunger3-cmd.github.io/VAR_is_Watching/
(the 2D version; the first start takes a few seconds to load)

It is the 94th minute of a cup final. The home side scores, the away side
claims offside, and the key VAR angle is missing. You are a junior VAR official
on your first day. A smug TV guest expert, Gianno Infantini, comments on everything you do.
Find the missing footage, survive the press, and make the call.

## Team

| Name | Student number |
|---|---|
| Eric Junger | 74702 |
| Max Friedrich | 75436 |
| Brian Riebandt | 71843 |

## How to run

You need Python 3. Open a terminal in this folder.

**Terminal version** (no extra packages):

```
py game.py
```

**2D version** (needs the pygame-ce package, install it once):

```
py -m pip install -r requirements.txt
py game_2d.py
```

**Tests:**

```
py test_game.py
```

**Web version (in the browser):** GitHub builds it automatically after every
push to `main` and puts it online at the address above
(`.github/workflows/deploy.yml`: run the tests, build with pygbag, publish on
GitHub Pages). To try the web version on your own computer:

```
py -m pygbag --title "VAR Is Watching" .
```

Then open http://localhost:8000 and click into the game. The web version
starts from `main.py`. In the browser the progress and the volume are saved in
the browser's storage (localStorage) instead of files (`storage.py`), the
sounds are `.ogg` copies of the `.wav` files (`tools/make_ogg.py`), pygame's
own font replaces the Windows fonts, and there is no Fullscreen / Exit option
(use the browser's fullscreen instead).

(On Mac/Linux, or if `py` does not work: use `python` or `python3` instead of `py`.)

**Desktop shortcut (Windows):** a shortcut can start the 2D version with a double-click.
Its target is `pyw game_2d.py` (`pyw` starts Python without a console window), its
"Start in" folder is this game folder, and its icon is `var_is_watching.ico`.

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
| `Escape` | pause menu: Resume, Tutorial, Volume, Fullscreen on/off, Restart, Back to the title screen (also closes a menu or close-up) |
| `F11` | switch between window and fullscreen (works everywhere) |
| `M` | mute / unmute all sound (works everywhere) |
| `←` `→` on *Volume* | turn the volume down / up (title menu and pause menu) |
| `Y` / `N` | answer a yes/no question |
| `Space`, `Enter` or `E` during a cut scene | skip to the end of that cut scene |

- **Title screen:** *Play* continues your saved game (or starts one),
  *New Game* starts again (asks first if there is a save), *Fullscreen* switches
  between window and fullscreen, *Exit* closes the game. The game always starts in a window.
- **Inventory:** the slots in the top left corner always show your items.
  A new item flies into its slot when you pick it up.
- **The VAR Review:** it starts with a short explanation of the offside rule;
  `Enter` starts the footage. `←` `→` move through the footage in 0.1 s steps, `Enter`
  locks the moment. Then `←` `→` move the offside line in 0.1 m steps, `Enter`
  locks it. `Escape` goes back one step (from the explanation or the first step
  it closes the review without deciding).
- **The end:** after your answer to the press, two short cut scenes play (see
  *The end in the 2D version* below), then the ending screen. `Space` skips a
  cut scene.
- **After an ending:** `N` = new game (asks first), `Q` = back to the title screen.
- **Timer:** the "STADIUM WAITS" clock in the top left counts down from 5 minutes. It only
  runs while you walk around: it stops while a text, the sticky note, a menu, the VAR Review,
  the pause menu, a yes/no question or the tutorial is open.
- **Tutorial:** a new game starts with a short tour of the screen (7 steps). `Space`
  shows the next step, `Escape` skips it. You can watch it again from the pause menu.

## Files

| File | What it contains |
|---|---|
| `game.py` | the terminal game, and the game rules both versions use (saving, items, locks, endings) |
| `game_2d.py` | the 2D game: the game loop, walking, keys, timer, title screen and pause menu |
| `main.py` | the start file of the web version (pygbag always starts `main.py`); it starts the 2D game |
| `storage.py` | saves and loads the progress and the volume: files on a computer, the browser's storage in the web version |
| `requirements.txt` | the packages with their exact versions (pygame-ce, and pygbag for the web version) |
| `.github/workflows/deploy.yml` | tells GitHub to test, build and publish the web version after every push to `main` |
| `rooms.py` | draws the five rooms and the people in them, and the press pack that storms the pitch |
| `clips.py` | the cut scenes at the end of the 2D game: on the pitch and in Infantini's TV studio |
| `sprites.py` | the pixel art (player, characters, items) as grids of colours |
| `ui.py` | the text box, the pundit's TV, close-ups, menus, the VAR Review screen and the inventory bar |
| `story.json` | all the story content: scenes, actions, items, the pundit's hints and the endings (shared by both versions) |
| `test_game.py` | automatic tests for the acceptance scenarios A1-A6 and the main rules: run `py test_game.py` |
| `EXAM_NOTES.md` | exam cheat sheet: where each requirement is in the code, the key functions and typical questions |
| `save.json` | terminal progress; created by the game and saved after every accepted action. A broken save file (empty or half written) is ignored: the game starts a new one instead of crashing |
| `save_2d.json` | 2D progress, same format; saved after every accepted action |
| `settings.json` | the 2D volume and mute setting (kept after a New Game) |
| `sound.py` | loads and plays the sounds and music of the 2D game; remembers the volume |
| `sounds/` | all sound effects, room sounds and music as .wav files (and .ogg copies for the web version) |
| `tools/make_sounds.py` | the tool that made the sounds (not part of the game): run `py tools/make_sounds.py` to make them again |
| `tools/make_ogg.py` | makes the .ogg copies of the sounds for the web version (needs `py -m pip install soundfile`) |
| `icon.png`, `var_is_watching.ico` | the game's logo: the window icon (png) and the desktop shortcut icon (ico) |

## Sound and music (2D version)

All sounds are original and made with code (`tools/make_sounds.py`), in the style of old
game consoles: square waves, triangle waves and noise. No sound files from the internet.

- **Music:** a chill theme on the title screen and a calmer mystery theme while you play.
- **Effects:** doors, locked doors, picking up items, the Lucky Whistle, Bernie's growl,
  cameras on the pitch (clicking non-stop while the press storms in), the VAR Review
  beeps, kicking the ball, a goal cheer, the referee's final whistle, menu blips and a
  soft blip while the text appears. Each cut scene at the end starts with its own sound.
- **Room sounds:** the crowd on the pitch and the shower in the referee's room.
- **Endings:** a happy jingle for the good endings and a sad one for the bad endings.
- **Volume:** a slider in the title menu and the pause menu (0 to 10), and `M` to mute.
  If the computer has no sound device, the game simply runs without sound.

## Help for new players

- **Tutorial (2D):** a new game starts with a tour of the screen. Each step lights
  up one part and explains it: Infantini on the TV (the hints), your items, the timer,
  you and the "!" markers, the story text, and the goal of the game. The steps are
  `TUTORIAL_STEPS` in `ui.py`; `tutorial_area` in `game_2d.py` finds each part.
  The terminal version prints the goal of the game at the start.
- **Follow the "!":** besides the things you can use, the door on the way to
  Infantini's current hint also gets a bouncing "!" (terminal: a "(!)" after the
  action). Each hint has a `"room"` in `story.json`; `door_to_hint` in `game.py`
  finds the door.
- **The pundit gives the hints.** Gianno Infantini always says (rudely, but clearly)
  what to do next, e.g. "Read the sticky note, rookie!". The hints are
  the `"hints"` list in `story.json`; the first one that is not done yet is shown.
  He even gives himself away (his press pass, "stay out of the server room").
  Right after you find a clue he reacts to it, nervously ("A betting slip?
  0:0, signed G.I.? Lots of people are called G.I."). The reaction only pops
  up for a few seconds (2D) or once above his hint (terminal), then he tells
  you again what to do next. The reactions are `"clue_reactions"` in `story.json`.
- **He gets nervous.** With every clue against him his name changes:
  GIANNO INFANTINI, (nervous), (sweating), (panicking), (furious). In the 2D
  version his face also gets redder, sweatier and angrier.
- **New hint signal (2D):** when he says something new, his speech box and his
  TV light up with a thick yellow frame and blink for 3 seconds.
- **Secret clues:** the game never shows how many clues exist or how many you
  found. The option to expose Infantini only appears once you have all of them.
- **The truth at the end:** every ending shows the right call (GOAL, onside by
  30 cm) and a tip for the next game.

## The game at a glance

- **Who is who on the pitch:** the home side plays in red (Bayern style), the
  away side in yellow and black (Dortmund style). The referee and the linesman
  wear turquoise (the referee with a whistle, the linesman with his flag). You,
  the VAR official, wear orange with "VAR" on your shirt. The press wears all
  black with a blue press pass and "PRESS". The scoreboard says FCB 1 - 0 BVB,
  and FULL TIME after your call (0 - 0 if you ruled OFFSIDE).
- **The sabotage:** the offside camera's monitor hangs crooked and flickers. Its
  red cable (with an "OFFSIDE CAM" tag) runs into the Server Room, where someone
  cut it.
- **5 scenes:** VAR Booth (start), Server Room, Referee's Dressing Room, Mascot
  Changing Room, The Pitch.
- **2 items:** the Lucky Whistle opens the Mascot Changing Room; Bernie the bear
  mascot gives you the USB Stick with the missing angle. Items are reusable and
  can only be collected once.
- **4 hidden clues against Infantini:** his Press Pass (behind the booth desk),
  his Betting Slip (in the bin in the referee's room), the tip of his tie
  (stuck in the cut cable in the Server Room) and Dave's statement. They are not
  items: the game remembers them secretly and never shows how many there are.
- **The twist:** Bernie is really Dave, the missing VAR operator, and the TV expert
  Gianno Infantini cut the camera cable because he bet on a 0:0 draw: he wants
  you to rule OFFSIDE, but the striker was onside. Cutting the cable, he also
  cut off the tip of his own tie. Finding this out is optional.
- **The VAR Review:** plug the USB Stick into the VAR computer, find the exact
  moment the ball leaves the passer's boot (0.0 - 3.0 s in steps of 0.1 s), lock
  it, then draw the offside line (terminal: type metres; 2D: move the line).
  You only get one look.
  (The right answer: 1.2 s, line on defender number 4 at 21.5 m: onside.)
- **The end on the pitch:** you tell the referee GOAL or OFFSIDE, he blows the
  final whistle, and the press rushes at you. You answer "Clearly ONSIDE /
  OFFSIDE" (it matches your call), "No comment", or you expose Infantini (needs
  all 4 clues). Your answer ends the game.
- **The stadium is waiting:** you have 40 actions (terminal) or 5 minutes of
  walking around (2D version). Run out and the referee flips a coin.
- **5 endings:**
  - *Daylight Robbery*: you rule OFFSIDE
  - *Lucky Guess*: GOAL without doing the review
  - *By the Book*: GOAL after the review
  - *VAR Is Watching*: GOAL after the review + you exposed Infantini
  - *The Stadium Went Home*: you ran out of time
- **Infantini in the studio:** after every ending you see what happens to him:
  he is **arrested** (you exposed him), he **wins** his bet (it ended 0:0) or
  he **loses** it (the goal counts).

## The end in the 2D version

1. **The press storms the pitch.** After your call the referee blows the final
   whistle, and a pack of reporters runs out of the tunnel on the left, one after
   the other, trampling and kicking up dust while the screen shakes a little. Interviewers
   with microphones stand right next to you, photographers behind them flash all
   the time. The red and the yellow player step aside. Then the press asks you
   their question (`draw_press_pack` in `rooms.py`).
2. **A slow circle** closes over the pitch: a new scene begins.
3. **Cut scene 1, on the pitch** (5 seconds, `clips.py`):
   - after GOAL: the red striker slides on his knees, the passer jumps, red and
     white confetti falls, the yellow players hang their heads;
   - after OFFSIDE: the yellow players jump for joy, the red striker kneels with
     his hands on his head;
   - when time ran out: the referee flips a coin, it lands on OFFSIDE, the
     floodlights go out and Bernie walks home.
4. **Cut scene 2, in Infantini's TV studio** (5 seconds):
   - arrested: two police officers walk in, the handcuffs click, they lead him
     away, then the TV picture turns to static: SIGNAL LOST;
   - his bet wins: he kisses his betting slip, money rains down;
   - his bet is lost: his face turns red, steam comes out, he crumples the slip.
5. **The ending screen** with a short text, what happened to Infantini, the right
   call and a tip.

The terminal version shows the same ending as text.

## Automatic tests

`test_game.py` checks A1-A6 (and the offside rule, the clues for exposing Infantini,
the press after the ruling, every ending, old save files, the pundit's hints and
reactions, the "!" door and the ending summary) with the functions from `game.py`. It uses
its own save file, so your saved game is never touched.

```
py test_game.py
```

It prints PASS or FAIL for every test and "17 of 17 tests passed." at the end.
The checklists below test the same scenarios by hand, in the real game.

## Acceptance test checklist (A1-A6): terminal version

Start each test from a new game: delete `save.json` first, or choose `n` and then `y`
in the start menu. Type the inputs one at a time, pressing Enter after each one.

**Menu numbers.**
- **VAR Booth:** `1` Server Room, `2` Dressing Room, `3` Mascot Room, `4` Pitch,
  `5` sticky note, `6` look behind the desk, `7` plug in the USB Stick.
- **Pitch:** `1` GOAL, `2` OFFSIDE, `3` back. After your call: the press answers.
- **Other rooms:** item and clue actions come first; "Back to the VAR Booth"
  is always the last numbered action.
- Actions you have already done disappear, so the numbers after them move up.

| Test | Inputs | Expected result |
|---|---|---|
| **A1 Locked route** | `3`, then `i` | "Locked..." You stay in the VAR Booth and your pockets are empty. |
| **A2 Unlocked route** | `2`, `1` (open drawer), `1` (take whistle), `2` (back), `3`, then `i` | The door opens and you are in the Mascot Changing Room. The inventory still shows the Lucky Whistle. |
| **A3 No duplicate** | `2`, `1` (open drawer), `1` (take whistle), `2` (back), `2` (Dressing Room again), then `i` | After taking it, the "Take the Lucky Whistle" action is gone, also on the second visit. The inventory shows the Lucky Whistle only once. |
| **A4 Resume** | `2`, `1`, `1`, `2`, `3`, `1` (USB), `1` (back), `4`, `1` (GOAL), `q`. Then run `py game.py` again and type `c`, `i` | You continue on the Pitch: only the press answers are left, there is no way back to the booth. The inventory shows both items. |
| **A5 Two outcomes** | Game 1: `4`, `1` (GOAL), `2` (No comment) gives **Lucky Guess**. Type `n`, `y`. Game 2: `2`, `1`, `1`, `2`, `3`, `1`, `1`, `7` (review), `1.2`, `l`, `21.5`, `4`, `1`, `2` gives **By the Book**. Type `q`, run again, `c` | Two different endings. Reopening a finished game shows the same ending, with only `v`, `n` and `q`. |
| **A6 Restart safely** | `2`, `1` (open drawer), `1` (take whistle), then `r`, `n`, `i`. Then `r`, `y`, `i`, `4` | After `n`: you are still in the Dressing Room with the whistle. After `y`: you are back in the VAR Booth, your pockets are empty, and the referee asks for your call again. |

## Acceptance test checklist (A1-A6): 2D version

Start each test with **New Game** on the title screen (and `Y` if it asks),
or delete `save_2d.json` first. A new game starts with the tutorial: press
`Escape` to skip it.

**Where things are.**
- **VAR Booth**, from left to right: the Server Room door, the desk with the VAR
  computer, the monitors with the sticky note, then the Dressing Room door, the
  Mascot Room door and the tunnel to the Pitch.
- **Other rooms:** the door back to the VAR Booth is on the far left.
  You arrive in front of it.
- "Walk to X, `E`" means: walk until you stand in front of X, then press `E`.

| Test | What you do | Expected result |
|---|---|---|
| **A1 Locked route** | Walk to the Mascot Room door (with the padlock), `E` | "Locked..." You stay in the VAR Booth and the inventory bar is empty. |
| **A2 Unlocked route** | Dressing Room door, `E`. Walk to the kit cabinet, `E` (open drawer), `E` (take whistle). Back door, `E`. Mascot Room door, `E` | The door opens and you are in the Mascot Changing Room. The Lucky Whistle is still in the inventory bar. |
| **A3 No duplicate** | Take the whistle as in A2, press `E` at the cabinet again, then leave and come back to the Dressing Room | The drawer is open and empty, and there is nothing more to take. The whistle is in the bar only once. |
| **A4 Resume** | Take the whistle, go to the Mascot Room, talk to Bernie (USB Stick), go to the Pitch and tell the referee **GOAL**. When the press questions appear, close the window. Run `py game_2d.py` again and choose *Play* | You continue on the Pitch and the press questions open again (they cannot be closed). The bar shows the whistle and the USB Stick. |
| **A5 Two outcomes** | Game 1: Pitch, referee, **GOAL**, "No comment" gives **Lucky Guess**. Press `N`, `Y`. Game 2: get the whistle and the USB Stick, then use the VAR computer: `Enter` after the explanation, move to 1.2 s, `Enter`, put the line on defender number 4, `Enter`. Pitch, **GOAL**, "No comment" gives **By the Book**. Close the window, run again, *Play* | Two different endings (each after the press and the two cut scenes; `Space` skips a cut scene). Reopening a finished game shows the same ending again at once, with only `N` and `Q`. |
| **A6 Restart safely** | Take the whistle. `Escape`, *Restart*, `N`. Then `Escape`, *Restart*, `Y` | After `N`: you are still in the Dressing Room with the whistle. After `Y`: you are back in the VAR Booth, the bar is empty, the timer is back at 5:00, and the Mascot Room door has its padlock again. |
