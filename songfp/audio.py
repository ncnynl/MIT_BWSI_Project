import librosa
import matplotlib.mlab as mlab
import pyaudio
from microphone import record_audio
from microphone import play_audio
import numpy as np
from random import randint

import matplotlib.pyplot as plt

def sample(song_path):
    samples, fs = librosa.load(song_path, sr=44100, mono=True)
    #audio file to sample data r"C:\Users\Julie\Desktop\some_song.mp3" song_path is a string that indicates path to audio file
    # clip = clipSong(samples, 10, 44100)
    if samples.max() <= 1:
        samples = samples * 2**15

    S, freqs, times= mlab.specgram(samples, NFFT=4096, Fs=44100, window=mlab.window_hanning, noverlap=(4096 // 2))
            #S is 2D array of Ck values. Frequency (row), time(col)
            #freqs[i] returns frequency that axis-0 bin i corresponds to. Same for times
    ft = zip(freqs, times)
    return [freqs, times, S]


def mic(time):
    byte_encoded_signal, sampling_rate = record_audio(time)
    fs= 44100

    sample = np.hstack(np.fromstring(np.array(byte_encoded_signal), dtype = np.int16))
    S, freqs, times= mlab.specgram(sample, NFFT=4096, Fs=44100, window=mlab.window_hanning, noverlap=(4096 // 2))

    return [freqs, times, S]


def clipSong(song, time, rate):
    length = time*rate
    start = randint(0, len(song)-length)
    return song[start:start + length]
