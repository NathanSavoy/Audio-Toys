### BASIC FUNCTIONS AND LIBRARIES ###
from scipy.io import wavfile
from scipy.fftpack import fft, ifft
import numpy as np
import matplotlib.pyplot as plt

# turn off plot axes
#plt.axis('off')

# import data #
def import_audio(path):
    global samplerate
    global data
    samplerate, data = wavfile.read(path)


# conversion from frequency to note ('tuning' (optional) specifies frequency of A4)
def freq_to_note(freq, tuning=440):
    notes = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']

    note_number = 12 * np.log2(freq / tuning) + 49 
    note_number = round(note_number)
        
    note = int((note_number - 1 ) % len(notes))
    note = notes[note]
    
    octave = (note_number + 8 ) // len(notes)
    
    return note, octave

# generate a Gaussian distribution
def gaussian(x, mean, sd):
    return (1/(sd*np.sqrt(2*np.pi)))*np.exp(-0.5*(((x-mean)/sd)**2))

# generate amplitude plot of signal 
def plot_amp():
    x = np.arange(0, len(data))
    y_l = abs(data[:,0])
    y_r = -abs(data[:,1])
    #x_ticks = range(0, len(data), 4*samplerate)
    plt.axis('off')
    plt.clf()
    plt.plot(x, y_l)
    plt.plot(x, y_r)
    plt.savefig("media/amplitude_plot.jpg", dpi=350)

    return True

### TIME FREQUENCY ANALYSIS ###
# Gaussian Windowed Fourier Transform 
def g_wft(samplerate, amp_data, t):
    x = np.arange(-0.5, 0.5, 1/samplerate) # define one-second Gaussian window
    window = gaussian(x, 0, 0.5)

    int_l = int(t*samplerate)-samplerate//2 # define lower and upper bounds of interval centered at t
    int_u = int(t*samplerate)+samplerate//2

    if (int_u-int_l == samplerate):
        interval = window*amp_data[int_l:int_u,0] # apply gaussian window (ONLY TO LEFT STREAM A.T.M.)
        freq_data = fft(interval) 

    return(freq_data)

# separate frequency band data and return as amplitude data
def extract_bands(freq_data, bands): # takes frequency spectrum and 4 element list of frequencies bands [0,200,1200,2400]
    band_data = []
    band_amp = []
    for i in range(len(bands)-2):
        band_data.append(np.zeros(len(freq_data)))
        band_amp.append(np.zeros(len(freq_data)))
    band_data = np.array(band_data)
    band_amp = np.array(band_amp)

    for i in range(len(bands)-2): # populate rows of band_data with appropriate frequency data
        band_data[i,bands[i]:bands[i+2]] = freq_data[bands[i]:bands[i+2]]   
        band_data[i,-bands[i+2]:-bands[i]] = freq_data[-bands[i+2]:-bands[i]]
    
    for i in range(len(bands)-2): ## replace with libary or at least reference number of rows of band_data
        band_amp[i] = ifft(band_data[i])
                
    return(band_data, band_amp)

# generate time-frequency plot of input data
def tf_analysis(samplerate, data, bands=[0,200,1200,2400,8000]):
    tf_data = []
    for i in range(len(bands)-2):  
        tf_data.append(np.zeros(len(data)))
    tf_data = np.array(tf_data)

    freq_a = g_wft(samplerate, data, 0.5) # initialize frequency intervals (0th time interval)
    freq_b = g_wft(samplerate, data, 1)

    for i in range(1, 2*(len(data)//samplerate)-2): # index from 1 through length of audio, 1/2 seconds per step
        t = i/2 + 1 # shift and rescale timestep

        amp_a = extract_bands(freq_a, bands)[1] # frequency-separated amplitude data for each timestep (np.array)
        amp_b = extract_bands(freq_b, bands)[1]
        # add the average of the overlapping region of the two timesteps to tf_data
        tf_data[:,int((t-1)*samplerate):int((t-0.5)*samplerate)] = 0.5*amp_a[:,amp_a.shape[1]//2:] + 0.5*amp_b[:,:amp_b.shape[1]//2] 

        freq_a = freq_b #  shift the windows to next half-second interval
        freq_b = g_wft(samplerate, data, t)

    return(tf_data)


# generate plot #
def plot_tf(colors=['cornflowerblue','green','white']):
    plt_data = tf_analysis(samplerate, data)
    plt.axis('off')
    plt.clf()
    plt.plot(0.75*plt_data[1], alpha = 0.7, color = colors[1], label="Mid") # mids
    plt.plot(plt_data[0], alpha = 0.7, color = colors[0], label="Low") # lows
    plt.plot(plt_data[2], alpha = 0.7, color = colors[2], label="High") # highs
    plt.legend(loc="upper right")
    plt.title("Time-Frequency Plot")
    plt.savefig("media/tf_plot.jpg", dpi=350)
    return True

# find tempo #
def find_tempo():
    data_ = data[30*samplerate:55*samplerate,0]
    t = np.linspace(0, len(data_), len(data_))
    amplitude = np.max(data_)
    errs = np.array([])

    for i in range(55, 200): # check tempos between 40 and 200
        fit_ = np.abs(amplitude*np.cos(np.pi*(i/60)*(t/samplerate)))
        err = ((np.abs(data_) - fit_)**2).mean()
        errs = np.append(errs, err)
    
    tempo = 55 + np.argmax(errs)
    return(tempo)

# key determination #
### FREQUENCY BANDS (C2 -> B4) ### 
key_bands = np.zeros(38, dtype=int)
band_adj = np.zeros(38, dtype=int)
for i in range(15,53):
    key_bands[i-15] = 440*2**((i-49)/12)
    band_adj[i-15] = 18*(i-15)/38 + 2

# Bellman-Budge key weights
bb_major = [16.8, 0.86, 12.95, 1.41, 13.49, 11.93, 1.25, 20.28, 1.8, 8.04, 0.62, 10.57]
bb_minor = [18.16, 0.69, 12.99, 13.34, 1.07, 11.15, 1.38, 21.07, 7.49, 1.53, 0.92, 10.21]

# table of keys for output
mode_table = [
    "C Major", "C Minor", "C# Major", "C# Minor", "D Major", "D Minor", "D# Major", "D# Minor", "E Major",
    "E Minor", "F Major", "F Minor", "F# Major", "F# Minor", "G Major", "G Minor", "G# Major", "G# Minor",
    "A Major", "A Minor", "A# Major", "A# Minor", "B Major", "B Minor"
]

# find key 
def determine_key():
    key_magnitudes = np.zeros(12)
    tf_data = tf_analysis(samplerate, data, key_bands)
    corr_res = [] # correlation result

    for i in range(12): 
        key_magnitudes[i] = np.linalg.norm(tf_data[i] + tf_data[i+12] + tf_data[i+24])

    for idx in range(24):
        shift_idx = 12 - idx // 2
        if idx % 2 == 0:
            weight = bb_major[shift_idx:] + bb_major[:shift_idx]
        else:
            weight = bb_minor[shift_idx:] + bb_minor[:shift_idx]
        corr_res.append(np.linalg.norm(np.corrcoef(key_magnitudes, weight)))
    corr_res = np.array(corr_res)

    best_key = mode_table[np.argmax(corr_res)]

    return best_key
    
def find_loudness(): # computes average relative volume of song in decibels
    loudness = 10*np.log10(np.linalg.norm(data) / np.linalg.norm(np.ones(len(data), dtype=data.dtype)*np.iinfo(data.dtype).max))
    return(round(loudness,2))