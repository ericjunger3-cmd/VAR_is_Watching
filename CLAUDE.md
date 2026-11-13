# VAR Is Watching

A short comedy mystery game for the terminal, built as a solo uni project for
Nova SBE *Introduction to Programming* (Block 2), from the "Plot Twist" brief:
https://nova-sbe-introduction-to-programming.github.io/intro-to-programming-2026/weeks/week-05/01-plot-twist-brd.html

## How to work with me (most important)

- I am a beginner and must **explain all of the code in an exam**.
- Keep the code **simple and well commented**. No advanced patterns (no classes
  unless really needed, no decorators, no clever one-liners, no extra libraries).
- Build **one small step at a time** and **explain every change** in plain words.
- **Never make big changes without asking first.**

## Story

94th minute of a cup final. The home side scores, the away side claims offside,
and the offside camera is dead: its monitor hangs crooked and flickers, and its
red cable ("OFFSIDE CAM" tag) runs into the Server Room, where it is cut. The player is a junior VAR official on their
first day. A smug TV guest expert, Gianno Infantini (a fictional character),
narrates everything. It is 0:0 before the goal.

Teams: home side in red (Bayern style: striker, passer), away side in yellow and
black (Dortmund style: captain, defenders; the review goalkeeper is purple). The
referee and linesman wear turquoise, the player (VAR) orange with "VAR". Scoreboard: FCB 1 - 0 BVB; home
fans on the left half of the stands, away fans on the right (`fan_colour` in rooms.py).

### The pundit gives the hints

- Infantini always says (rudely, but clearly) what to do next: the `"hints"` list in
  story.json, each with a `"done_when"` id (item or choice); `current_hint` in
  game.py shows the first one not done. A hint can have `"if_clue"` /
  `"pundit_if_clue"` for a different line once that clue is found.
- His mood shows in his name, from `"pundit_moods"` by clue count:
  GIANNO INFANTINI, (nervous), (sweating), (panicking), (furious) (`pundit_line`).
  2D: his face changes too (5 faces, `make_pundit(mood)`).
- Right after you find a clue he reacts to exactly that clue (`"clue_reactions"`
  in story.json, `progress["last_clue"]`, `remember_clue`, `reaction_line`).
  It only pops up briefly, because his main job is to say what to do next:
  2D shows it for 5 seconds (`REACTION_FRAMES`, counted while no box is open,
  `pundit_text_now`), then his hint is back; the terminal prints the reaction
  once, above the hint.
- 2D: a new line makes his speech box and TV light up with a thick yellow
  frame and a soft glow, blinking for 3 seconds (`HINT_FLASH_FRAMES` = 90),
  without a sound.
- Clues are secret: no counter anywhere. Exposing Infantini stays hidden until all
  4 clues are found (`needs_choices` + `hide_if_blocked`).
- Each hint has a `"room"`; `door_to_hint` finds the door on the way there
  (from the booth: that room's door, elsewhere: the door back to the booth).
  2D draws a "!" at its `"door_marker"`; the terminal adds "(!)" to the action.
- Every ending shows the truth and its `"tip"` (`ending_summary`); tips never
  say how many clues there are.
- Dialogue texts are kept short: every text fits on one page of the text box.

### Tutorial (2D)

- A new game starts with a tour of the screen: `TUTORIAL_STEPS` in ui.py (7 steps:
  welcome, Infantini on TV, items, timer, the player and the "!", the story text, the
  goal). Each step darkens the screen except one area (`tutorial_area` in
  game_2d.py) and explains it in a caption box (`draw_tutorial`).
- `screen["tutorial"]` is the current step (None = closed). Space = next,
  Escape = skip; it counts as an open box, so the timer stops. It can be
  replayed from the pause menu ("Tutorial"). The terminal prints `"goal"`.

### The twist (optional to discover)

- **Bernie is Dave**, the missing VAR operator from the sticky note, working a
  second job as the mascot. He filmed the goal on his head-cam (the USB Stick)
  and saw a man in a shiny suit run out of the booth at 93:30.
- **The TV expert, Gianno Infantini, cut the camera cable** in the Server Room because
  he bet 500 on a 0:0 draw. He wants the VAR to rule OFFSIDE so the goal is gone
  and his bet wins. When he cut the cable, he cut off the tip of his own tie too
  (his tie on TV is too short). Before kick-off he tried to "chat" with the ref.
- 4 clues (choices, `clue_choices`): the **Press Pass** (behind the booth desk),
  the **Betting Slip** (bin in the ref's room), the **tie tip** with gold
  initials G.I. (stuck in the cut cable in the Server Room) and **Dave's statement**.
- The truth: the striker was **onside by 30 cm**, so GOAL is the right call.

### Scenes

1. **VAR Booth** – start. Doors from left to right: Server Room, Ref, Mascot,
   tunnel to the Pitch. The window, monitors and desk are drawn 58 px to the
   right (`BOOTH_SHIFT`, a subsurface). Sticky note (close-up), press pass
   behind the desk, VAR computer for the **VAR Review** (needs the USB; one look only).
2. **Referee's Dressing Room** – the **Lucky Whistle**, the Betting Slip in the bin.
3. **Mascot Changing Room** – locked; needs the Lucky Whistle.
   Bernie/Dave gives the **USB Stick** and his statement.
4. **Server Room** – racks, a technician's desk ("NO SIGNAL" monitor), the cut
   red cable (sparks, smoke) over a floor vent, and the tie tip fluttering in the cold air.
5. **The Pitch** – rule **Goal** or **Offside** (both allowed). The ref blows
   the final whistle, the press rushes in, and you answer (this ends the game):
   **"Clearly ONSIDE/OFFSIDE"** (matches your ruling, `needs_ruling`),
   **"No comment"** or **expose Infantini** (needs all 4 clues). After the
   ruling you cannot go back to the booth (`hidden_after`); in 2D the press
   questions open by themselves and cannot be closed (`press_next`, `locked`).

### VAR Review

It starts with a "rules" step that explains offside in plain words (`"rules"` in
story.json, also printed in the terminal); Enter starts the footage.
A timeline of 3.0 s in 0.1 s steps (no names, no hints). Find the last moment
the passer's boot touches the ball (1.2 s), lock it, then move a free offside
line in 0.1 m steps (2D: no number shown; terminal: type metres).
Correct: 1.2 s + line on defender 4 (21.5 m); striker at 21.8 m = onside
(level counts as onside). One step late (1.3 s) = offside. Positions are
"tracks" of [time, metres, lane] points in story.json; `value_at` interpolates,
`judge_offside(striker_metres, line_metres)` compares.

### Items

- Lucky Whistle, USB Stick. (The 4 clues are hidden in `choices`, not items.
  The player never sees a clue count.)
- Items are **reusable** (not used up) and **cannot be duplicated**.

### Endings (`choose_ending` in game.py, checked top to bottom)

- **Daylight Robbery** – ruled OFFSIDE.
- **Lucky Guess** – GOAL without the review.
- **VAR Is Watching** – GOAL after the review + exposed Infantini (best ending).
- **By the Book** – GOAL after the review, Infantini not exposed.
- **The Stadium Went Home** – time ran out (the coin says OFFSIDE).

Every ending then shows Infantini in the TV studio (`studio_outcome`,
`"epilogues"` in story.json): **arrested** (you exposed him), **wins** (it
ended 0:0: OFFSIDE or time up) or **loses** (the goal counts). Ending texts are
short and funny. Old saves are updated on loading (`update_old_save`).

## Tech

- Python. Terminal version: `game.py`. 2D pixel-art version (pygame-ce):
  `game_2d.py` (game loop), `rooms.py` (room drawings), `sprites.py` (pixel
  grids), `ui.py` (dialogue box, pundit TV, close-ups, inventory bar).
- `sound.py` – sounds and music for the 2D version (pygame.mixer); the .wav files
  are in `sounds/` and are made by `tools/make_sounds.py` (chiptune synthesis with
  math/wave/random only; a tool, not part of the game). Volume slider 0-10 + M mute,
  remembered in `settings.json` (separate from the save, so New Game keeps it).
- `story.json` – all story content, shared by both versions.
- `save.json` – terminal progress, **saved after every accepted action**.
  The 2D version saves to `save_2d.json` (same format).
- Time limit: 40 actions (terminal) or 300 seconds (2D). In 2D the timer only
  runs while no box is open (`box_is_open`), so reading never costs time.
- 2D door animation: walking through a door takes a "photo" of the old room,
  a black circle closes over it and opens again on the new room
  (`screen["door"]`, `DOOR_FRAMES` = 16, `draw_door_transition` in ui.py).
  The room changes (and is saved) at once; keys and the timer wait meanwhile.
  The same circle, much slower (`ENDING_FRAMES` = 60, 2 s), plays once when
  the last text is read, and opens on the ending screen (`start_circle`,
  `screen["ending_circle"]`). The ending jingle waits until it is finished.
- 2D end clips (`clips.py`): after the slow circle, short "film scenes" play
  (`screen["clips"]`, `CLIP_FRAMES` = 150 = 5 s each, Space skips), each
  followed by a circle (`CLIP_CHANGE_FRAMES`), then the ending screen.
  Clip 1 is on the pitch (`pitch_clip_name`): **pitch_goal** (striker knee
  slide, passer jumps, red confetti, away players sad), **pitch_offside**
  (away players jump, yellow confetti, striker on his knees, hands on head),
  **pitch_time_up** (the ref's coin lands on OFFSIDE, lights go out, Bernie
  walks home). The clip camera films a 320 x 180 part of the canvas 3x bigger
  (`CLIP_LEFT`, `CLIP_TOP`, `CLIP_ZOOM`, `to_window`), with black film bars.
  Extra player pictures: "passer", "defender" and the sad away players
  without the raised arm (`CAPTAIN_ARM_DOWN`).
  Clip 2 is in Infantini's TV studio ("studio_" + `studio_outcome`): he
  stands there with his whole body (`make_infantini(mood)` = his TV head +
  `INFANTINI_BODY`), drawn 2x bigger (`bigger`), next to a small desk, with
  the final score on a big screen (`final_score`): **studio_wins** (he kisses
  the slip, hearts, money rain), **studio_loses** (his face turns furious,
  steam, he crumples the slip and throws it away), **studio_arrested** (two
  serious police officers, `POLICE` + `POLICE_COLOURS`: checked cap band,
  hi-vis vest with "POLICE", walk in, handcuffs "CLICK!", they lead him away
  with his head down, slowly, then TV static and "[SIGNAL LOST]").
- The press pack (2D): after the ruling text, the press storms out of the
  tunnel on the left one after the other (`PRESS_PEOPLE`, `PRESS_DELAY`,
  `PRESS_RUN`), trampling and kicking up dust (`draw_press_dust`), then they
  spread out: 3 interviewers (`INTERVIEWER`: all black, blue press pass,
  microphone in the stretched hand) right next to you, 10 photographers
  (`PHOTOGRAPHER`: the same outfit, a camera with a long white lens,
  flashing all the time) behind them in staggered rows (the 4th number in
  `PRESS_PEOPLE` = how far back), partly hiding each other. All of them have "PRESS" on the
  shirt. People right of you are flipped to look at you. When the press
  comes, the striker walks to the corner flag and the captain to the goal
  (`player_step_aside`),
  and the captain's "OFFSIDE!" bubble goes away. `screen["press_rush"]` counts the frames
  (`PRESS_RUSH_FRAMES` = 100), the screen shakes a little meanwhile, then the press
  questions open. The words PRESS / VAR are sharp text
  (`press_labels`, drawn in `draw_game`).
- On the pitch the referee stands at x 264, left of where you stand to give
  your call (x 295), so you never hide him.
- Clothes on the pitch, so everyone is easy to tell apart: home red, away
  yellow, referee and linesman turquoise with black (the referee has a
  whistle in his mouth), you plain orange with "VAR", the press all black
  with a blue press pass and "PRESS".
- After the ruling the scoreboard shows FULL TIME and 1 - 0 (GOAL) or 0 - 0
  (OFFSIDE) (`draw_scoreboard_text`).
- 2D pundit faces: `make_pundit(mood)` in sprites.py swaps rows
  (`PUNDIT_MOOD_ROWS`) and skin colours (`PUNDIT_MOOD_SKIN`) per clue count.
- `test_game.py` – automatic tests for A1-A6 and the main rules, plain asserts,
  no extra libraries: `py test_game.py`.
- Web version (team project needs a public URL): pygbag builds the 2D game for the
  browser, GitHub Actions (`.github/workflows/deploy.yml`) tests, builds and publishes
  it on GitHub Pages after every push to main (https://ericjunger3-cmd.github.io/VAR_is_Watching/).
  `main.py` starts it (`asyncio.run(main())`, must import pygame); `title_screen`, `play`
  and `main` are async with `await asyncio.sleep(0)` per frame. `storage.py` saves to
  files on a computer and to localStorage in the browser (`IN_BROWSER`). Sounds are .ogg
  copies in the browser (`SOUND_TYPE`, `tools/make_ogg.py`); the music is a normal Sound
  on its own channel (channel 1, ambience is 0), not pygame.mixer.music (that crackled in the browser). `make_font` uses pygame's own font x1.6 in the browser. No Fullscreen/Exit there.
  Test locally: `py -m pygbag .` (from the parent folder: `py -m pygbag VAR_is_Watching`).
- Run with `py game.py` / `py game_2d.py` (Python 3.15 on this PC; `python`
  points to the Microsoft Store alias).

## Brief requirements (Plot Twist BRD v1.0)

> Note: the wording below is a summary of the brief, not an exact copy.
> Check the brief page for the official text.

### Content and constraints

- One original mystery/escape game, about ten minutes of play.
- At least 5 scenes, 2 collectible items and 2 reachable endings.
  At least one ending depends on an earlier choice or item.
- Text and simple controls; images and sound are optional.
- Save after each accepted action; accepted changes survive restarting the app.
  Rejected actions leave the saved data unchanged.
- Works offline with the supplied content (no paid service or live integration).
- Out of scope: visual story editor, procedural story generation, multiplayer,
  combat, live AI dialogue.

### Functional requirements

- **PT01 Start and resume** – Offer a new game, and resume an existing save when
  one exists. Ask for confirmation before a new game replaces saved progress.
- **PT02 Explore** – Show the current scene and its actions. Every accepted
  choice gives a visible result.
- **PT03 Collect and use** – The player can view their inventory. At least one
  item unlocks an action. Collecting the same item twice is not allowed.
- **PT04 Apply consequences** – At least one remembered decision affects a later
  action or ending. Blocked actions are explained or hidden.
- **PT05 Finish and replay** – Each ending is clearly labelled. Story actions stop
  after an ending, and the player can review the outcome or start over.

### Business rules

- **R1** – An action runs only when its scene and prerequisites are met.
  A blocked action changes nothing.
- **R2** – An item can be collected only where the story makes it available, and
  only once per game. Items in the required release are reusable.
- **R3** – Revisited scenes reflect earlier changes (e.g. an emptied drawer does
  not offer a second key).
- **R4** – A new game resets progress but keeps the story content. Every ending
  must be reachable from a new game.

### Acceptance scenarios

- **A1 Locked route** – Without the key, the locked route is unavailable or
  rejected, and location and inventory stay the same.
- **A2 Unlocked route** – With the key, the route leads to the intended scene,
  and the key stays in the inventory.
- **A3 No duplicate collection** – Collecting an item again still leaves only one
  copy in the inventory.
- **A4 Resume** – After getting an item and making a consequential choice,
  reopening the app restores the scene, item, choice and available routes.
- **A5 Two outcomes** – Two valid paths from separate new games reach different
  endings, and an ending cannot be changed afterwards.
- **A6 Restart safely** – Cancelling a restart keeps progress. Confirming it
  restores the opening scene, an empty inventory and the initial decisions.

### How this game maps to the brief

- A1/A2: the Lucky Whistle is the "key" for the Mascot Changing Room.
- A3: every item can be collected only once (taken items disappear).
- PT04: the review result and the press answer are remembered and change the
  ending; exposing Infantini needs earlier clues (needs_choices).
