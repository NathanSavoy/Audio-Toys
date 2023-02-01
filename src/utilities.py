### GENERALLY USEFUL FUNCTIONS ###
##################################
import numpy as np

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
