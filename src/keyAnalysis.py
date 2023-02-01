### CORRELATE AUDIO WITH A MAJOR OR MINOR KEY ###
#################################################
import numpy as np
from src.timeFreqAnalysis import tf_analysis
import src.fileHandler as file

def init():
    global samplerate
    global data
    samplerate = file.samplerate_
    data = file.data_

### GENERATE FREQUENCY BANDS (C2 -> B4) ### 
key_bands = np.zeros(38, dtype=int) # note frequencies
band_adj = np.zeros(38, dtype=int) # correction value for separation
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
        key_magnitudes[i] = np.linalg.norm(tf_data[i] + tf_data[i+12] + tf_data[i+24]) # combine data across three octaves

    for idx in range(24): # cycle through keys to generate correlation values
        shift_idx = 12 - idx // 2
        if idx % 2 == 0:
            weight = bb_major[shift_idx:] + bb_major[:shift_idx]
        else:
            weight = bb_minor[shift_idx:] + bb_minor[:shift_idx]
        corr_res.append(np.linalg.norm(np.corrcoef(key_magnitudes, weight)))
    corr_res = np.array(corr_res)

    best_key = mode_table[np.argmax(corr_res)] # pull out the best correlated key

    return best_key
