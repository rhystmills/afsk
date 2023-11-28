import time
from scipy.io import wavfile 
import bitarray
import numpy as np
import pyaudio
import functools 


p = pyaudio.PyAudio()

testString = "av a washi"
volume = 0.01  # range [0.0, 1.0]
fs = 44100  # sampling rate, Hz, must be integer
duration = 0.1  # in seconds, may be float
f = 300.0  # sine frequency, Hz, may be float

notes = [300,600,900,1200,1500,1800,2100,2400,2700,3000]

def freqToNote(freq: int):
    return (np.sin(
        2 * np.pi * np.arange(fs * duration) * freq / fs, 
    )).astype(np.float32)

# def concat(a: np.ndarray[np.float32] ,b: np.ndarray[np.float32]):
#     functools.reduce(lambda a,b: np.concatenate((a,b)), freqs_as_notes) 

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


freqs_as_notes = map(lambda a: (volume * freqToNote(a)), notes)
# freqs_as_notes_reversed = map(lambda a: (volume * freqToNote(a)), reversed(notes))

notes = functools.reduce(lambda a,b: np.concatenate((a,b)), freqs_as_notes)
# notes_reversed = functools.reduce(lambda a,b: np.concatenate((a,b)), freqs_as_notes_reversed)

# concat = np.concatenate((notes, notes_reversed, notes, notes_reversed))
# generate samples, note conversion to float32 array
# output_bytes = functools.reduce(lambda a,b: a+b, freqs_as_notes)
# output_bytes_reversed = functools.reduce(lambda a,b: a+b, freqs_as_notes_reversed)

# all_bytes = output_bytes + output_bytes_reversed + output_bytes + output_bytes_reversed

# per @yahweh comment explicitly convert to bytes sequence
# output_bytes = (volume * samples).tobytes() + (volume * sample2).tobytes()

# for paFloat32 sample values must be in range [-1.0, 1.0]
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=fs,
                output=True)

# play. May repeat with different volume values (if done interactively)
# start_time = time.time()
# stream.write(all_bytes)
# print("Played sound for {:.2f} seconds".format(time.time() - start_time))
# stream.stop_stream()
# stream.close()

our_notes = stringToNotes(testString)
print(notes)
print(our_notes)
wavfile.write('abc1.wav', fs, our_notes)



p.terminate()