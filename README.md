# VAR Is Watching

A short comedy mystery game for the terminal (about 10 minutes of play).
Solo project for Nova SBE *Introduction to Programming*, based on the
"Plot Twist" brief.

It is the 94th minute of a cup final. The home side scores, the away side
claims offside, and the key VAR angle is missing. You are a junior VAR official
on your first day. A smug TV pundit comments on everything you do.
Find the missing footage, survive the press, and make the call.

## How to run

You need Python 3 (no extra packages). Open a terminal in this folder and run:

```
py game.py
```

(On Mac/Linux, or if `py` does not work: `python game.py` or `python3 game.py`.)

Run it in a real terminal window, because the game waits for you to type.

## Controls

| Key | What it does |
|---|---|
| `1`, `2`, `3` ... | choose an action from the list |
| `i` | show your inventory |
| `r` | restart (asks for confirmation) |
| `q` | quit (your progress is saved) |

At the start, if a saved game exists: `n` = new game (asks for confirmation),
`c` = continue. After an ending: `v` = view the ending again, `n` = new game,
`q` = quit.

## Files

| File | What it contains |
|---|---|
| `game.py` | all the game logic |
| `story.json` | all the story content: scenes, actions, items and endings |
| `save.json` | your progress; created by the game and saved after every accepted action |

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
  it, then draw the offside line in metres. You only get one look.
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

## Acceptance test checklist (A1-A6)

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
