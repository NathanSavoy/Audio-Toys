from tkinter import *
import tkinter.messagebox as mb
from tkinter import filedialog as fd
from PIL import ImageTk,Image
import src.analysis as sp
from src.params import *
from tinytag import TinyTag


### INITIALIZATION ###
###
root = Tk()
root.geometry('800x480')
root.title('Audio ToyBox')
root.config(bg=sp.frg_clr)
filepath = StringVar()
filepath.set("")
filename = StringVar()
filename.set("No File Selected")
bpm = StringVar()
bpm.set("")
key = StringVar()
key.set("")
norm = StringVar()
norm.set("")
status = StringVar()
status.set(" Awaiting Import...")


### FUNCTIONS ###
###
def import_audio():
    print("Importing Audio...")
    status.set(" Importing Audio...")
    root.update_idletasks()
    filepath_ = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=[('Wave Files', '*.wav')]
        )

    filepath.set(filepath_)
    
    metadata = TinyTag.get(filepath_)
    if (metadata.title != None):
        filename.set(metadata.title)
    else:
        strt_ = len(filepath_) - filepath_[::-1].find("/")
        end_ = filepath_.find(".")
        filename.set(filepath_[strt_:end_].capitalize())

    sp.import_audio(str(filepath_))
    print("Plotting Amplitude...")
    status.set(" Plotting Amplitude...")    
    root.update_idletasks()
    if (sp.plot_amp()):
        update_image(amp_cont, "media/amp_plot.png")
    print("Ready for Analysis!")
    status.set(" Ready for Analysis!")   

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
    status.set(" Analyzing Audio...")
    root.update_idletasks()
    print("Plotting Time-Frequency Analysis...")
    status.set(" Generating Time-Frequency Analysis...")
    root.update_idletasks()
    if (sp.plot_tf()):
        update_image(tf_cont, "media/tf_plot.png")
    
    print("Analyzing Key...")
    status.set(" Analyzing Key (This may take a while)...")
    root.update_idletasks()
    key.set(sp.determine_key())
    
    print("Analyzing Tempo...")
    status.set(" Analyzing Tempo...")
    root.update_idletasks()
    bpm.set(sp.find_tempo())
    
    print("Analyzing Loudness...")
    status.set(" Analyzing Loudness...")
    root.update_idletasks()
    norm.set(str(sp.find_loudness()) + " dB")

    print("Analysis Complete!")
    status.set(" Analysis Complete!")   

def do_zoom(event):
    x = lower_frame.canvasx(event.x)
    y = lower_frame.canvasy(event.y)
    factor = 1.001 ** event.delta
    lower_frame.scale(ALL, x, y, factor, 1.0)

### GUI ELEMENTS ###
###
## FRAMES ##
upper_frame = Frame(root, width=780, height=110, bg=bkg_clr)
upper_frame.pack(fill="both", expand=True, padx=10, pady=10)

lower_frame = Canvas(root, width=780, height=300, bg=bkg_clr)
lower_frame.pack(fill="x", expand=False, padx=10, pady=10)

status_frame = Frame(root, width=780, height=20, bg=frg_clr)
status_frame.pack(fill="both", expand=True, padx=10, pady=0)

# upper frame elements 
## sub-frames 
# rows
uf_row0 = Frame(upper_frame, width=660, height=20, bg=bkg_clr)
uf_row0.pack(fill="x", expand=True, padx=4, pady=0)
uf_row1 = Frame(upper_frame, width=660, height=20, bg=bkg_clr)
uf_row1.pack(fill="x", expand=True, padx=4, pady=0)
uf_row2 = Frame(upper_frame, width=660, height=40, bg=bkg_clr)
uf_row2.pack(fill="x", expand=True, padx=4, pady=5)

#lf_row0 = Canvas(lower_frame, width=700, height=90, bg=bkg_clr)
#lf_row0.pack(fill="x", expand=True, padx=0, pady=5)
#lf_row1 = Canvas(lower_frame, width=700, height=90, bg="red")
#lf_row1.pack(fill="x", expand=True, padx=0, pady=5)

# columns
uf_row1_c0 = Frame(uf_row1, bg=bkg_clr)
uf_row1_c0.place(relx=.5, rely=.5,anchor= CENTER)

uf_row2_c0 = Frame(uf_row2, bg=bkg_clr)
uf_row2_c0.place(relx=.5, rely=.5,anchor= CENTER)

## widgets 
title = Label(uf_row0, bd=0, textvariable=filename, width=50, height=1, bg=bkg_clr, font='Helvetica 14 bold')
title.pack(fill="both", expand=True)

bpm_lab = Label(uf_row1_c0, bd=0, text="BPM:", bg=bkg_clr, font='Helvetica 10')
bpm_lab.grid(row=0, column=0, padx=10, pady=0)
bpm_val = Label(uf_row1_c0, bd=0, textvariable=bpm, width=5, height=1, bg=bkg_clr, font='Helvetica 10 bold')
bpm_val.grid(row=0, column=1, padx=10, pady=0)

key_lab = Label(uf_row1_c0, bd=0, text="Key:", bg=bkg_clr, font='Helvetica 10')
key_lab.grid(row=0, column=2, padx=10, pady=0)
key_val = Label(uf_row1_c0, bd=0, textvariable=key, width=10, height=1, bg=bkg_clr, font='Helvetica 10 bold')
key_val.grid(row=0, column=3, padx=10, pady=0)

norm_lab = Label(uf_row1_c0, bd=0, text="Loudness:", bg=bkg_clr, font='Helvetica 10')
norm_lab.grid(row=0, column=4, padx=10, pady=0)
norm_val = Label(uf_row1_c0, bd=0, textvariable=norm, width=7, height=1, bg=bkg_clr, font='Helvetica 10 bold')
norm_val.grid(row=0, column=5, padx=10, pady=0)

import_btn = Button(uf_row2_c0, text="Import New", width=10, height=1, command=import_audio, bg=hlt3_clr)
import_btn.grid(row=0, column=0, padx=10, pady=5)

analyze_btn = Button(uf_row2_c0, text="Analyze Audio", width=15, height=1, command=analyze_audio, bg=hlt2_clr)
analyze_btn.grid(row=0, column=1, padx=10, pady=5)

amp_cont = lower_frame.create_image(-50, 0, anchor=NW)
tf_cont = lower_frame.create_image(-50, 150, anchor=NW)

status_lab = Label(status_frame, bd=0, textvariable=status, width=39, height=1, bg=bkg_clr, font='Helvetica 10 italic', anchor="w", justify=LEFT)
status_lab.grid(row=0, column=0, padx=2, pady=0)

# add bindings to image frame
lower_frame.bind("<MouseWheel>", do_zoom)
lower_frame.bind('<ButtonPress-1>', lambda event: lower_frame.scan_mark(event.x, event.y))
lower_frame.bind("<B1-Motion>", lambda event: lower_frame.scan_dragto(event.x, event.y, gain=1))

root.mainloop()
