from functools import reduce
import math
import os
from threading import Timer
import time
from scipy.io import wavfile 
import pyaudio
import numpy as np
import wave
import matplotlib.pyplot as plt
from scipy import signal
import pylab


#AUDIO INPUT
FORMAT = pyaudio.paFloat32
CHANNELS = 1
RATE = 44100
CHUNK = 2048
RECORD_SECONDS = 30
WAVE_OUTPUT_FILENAME = "output.wav"
LOWCUT = 200.0
HIGHCUT = 4050.0

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



# Close the stream (5)

audio.terminate()

def butter_bandpass(lowcut, highcut, fs, order=5):
    return signal.butter(order, [lowcut, highcut], fs=fs, btype='band')

def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = signal.lfilter(b, a, data)
    return y

bandpass_filtered = butter_bandpass_filter(all_data, LOWCUT, HIGHCUT, RATE, order=6)
trimmed_file = bandpass_filtered[np.absolute(bandpass_filtered) > 50]


def plot_signal_freq(floats):
    # np.fft.fftfreq(1, floats)
    # signal_span = np.r_[0: 2*np.pi: np.pi/4]
    # signal_in = np.sin(signal_span)
    # f, t, Sxx = signal.spectrogram(floats, RATE)
    a = 0.02
    T = 0.05
    f0 = 300.0
    # y = butter_bandpass_filter(floats, LOWCUT, HIGHCUT, RATE, order=6)
    # plt.plot(t, y, label='Filtered signal (%g Hz)' % f0)
    # plt.xlabel('time (seconds)')
    # plt.hlines([-a, a], 0, T, linestyles='--')
    # plt.grid(True)
    # plt.axis('tight')
    # plt.legend(loc='upper left')
    f, t, Sxx = signal.spectrogram(floats, RATE)
    off_bucket = 16
    on_bucket = 10
    mean_off = sum(Sxx[off_bucket])/len(Sxx[off_bucket])
    mean_on = sum(Sxx[on_bucket])/len(Sxx[on_bucket])
    current = -1
    count = 0
    for i in range(0,len(Sxx[off_bucket])):
        if Sxx[off_bucket][i] > mean_off:
            if current == 0:
                count += 1
            else:
                for j in range(0,math.ceil(count/50)):
                    print("1", end="")
                current = 0
                count = 1
        elif Sxx[on_bucket][i] > mean_on:
            if current == 1:
                count += 1
            else:
                for j in range(0,math.ceil(count/50)):
                    print("0", end="")
                current = 1
                count = 1
        else:
            if current == -1:
                count += 1
            else:
                # print(f"{current} x {count}")
                # current = -1
                # count = 1
                pass
    print("")
    plt.pcolormesh(t, f, Sxx, shading='gouraud')
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')
    plt.ylim((0, HIGHCUT))
    plt.show()
    # 

plot_signal_freq(np.frombuffer(all_data, dtype=np.float32))
# wavfile.write(WAVE_OUTPUT_FILENAME, RATE, np.frombuffer(bandpass_filtered, dtype=np.float32))

