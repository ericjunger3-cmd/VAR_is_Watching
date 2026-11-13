# Makes an .ogg copy of every .wav sound in the sounds folder.
# Browsers cannot play our .wav files in the web version, but they can play
# .ogg files, so the web version uses these copies (see sound.py).
# This is a tool, not part of the game. It needs the soundfile package
# (numpy comes with it):
#   py -m pip install soundfile
# Run it from the game folder after changing a sound:
#   py tools/make_ogg.py

import os
import numpy
import soundfile

for name in sorted(os.listdir("sounds")):
    if name.endswith(".wav"):
        wav_path = "sounds/" + name
        ogg_path = "sounds/" + name[:-4] + ".ogg"
        # Skip sounds whose .ogg copy is already newer than the .wav file.
        # (The encoder sometimes stops after many files: then simply run
        # the tool again, and it goes on where it stopped.)
        if os.path.exists(ogg_path) and os.path.getmtime(ogg_path) >= os.path.getmtime(wav_path):
            continue
        # Read the samples of the .wav file and write them again as .ogg.
        samples, rate = soundfile.read(wav_path)
        # The OGG encoder crashes on very short sounds (like the typing click),
        # so a sound shorter than 0.1 s gets some silence (zeros) at the end.
        shortest = rate // 10
        if len(samples) < shortest:
            samples = numpy.concatenate([samples, numpy.zeros(shortest - len(samples))])
        soundfile.write(ogg_path, samples, rate, format="OGG", subtype="VORBIS")
        print("made " + ogg_path)
