import time

import numpy as np
import pyaudio
import functools 

p = pyaudio.PyAudio()

volume = 0.5  # range [0.0, 1.0]
fs = 44100  # sampling rate, Hz, must be integer
duration = 0.1  # in seconds, may be float
f = 300.0  # sine frequency, Hz, may be float

notes = [300,600,900,1200,1500,1800,2100,2400,2700,3000]

def freqToNote(freq: int):
    return (np.sin(
        2 * np.pi * np.arange(fs * duration) * freq / fs, 
    )).astype(np.float32)

freqs_as_notes = map(lambda a: (volume * freqToNote(a)).tobytes(), notes)

# generate samples, note conversion to float32 array
output_bytes = functools.reduce(lambda a,b: a+b, freqs_as_notes)

print(output_bytes)

# per @yahweh comment explicitly convert to bytes sequence
# output_bytes = (volume * samples).tobytes() + (volume * sample2).tobytes()

# for paFloat32 sample values must be in range [-1.0, 1.0]
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=fs,
                output=True)

# play. May repeat with different volume values (if done interactively)
start_time = time.time()
stream.write(output_bytes + output_bytes)
print("Played sound for {:.2f} seconds".format(time.time() - start_time))

stream.stop_stream()
stream.close()

p.terminate()