# Makes all the sound effects and the music of VAR Is Watching, in the style
# of old game consoles (8-bit "chiptune"). Everything is built from simple
# waves: square waves (the classic beep), triangle waves (a soft bass) and
# noise (drums, the crowd, the shower). The results are saved as .wav files
# in the sounds folder.
#
# This is a tool, not part of the game: the game only plays the .wav files.
# Run it from the game folder with:   py tools/make_sounds.py

import math
import random
import struct
import wave

RATE = 22050          # samples per second (like old consoles: not too many)
FOLDER = "sounds/"

# The same random numbers every time, so the sounds never change.
random.seed(94)


# ---------------------------------------------------------------- building blocks

def tone(frequency, seconds, shape="square", volume=0.3, duty=0.5, slide_to=None, vibrato=0.0):
    # A list of samples (numbers between -1 and 1) for one note.
    # shape: "square", "triangle" or "sine". duty: how much of a square
    # wave is "up" (0.5 sounds full, 0.125 thin and buzzy).
    # slide_to: the frequency slides to this one (e.g. for a "boing").
    # vibrato: how much the pitch wobbles (0 = not at all).
    samples = []
    count = int(seconds * RATE)
    phase = 0.0
    for i in range(count):
        progress = i / count
        f = frequency
        if slide_to is not None:
            f = frequency + (slide_to - frequency) * progress
        if vibrato > 0:
            f = f * (1 + vibrato * math.sin(2 * math.pi * 6 * i / RATE))
        phase = (phase + f / RATE) % 1.0
        if shape == "square":
            value = 1.0 if phase < duty else -1.0
        elif shape == "triangle":
            value = 4 * abs(phase - 0.5) - 1
        else:
            value = math.sin(2 * math.pi * phase)
        samples.append(value * volume)
    return samples


def noise(seconds, volume=0.3, smooth=0.0):
    # Random samples: a "shhh" sound. smooth between 0 and 1 makes it
    # darker (more like a rumble): every sample is mixed with the last one.
    samples = []
    last = 0.0
    for i in range(int(seconds * RATE)):
        value = random.uniform(-1, 1)
        last = last * smooth + value * (1 - smooth)
        samples.append(last * volume)
    return samples


def fade(samples, fade_in=0.005, fade_out=0.05):
    # Make the start and the end soft, so there are no clicks.
    count = len(samples)
    start = int(fade_in * RATE)
    end = int(fade_out * RATE)
    result = []
    for i in range(count):
        level = 1.0
        if start > 0 and i < start:
            level = i / start
        if end > 0 and i > count - end:
            level = min(level, (count - i) / end)
        result.append(samples[i] * level)
    return result


def decay(samples, speed=6.0):
    # The sound gets quieter over time, like a plucked string.
    return [value * math.exp(-speed * i / RATE) for i, value in enumerate(samples)]


def silence(seconds):
    return [0.0] * int(seconds * RATE)


def mix(*tracks):
    # Play several lists of samples at the same time (add them up).
    length = max(len(track) for track in tracks)
    result = [0.0] * length
    for track in tracks:
        for i, value in enumerate(track):
            result[i] = result[i] + value
    return result


def join(*parts):
    # Play lists of samples one after the other.
    result = []
    for part in parts:
        result = result + part
    return result


def save(name, samples):
    # Write the samples as a 16-bit mono .wav file.
    with wave.open(FOLDER + name + ".wav", "wb") as file:
        file.setnchannels(1)
        file.setsampwidth(2)
        file.setframerate(RATE)
        frames = bytearray()
        for value in samples:
            value = max(-1.0, min(1.0, value))
            frames += struct.pack("<h", int(value * 32000))
        file.writeframes(bytes(frames))
    print("made", name)


def make_loop(samples, overlap=0.5):
    # Make a sound that can repeat without a bump: the end is faded into
    # the start, so the last sample flows into the first one.
    count = int(overlap * RATE)
    body = samples[:len(samples) - count]
    tail = samples[len(samples) - count:]
    for i in range(count):
        mix_level = i / count
        body[i] = body[i] * mix_level + tail[i] * (1 - mix_level)
    return body


def place(track, samples, start_seconds):
    # Add a sound into a longer track, starting at start_seconds.
    # (Parts that would go past the end are left out.)
    start = int(start_seconds * RATE)
    for i, value in enumerate(samples):
        if start + i < len(track):
            track[start + i] = track[start + i] + value


def soften(samples, amount=0.6):
    # Take away the sharp high part of a sound (a simple "low-pass filter"):
    # every sample moves only part of the way towards the new value.
    result = []
    last = 0.0
    for value in samples:
        last = last * amount + value * (1 - amount)
        result.append(last)
    return result


def normalize(samples, loudest=0.7):
    # Make the loudest point exactly "loudest", so nothing crackles.
    peak = max(abs(value) for value in samples)
    return [value * loudest / peak for value in samples]


# ---------------------------------------------------------------- notes and music

NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


def frequency(note):
    # "A4" -> 440 Hz. Every step up is 2 ** (1/12) times higher.
    name = note[:-1]
    octave = int(note[-1])
    steps = NOTE_NAMES.index(name) + (octave - 4) * 12 - 9
    return 440.0 * 2 ** (steps / 12)


def melody(notes, bpm, shape="square", volume=0.2, duty=0.5, length=0.9):
    # notes is a list of (note, beats); "-" is a rest. length is how much
    # of each note is played (0.5 = short and bouncy, 0.95 = smooth).
    beat = 60.0 / bpm
    result = []
    for note, beats in notes:
        seconds = beats * beat
        if note == "-":
            result = result + silence(seconds)
        else:
            sound = fade(tone(frequency(note), seconds * length, shape, volume, duty), 0.003, 0.02)
            result = result + sound + silence(seconds - len(sound) / RATE)
    return result


# ---------------------------------------------------------------- sound effects

def make_effects():
    # Picking up an item: the classic two-note "coin" sound.
    save("pickup", join(tone(988, 0.06, volume=0.25), decay(tone(1319, 0.3, volume=0.25), 8)))

    # Opening a door: a creak sliding down, then a soft thump.
    creak = fade(tone(320, 0.22, "square", 0.12, duty=0.125, slide_to=180, vibrato=0.04))
    thump = decay(mix(noise(0.12, 0.35, 0.8), tone(90, 0.12, "triangle", 0.4, slide_to=50)), 22)
    save("door", join(creak, thump))

    # A locked door or a blocked action: a low "bonk-bonk".
    save("bonk", join(fade(tone(150, 0.08, volume=0.25)), silence(0.02), decay(tone(110, 0.18, volume=0.25), 10)))

    # Menus: moving the selection, confirming, and the text "typing" blip.
    save("blip", fade(tone(880, 0.04, volume=0.15, duty=0.25), 0.002, 0.01))
    save("confirm", join(fade(tone(660, 0.05, volume=0.2)), decay(tone(990, 0.12, volume=0.2), 12)))
    save("type", fade(tone(1250, 0.014, volume=0.07, duty=0.25), 0.001, 0.005))

    # The Lucky Whistle: a high trill (the pitch wobbles very fast), twice.
    def trill(seconds):
        samples = []
        for i in range(int(seconds * RATE)):
            t = i / RATE
            f = 2900 + 300 * math.sin(2 * math.pi * 28 * t)
            samples.append(math.sin(2 * math.pi * f * t) * 0.18)
        return fade(mix(samples, noise(seconds, 0.03)), 0.01, 0.05)
    save("whistle", join(trill(0.22), silence(0.06), trill(0.55)))

    # Pombo: a pigeon "coo-coo" (a low wobbly tone that slides down).
    coo1 = fade(tone(380, 0.22, "sine", 0.3, slide_to=330, vibrato=0.03), 0.03, 0.08)
    coo2 = fade(tone(340, 0.34, "sine", 0.3, slide_to=280, vibrato=0.03), 0.03, 0.12)
    save("coo", join(coo1, silence(0.06), coo2))

    # A camera: the click of the shutter and a little flash whine.
    click = decay(noise(0.03, 0.4), 80)
    whine = fade(tone(2400, 0.08, "sine", 0.05, slide_to=3200))
    save("camera", join(click, silence(0.03), decay(noise(0.025, 0.3), 90), whine))

    # The VAR Review: three beeps when it opens, a tick for every step,
    # and a rising "lock" sound.
    beep = fade(tone(1200, 0.07, volume=0.15, duty=0.25))
    save("beep", join(beep, silence(0.06), beep, silence(0.06), beep))
    save("tick", fade(tone(1600, 0.012, volume=0.08, duty=0.25), 0.001, 0.004))
    save("lock", join(fade(tone(800, 0.06, volume=0.18)), fade(tone(1200, 0.14, volume=0.18))))

    # Kicking the ball: a short thump.
    save("kick", decay(mix(noise(0.08, 0.3, 0.5), tone(140, 0.1, "triangle", 0.4, slide_to=55)), 25))


def make_ambience():
    # The shower: a bright hiss (noise minus its smooth part) with water
    # drops (tiny high pings) here and there.
    hiss = noise(4.5, 0.25)
    shower = []
    last = 0.0
    for value in hiss:
        last = last * 0.7 + value * 0.3
        shower.append((value - last) * 0.6)
    for drop in range(18):
        start = random.randint(0, len(shower) - 2000)
        ping = decay(tone(random.randint(1800, 3200), 0.05, "sine", 0.06), 60)
        for i, value in enumerate(ping):
            shower[start + i] = shower[start + i] + value
    save("shower", make_loop(shower))


# The vowels a voice can make. Our mouth makes some frequencies of the voice
# louder (called "formants"); every vowel has its own two main ones.
VOWELS = {"ah": (800, 1200), "oh": (500, 900), "eh": (500, 1800), "ee": (300, 2300), "oo": (350, 800)}


def resonate(samples, centre, width):
    # A "resonance filter": it keeps the part of the sound around the
    # frequency "centre" and makes everything else quiet, like a mouth
    # shaped for a vowel. (The numbers are the standard "band-pass" recipe.)
    w = 2 * math.pi * centre / RATE
    alpha = math.sin(w) * width / (2 * centre)
    a0 = 1 + alpha
    a1 = -2 * math.cos(w)
    a2 = 1 - alpha
    result = []
    x1 = x2 = y1 = y2 = 0.0
    for x in samples:
        y = (alpha * x - alpha * x2 - a1 * y1 - a2 * y2) / a0
        result.append(y)
        x2 = x1
        x1 = x
        y2 = y1
        y1 = y
    return result


def syllable(pitch, seconds, vowel, end_pitch=None):
    # One syllable of a voice: a buzzy tone (like our vocal cords) shaped
    # into a vowel by two resonance filters (like our mouth).
    if end_pitch is None:
        end_pitch = pitch * random.uniform(0.9, 1.1)
    buzz = []
    phase = 0.0
    count = int(seconds * RATE)
    for i in range(count):
        f = pitch + (end_pitch - pitch) * i / count
        phase = (phase + f / RATE) % 1.0
        buzz.append(phase * 2 - 1)          # a "sawtooth" wave: very buzzy
    first, second = VOWELS[vowel]
    voice = mix(resonate(buzz, first, 140), [v * 0.5 for v in resonate(buzz, second, 200)])
    return fade(voice, 0.03, 0.06)


def talker(pitch, syllables, volume):
    # One fan saying a short sentence: a few syllables with different
    # vowels, each a little higher or lower, with tiny pauses between.
    sentence = []
    for i in range(syllables):
        vowel = random.choice(list(VOWELS))
        length = random.uniform(0.09, 0.22)
        start = pitch * random.uniform(0.9, 1.15)
        sentence = sentence + syllable(start, length, vowel) + silence(random.uniform(0.0, 0.06))
    return [value * volume for value in sentence]


def clap(volume):
    # One hand clap: a very short burst of noise.
    return decay(soften(noise(0.04, volume), 0.3), 110)


def crowd_track(seconds, talkers):
    # Many fans talking at the same time, starting at random moments,
    # some low voices and some high voices, a few claps and whistles.
    track = silence(seconds)
    for i in range(talkers):
        if random.random() < 0.6:
            pitch = random.uniform(95, 150)        # a lower voice
        else:
            pitch = random.uniform(170, 260)       # a higher voice
        sentence = talker(pitch, random.randint(3, 8), random.uniform(0.6, 1.0))
        start = random.uniform(-0.5, seconds - 0.3)
        place(track, sentence, max(0.0, start))
    # Now and then a few people clap.
    for group in range(int(seconds / 2)):
        start = random.uniform(0, seconds - 0.5)
        for c in range(random.randint(2, 4)):
            place(track, clap(0.1), start + c * random.uniform(0.08, 0.13))
    # A few fans whistling.
    for whistle in range(max(1, int(seconds / 5))):
        start = random.uniform(0, seconds - 0.6)
        place(track, fade(tone(2100, 0.35, "sine", 0.02, slide_to=2600)), start)
    return track


def cheer_track(seconds, fans):
    # A goal: everybody shouts a long rising "yeahhh" ("eh" to "ah") at
    # almost the same moment, then some keep cheering, with lots of claps.
    track = silence(seconds)
    for i in range(fans):
        if random.random() < 0.6:
            pitch = random.uniform(110, 170)
        else:
            pitch = random.uniform(200, 300)
        start = random.uniform(0, 0.25)
        length = random.uniform(0.9, 1.8)
        yeah = join(syllable(pitch, 0.15, "eh", pitch * 1.2),
                    syllable(pitch * 1.2, length, "ah", pitch * random.uniform(1.35, 1.6)))
        place(track, [value * random.uniform(0.5, 1.0) for value in yeah], start)
        # Some fans cheer a second time ("ohhh!").
        if random.random() < 0.4:
            place(track, syllable(pitch * 1.3, random.uniform(0.5, 0.9), "oh", pitch * 1.1), start + length + 0.2)
    for c in range(int(seconds * 12)):
        place(track, clap(0.12), random.uniform(0.3, seconds - 0.2))
    return track


def make_crowd_sounds():
    # The crowd on the pitch: lots of fans talking at once, made to repeat
    # without a bump.
    save("crowd", normalize(make_loop(crowd_track(10.5, 120)), 0.5))

    # A goal: everybody cheers at once, then it slowly calms down.
    cheer = cheer_track(3.5, 70)
    for i in range(len(cheer)):
        t = i / RATE
        cheer[i] = cheer[i] * math.exp(-max(0.0, t - 1.4) * 1.2)
    save("goal", normalize(cheer, 0.6))


# ---------------------------------------------------------------- jingles

def make_jingles():
    # A happy fanfare for the good endings.
    lead = melody([("C5", 0.25), ("E5", 0.25), ("G5", 0.25), ("C6", 0.5), ("G5", 0.25), ("C6", 1.5)],
                  bpm=150, volume=0.22, duty=0.25)
    bass = melody([("C3", 1.0), ("G3", 0.5), ("C3", 1.5)], bpm=150, shape="triangle", volume=0.3)
    save("jingle_good", fade(mix(lead, bass), 0.005, 0.3))

    # A sad "wah wah wah waaah" for the bad endings.
    notes = []
    for note, seconds in [("G4", 0.32), ("F#4", 0.32), ("F4", 0.32)]:
        notes = notes + fade(tone(frequency(note), seconds, volume=0.2, duty=0.25), 0.01, 0.06) + silence(0.04)
    last = fade(tone(frequency("E4"), 1.1, volume=0.2, duty=0.25, vibrato=0.025), 0.01, 0.4)
    save("jingle_bad", notes + last)


# ---------------------------------------------------------------- chill music
# Soft instruments: a round lead, a mellow electric piano ("keys"), warm
# pads (long chords), a deep bass and soft drums with a little swing.

def soft_lead(f, seconds):
    sound = mix(tone(f, seconds, "triangle", 0.13, vibrato=0.004), tone(f * 2, seconds, "sine", 0.025))
    return fade(sound, 0.02, 0.18)


def keys(f, seconds):
    # Like an electric piano: a sine with a bit of its octave, fading out.
    sound = mix(tone(f, seconds, "sine", 0.07), tone(f * 2, seconds, "sine", 0.02))
    return fade(decay(sound, 3.0), 0.005, 0.1)


def pad(notes, seconds):
    # A long soft chord: every note twice, a tiny bit out of tune,
    # which makes it sound wide and warm.
    sound = []
    for note in notes:
        f = frequency(note)
        sound = mix(sound, tone(f * 0.997, seconds, "triangle", 0.022), tone(f * 1.003, seconds, "triangle", 0.022))
    return fade(sound, 0.4, 0.6)


def deep_bass(f, seconds):
    return fade(mix(tone(f, seconds, "sine", 0.28), tone(f * 2, seconds, "triangle", 0.04)), 0.01, 0.12)


def soft_kick():
    return decay(tone(95, 0.2, "sine", 0.45, slide_to=42), 14)


def soft_snare():
    return mix(decay(soften(noise(0.18, 0.28), 0.45), 16), decay(tone(190, 0.08, "sine", 0.08), 30))


def soft_hat():
    return decay(noise(0.03, 0.05), 120)


def when(beat, bpm, swing):
    # The time (in seconds) of a beat. With swing, every "and" between
    # two beats comes a little late, which makes the rhythm laid-back.
    if (beat * 2) % 2 == 1:
        beat = beat + swing
    return beat * 60.0 / bpm


def add_notes(track, notes, bpm, swing, instrument, start_beat=0.0):
    # Place a list of (note, beats) into the track with an instrument.
    beat = start_beat
    for note, beats in notes:
        if note != "-":
            place(track, instrument(frequency(note), beats * 60.0 / bpm), when(beat, bpm, swing))
        beat = beat + beats


def add_vinyl(track):
    # A little lo-fi record crackle: soft hiss and tiny random clicks.
    for i in range(len(track)):
        track[i] = track[i] + random.uniform(-1, 1) * 0.004
        if random.random() < 0.0004:
            track[i] = track[i] + random.uniform(-0.06, 0.06)


def chill_song(bpm, swing, chords, lead, comp_beats, drum_bars, lead_instrument):
    # chords: a list of (pad notes, bass note, beats).
    total_beats = sum(beats for notes, bass, beats in chords)
    track = silence(total_beats * 60.0 / bpm + 1.0)
    beat = 0.0
    for notes, bass, beats in chords:
        seconds = beats * 60.0 / bpm
        place(track, pad(notes, seconds + 0.3), when(beat, bpm, swing))
        place(track, deep_bass(frequency(bass), seconds * 0.9), when(beat, bpm, swing))
        # The keys play the chord on some beats of every bar (comping).
        for comp in comp_beats:
            if comp < beats:
                for note in notes:
                    place(track, keys(frequency(note) * 2, 0.9), when(beat + comp, bpm, swing))
        beat = beat + beats
    add_notes(track, lead, bpm, swing, lead_instrument)
    # Drums: one letter group per half beat ("k" kick, "s" snare, "h" hat).
    for bar in range(int(total_beats / 4)):
        for step, letters in enumerate(drum_bars):
            moment = when(bar * 4 + step * 0.5, bpm, swing)
            if "k" in letters:
                place(track, soft_kick(), moment)
            if "s" in letters:
                place(track, soft_snare(), moment)
            if "h" in letters:
                place(track, soft_hat(), moment)
    add_vinyl(track)
    # Cut to the exact length, so the song loops in time.
    return track[:int(total_beats * 60.0 / bpm * RATE)]


def make_title_theme():
    # A chill, sunny theme in C major (80 beats per minute, 16 bars).
    F7 = ["F3", "A3", "C4", "E4"]
    E7 = ["E3", "G3", "B3", "D4"]
    D7 = ["D3", "F3", "A3", "C4"]
    C7 = ["C3", "E3", "G3", "B3"]
    G7 = ["G3", "B3", "D4", "F4"]
    part = [(F7, "F2", 4), (E7, "E2", 4), (D7, "D2", 4), (C7, "C2", 4),
            (F7, "F2", 4), (E7, "E2", 4), (D7, "D2", 2), (G7, "G2", 2), (C7, "C2", 4)]
    lead = [
        ("A5", 1), ("G5", 0.5), ("E5", 0.5), ("C5", 1.5), ("-", 0.5),
        ("B4", 0.5), ("D5", 0.5), ("E5", 1), ("G5", 1), ("-", 1),
        ("F5", 0.5), ("E5", 0.5), ("D5", 1), ("A4", 1), ("C5", 1),
        ("E5", 2.5), ("-", 1.5),
        ("A5", 0.5), ("C6", 0.5), ("A5", 0.5), ("G5", 0.5), ("E5", 1), ("-", 1),
        ("G5", 0.5), ("B5", 0.5), ("G5", 0.5), ("E5", 0.5), ("D5", 1), ("-", 1),
        ("F5", 1), ("E5", 0.5), ("D5", 0.5), ("B4", 1), ("D5", 1),
        ("C5", 3), ("-", 1),
        ("C6", 1), ("A5", 0.5), ("G5", 0.5), ("A5", 1), ("-", 1),
        ("B5", 1), ("G5", 0.5), ("E5", 0.5), ("G5", 1.5), ("-", 0.5),
        ("A5", 0.5), ("G5", 0.5), ("F5", 0.5), ("E5", 0.5), ("D5", 1), ("F5", 1),
        ("E5", 0.5), ("G5", 0.5), ("B5", 1), ("-", 2),
        ("C6", 0.5), ("B5", 0.5), ("A5", 0.5), ("G5", 0.5), ("A5", 1), ("C6", 1),
        ("B5", 1.5), ("A5", 0.5), ("G5", 1), ("-", 1),
        ("A5", 0.5), ("G5", 0.5), ("F5", 1), ("D5", 0.5), ("B4", 0.5), ("D5", 1),
        ("C5", 2), ("-", 2),
    ]
    drums = ["kh", "h", "sh", "h", "kh", "kh", "sh", "h"]
    song = chill_song(80, 0.09, part + part, lead, [0, 1.5, 3], drums, soft_lead)
    save("title_theme", normalize(song, 0.6))


def make_game_theme():
    # A calm, curious mystery theme in A minor (72 beats per minute, 8 bars),
    # with the melody on the electric piano.
    Am = ["A3", "C4", "E4", "G4"]
    F7 = ["F3", "A3", "C4", "E4"]
    D7 = ["D3", "F3", "A3", "C4"]
    E7 = ["E3", "G#3", "B3", "D4"]
    Bm = ["B2", "D3", "F3", "A3"]
    chords = [(Am, "A2", 4), (F7, "F2", 4), (D7, "D2", 4), (E7, "E2", 4),
              (Am, "A2", 4), (F7, "F2", 4), (Bm, "B2", 4), (E7, "E2", 4)]
    lead = [
        ("-", 1), ("E5", 0.5), ("A5", 0.5), ("C6", 1), ("B5", 1),
        ("A5", 1.5), ("-", 0.5), ("E5", 1), ("-", 1),
        ("-", 1), ("F5", 0.5), ("A5", 0.5), ("D6", 1), ("C6", 1),
        ("B5", 1.5), ("-", 0.5), ("G#5", 1), ("-", 1),
        ("-", 1), ("E5", 0.5), ("A5", 0.5), ("E6", 1), ("D6", 0.5), ("C6", 0.5),
        ("C6", 1), ("A5", 1), ("F5", 1), ("-", 1),
        ("D5", 0.5), ("F5", 0.5), ("A5", 0.5), ("B5", 0.5), ("D6", 1), ("C6", 1),
        ("B5", 2), ("G#5", 1), ("-", 1),
    ]
    drums = ["kh", "h", "h", "h", "sh", "h", "kh", "h"]
    song = chill_song(72, 0.1, chords, lead, [0, 2.5], drums, keys)
    save("game_theme", normalize(song, 0.55))


make_effects()
make_ambience()
make_crowd_sounds()
make_jingles()
make_title_theme()
make_game_theme()
print("All sounds are in the sounds folder.")
