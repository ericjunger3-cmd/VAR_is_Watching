# Sound effects and music for the 2D game.
# The sounds are .wav files in the sounds folder (made by tools/make_sounds.py).
# If the computer has no sound device, the game simply runs without sound.

import json
import pygame

SOUND_FOLDER = "sounds/"

# The volume is remembered in its own small file (not in the save file),
# so it stays the same after a New Game and after closing the game.
SETTINGS_FILE = "settings.json"

# Short sounds (effects) and long sounds that repeat (the background of a room).
EFFECTS = ["pickup", "door", "bonk", "blip", "confirm", "type", "whistle", "coo",
           "camera", "beep", "tick", "lock", "kick", "goal", "jingle_good", "jingle_bad"]
AMBIENCE = ["crowd", "shower"]

# How loud the music is compared to the effects (the music stays in the back).
MUSIC_LEVEL = 0.55
AMBIENCE_LEVEL = 0.7

# Everything the sound part of the game remembers, in one dictionary.
state = {
    "working": False,     # False if there is no sound device
    "volume": 7,          # the volume slider: 0 (off) to 10 (loudest)
    "muted": False,       # M mutes and unmutes everything
    "music": None,        # the name of the song that is playing
    "ambience": None,     # the name of the room sound that is playing
    "sounds": {},         # name -> the loaded sound
    "channel": None,      # the channel that plays the room sound
}


def load_settings():
    # Read the volume from last time. If there is no settings file yet
    # (first time playing) or it is broken, we keep the normal volume.
    try:
        with open(SETTINGS_FILE) as file:
            settings = json.load(file)
        state["volume"] = max(0, min(10, int(settings["volume"])))
        state["muted"] = settings["muted"] == True
    except (FileNotFoundError, ValueError, KeyError, TypeError):
        return


def save_settings():
    # Write the volume to the settings file, so it is remembered next time.
    settings = {"volume": state["volume"], "muted": state["muted"]}
    with open(SETTINGS_FILE, "w") as file:
        json.dump(settings, file)


def start():
    # Switch the sound system on and load all sounds. If that fails
    # (for example: no speakers), the game works without sound.
    load_settings()
    try:
        pygame.mixer.init()
        for name in EFFECTS + AMBIENCE:
            state["sounds"][name] = pygame.mixer.Sound(SOUND_FOLDER + name + ".wav")
    except (pygame.error, FileNotFoundError):
        return
    # Channel 0 is kept free for the room sound (crowd, shower), so the
    # effects never cut it off.
    pygame.mixer.set_reserved(1)
    state["channel"] = pygame.mixer.Channel(0)
    state["working"] = True
    apply_volume()


def loudness():
    # The volume as a number from 0.0 to 1.0 (0 when muted).
    if state["muted"]:
        return 0.0
    return state["volume"] / 10


def apply_volume():
    # Give every sound, the music and the room sound the current volume.
    if not state["working"]:
        return
    for name in EFFECTS:
        state["sounds"][name].set_volume(loudness())
    pygame.mixer.music.set_volume(loudness() * MUSIC_LEVEL)
    state["channel"].set_volume(loudness() * AMBIENCE_LEVEL)


def play(name):
    # Play a short sound effect once.
    if state["working"]:
        state["sounds"][name].play()


def play_music(name):
    # Start a song (it repeats forever). If it is already playing, nothing
    # changes, so the song does not start again from the beginning.
    if not state["working"] or state["music"] == name:
        return
    pygame.mixer.music.load(SOUND_FOLDER + name + ".wav")
    pygame.mixer.music.play(-1)
    state["music"] = name


def stop_music():
    if state["working"]:
        pygame.mixer.music.stop()
        state["music"] = None


def set_ambience(name):
    # The room sound: "crowd", "shower" or None (silence). It repeats
    # until another room sound is chosen.
    if not state["working"] or state["ambience"] == name:
        return
    state["channel"].stop()
    if name is not None:
        state["channel"].play(state["sounds"][name], loops=-1)
    state["ambience"] = name


def change_volume(step):
    # Move the volume slider: step is -1 (quieter) or +1 (louder).
    # min and max keep it between 0 and 10.
    state["volume"] = max(0, min(10, state["volume"] + step))
    state["muted"] = False
    apply_volume()
    save_settings()
    play("blip")


def toggle_mute():
    # M: everything silent, or back to the slider's volume.
    state["muted"] = not state["muted"]
    apply_volume()
    save_settings()


def volume_text():
    # The slider as text for the pause menu, e.g. "Volume: [#######---]".
    if state["muted"]:
        return "Volume: [----------] muted (M)"
    return "Volume: [" + "#" * state["volume"] + "-" * (10 - state["volume"]) + "]  < >"
