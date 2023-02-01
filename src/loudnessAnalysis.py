### DETERMINE LOUDNESS OF AUDIO ###
###################################
import numpy as np
import src.fileHandler as file

def init():
    global data
    data = file.data_

def find_loudness(): # computes average relative volume of song in decibels
    loudness = 10*np.log10(np.linalg.norm(data) / np.linalg.norm(np.ones(len(data), dtype=data.dtype)*np.iinfo(data.dtype).max))
    return(round(loudness,2))
