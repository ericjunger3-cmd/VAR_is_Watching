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
and the key VAR angle is missing. The player is a junior VAR official on their
first day. A smug TV pundit narrates everything.

### The twist (optional to discover)

- **Pombo is Dave**, the missing VAR operator from the sticky note, working a
  second job as the mascot. He filmed the goal on his head-cam (the USB Stick)
  and saw a man in a shiny suit run out of the booth at 93:30.
- **The pundit, Rex Smugworth, pulled the camera cable** because he bet 500 on
  the away team. Clues: the Press Lanyard (behind the booth desk), the Betting
  Slip (press room), Dave's statement. The pundit gets more nervous with every
  clue. Every ending except the best one ends with an epilogue hinting at him.
- The truth: the striker was **onside by 30 cm**, so GOAL is the right call.

### Scenes

1. **VAR Booth** – start. Sticky note (close-up), lanyard behind the desk,
   VAR computer for the **VAR Review** (needs the USB; one look only).
2. **Referee's Dressing Room** – the **Lucky Whistle**.
3. **Mascot Changing Room** – locked; needs the Lucky Whistle.
   Pombo/Dave gives the **USB Stick** and his statement.
4. **Press Room** – one answer only: **"Clearly a goal!"**, **"No comment"** or
   **expose Rex** (needs lanyard + slip + Dave). Betting Slip by the TV camera.
5. **The Pitch** – open from the start, but the referee only takes the call
   after the press answer; rule **Goal** or **Offside** (both allowed).

### VAR Review

A timeline of 3.0 s in 0.1 s steps (no names, no hints). Find the last moment
the passer's boot touches the ball (1.2 s), lock it, then move a free offside
line in 0.1 m steps (2D: no number shown; terminal: type metres).
Correct: 1.2 s + line on defender 4 (21.5 m); striker at 21.8 m = onside
(level counts as onside). One step late (1.3 s) = offside. Positions are
"tracks" of [time, metres, lane] points in story.json; `value_at` interpolates,
`judge_offside(striker_metres, line_metres)` compares.

### Items

- Lucky Whistle, USB Stick, Press Lanyard, Betting Slip.
- Items are **reusable** (not used up) and **cannot be duplicated**.

### Endings (`choose_ending` in game.py, checked top to bottom)

- **Daylight Robbery** – ruled OFFSIDE.
- **Clip of the Year** – GOAL without the review.
- **VAR Is Watching** – GOAL after the review + exposed Rex (best ending).
- **Justice Served** – GOAL after the review + "No comment".
- **Right Call, Wrong Mouth** – GOAL after the review + "Clearly a goal!".

## Tech

- Python. Terminal version: `game.py`. 2D pixel-art version (pygame-ce):
  `game_2d.py` (game loop), `rooms.py` (room drawings), `sprites.py` (pixel
  grids), `ui.py` (dialogue box, pundit TV, close-ups, inventory bar).
- `story.json` – all story content, shared by both versions.
- `save.json` – terminal progress, **saved after every accepted action**.
  The 2D version saves to `save_2d.json` (same format).
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
  ending; exposing Rex needs earlier clues (needs_items + needs_choice).
