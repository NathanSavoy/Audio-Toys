from tkinter import *
import tkinter.messagebox as mb
from tkinter import filedialog as fd
from PIL import ImageTk,Image
import signal_processing.analysis as sp


### INITIALIZATION ###
###
root = Tk()
root.geometry('800x400')
root.title('Audio ToyBox')
#filename = StringVar()
#filename.set("No File Selected")
img = ""

### FUNCTIONS ###
###
def import_audio():
    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=[('Wave Files', '*.wav')]
        )
#    filename.set(filename_)
    sp.import_audio(str(filename))
    print("Analyzing Audio...")
    if (sp.plot_audio()):
        print("Updating Image...")
        update_image()

def update_image():
    label.configure(image='')
    label.image=None
    img_ = Image.open("Python Audio Processing/AudioToyBox/media/amplitude_plot.jpg")
    img = ImageTk.PhotoImage(img_.resize((700, 150)))
    label.configure(image=img)
    label.image=img



### GUI ELEMENTS ###
###
# button
import_btn = Button(
    root, 
    text="Import Audio", 
    width=10, 
    height=2, 
    command=import_audio
)
import_btn.place(x=400, y=200)
import_btn.pack(padx=30,pady=30)

# label
#lab = Label(root, bd=20, textvariable=filename, width=20, height=2)
#lab.place(x=400, y=200)

# image frame
frame = Frame(root, width=700, height=150, background='white')
frame.pack_propagate(0)    
frame.pack(padx=30, pady=30)
label = Label(frame, image='')
label.pack()

root.mainloop()
