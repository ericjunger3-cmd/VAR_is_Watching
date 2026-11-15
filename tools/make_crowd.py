# Makes the crowd sounds of the game from a real stadium recording:
#   sounds/crowd.wav - the crowd on the pitch (repeats without a bump)
#   sounds/goal.wav  - the cheer when a goal is scored
#
# The recording: "Arrowhead Stadium crowd noise" by Kj1595,
# https://commons.wikimedia.org/wiki/File:Arrowhead_Stadium_crowd_noise.wav
# License: CC BY-SA 4.0 (https://creativecommons.org/licenses/by-sa/4.0/).
# Our two sounds are changed versions of it (shorter, softer, looped), so
# they have the same license. The original is in tools/recordings/.
#
# This is a tool, not part of the game. It needs the soundfile package
# (numpy comes with it):  py -m pip install soundfile
# Run it from the game folder:  py tools/make_crowd.py
# Afterwards run py tools/make_ogg.py for the web version.

import numpy
import soundfile

RATE = 22050    # the same rate as all other sounds of the game


def soften(samples, amount):
    # Take away the sharp, shrill part of the sound (a simple low-pass
    # filter): every sample moves only part of the way to the new value.
    # The recording is very loud and a little distorted; this makes it warmer.
    result = numpy.zeros(len(samples))
    last = 0.0
    for i in range(len(samples)):
        last = last * amount + samples[i] * (1 - amount)
        result[i] = last
    return result


def part(samples, start_seconds, end_seconds):
    # The samples between two moments of the recording.
    return samples[int(start_seconds * RATE):int(end_seconds * RATE)]


def make_loop(samples, overlap_seconds):
    # Let the end fade into the start, so the sound can repeat forever
    # without a bump: the last part is mixed into the first part.
    count = int(overlap_seconds * RATE)
    body = samples[:len(samples) - count].copy()
    tail = samples[len(samples) - count:]
    for i in range(count):
        level = i / count
        body[i] = body[i] * level + tail[i] * (1 - level)
    return body


def loudest_at(samples, loudest):
    # Make the loudest point exactly "loudest" (so nothing crackles).
    return samples * (loudest / numpy.abs(samples).max())


# Read the recording (44100 samples per second) and make it 22050:
# every two samples become their average.
recording, rate = soundfile.read("tools/recordings/arrowhead_stadium_crowd_noise.wav")
pairs = len(recording) // 2
recording = (recording[0:pairs * 2:2] + recording[1:pairs * 2:2]) / 2
recording = soften(recording, 0.3)

# The crowd: the first 9 seconds are evenly loud (later it gets quieter).
crowd = make_loop(part(recording, 0.5, 9.5), 1.5)
soundfile.write("sounds/crowd.wav", loudest_at(crowd, 0.6), RATE, subtype="PCM_16")
print("made sounds/crowd.wav")

# The goal: 3.5 seconds of the crowd that get louder at once (everybody
# jumps up) and then slowly calm down, with a soft end.
goal = part(recording, 5.0, 8.5)
for i in range(len(goal)):
    t = i / RATE
    rise = min(1.0, t / 0.25)
    calm = numpy.exp(-max(0.0, t - 1.2) * 0.9)
    goal[i] = goal[i] * (0.35 + 0.65 * rise) * calm
fade_count = int(0.4 * RATE)
for i in range(fade_count):
    goal[len(goal) - fade_count + i] = goal[len(goal) - fade_count + i] * (1 - i / fade_count)
soundfile.write("sounds/goal.wav", loudest_at(goal, 0.7), RATE, subtype="PCM_16")
print("made sounds/goal.wav")
