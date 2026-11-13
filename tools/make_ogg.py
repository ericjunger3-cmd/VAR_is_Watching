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

# The OGG encoder crashes if it gets a long sound in one piece (like the
# 48 s title music), so we give it the samples in small blocks.
BLOCK = 4096

for name in sorted(os.listdir("sounds")):
    if name.endswith(".wav"):
        wav_path = "sounds/" + name
        ogg_path = "sounds/" + name[:-4] + ".ogg"
        # Read the samples of the .wav file.
        samples, rate = soundfile.read(wav_path)
        # The encoder also has trouble with very short sounds (like the typing
        # click), so a sound shorter than 0.1 s gets some silence at the end.
        shortest = rate // 10
        if len(samples) < shortest:
            samples = numpy.concatenate([samples, numpy.zeros(shortest - len(samples))])
        # Write them again as .ogg, one block after the other.
        with soundfile.SoundFile(ogg_path, "w", rate, 1, format="OGG", subtype="VORBIS") as ogg:
            for start in range(0, len(samples), BLOCK):
                ogg.write(samples[start:start + BLOCK])
        print("made " + ogg_path)
