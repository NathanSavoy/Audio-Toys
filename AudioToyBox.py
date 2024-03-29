### BUILD GUI AND POPULATE FIELDS FROM src
##########################################
from tkinter import *
from tkinter import filedialog as fd
from PIL import ImageTk,Image
from tinytag import TinyTag
from src.params import bkg_clr, frg_clr, hlt1_clr, hlt2_clr, hlt3_clr, txt_clr
import src.fileHandler as file
import src.keyAnalysis as keys
import src.loudnessAnalysis as loudness
import src.plotter as plots
import src.tempoAnalysis as tempo

### INITIALIZATION ###
###
root = Tk()
root.geometry('800x480')
root.title('Audio ToyBox')
root.config(bg=frg_clr)
filepath = StringVar() # location of file
filepath.set("")
filename = StringVar() # name of file (from metadata or path)
filename.set("No File Selected")
bpm = StringVar() # tempo
bpm.set("")
key = StringVar() # key
key.set("")
norm = StringVar() # loudness (normalization)
norm.set("")
status = StringVar() # status
status.set(" Awaiting Import...")


### FUNCTIONS ###
###
def import_audio():
    status.set(" Importing Audio...")
    root.update_idletasks()
    bpm.set("")
    key.set("")
    norm.set("")
    filepath_ = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=[('Wave Files', '*.wav')]
        )
    filepath.set(filepath_)
    metadata = TinyTag.get(filepath_) # set the song name
    if (metadata.title != None):
        filename.set(metadata.title)
    else:
        strt_ = len(filepath_) - filepath_[::-1].find("/")
        end_ = filepath_.find(".")
        filename.set(filepath_[strt_:end_].title())
    lower_frame.itemconfig(amp_cont, image="") # remove any old plot images
    lower_frame.itemconfig(tmln_cont, image="")
    lower_frame.itemconfig(tf_cont, image="")
    status.set(" Plotting Amplitude...")   
    root.update_idletasks()
    if file.importAudio(str(filepath_)): # initialize analysis files with new file data
        keys.init()
        loudness.init()
        tempo.init()
        plots.init()
    if plots.plot_amp(): # update image upon successful execution
        update_image(amp_cont, "media/amp_plot.png")
        update_image(tmln_cont, "media/timeline.png")
        status.set(" Ready for Analysis!")   

def update_image(cont, file): # general image update handler
    global amp_img
    global tf_img
    global tln_img
    if (file == "media/amp_plot.png"):
        amp_img = ImageTk.PhotoImage(Image.open(str(file)).resize((int(1.2*lower_frame.winfo_width()), int(lower_frame.winfo_height()/2))))
        lower_frame.itemconfig(cont,image=amp_img)
    elif (file == "media/tf_plot.png"):
        tf_img = ImageTk.PhotoImage(Image.open(str(file)).resize((int(1.2*lower_frame.winfo_width()), int(lower_frame.winfo_height()/2))))
        lower_frame.itemconfig(cont, image=tf_img)
    elif (file == "media/timeline.png"):
        tln_img = ImageTk.PhotoImage(Image.open(str(file)).resize((int(1.2*lower_frame.winfo_width()), int(lower_frame.winfo_height()/5))))
        lower_frame.itemconfig(cont, image=tln_img)
    else: 
        status.set("Error in update_image(): Canvas not found")


def analyze_audio(): # runs all analysis files, updating status as it does
    status.set(" Analyzing Audio...")
    root.update_idletasks()
    status.set(" Generating Time-Frequency Analysis...")
    root.update_idletasks()
    if (plots.plot_tf()): # generate time-frequency plot
        update_image(tf_cont, "media/tf_plot.png")
    status.set(" Analyzing Key (This may take a while)...")
    root.update_idletasks()
    key.set(keys.determine_key()) # deterine key
    status.set(" Analyzing Tempo...")
    root.update_idletasks()
    bpm.set(tempo.find_tempo()) # analyze the tempo
    status.set(" Analyzing Loudness...")
    root.update_idletasks()
    norm.set(str(loudness.find_loudness()) + " dB") # analyze and return the tempo
    status.set(" Analysis Complete!")

def do_zoom(event): # handle panning and zooming of plot canvas (such as it is...)
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

# columns
uf_row1_c0 = Frame(uf_row1, bg=bkg_clr)
uf_row1_c0.place(relx=.5, rely=.5,anchor= CENTER)
uf_row2_c0 = Frame(uf_row2, bg=bkg_clr)
uf_row2_c0.place(relx=.5, rely=.5,anchor= CENTER)

## widgets 
# title
title = Label(uf_row0, bd=0, textvariable=filename, width=50, height=1, bg=bkg_clr, font='Helvetica 14 bold')
title.pack(fill="both", expand=True)
# tempo
bpm_lab = Label(uf_row1_c0, bd=0, text="BPM:", bg=bkg_clr, font='Helvetica 10')
bpm_lab.grid(row=0, column=0, padx=10, pady=0)
bpm_val = Label(uf_row1_c0, bd=0, textvariable=bpm, width=5, height=1, bg=bkg_clr, font='Helvetica 10 bold')
bpm_val.grid(row=0, column=1, padx=10, pady=0)
# key
key_lab = Label(uf_row1_c0, bd=0, text="Key:", bg=bkg_clr, font='Helvetica 10')
key_lab.grid(row=0, column=2, padx=10, pady=0)
key_val = Label(uf_row1_c0, bd=0, textvariable=key, width=10, height=1, bg=bkg_clr, font='Helvetica 10 bold')
key_val.grid(row=0, column=3, padx=10, pady=0)
# loudness
norm_lab = Label(uf_row1_c0, bd=0, text="Loudness:", bg=bkg_clr, font='Helvetica 10')
norm_lab.grid(row=0, column=4, padx=10, pady=0)
norm_val = Label(uf_row1_c0, bd=0, textvariable=norm, width=7, height=1, bg=bkg_clr, font='Helvetica 10 bold')
norm_val.grid(row=0, column=5, padx=10, pady=0)
# import button
import_btn = Button(uf_row2_c0, text="Import New", width=10, height=1, command=import_audio, bg=hlt3_clr)
import_btn.grid(row=0, column=0, padx=10, pady=5)
# analyze button
analyze_btn = Button(uf_row2_c0, text="Analyze Audio", width=15, height=1, command=analyze_audio, bg=hlt2_clr)
analyze_btn.grid(row=0, column=1, padx=10, pady=5)
# plot image containers
amp_cont = lower_frame.create_image(-45, 0, anchor=NW)
tf_cont = lower_frame.create_image(-45, 150, anchor=NW)
tmln_cont = lower_frame.create_image(-22, 180, anchor=SW)
# status label
status_lab = Label(status_frame, bd=0, textvariable=status, width=39, height=1, bg=bkg_clr, font='Helvetica 10 italic', anchor="w", justify=LEFT)
status_lab.grid(row=0, column=0, padx=2, pady=0)
# legend label
legend_lab_L = Label(status_frame, bd=0, text=" LOW", width=5, height=1, bg=hlt1_clr, fg=bkg_clr, font='Helvetica 10 bold', anchor="w", justify=LEFT)
legend_lab_L.grid(row=0, column=1, padx=2, pady=0)
legend_lab_M = Label(status_frame, bd=0, text=" MID", width=5, height=1, bg=hlt2_clr, fg=bkg_clr, font='Helvetica 10 bold', anchor="w", justify=LEFT)
legend_lab_M.grid(row=0, column=2, padx=2, pady=0)
legend_lab_H = Label(status_frame, bd=0, text=" HIGH", width=6, height=1, bg=hlt3_clr, fg=bkg_clr, font='Helvetica 10 bold', anchor="w", justify=LEFT)
legend_lab_H.grid(row=0, column=3, padx=2, pady=0)
# add  mouse bindings to image frame
lower_frame.bind("<MouseWheel>", do_zoom)
lower_frame.bind('<ButtonPress-1>', lambda event: lower_frame.scan_mark(event.x, event.y))
lower_frame.bind("<B1-Motion>", lambda event: lower_frame.scan_dragto(event.x, event.y, gain=1))
# run it!
root.mainloop()

#LOW=hlt1_clr
#MID=hlt2_clr
#HIGH=hlt3_clr