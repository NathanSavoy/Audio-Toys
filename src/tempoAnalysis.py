### ASCRIBE TEMPO TO AUDIO ###
##############################
import numpy as np
import src.fileHandler as file
from importlib import reload

def init():
    global samplerate
    global data
    samplerate = file.samplerate_
    data = file.data_

# find tempo #
def find_tempo():
    data_ = data[30*samplerate:55*samplerate,0] # extract section of audio
    t = np.linspace(0, len(data_), len(data_))
    amplitude = np.max(data_)
    errs = np.array([])

    for i in range(55, 200): # check tempos between 55 and 200
        fit_ = np.abs(amplitude*np.cos(np.pi*(i/60)*(t/samplerate))) # generate abs(sin(t)) for each tempo
        err = ((np.abs(data_) - fit_)**2).mean() # check how the curve fits (RMS error)
        errs = np.append(errs, err)
    
    tempo = 55 + np.argmax(errs) # return the best fitting tempo 
    return(tempo)
