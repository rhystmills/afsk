import time
from scipy.io import wavfile 
import bitarray
import numpy as np
import pyaudio
import functools 


p = pyaudio.PyAudio()

play = False
testString = "some text"
volume = 0.01  # range [0.0, 1.0]
fs = 44100  # sampling rate, Hz, must be integer
signal_length = 0.05  # in seconds, may be float
f = 300.0  # sine frequency, Hz, may be float
on_freq=500 # these are picked to be within supported telephone frequencies(300Hz - 3400Hz) but distinct
off_freq = 2700


def freqToNote(freq: int):
    return (np.sin(
        2 * np.pi * np.arange(fs * signal_length) * freq / fs, 
    )).astype(np.float32)

def stringToInts(string: str):
    ba = bitarray.bitarray()
    ba.frombytes(string.encode('utf-8'))
    l = ba.tolist()
    notes: list[int] = []
    for i in range(0, len(l)):
        notes.append(500 if l[i] else 2700)
    return notes  

def intsToNotes(ints: list[int]):
    freqs_as_notes = map(lambda a: (volume * freqToNote(a)), ints)
    return functools.reduce(lambda a,b: np.concatenate((a,b)), freqs_as_notes)

def stringToNotes(str: str):
    return intsToNotes(stringToInts(str))

our_notes = stringToNotes(testString)

if (play):
    output_bytes = our_notes.tobytes()
    stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=fs,
                output=True)
    start_time = time.time()
    stream.write(output_bytes)
    print("Played sound for {:.2f} seconds".format(time.time() - start_time))
    stream.stop_stream()
    stream.close()

wavfile.write('pookmo.wav', fs, our_notes)



p.terminate()