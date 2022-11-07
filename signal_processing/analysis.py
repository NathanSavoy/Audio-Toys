### DEFINE FUNCTIONS AND IMPORT LIBRARIES ###
from scipy.io import wavfile
from scipy.fftpack import fft, ifft
import numpy as np
import matplotlib.pyplot as plt

# import data #
def import_audio(path):
    global samplerate
    global data
    samplerate, data = wavfile.read(path)

# function for converting from frequency to note ('tuning' (optional) specifies frequency of A4)
def freq_to_note(freq, tuning=440):
    notes = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']

    note_number = 12 * np.log2(freq / tuning) + 49 
    note_number = round(note_number)
        
    note = int((note_number - 1 ) % len(notes))
    note = notes[note]
    
    octave = (note_number + 8 ) // len(notes)
    
    return note, octave

def plot_audio():
    x = np.arange(0, len(data))
    y_l = abs(data[:,0])
    y_r = -abs(data[:,1])
    #x_ticks = range(0, len(data), 4*samplerate)
    plt.clf()
    plt.plot(x, y_l)
    plt.plot(x, y_r)
    plt.savefig("media/amplitude_plot.jpg", dpi=350)

    return True

def plot_analysis():
    # specify frequency bands
    lo_cut = 200
    mid_cut = 1200
    hi_cut = 24000

    # extract a portion of the audio
    sig_i = sig_in[65*samplerate:85*samplerate,0]
    N = len(sig_i)
