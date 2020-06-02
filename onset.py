import argparse
import os
import sys
import librosa
import mido
import json
import numpy as np
from scipy import stats
import time

from madmom.audio.filters import LogarithmicFilterbank
from madmom.features.onsets import SpectralOnsetProcessor
from madmom.audio.signal import normalize
from scipy import signal

class Note:
    def __init__(self, frame, frame_pitch, onset_time, offset_time):
        self.frame_pitch = frame_pitch
        self.frame = frame
        self.onset_time = onset_time
        self.offset_time = offset_time
        self.pitch = 0

def get_onset(wav_path):
    y, sr = librosa.core.load(wav_path, sr= None)
    sos = signal.butter(25, 100, btype= 'highpass', fs= sr, output='sos')
    wav_data= signal.sosfilt(sos, y)
    wav_data= normalize(wav_data)

    sodf = SpectralOnsetProcessor(onset_method='complex_flux', fps= 50, filterbank=LogarithmicFilterbank, fmin= 100, num_bands= 24, norm= True)
    from madmom.audio.signal import Signal
    onset_strength= (sodf(Signal(data= wav_data, sample_rate= sr)))
    onset_strength= librosa.util.normalize(onset_strength)
    h_length= int(librosa.time_to_samples(1./50, sr=sr))

    onset_times= librosa.onset.onset_detect(onset_envelope= onset_strength,
                                      sr=sr,
                                      hop_length= h_length,
                                      units='time', pre_max= 5, post_max= 5, 
                                      pre_avg= 5, post_avg= 5)
    f = open(onset_path, 'w')
    for x in onset_times:
        f.write(f"{x}\n")
    return onset_times


def main(wav_path, ep_path, output_path):
    ep_frames = json.load(open(ep_path))
    onset_times = get_onset(wav_path)

if __name__ == '__main__':
    for i in range(1, 1501):
        wav_path= f"../test/{i}/{i}.wav"
        if not os.path.isfile(wav_path):
            continue
        print(i)
        ep_path= f"../test/{i}/{i}_vocal.json"
        output_path= f"../test/{i}/test.txt"
        onset_path= f"../test/{i}/onset.txt"
        main(wav_path=wav_path, ep_path=ep_path, output_path=output_path)
