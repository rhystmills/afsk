import os
from threading import Timer
import time
from scipy.io import wavfile 
import pyaudio
import numpy as np
import wave

#AUDIO INPUT
FORMAT = pyaudio.paFloat32
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 2
WAVE_OUTPUT_FILENAME = "output.wav"

audio = pyaudio.PyAudio()

all_data = bytearray()

# start Recording
# stream = audio.open(format=FORMAT, channels=CHANNELS,
#                 rate=RATE, input=True,
#                 frames_per_buffer=CHUNK)

def callback(input_data, frame_count, time_info, flags):
    os.system('cls' if os.name == 'nt' else 'clear')
    if input_data and isinstance(input_data, bytes) :
        # print(input_data)
        all_data.extend(bytearray(input_data))
    return input_data, pyaudio.paContinue


stream = audio.open(format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    stream_callback=callback,
    frames_per_buffer=CHUNK)

r = Timer(RECORD_SECONDS, stream.close)
time.sleep(RECORD_SECONDS)

wavfile.write('testo.wav', RATE, np.frombuffer(all_data, dtype=np.float32))

# Close the stream (5)

audio.terminate()
