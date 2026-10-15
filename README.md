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
- **2 items:** the Lucky Whistle opens the Mascot Changing Room; Pombo the pigeon
  mascot gives you the USB Stick with the missing angle. Items are reusable and
  can only be collected once.
- **1 remembered decision:** in the Press Room you say "Clearly a goal!" or
  "No comment". The Pitch is locked until you answer.
- **3 endings:**
  - *Justice Served*: USB Stick + "No comment"
  - *Clip of the Year*: no USB Stick
  - *Right Call, Wrong Mouth*: USB Stick + "Clearly a goal!"

## Acceptance test checklist (A1-A6)

Start each test from a new game: delete `save.json` first, or choose `n` and then `y`
in the start menu. Type the inputs one at a time, pressing Enter after each one.

**Menu numbers.**
- **VAR Booth:** `1` Dressing Room, `2` Mascot Room, `3` Press Room, `4` Pitch.
- **Other rooms:** an item or answer action comes first; "Back to the VAR Booth"
  is the last numbered action.

| Test | Inputs | Expected result |
|---|---|---|
| **A1 Locked route** | `2`, then `i` | "The door is locked..." You stay in the VAR Booth and your pockets are empty. |
| **A2 Unlocked route** | `1`, `1` (take whistle), `1` (back), `2`, then `i` | The door opens and you are in the Mascot Changing Room. The inventory still shows the Lucky Whistle. |
| **A3 No duplicate** | `1`, `1` (take whistle), `1` (back), `1` (Dressing Room again), then `i` | After taking it, the "Take the Lucky Whistle" action is gone, also on the second visit. The inventory shows the Lucky Whistle only once. |
| **A4 Resume** | `1`, `1`, `1`, `2`, `1` (USB), `1`, `3`, `2` (No comment), `q`. Then run `py game.py` again and type `c`, `i`, `1`, `4` | You continue in the Press Room without the answer options. The inventory shows both items. The Pitch is open. |
| **A5 Two outcomes** | Game 1: `3`, `1`, `1`, `4`, `1` gives **Clip of the Year**. Type `n`, `y`. Game 2: `1`, `1`, `1`, `2`, `1`, `1`, `3`, `2`, `1`, `4`, `1` gives **Justice Served**. Type `q`, run again, `c` | Two different endings. Reopening a finished game shows the same ending, with only `v`, `n` and `q`. |
| **A6 Restart safely** | `1`, `1` (take whistle), then `r`, `n`, `i`. Then `r`, `y`, `i`, `3` | After `n`: you are still in the Dressing Room with the whistle. After `y`: you are back in the VAR Booth, your pockets are empty, and the Press Room shows both answers again. |
