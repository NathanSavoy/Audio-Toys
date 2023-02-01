### FILE IMPORT AND HANDLING ###
################################
import numpy as np
from scipy.io import wavfile

# import data #
def importAudio(path):
        global samplerate_
        global data_
        if path != "":
                samplerate_, data_ = wavfile.read(path)
        return True
importAudio("") 
