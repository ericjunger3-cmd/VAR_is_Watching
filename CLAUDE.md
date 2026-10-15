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

### Scenes

1. **VAR Booth** – starting scene.
2. **Referee's Dressing Room** – the **Lucky Whistle** can be collected here.
3. **Mascot Changing Room** – locked; needs the Lucky Whistle to enter.
   Pombo the pigeon mascot gives the **USB Stick**.
4. **Press Room** – decision: say **"Clearly a goal!"** or **"No comment"**.
5. **The Pitch** – the player rules **Goal** or **Offside**.

### Items

- Lucky Whistle, USB Stick.
- Items are **reusable** (not used up) and **cannot be duplicated**.

### Endings

- **Justice Served** – has the USB Stick + said "No comment".
- **Clip of the Year** – no USB Stick.
- **Right Call, Wrong Mouth** – has the USB Stick + said "Clearly a goal!".

## Tech

- Python terminal app.
- `story.json` – all story content (scenes, text, actions, items, endings).
- `game.py` – the game logic.
- `save.json` – player progress, **saved after every accepted action**.

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
- A3: the Lucky Whistle and USB Stick can each be collected only once.
- PT04: the Press Room answer is remembered and changes the final ending.
