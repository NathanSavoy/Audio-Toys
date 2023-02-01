### GENERATE TIME-FREQUENCY ANALYSIS OF AUDIO ###
#################################################
import numpy as np
from scipy.fftpack import fft, ifft
from src.utilities import gaussian
import src.fileHandler as file
from importlib import reload

def init():
    global samplerate
    global data
    samplerate = file.samplerate_
    data = file.data_

# Gaussian Windowed Fourier Transform 
def g_wft(samplerate, amp_data, t):
    x = np.arange(-0.5, 0.5, 1/samplerate) # define one-second Gaussian window
    window = gaussian(x, 0, 0.5)

    int_l = int(t*samplerate)-samplerate//2 # define lower and upper bounds of interval centered at t
    int_u = int(t*samplerate)+samplerate//2

    if (int_u-int_l == samplerate):
        interval = window*amp_data[int_l:int_u,0] # apply gaussian window (ONLY TO LEFT STREAM A.T.M.)
        freq_data = fft(interval) 

    return(freq_data) # return fft data

# separate frequency data into the given bands, returning an array of frequency data AND the separated amplitude data 
def extract_bands(freq_data, bands): # takes frequency spectrum and list of frequency separation values
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
    
    for i in range(len(bands)-2): # perform ifft
        band_amp[i] = ifft(band_data[i])
                
    return(band_data, band_amp)

# generate time-frequency plot of input data:
# steps through amplitude data, separating by frequency bands at each step
def tf_analysis(samplerate, data, bands=[0,200,1200,2400,8000]):
    tf_data = []
    for i in range(len(bands)-2):  # intialize resultant array
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
