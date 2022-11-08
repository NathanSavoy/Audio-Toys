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
    band_data = np.array([np.zeros(len(freq_data)), np.zeros(len(freq_data)), np.zeros(len(freq_data))]) # update these to adapt to len(bands)
    band_amp = np.array([np.zeros(len(freq_data)), np.zeros(len(freq_data)), np.zeros(len(freq_data))])

    for i in range(len(bands)-1): # might need to change for his, depending on typical energy in this band
        band_data[i,bands[i]:bands[i+1]] = freq_data[bands[i]:bands[i+1]]   
        band_data[i,-bands[i+1]:-bands[i]] = freq_data[-bands[i+1]:-bands[i]]
    
    for i in range(len(bands)-1): ## convert to explicit definition (remove loop)
        band_amp[i] = ifft(band_data[i])
                
    return(band_amp)

# generate time-frequency plot of input data
def tf_analysis(samplerate, data, bands=[0,200,1200,2400]):
    tf_data = np.array([np.zeros(len(data)),np.zeros(len(data)),np.zeros(len(data))])
    freq_a = g_wft(samplerate, data, 0.5) # initialize frequency intervals (0th step)
    freq_b = g_wft(samplerate, data, 1)

    for i in range(1, 2*(len(data)//samplerate)-2): # index from 1 through length of audio GO BY SECONDS NOT SAMPLES MY GUY
        t = i/2 + 1 # shift and rescale timestep

        amp_a = extract_bands(freq_a, bands) # frequency-separated amplitude data for each timestep (np.array)
        amp_b = extract_bands(freq_b, bands)
        # add the average of the overlapping region of the two timesteps to tf_data
        tf_data[:,int((t-1)*samplerate):int((t-0.5)*samplerate)] = 0.5*amp_a[:,amp_a.shape[1]//2:] + 0.5*amp_b[:,:amp_b.shape[1]//2] 

        freq_a = freq_b #  shift the windows to next half-second interval
        freq_b = g_wft(samplerate, data, t)

    return(tf_data)

# generate plot
def plot_tf(colors=['b','y','r']):
    plt_data = tf_analysis(samplerate, data)
    plt.axis('off')
    plt.clf()
    plt.plot(0.75*plt_data[1], alpha = 0.7, color = colors[1], label="Mid") # mids
    plt.plot(plt_data[2], alpha = 0.7, color = colors[2], label="High") # highs
    plt.plot(plt_data[0], alpha = 0.7, color = colors[0], label="Low") # lows
    plt.legend(loc="upper right")
    plt.title("Time-Frequency Plot")
    plt.savefig("media/tf_plot.jpg", dpi=350)
    return True

