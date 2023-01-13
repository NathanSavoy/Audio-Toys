from tkinter import *
import tkinter.messagebox as mb
from tkinter import filedialog as fd
from PIL import ImageTk,Image
import signal_processing.analysis as sp


### INITIALIZATION ###
###
root = Tk()
root.geometry('800x450')
root.title('Audio ToyBox')
root.config(bg='gray21')
filename = StringVar()
filename.set("No File Selected")
bpm = StringVar()
bpm.set("")
key = StringVar()
key.set("")
norm = StringVar()
norm.set("")


### FUNCTIONS ###
###
def import_audio():
    filename_ = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=[('Wave Files', '*.wav')]
        )
    filename.set(filename_)
    sp.import_audio(str(filename_))
    print("Importing Audio...")
    if (sp.plot_amp()):
        print("Plotting Amplitude...")
        update_image(amp_cont, "media/amp_plot.png")

def update_image(cont, file):
    global amp_img
    global tf_img
    if (file == "media/amp_plot.png"):
        amp_img = ImageTk.PhotoImage(Image.open(str(file)).resize((int(1.25*lower_frame.winfo_width()), int(lower_frame.winfo_height()/2))))
        lower_frame.itemconfig(cont,image=amp_img)
    elif (file == "media/tf_plot.png"):
        tf_img = ImageTk.PhotoImage(Image.open(str(file)).resize((int(1.25*lower_frame.winfo_width()), int(lower_frame.winfo_height()/2))))
        lower_frame.itemconfig(cont, image=tf_img)
    else: 
        print("Error in update_image: Canvas not found")

def analyze_audio():
    print("Analyzing Audio...")
    if (sp.plot_tf()):
        print("Plotting Time-Frequency Analysis...")
        update_image(tf_cont, "media/tf_plot.png")
    print("Finding Key...")
    key.set(sp.determine_key())
    print("Finding Tempo...")
    bpm.set(sp.find_tempo())
    norm.set(str(sp.find_loudness()) + " dB")

def do_zoom(event):
    x = lower_frame.canvasx(event.x)
    y = lower_frame.canvasy(event.y)
    factor = 1.001 ** event.delta
    lower_frame.scale(ALL, x, y, factor, 1.0)

### GUI ELEMENTS ###
###
## FRAMES ##
upper_frame = Frame(root, width=780, height=110, bg="gray64")
upper_frame.pack(fill="both", expand=True, padx=10, pady=10)

lower_frame = Canvas(root, width=780, height=300, bg="gray64")
lower_frame.pack(fill="x", expand=False, padx=10, pady=10)

# upper frame elements 
## sub-frames 
# rows
uf_row0 = Frame(upper_frame, width=660, height=20, bg="gray64")
uf_row0.pack(fill="x", expand=True, padx=4, pady=0)
uf_row1 = Frame(upper_frame, width=660, height=20, bg="gray64")
uf_row1.pack(fill="x", expand=True, padx=4, pady=0)
uf_row2 = Frame(upper_frame, width=660, height=40, bg="gray64")
uf_row2.pack(fill="x", expand=True, padx=4, pady=5)

#lf_row0 = Canvas(lower_frame, width=700, height=90, bg="gray64")
#lf_row0.pack(fill="x", expand=True, padx=0, pady=5)
#lf_row1 = Canvas(lower_frame, width=700, height=90, bg="red")
#lf_row1.pack(fill="x", expand=True, padx=0, pady=5)

# columns
uf_row1_c0 = Frame(uf_row1, bg="gray64")
uf_row1_c0.place(relx=.5, rely=.5,anchor= CENTER)

uf_row2_c0 = Frame(uf_row2, bg="gray64")
uf_row2_c0.place(relx=.5, rely=.5,anchor= CENTER)

## widgets 
title = Label(uf_row0, bd=0, textvariable=filename, width=50, height=1, bg="gray64")
title.pack(fill="both", expand=True)

bpm_lab = Label(uf_row1_c0, bd=0, text="BPM:", bg="gray64")
bpm_lab.grid(row=0, column=0, padx=10, pady=0)
bpm_val = Label(uf_row1_c0, bd=0, textvariable=bpm, width=5, height=1, bg="gray64")
bpm_val.grid(row=0, column=1, padx=10, pady=0)

key_lab = Label(uf_row1_c0, bd=0, text="Key:", bg="gray64")
key_lab.grid(row=0, column=2, padx=10, pady=0)
key_val = Label(uf_row1_c0, bd=0, textvariable=key, width=10, height=1, bg="gray64")
key_val.grid(row=0, column=3, padx=10, pady=0)

norm_lab = Label(uf_row1_c0, bd=0, text="Loudness:", bg="gray64")
norm_lab.grid(row=0, column=4, padx=10, pady=0)
norm_val = Label(uf_row1_c0, bd=0, textvariable=norm, width=7, height=1, bg="gray64")
norm_val.grid(row=0, column=5, padx=10, pady=0)

import_btn = Button(uf_row2_c0, text="Import New", width=10, height=1, command=import_audio, bg="red3")
import_btn.grid(row=0, column=0, padx=10, pady=5)

analyze_btn = Button(uf_row2_c0, text="Analyze Audio", width=15, height=1, command=analyze_audio, bg="green3")
analyze_btn.grid(row=0, column=1, padx=10, pady=5)

amp_cont = lower_frame.create_image(-50, 0, anchor=NW)
tf_cont = lower_frame.create_image(-50, 150, anchor=NW)

# add bindings to image frame
lower_frame.bind("<MouseWheel>", do_zoom)
lower_frame.bind('<ButtonPress-1>', lambda event: lower_frame.scan_mark(event.x, event.y))
lower_frame.bind("<B1-Motion>", lambda event: lower_frame.scan_dragto(event.x, event.y, gain=1))



'''
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
'''
root.mainloop()
